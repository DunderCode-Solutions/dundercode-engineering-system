"""Build and validate the governed DESys reference corpus inventory."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.desys_indexer.config import IndexerConfig, load_config
from tools.desys_metadata import (
    MANAGED_FILENAME_PATTERN,
    FrontMatterError,
    UniqueKeyLoader,
    parse_front_matter,
    validate_document_metadata,
)

INVENTORY_SCHEMA = "1.0.0"
CORPUS_VERSION = "0.1.0"
DEFAULT_OUTPUT = Path("corpus/inventory.yaml")
DEFAULT_CONFIG = Path("tools/desys_indexer.yaml")
DEFAULT_ASSETS = Path("corpus/assets.yaml")
REFERENCE_ROOT = PurePosixPath("docs/desys/reference")
DISTRIBUTION_STATES = {"approved", "excluded", "pending"}
CLASSIFICATIONS = {"document", "navigation", "placeholder", "schema", "supplemental"}
ENTRY_FIELDS = {
    "source",
    "target",
    "collection",
    "classification",
    "distribution",
    "indexable",
    "review_owner",
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
    for value in payload["assets"]:
        if not isinstance(value, dict) or set(value) != {"source", "classification", "review_owner"}:
            raise InventoryError("Each configured asset must define source, classification, and review_owner.")
        source_value = value["source"]
        if not isinstance(source_value, str) or not source_value.strip():
            raise InventoryError("Configured asset source must be a non-empty relative path.")
        relative = PurePosixPath(source_value)
        if relative.is_absolute() or ".." in relative.parts:
            raise InventoryError(f"Configured asset source must remain inside the repository: {source_value}")
        candidate = root / relative
        source = candidate.resolve()
        if candidate.is_symlink() or not source.is_relative_to(root) or not source.is_file():
            raise InventoryError(f"Configured asset must be a regular repository file: {source_value}")
        if not any(source.is_relative_to(source_root) for source_root in source_roots):
            raise InventoryError(f"Configured asset must belong to a configured source root: {source_value}")
        if source.suffix.casefold() == ".md":
            raise InventoryError(f"Markdown assets are discovered automatically: {source_value}")
        if source in seen:
            raise InventoryError(f"Duplicate configured asset: {source_value}")
        classification = value["classification"]
        if classification not in CLASSIFICATIONS - {"document", "navigation", "placeholder"}:
            raise InventoryError(f"Invalid configured asset classification: {classification!r}")
        review_owner = value["review_owner"]
        if not isinstance(review_owner, str) or not review_owner.strip():
            raise InventoryError(f"Configured asset review_owner must be non-empty: {source_value}")
        seen.add(source)
        assets.append(CorpusAsset(source, classification, review_owner))
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
        unchanged = old is not None and old.get("checksum") == checksum

        default_exclusion = description.get("exclusion_reason")
        distribution = "excluded" if default_exclusion is not None else "pending"
        review_owner = description["review_owner"]
        exclusion_reason = default_exclusion
        if unchanged and default_exclusion is None:
            distribution = old.get("distribution", distribution)
            review_owner = old.get("review_owner", review_owner)
            exclusion_reason = old.get("exclusion_reason", exclusion_reason)

        entry: dict[str, Any] = {
            "source": source,
            "target": (REFERENCE_ROOT / source).as_posix(),
            "collection": PurePosixPath(source).parts[0],
            "classification": description["classification"],
            "distribution": distribution,
            "indexable": description["indexable"],
            "review_owner": review_owner,
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
    required_top_level = {"inventory_schema", "corpus_version", "source_roots", "entries"}
    if set(payload) != required_top_level:
        raise InventoryError("Inventory top-level fields do not match the supported contract.")
    if payload["inventory_schema"] != INVENTORY_SCHEMA:
        raise InventoryError(f"inventory_schema must be {INVENTORY_SCHEMA!r}.")
    if payload["corpus_version"] != CORPUS_VERSION:
        raise InventoryError(f"corpus_version must be {CORPUS_VERSION!r}.")

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


def render_inventory(payload: dict[str, Any]) -> str:
    """Serialize an inventory deterministically."""
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120)


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
        "checksum",
    }
    missing = required - set(entry)
    if missing:
        raise InventoryError(f"Missing inventory entry field(s): {', '.join(sorted(missing))}")

    source = path.relative_to(config.repository_root).as_posix()
    expected_target = (REFERENCE_ROOT / source).as_posix()
    if entry["source"] != source or entry["target"] != expected_target:
        raise InventoryError(f"Invalid source or target mapping for {source}.")
    if entry["target"] in seen_targets:
        raise InventoryError(f"Duplicate inventory target: {entry['target']}")
    seen_targets.add(entry["target"])
    if entry["collection"] != PurePosixPath(source).parts[0]:
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
    except (FileNotFoundError, InventoryError, UnicodeDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
