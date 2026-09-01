"""Render or verify a non-official DSK review candidate outside the repository."""

from __future__ import annotations

import argparse
import hashlib
import stat
import sys
import tempfile
from copy import deepcopy
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from tools.build_corpus_bundle import BundleError, build_bundle, validate_or_write_bundle
from tools.build_corpus_inventory import (
    DEFAULT_ASSETS,
    DEFAULT_CONFIG,
    DEFAULT_OUTPUT,
    InventoryError,
    load_asset_config,
    load_inventory,
    validate_inventory,
)
from tools.corpus_reviews import ReviewError, load_review_record, validate_record_for_candidate
from tools.desys_indexer.config import load_config
from tools.project_transaction import TransactionError, guard_operation

CANDIDATE_REVIEW_SCHEMA = "1.0.0"


def build_review_candidate(
    inventory: dict[str, Any],
    repository_root: Path,
    record: dict[str, Any],
    *,
    require_pending: bool,
) -> tuple[dict[str, Any], dict[PurePosixPath, bytes], dict[str, Any]]:
    """Build prospective package bytes from approved entries plus exact reviewed DSK sources."""
    validate_record_for_candidate(record, inventory, require_pending=require_pending)
    selected_sources = {artifact["source"] for artifact in record["source_review"]["artifacts"]}
    prospective = deepcopy(inventory)
    for entry in prospective["entries"]:
        if entry["source"] in selected_sources:
            entry["distribution"] = "approved"

    manifest, files = build_bundle(prospective, repository_root)
    binding = candidate_binding(manifest, files, inventory, record)
    report = {
        "candidate_review_schema": CANDIDATE_REVIEW_SCHEMA,
        "record_id": record["record_id"],
        "source_review_status": record["source_review"]["status"],
        "candidate": binding,
    }
    return manifest, files, report


def candidate_binding(
    manifest: dict[str, Any],
    files: dict[PurePosixPath, bytes],
    inventory: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    """Return the exact package-stage binding copied into an approved review record."""
    entries = {entry["source"]: entry for entry in inventory["entries"]}
    selected_entries = []
    packaged_copies = []
    for artifact in record["source_review"]["artifacts"]:
        entry = entries[artifact["source"]]
        packaged_path = PurePosixPath("corpus-files") / entry["target"]
        content_checksum = f"sha256:{hashlib.sha256(files[packaged_path]).hexdigest()}"
        if content_checksum != entry["checksum"]:
            raise ReviewError(f"Prospective packaged copy differs from selected source: {entry['source']}")
        selected_entries.append(
            {
                "source": entry["source"],
                "target": entry["target"],
                "checksum": entry["checksum"],
                "review_fingerprint": entry["review_fingerprint"],
            }
        )
        packaged_copies.append({"path": packaged_path.as_posix(), "checksum": content_checksum})
    descriptor_checksum = f"sha256:{hashlib.sha256(files[PurePosixPath('bundle.yaml')]).hexdigest()}"
    entries_bytes = yaml.safe_dump(
        manifest["entries"],
        sort_keys=False,
        allow_unicode=False,
        width=120,
    ).encode("utf-8")
    entry_count = len(manifest["entries"])
    return {
        "bundle_checksum": manifest["bundle_checksum"],
        "entries_checksum": f"sha256:{hashlib.sha256(entries_bytes).hexdigest()}",
        "descriptor": {"path": "bundle.yaml", "checksum": descriptor_checksum},
        "entry_count": entry_count,
        "closure": {"status": "VALIDATED", "entry_count": entry_count},
        "selected_entries": selected_entries,
        "packaged_copies": packaged_copies,
    }


def validate_or_write_candidate(
    output: Path,
    repository_root: Path,
    files: dict[PurePosixPath, bytes],
    report: dict[str, Any],
    *,
    check: bool,
) -> None:
    """Write only to an explicit external review directory, or verify it without mutation."""
    root = repository_root.resolve()
    destination = output.resolve(strict=False)
    if destination == root or destination.is_relative_to(root):
        raise ReviewError("Review candidate output must be outside the repository.")
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if destination != temporary_root and not destination.is_relative_to(temporary_root):
        raise ReviewError(f"Review candidate output must be under the temporary directory: {temporary_root}")
    if output.is_symlink():
        raise ReviewError(f"Review candidate output is a symlink: {output}")
    if output.exists() and not output.is_dir():
        raise ReviewError(f"Review candidate output is not a directory: {output}")
    expected_children = {"package", "review-candidate.yaml"}
    if output.is_dir():
        unexpected = {path.name for path in output.iterdir()} - expected_children
        if unexpected:
            raise ReviewError(f"Review candidate output contains unexpected paths: {', '.join(sorted(unexpected))}")

    report_bytes = yaml.safe_dump(report, sort_keys=False, allow_unicode=False, width=120).encode("utf-8")
    report_path = output / "review-candidate.yaml"
    if check:
        validate_or_write_bundle(output / "package", files, check=True)
        if not report_path.is_file() or report_path.is_symlink() or report_path.read_bytes() != report_bytes:
            raise ReviewError("Review candidate report is missing or stale.")
        return

    output.mkdir(parents=True, exist_ok=True)
    _preflight_report(report_path)
    validate_or_write_bundle(output / "package", files, check=False)
    report_path.write_bytes(report_bytes)


def _preflight_report(path: Path) -> None:
    if path.is_symlink():
        raise ReviewError(f"Review candidate report is a symlink: {path}")
    if not path.exists():
        return
    status = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
        raise ReviewError(f"Review candidate report is not a safe regular file: {path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--review-record", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="Verify an existing candidate without writing.")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        config = load_config(args.config)
        guard_operation(config.repository_root)
        assets_path = args.assets if args.assets.is_absolute() else config.repository_root / args.assets
        inventory_path = args.inventory if args.inventory.is_absolute() else config.repository_root / args.inventory
        record_path = (
            args.review_record
            if args.review_record.is_absolute()
            else config.repository_root / args.review_record
        )
        assets = load_asset_config(assets_path, config.repository_root, config.sources)
        inventory = load_inventory(inventory_path)
        if inventory is None:
            raise ReviewError(f"Corpus inventory does not exist: {inventory_path}")
        validate_inventory(inventory, config, assets)
        record = load_review_record(record_path)
        manifest, files, report = build_review_candidate(
            inventory,
            config.repository_root,
            record,
            require_pending=True,
        )
        validate_or_write_candidate(args.output, config.repository_root, files, report, check=args.check)
    except (
        BundleError,
        FileNotFoundError,
        InventoryError,
        OSError,
        ReviewError,
        TransactionError,
        UnicodeError,
        yaml.YAMLError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    action = "Verified" if args.check else "Wrote"
    print(
        f"{action} DSK review candidate with {len(manifest['entries'])} entries "
        f"({manifest['bundle_checksum']}) at {args.output}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
