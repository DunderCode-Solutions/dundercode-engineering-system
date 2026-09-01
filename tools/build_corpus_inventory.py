"""Build and validate the governed DESys reference corpus inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.corpus_reviews import ReviewError, load_review_records, validate_dsk_distribution_reviews
from tools.desys_indexer.config import IndexerConfig, load_config
from tools.desys_metadata import (
    MANAGED_FILENAME_PATTERN,
    FrontMatterError,
    UniqueKeyLoader,
    parse_front_matter,
    validate_document_metadata,
)
from tools.project_transaction import TransactionError, guard_operation

INVENTORY_SCHEMA = "1.2.0"
CORPUS_VERSION = "0.1.0"
RELEASE_TAG = "v0.3.0-alpha.1"
SOURCE_COMMIT = "d84693cd117e5b792fe63fcaaa1550acda427c16"
DEFAULT_OUTPUT = Path("corpus/inventory.yaml")
DEFAULT_CONFIG = Path("tools/desys_indexer.yaml")
DEFAULT_ASSETS = Path("corpus/assets.yaml")
REFERENCE_ROOT = PurePosixPath("docs/desys/reference")
DISTRIBUTION_STATES = {"approved", "excluded", "pending"}
CLASSIFICATIONS = {"document", "legal", "navigation", "placeholder", "schema", "supplemental"}
COLLECTIONS = {"delivery", "engineering", "foundation", "knowledge", "legal", "skills"}
REQUIRED_LEGAL_ASSETS = {
    "LICENSE": PurePosixPath("docs/desys/LICENSE"),
    "THIRD_PARTY_NOTICES.md": PurePosixPath("docs/desys/THIRD_PARTY_NOTICES.md"),
}
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
WINDOWS_FORBIDDEN_CHARACTERS = set('<>:"|?*\\')
ENTRY_FIELDS = {
    "source",
    "target",
    "collection",
    "classification",
    "distribution",
    "indexable",
    "review_owner",
    "review_fingerprint",
    "checksum",
    "document_id",
    "canonical_id",
    "metadata_status",
    "exclusion_reason",
}


class InventoryError(ValueError):
    """Raised when the corpus inventory is invalid or stale."""


@dataclass(frozen=True, slots=True)
class CorpusAsset:
    """Explicit non-Markdown asset included in corpus inventory coverage."""

    source: Path
    classification: str
    review_owner: str
    target: PurePosixPath | None = None
    collection: str | None = None


def load_inventory(path: Path) -> dict[str, Any] | None:
    """Load an existing inventory while rejecting malformed YAML."""
    if not path.is_file():
        return None
    try:
        payload = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise InventoryError(f"Invalid inventory YAML: {error}") from error
    if not isinstance(payload, dict):
        raise InventoryError("Inventory must be a YAML mapping.")
    return payload


def load_asset_config(
    path: Path,
    repository_root: Path,
    source_roots: tuple[Path, ...],
) -> tuple[CorpusAsset, ...]:
    """Load and validate explicitly allowlisted non-Markdown corpus assets."""
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        payload = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise InventoryError(f"Invalid asset configuration YAML: {error}") from error
    if not isinstance(payload, dict) or set(payload) != {"version", "assets"}:
        raise InventoryError("Asset configuration fields must be 'version' and 'assets'.")
    if payload["version"] != 1:
        raise InventoryError(f"Unsupported asset configuration version: {payload['version']!r}")
    if not isinstance(payload["assets"], list):
        raise InventoryError("Asset configuration assets must be a list.")

    root = repository_root.resolve()
    assets: list[CorpusAsset] = []
    seen: set[Path] = set()
    seen_targets: set[str] = set()
    for value in payload["assets"]:
        required_fields = {"source", "target", "collection", "classification", "review_owner"}
        if not isinstance(value, dict) or set(value) != required_fields:
            raise InventoryError(
                "Each configured asset must define source, target, collection, classification, and review_owner."
            )
        source_value = value["source"]
        if (
            not isinstance(source_value, str)
            or not source_value.strip()
            or "\\" in source_value
            or any(ord(character) < 32 for character in source_value)
        ):
            raise InventoryError("Configured asset source must be a non-empty relative path.")
        relative = PurePosixPath(source_value)
        if relative.is_absolute() or ".." in relative.parts:
            raise InventoryError(f"Configured asset source must remain inside the repository: {source_value}")
        candidate = root / relative
        current = root
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                raise InventoryError(f"Configured asset source contains a symlink: {source_value}")
        source = candidate.resolve()
        if candidate.is_symlink() or not source.is_relative_to(root) or not source.is_file():
            raise InventoryError(f"Configured asset must be a regular repository file: {source_value}")
        belongs_to_source_root = any(source.is_relative_to(source_root) for source_root in source_roots)
        if not belongs_to_source_root and source_value not in REQUIRED_LEGAL_ASSETS:
            raise InventoryError(f"Configured asset outside source roots is not an approved legal asset: {source_value}")
        if belongs_to_source_root and source.suffix.casefold() == ".md":
            raise InventoryError(f"Markdown assets are discovered automatically: {source_value}")
        if source in seen:
            raise InventoryError(f"Duplicate configured asset: {source_value}")
        classification = value["classification"]
        if classification not in CLASSIFICATIONS - {"document", "navigation", "placeholder"}:
            raise InventoryError(f"Invalid configured asset classification: {classification!r}")
        target_value = value["target"]
        if (
            not isinstance(target_value, str)
            or not target_value.strip()
            or "\\" in target_value
            or any(ord(character) < 32 for character in target_value)
        ):
            raise InventoryError(f"Configured asset target must be a non-empty relative path: {source_value}")
        target = PurePosixPath(target_value)
        try:
            validate_portable_target(target)
        except InventoryError as error:
            raise InventoryError(f"Invalid configured asset target {target_value!r}: {error}") from error
        if (
            target.is_absolute()
            or ".." in target.parts
            or target.parts[:2] != ("docs", "desys")
            or portable_path_key(target) == portable_path_key(PurePosixPath("docs/desys/corpus-manifest.yaml"))
        ):
            raise InventoryError(f"Configured asset target must remain inside docs/desys: {target_value}")
        target_key = portable_path_key(target)
        if target_key in seen_targets:
            raise InventoryError(f"Duplicate configured asset target: {target_value}")
        collection = value["collection"]
        if collection not in COLLECTIONS:
            raise InventoryError(f"Invalid configured asset collection: {collection!r}")
        expected_legal_target = REQUIRED_LEGAL_ASSETS.get(source_value)
        if expected_legal_target is not None:
            if target != expected_legal_target or collection != "legal" or classification != "legal":
                raise InventoryError(f"Invalid legal asset mapping: {source_value}")
        elif classification == "legal" or collection == "legal":
            raise InventoryError(f"Only required legal assets may use legal classification: {source_value}")
        else:
            expected_target = REFERENCE_ROOT / source_value
            expected_collection = relative.parts[0]
            if target != expected_target or collection != expected_collection:
                raise InventoryError(f"Configured source-root asset must preserve its reference path: {source_value}")
        review_owner = value["review_owner"]
        if not isinstance(review_owner, str) or not review_owner.strip():
            raise InventoryError(f"Configured asset review_owner must be non-empty: {source_value}")
        seen.add(source)
        seen_targets.add(target_key)
        assets.append(CorpusAsset(source, classification, review_owner, target, collection))
    configured_sources = {asset.source.relative_to(root).as_posix() for asset in assets}
    missing_legal = set(REQUIRED_LEGAL_ASSETS) - configured_sources
    if missing_legal:
        raise InventoryError(f"Missing required legal asset(s): {', '.join(sorted(missing_legal))}")
    return tuple(sorted(assets, key=lambda asset: asset.source.relative_to(root).as_posix()))


def build_inventory(
    config: IndexerConfig,
    previous: dict[str, Any] | None = None,
    assets: tuple[CorpusAsset, ...] = (),
) -> dict[str, Any]:
    """Build a deterministic inventory, preserving reviews for unchanged files."""
    previous_entries = _previous_entries(previous)
    source_roots = [source.relative_to(config.repository_root).as_posix() for source in config.sources]
    entries = []

    assets_by_path = {asset.source: asset for asset in assets}
    for path in _discover_corpus_files(config, assets):
        source = path.relative_to(config.repository_root).as_posix()
        content = path.read_bytes()
        checksum = f"sha256:{hashlib.sha256(content).hexdigest()}"
        description = _describe_document(path, content, config.repository_root, assets_by_path)
        old = previous_entries.get(source)
        asset = assets_by_path.get(path)
        target = asset.target if asset is not None and asset.target is not None else REFERENCE_ROOT / source
        collection = (
            asset.collection
            if asset is not None and asset.collection is not None
            else PurePosixPath(source).parts[0]
        )
        review_fingerprint = _review_fingerprint(
            source=source,
            target=target.as_posix(),
            collection=collection,
            classification=description["classification"],
            indexable=description["indexable"],
            review_owner=description["review_owner"],
            checksum=checksum,
        )
        unchanged = old is not None and old.get("review_fingerprint") == review_fingerprint

        default_exclusion = description.get("exclusion_reason")
        distribution = "excluded" if default_exclusion is not None else "pending"
        review_owner = description["review_owner"]
        exclusion_reason = default_exclusion
        if unchanged and default_exclusion is None:
            distribution = old.get("distribution", distribution)
            exclusion_reason = old.get("exclusion_reason", exclusion_reason)

        entry: dict[str, Any] = {
            "source": source,
            "target": target.as_posix(),
            "collection": collection,
            "classification": description["classification"],
            "distribution": distribution,
            "indexable": description["indexable"],
            "review_owner": review_owner,
            "review_fingerprint": review_fingerprint,
            "checksum": checksum,
        }
        for field in ("document_id", "canonical_id", "metadata_status"):
            if description.get(field) is not None:
                entry[field] = description[field]
        if exclusion_reason is not None:
            entry["exclusion_reason"] = exclusion_reason
        entries.append(entry)

    payload = {
        "inventory_schema": INVENTORY_SCHEMA,
        "corpus_version": CORPUS_VERSION,
        "release_tag": RELEASE_TAG,
        "source_commit": SOURCE_COMMIT,
        "source_roots": source_roots,
        "entries": entries,
    }
    validate_inventory(payload, config, assets)
    return payload


def validate_inventory(
    payload: dict[str, Any],
    config: IndexerConfig,
    assets: tuple[CorpusAsset, ...] = (),
) -> None:
    """Validate inventory structure, coverage, paths, metadata, and checksums."""
    required_top_level = {
        "inventory_schema",
        "corpus_version",
        "release_tag",
        "source_commit",
        "source_roots",
        "entries",
    }
    if set(payload) != required_top_level:
        raise InventoryError("Inventory top-level fields do not match the supported contract.")
    if payload["inventory_schema"] != INVENTORY_SCHEMA:
        raise InventoryError(f"inventory_schema must be {INVENTORY_SCHEMA!r}.")
    if payload["corpus_version"] != CORPUS_VERSION:
        raise InventoryError(f"corpus_version must be {CORPUS_VERSION!r}.")
    if payload["release_tag"] != RELEASE_TAG:
        raise InventoryError(f"release_tag must be {RELEASE_TAG!r}.")
    if payload["source_commit"] != SOURCE_COMMIT:
        raise InventoryError(f"source_commit must be {SOURCE_COMMIT!r}.")

    expected_roots = [source.relative_to(config.repository_root).as_posix() for source in config.sources]
    if payload["source_roots"] != expected_roots:
        raise InventoryError("source_roots must match the configured corpus sources in order.")
    entries = payload["entries"]
    if not isinstance(entries, list):
        raise InventoryError("entries must be a list.")

    expected_paths = _discover_corpus_files(config, assets)
    expected_sources = [path.relative_to(config.repository_root).as_posix() for path in expected_paths]
    actual_sources = [entry.get("source") for entry in entries if isinstance(entry, dict)]
    if actual_sources != expected_sources:
        raise InventoryError("Inventory entries must exactly cover corpus files in path order.")

    seen_targets: set[str] = set()
    assets_by_path = {asset.source: asset for asset in assets}
    for entry, path in zip(entries, expected_paths, strict=True):
        _validate_entry(entry, path, config, seen_targets, assets_by_path)

    try:
        records = load_review_records(config.repository_root / "corpus/reviews")
        validate_dsk_distribution_reviews(payload, records)
    except ReviewError as error:
        raise InventoryError(str(error)) from error


def render_inventory(payload: dict[str, Any]) -> str:
    """Serialize an inventory deterministically."""
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120)


def portable_path_key(path: PurePosixPath) -> str:
    """Return a case-insensitive Unicode-normalized key for portable paths."""
    return "/".join(unicodedata.normalize("NFC", part.casefold()) for part in path.parts)


def validate_portable_target(path: PurePosixPath) -> None:
    """Reject target names that are unsafe on any supported platform."""
    for part in path.parts:
        if not part or part.endswith((" ", ".")):
            raise InventoryError(f"target segment is empty or ends with a dot or space: {part!r}")
        if any(
            ord(character) < 32
            or 127 <= ord(character) <= 159
            or character in WINDOWS_FORBIDDEN_CHARACTERS
            for character in part
        ):
            raise InventoryError(f"target segment contains a forbidden character: {part!r}")
        if part.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
            raise InventoryError(f"target segment uses a reserved Windows device name: {part!r}")


def _review_fingerprint(**fields: Any) -> str:
    """Bind an editorial decision to content and generated distribution semantics."""
    encoded = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _discover_corpus_files(
    config: IndexerConfig,
    assets: tuple[CorpusAsset, ...] = (),
) -> list[Path]:
    paths: set[Path] = set()
    for source in config.sources:
        for path in source.rglob("*.md"):
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve()
            if resolved.is_relative_to(config.repository_root) and not config.is_excluded(resolved):
                paths.add(resolved)
    paths.update(asset.source for asset in assets)
    return sorted(paths, key=lambda path: path.relative_to(config.repository_root).as_posix())


def _describe_document(
    path: Path,
    content: bytes,
    repository_root: Path,
    assets_by_path: dict[Path, CorpusAsset] | None = None,
) -> dict[str, Any]:
    relative = path.relative_to(repository_root)
    asset = (assets_by_path or {}).get(path)
    if asset is not None:
        if not content:
            return {
                "classification": asset.classification,
                "indexable": False,
                "review_owner": asset.review_owner,
                "exclusion_reason": "empty-file",
            }
        return {
            "classification": asset.classification,
            "indexable": False,
            "review_owner": asset.review_owner,
        }
    text = content.decode("utf-8")
    managed = MANAGED_FILENAME_PATTERN.fullmatch(path.name) is not None
    if not text.strip():
        if managed:
            classification = "placeholder"
            exclusion_reason = "empty-placeholder"
        else:
            classification = "navigation" if path.name.casefold() == "readme.md" else "supplemental"
            exclusion_reason = "empty-file"
        return {
            "classification": classification,
            "indexable": False,
            "review_owner": "DunderCode Engineering",
            "exclusion_reason": exclusion_reason,
        }
    if not managed:
        return {
            "classification": "navigation" if path.name.casefold() == "readme.md" else "supplemental",
            "indexable": False,
            "review_owner": "DunderCode Engineering",
        }

    try:
        metadata, _ = parse_front_matter(text)
    except FrontMatterError as error:
        raise InventoryError(f"{relative.as_posix()}: {error}") from error
    errors = [
        issue.message
        for issue in validate_document_metadata(metadata, relative)
        if issue.severity == "error"
    ]
    if errors:
        raise InventoryError(f"{relative.as_posix()}: {'; '.join(errors)}")
    return {
        "classification": "document",
        "indexable": True,
        "review_owner": metadata["owner"],
        "document_id": metadata["document_id"],
        "canonical_id": metadata["canonical_id"],
        "metadata_status": metadata["status"],
    }


def _previous_entries(previous: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if previous is None:
        return {}
    entries = previous.get("entries")
    if not isinstance(entries, list):
        raise InventoryError("Existing inventory entries must be a list.")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise InventoryError("Existing inventory entries must be mappings.")
        unknown = set(entry) - ENTRY_FIELDS
        if unknown:
            raise InventoryError(f"Unknown inventory entry field(s): {', '.join(sorted(unknown))}")
        source = entry.get("source")
        if not isinstance(source, str) or not source:
            raise InventoryError("Existing inventory entry source must be a non-empty string.")
        if source in result:
            raise InventoryError(f"Duplicate inventory source: {source}")
        result[source] = entry
    return result


def _validate_entry(
    entry: Any,
    path: Path,
    config: IndexerConfig,
    seen_targets: set[str],
    assets_by_path: dict[Path, CorpusAsset],
) -> None:
    if not isinstance(entry, dict):
        raise InventoryError("Inventory entries must be mappings.")
    unknown = set(entry) - ENTRY_FIELDS
    if unknown:
        raise InventoryError(f"Unknown inventory entry field(s): {', '.join(sorted(unknown))}")
    required = {
        "source",
        "target",
        "collection",
        "classification",
        "distribution",
        "indexable",
        "review_owner",
        "review_fingerprint",
        "checksum",
    }
    missing = required - set(entry)
    if missing:
        raise InventoryError(f"Missing inventory entry field(s): {', '.join(sorted(missing))}")

    source = path.relative_to(config.repository_root).as_posix()
    asset = assets_by_path.get(path)
    expected_target = (
        asset.target if asset is not None and asset.target is not None else REFERENCE_ROOT / source
    ).as_posix()
    if entry["source"] != source or entry["target"] != expected_target:
        raise InventoryError(f"Invalid source or target mapping for {source}.")
    target_path = PurePosixPath(entry["target"])
    try:
        validate_portable_target(target_path)
    except InventoryError as error:
        raise InventoryError(f"Inventory target is not portable: {entry['target']}: {error}") from error
    target_key = portable_path_key(target_path)
    if target_key in seen_targets:
        raise InventoryError(f"Duplicate inventory target: {entry['target']}")
    seen_targets.add(target_key)
    expected_collection = (
        asset.collection if asset is not None and asset.collection is not None else PurePosixPath(source).parts[0]
    )
    if entry["collection"] != expected_collection:
        raise InventoryError(f"Invalid collection for {source}.")
    if entry["collection"] not in COLLECTIONS:
        raise InventoryError(f"Invalid collection for {source}.")
    if entry["classification"] not in CLASSIFICATIONS:
        raise InventoryError(f"Invalid classification for {source}.")
    if entry["distribution"] not in DISTRIBUTION_STATES:
        raise InventoryError(f"Invalid distribution state for {source}.")
    if not isinstance(entry["indexable"], bool):
        raise InventoryError(f"indexable must be a boolean for {source}.")
    if not isinstance(entry["review_owner"], str) or not entry["review_owner"].strip():
        raise InventoryError(f"review_owner must be a non-empty string for {source}.")

    checksum = f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
    if entry["checksum"] != checksum:
        raise InventoryError(f"Checksum is stale for {source}.")
    description = _describe_document(path, path.read_bytes(), config.repository_root, assets_by_path)
    if entry["review_owner"] != description["review_owner"]:
        raise InventoryError(f"Review owner is stale for {source}.")
    expected_fingerprint = _review_fingerprint(
        source=source,
        target=expected_target,
        collection=expected_collection,
        classification=description["classification"],
        indexable=description["indexable"],
        review_owner=description["review_owner"],
        checksum=checksum,
    )
    if entry["review_fingerprint"] != expected_fingerprint:
        raise InventoryError(f"Review fingerprint is stale for {source}.")
    for field in ("classification", "indexable", "document_id", "canonical_id", "metadata_status"):
        if entry.get(field) != description.get(field):
            raise InventoryError(f"Field {field!r} is stale for {source}.")
    if description.get("exclusion_reason") is not None:
        if entry["distribution"] != "excluded":
            raise InventoryError(f"Empty corpus file must be excluded: {source}.")
        if entry.get("exclusion_reason") != description["exclusion_reason"]:
            raise InventoryError(f"Empty corpus file has an invalid exclusion reason: {source}.")
    if entry["distribution"] == "excluded":
        reason = entry.get("exclusion_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise InventoryError(f"Excluded entry requires exclusion_reason: {source}.")
    elif "exclusion_reason" in entry:
        raise InventoryError(f"Non-excluded entry must not define exclusion_reason: {source}.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail when the tracked inventory is stale.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        config = load_config(args.config)
        guard_operation(config.repository_root)
        asset_config = args.assets if args.assets.is_absolute() else config.repository_root / args.assets
        assets = load_asset_config(asset_config, config.repository_root, config.sources)
        output = args.output if args.output.is_absolute() else config.repository_root / args.output
        previous = load_inventory(output)
        payload = build_inventory(config, previous, assets)
        rendered = render_inventory(payload)
        if args.check:
            if previous is None or output.read_text(encoding="utf-8") != rendered:
                raise InventoryError(f"Corpus inventory is stale: {output}")
            print(f"Validated corpus inventory with {len(payload['entries'])} entries.")
            return 0
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Wrote corpus inventory with {len(payload['entries'])} entries to {output}.")
        return 0
    except (FileNotFoundError, InventoryError, UnicodeDecodeError, TransactionError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
