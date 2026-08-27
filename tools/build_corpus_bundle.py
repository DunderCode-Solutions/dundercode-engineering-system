"""Build and validate immutable package resources for the approved corpus."""

from __future__ import annotations

import argparse
import hashlib
import re
import stat
import sys
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import yaml

from tools.build_corpus_inventory import (
    DEFAULT_ASSETS,
    DEFAULT_CONFIG,
    DEFAULT_OUTPUT,
    InventoryError,
    load_asset_config,
    load_inventory,
    validate_inventory,
)
from tools.desys_indexer.config import load_config
from tools.desys_metadata import FrontMatterError, parse_front_matter

BUNDLE_SCHEMA = "1.1.0"
DEFAULT_PACKAGE_ROOT = Path("tools/reference_corpus_data")
RESOURCE_DIRECTORY = "corpus-files"
FENCE_PATTERN = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
REFERENCE_DEFINITION_PATTERN = re.compile(r"^[ ]{0,3}\[([^]\n]+)\]:[ \t]*(.*)$")
REFERENCE_USE_PATTERN = re.compile(r"!?\[([^]\n]+)\]\[([^]\n]*)\]")
SHORTCUT_REFERENCE_PATTERN = re.compile(r"!?\[([^]\n]+)\](?![([])")
MARKDOWN_ESCAPE_PATTERN = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")
WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:[/\\]")


class BundleError(ValueError):
    """Raised when approved corpus resources cannot form a safe bundle."""


def build_bundle(inventory: dict, repository_root: Path) -> tuple[dict, dict[PurePosixPath, bytes]]:
    """Return a deterministic manifest and package files for approved entries."""
    approved = [entry for entry in inventory["entries"] if entry["distribution"] == "approved"]
    if not approved:
        raise BundleError("Corpus inventory has no approved entries.")
    approved_sources = {entry["source"] for entry in approved}
    metadata_by_source = _load_approved_metadata(approved, repository_root)
    approved_ids = _validate_metadata_identities(metadata_by_source)
    _validate_closure(approved, approved_sources, approved_ids, metadata_by_source, repository_root)

    entries = []
    files: dict[PurePosixPath, bytes] = {}
    for entry in approved:
        source = repository_root / entry["source"]
        content = source.read_bytes()
        packaged_path = PurePosixPath(RESOURCE_DIRECTORY) / entry["target"]
        files[packaged_path] = content
        bundled_entry = {
            key: entry[key]
            for key in (
                "source",
                "target",
                "collection",
                "classification",
                "indexable",
                "checksum",
            )
        }
        for key in ("document_id", "canonical_id", "metadata_status"):
            if key in entry:
                bundled_entry[key] = entry[key]
        entries.append(bundled_entry)

    descriptor = {
        "bundle_schema": BUNDLE_SCHEMA,
        "inventory_schema": inventory["inventory_schema"],
        "corpus_version": inventory["corpus_version"],
        "release_tag": inventory["release_tag"],
        "source_commit": inventory["source_commit"],
        "entries": entries,
    }
    descriptor_bytes = _render_yaml(descriptor)
    manifest = {
        **descriptor,
        "bundle_checksum": f"sha256:{hashlib.sha256(descriptor_bytes).hexdigest()}",
    }
    files[PurePosixPath("bundle.yaml")] = _render_yaml(manifest)
    return manifest, files


def validate_or_write_bundle(package_root: Path, files: dict[PurePosixPath, bytes], *, check: bool) -> None:
    """Validate exact generated coverage or replace generated package resources."""
    expected = {path.as_posix(): content for path, content in files.items()}
    if package_root.is_symlink():
        raise BundleError(f"Generated package root is a symlink: {package_root}")
    files_root = package_root / RESOURCE_DIRECTORY
    if files_root.is_symlink():
        raise BundleError(f"Generated files root is a symlink: {files_root}")
    if check:
        actual = _read_package_files(package_root)
        if actual != expected:
            raise BundleError("Packaged corpus resources are missing, stale, or contain unexpected files.")
        return

    package_root.mkdir(parents=True, exist_ok=True)
    descriptor = package_root / "bundle.yaml"
    descriptor_exists = _preflight_descriptor(descriptor)
    legacy_files_root = package_root / "files"
    legacy_descendants: tuple[Path, ...] = ()
    if legacy_files_root.exists() or legacy_files_root.is_symlink():
        if legacy_files_root.is_symlink():
            raise BundleError(f"Legacy generated files root is a symlink: {legacy_files_root}")
        legacy_descendants = _preflight_cleanup(legacy_files_root)
    current_descendants: tuple[Path, ...] = ()
    if files_root.exists():
        current_descendants = _preflight_cleanup(files_root)
    if descriptor_exists:
        descriptor.unlink()
    if legacy_descendants:
        for path in sorted(legacy_descendants, key=lambda item: (len(item.parts), item.as_posix()), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        legacy_files_root.rmdir()
    if current_descendants:
        for path in sorted(current_descendants, key=lambda item: (len(item.parts), item.as_posix()), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
    for relative, content in sorted(files.items(), key=lambda item: item[0].as_posix()):
        destination = package_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)


def _validate_closure(
    approved: list[dict],
    approved_sources: set[str],
    approved_ids: set[str],
    metadata_by_source: dict[str, dict],
    repository_root: Path,
) -> None:
    for entry in approved:
        source = repository_root / entry["source"]
        if source.is_symlink() or not source.is_file():
            raise BundleError(f"Approved source is missing or unsafe: {entry['source']}")
        if source.suffix.casefold() != ".md":
            continue
        text = source.read_text(encoding="utf-8")
        for raw_destination in _markdown_destinations(text):
            destination = _markdown_destination(raw_destination)
            if destination is None:
                continue
            resolved = (source.parent / destination).resolve()
            if not resolved.is_relative_to(repository_root):
                raise BundleError(f"Link escapes the repository in {entry['source']}: {destination}")
            linked_source = resolved.relative_to(repository_root).as_posix()
            if linked_source not in approved_sources:
                raise BundleError(f"Approved source links to unavailable bundle content: {entry['source']} -> {linked_source}")
        if not entry["indexable"]:
            continue
        for relationship in metadata_by_source[entry["source"]].get("relationships", []):
            target = relationship["target"]
            if target not in approved_ids:
                raise BundleError(f"Approved relationship target is unavailable: {entry['source']} -> {target}")


def _load_approved_metadata(approved: list[dict], repository_root: Path) -> dict[str, dict]:
    metadata_by_source: dict[str, dict] = {}
    for entry in approved:
        source = repository_root / entry["source"]
        if source.is_symlink() or not source.is_file():
            raise BundleError(f"Approved source is missing or unsafe: {entry['source']}")
        if not entry["indexable"]:
            continue
        try:
            metadata, _ = parse_front_matter(source.read_text(encoding="utf-8"))
        except FrontMatterError as error:
            raise BundleError(f"Invalid approved metadata in {entry['source']}: {error}") from error
        metadata_by_source[entry["source"]] = metadata
    return metadata_by_source


def _validate_metadata_identities(metadata_by_source: dict[str, dict]) -> set[str]:
    document_ids: dict[str, str] = {}
    canonical_ids: dict[str, str] = {}
    aliases: dict[str, str] = {}
    for source, metadata in metadata_by_source.items():
        _record_identity(document_ids, metadata["document_id"], source, "document ID")
        _record_identity(canonical_ids, metadata["canonical_id"], source, "canonical ID")
    for source, metadata in metadata_by_source.items():
        for alias in metadata.get("aliases", []):
            if alias in canonical_ids:
                raise BundleError(f"Approved metadata alias collides with a canonical ID: {source} -> {alias}")
            _record_identity(aliases, alias, source, "alias")
    return set(canonical_ids) | set(aliases)


def _record_identity(owners: dict[str, str], value: str, source: str, label: str) -> None:
    previous = owners.get(value)
    if previous is not None:
        raise BundleError(f"Duplicate approved {label}: {value} ({previous}, {source})")
    owners[value] = source


class _LinkAttributeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.destinations: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.casefold() in {"href", "src"} and value is not None:
                self.destinations.append(value)

    handle_startendtag = handle_starttag


def _markdown_destinations(text: str) -> tuple[str, ...]:
    text = _strip_fenced_code(text)
    definitions: dict[str, str] = {}
    content_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        match = REFERENCE_DEFINITION_PATTERN.match(line)
        if match is None:
            content_lines.append(line)
            continue
        definitions.setdefault(_reference_label(match.group(1)), match.group(2).strip())
        content_lines.append("\n" if line.endswith(("\n", "\r")) else "")
    content = "".join(content_lines)
    destinations = list(_inline_destinations(content))
    used_labels: set[str] = set()
    for match in REFERENCE_USE_PATTERN.finditer(content):
        used_labels.add(_reference_label(match.group(2) or match.group(1)))
    for match in SHORTCUT_REFERENCE_PATTERN.finditer(content):
        label = _reference_label(match.group(1))
        if label in definitions:
            used_labels.add(label)
    destinations.extend(definitions[label] for label in sorted(used_labels) if label in definitions)
    parser = _LinkAttributeParser()
    parser.feed(content)
    destinations.extend(parser.destinations)
    return tuple(destinations)


def _strip_fenced_code(text: str) -> str:
    rendered: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = FENCE_PATTERN.match(line)
        if fence_character is None:
            if match is None:
                rendered.append(line)
                continue
            marker = match.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
        elif match is not None:
            marker = match.group(1)
            if marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
        rendered.append("\n" if line.endswith(("\n", "\r")) else "")
    return "".join(rendered)


def _inline_destinations(text: str) -> tuple[str, ...]:
    destinations: list[str] = []
    index = 0
    while index < len(text) - 1:
        if text[index : index + 2] != "](" or (index > 0 and text[index - 1] == "\\"):
            index += 1
            continue
        start = index + 2
        cursor = start
        depth = 1
        quote: str | None = None
        angle_destination = False
        title_may_start = False
        while cursor < len(text):
            character = text[cursor]
            if character == "\\":
                cursor += 2
                continue
            if quote is not None:
                if character == quote:
                    quote = None
            elif title_may_start and character in {'"', "'"}:
                quote = character
                title_may_start = False
            elif quote is None and character == "<":
                angle_destination = True
            elif quote is None and angle_destination and character == ">":
                angle_destination = False
            elif quote is None and not angle_destination and depth == 1 and character.isspace():
                title_may_start = True
            elif quote is None and not angle_destination and character == "(":
                title_may_start = False
                depth += 1
            elif quote is None and not angle_destination and character == ")":
                depth -= 1
                if depth == 0:
                    destinations.append(text[start:cursor])
                    cursor += 1
                    break
            elif not character.isspace():
                title_may_start = False
            cursor += 1
        index = max(cursor, index + 1)
    return tuple(destinations)


def _reference_label(value: str) -> str:
    return " ".join(value.split()).casefold()


def _markdown_destination(raw: str) -> str | None:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    else:
        value = value.split(maxsplit=1)[0]
    value = MARKDOWN_ESCAPE_PATTERN.sub(r"\1", value)
    decoded = unquote(value)
    if decoded.startswith("/") or "\\" in decoded or WINDOWS_DRIVE_PATTERN.match(decoded):
        raise BundleError(f"Unsupported local Markdown link: {raw}")
    parsed = urlsplit(value)
    if parsed.scheme:
        if parsed.scheme.casefold() in {"http", "https", "mailto"}:
            return None
        raise BundleError(f"Unsupported Markdown link scheme: {raw}")
    if parsed.netloc:
        raise BundleError(f"Unsupported local Markdown link: {raw}")
    if not parsed.path:
        return None
    return unquote(parsed.path)


def _preflight_cleanup(files_root: Path) -> tuple[Path, ...]:
    if not files_root.is_dir():
        raise BundleError(f"Generated files root is not a directory: {files_root}")
    resolved_root = files_root.resolve()
    descendants: list[Path] = []
    for directory, directory_names, file_names in files_root.walk(follow_symlinks=False):
        for name in (*directory_names, *file_names):
            path = directory / name
            if path.is_symlink():
                raise BundleError(f"Generated bundle contains a symlink: {path}")
            status = path.stat(follow_symlinks=False)
            if not (stat.S_ISREG(status.st_mode) or stat.S_ISDIR(status.st_mode)):
                raise BundleError(f"Generated bundle contains a special filesystem node: {path}")
            if not path.resolve().is_relative_to(resolved_root):
                raise BundleError(f"Generated bundle escapes its files root: {path}")
            descendants.append(path)
    return tuple(descendants)


def _preflight_descriptor(descriptor: Path) -> bool:
    if descriptor.is_symlink():
        raise BundleError(f"Generated bundle descriptor is a symlink: {descriptor}")
    if not descriptor.exists():
        return False
    status = descriptor.stat(follow_symlinks=False)
    if not stat.S_ISREG(status.st_mode):
        raise BundleError(f"Generated bundle descriptor is not a regular file: {descriptor}")
    if status.st_nlink != 1:
        raise BundleError(f"Generated bundle descriptor has multiple hard links: {descriptor}")
    return True


def _read_package_files(package_root: Path) -> dict[str, bytes]:
    if package_root.is_symlink():
        raise BundleError(f"Generated package root is a symlink: {package_root}")
    if not package_root.is_dir():
        return {}
    files_root = package_root / RESOURCE_DIRECTORY
    if files_root.is_symlink():
        raise BundleError(f"Generated files root is a symlink: {files_root}")
    actual: dict[str, bytes] = {}
    for path in package_root.rglob("*"):
        if path.is_symlink():
            raise BundleError(f"Packaged corpus resource is a symlink: {path}")
        relative = path.relative_to(package_root)
        if relative.parts == ("__init__.py",) or relative.parts[:1] == ("__pycache__",):
            continue
        if path.is_dir() and path.name == "__pycache__":
            raise BundleError(f"Packaged corpus resources contain unexpected files: {path}")
        if path.is_file():
            actual[relative.as_posix()] = path.read_bytes()
        elif not path.is_dir():
            raise BundleError(f"Packaged corpus resource is not a regular file or directory: {path}")
    return actual


def _render_yaml(payload: dict) -> bytes:
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120).encode("utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        config = load_config(args.config)
        assets_path = args.assets if args.assets.is_absolute() else config.repository_root / args.assets
        inventory_path = args.inventory if args.inventory.is_absolute() else config.repository_root / args.inventory
        package_root = args.package_root if args.package_root.is_absolute() else config.repository_root / args.package_root
        assets = load_asset_config(assets_path, config.repository_root, config.sources)
        inventory = load_inventory(inventory_path)
        if inventory is None:
            raise BundleError(f"Corpus inventory does not exist: {inventory_path}")
        validate_inventory(inventory, config, assets)
        manifest, files = build_bundle(inventory, config.repository_root)
        validate_or_write_bundle(package_root, files, check=args.check)
    except (BundleError, FileNotFoundError, InventoryError, OSError, UnicodeError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    action = "Validated" if args.check else "Wrote"
    print(f"{action} corpus bundle with {len(manifest['entries'])} entries ({manifest['bundle_checksum']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
