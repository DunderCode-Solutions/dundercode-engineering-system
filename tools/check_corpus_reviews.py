"""Validate DSK review schemas, approval semantics, and generated candidate bindings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.build_corpus_bundle import build_bundle
from tools.build_corpus_inventory import (
    DEFAULT_ASSETS,
    DEFAULT_CONFIG,
    DEFAULT_OUTPUT,
    InventoryError,
    load_asset_config,
    load_inventory,
    validate_inventory,
)
from tools.build_corpus_review_candidate import build_review_candidate, candidate_binding
from tools.corpus_reviews import (
    ReviewError,
    load_review_records,
    public_record,
    validate_dsk_distribution_reviews,
    validate_record_for_candidate,
)
from tools.desys_indexer.config import load_config

DEFAULT_REVIEWS = Path("corpus/reviews")
DEFAULT_SCHEMA = DEFAULT_REVIEWS / "dsk-batch-review-1.0.0.schema.json"


def check_review_records(
    inventory: dict[str, Any],
    repository_root: Path,
    records: tuple[dict[str, Any], ...],
    schema: dict[str, Any],
) -> None:
    """Apply structural, semantic, approval, and deterministic package checks."""
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for record in records:
        errors = sorted(validator.iter_errors(public_record(record)), key=lambda error: list(error.absolute_path))
        if errors:
            error = errors[0]
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            raise ReviewError(f"Review schema violation at {location}: {error.message}")
    validate_dsk_distribution_reviews(inventory, records)
    for record in records:
        validate_record_for_candidate(record, inventory, require_pending=False)
        package_review = record["package_review"]
        if package_review["generation_status"] != "GENERATED":
            continue
        selected_sources = {artifact["source"] for artifact in record["source_review"]["artifacts"]}
        selected_entries = [entry for entry in inventory["entries"] if entry["source"] in selected_sources]
        if package_review["status"] == "APPROVED" and all(
            entry["distribution"] == "approved" for entry in selected_entries
        ):
            manifest, files = build_bundle(inventory, repository_root)
            official_binding = candidate_binding(manifest, files, inventory, record)
            if package_review["candidate"] != official_binding:
                raise ReviewError(f"Approved review does not match the official bundle: {record['record_id']}")
            continue
        _, _, report = build_review_candidate(
            inventory,
            repository_root,
            record,
            require_pending=False,
        )
        if package_review["candidate"] != report["candidate"]:
            raise ReviewError(f"Generated candidate binding is stale: {record['record_id']}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reviews", type=Path, default=DEFAULT_REVIEWS)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        config = load_config(args.config)
        assets_path = args.assets if args.assets.is_absolute() else config.repository_root / args.assets
        inventory_path = args.inventory if args.inventory.is_absolute() else config.repository_root / args.inventory
        reviews_path = args.reviews if args.reviews.is_absolute() else config.repository_root / args.reviews
        schema_path = args.schema if args.schema.is_absolute() else config.repository_root / args.schema
        assets = load_asset_config(assets_path, config.repository_root, config.sources)
        inventory = load_inventory(inventory_path)
        if inventory is None:
            raise ReviewError(f"Corpus inventory does not exist: {inventory_path}")
        validate_inventory(inventory, config, assets)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        records = load_review_records(reviews_path)
        check_review_records(inventory, config.repository_root, records, schema)
    except (FileNotFoundError, InventoryError, json.JSONDecodeError, OSError, ReviewError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(records)} governed DSK review record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
