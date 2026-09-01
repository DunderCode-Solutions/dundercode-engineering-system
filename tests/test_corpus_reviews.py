from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from tools.build_corpus_bundle import build_bundle
from tools.build_corpus_inventory import load_asset_config, load_inventory, validate_inventory
from tools.build_corpus_review_candidate import build_review_candidate, validate_or_write_candidate
from tools.check_corpus_reviews import check_review_records
from tools.corpus_reviews import (
    ReviewError,
    load_review_record,
    public_record,
    validate_dsk_distribution_reviews,
)
from tools.desys_indexer.config import load_config

REVIEW_PATH = Path("corpus/reviews/pr6-phase-1-domain-reference-review-2026-08-30.yaml")
SCHEMA_PATH = Path("corpus/reviews/dsk-batch-review-1.0.0.schema.json")
CHECKSUM = "sha256:" + "1" * 64
FINGERPRINT = "sha256:" + "2" * 64
BUNDLE_CHECKSUM = "sha256:" + "3" * 64
DESCRIPTOR_CHECKSUM = "sha256:" + "4" * 64
ENTRIES_CHECKSUM = "sha256:" + "6" * 64


def _entry(*, fingerprint: str = FINGERPRINT, distribution: str = "approved", suffix: str = "9999") -> dict:
    return {
        "source": f"skills/dsk/test/DSK-{suffix}-review-test.md",
        "target": f"docs/desys/reference/skills/dsk/test/DSK-{suffix}-review-test.md",
        "distribution": distribution,
        "checksum": CHECKSUM,
        "review_fingerprint": fingerprint,
        "document_id": f"DSK-{suffix}",
        "canonical_id": f"dsk.test.review-test-{suffix}",
        "metadata_status": "review",
    }


def _decision(status: str = "APPROVED") -> dict:
    if status == "PENDING":
        return {"status": status, "approver": None, "decided_at": None, "evidence": None}
    return {
        "status": status,
        "approver": "authorized-reviewer@example.test",
        "decided_at": "2026-08-30T12:00:00Z",
        "evidence": "review-evidence://DSK-9999",
    }


def _record(entry: dict | None = None) -> dict:
    entry = entry or _entry()
    artifact = {
        key: entry[key]
        for key in (
            "document_id",
            "canonical_id",
            "source",
            "checksum",
            "review_fingerprint",
            "metadata_status",
        )
    }
    selected = {
        "source": entry["source"],
        "target": entry["target"],
        "checksum": entry["checksum"],
        "review_fingerprint": entry["review_fingerprint"],
    }
    packaged = {"path": f"corpus-files/{entry['target']}", "checksum": entry["checksum"]}
    return {
        "review_record_schema": "1.0.0",
        "record_id": "synthetic-dsk-review",
        "phase": 2,
        "review_date": "2026-08-30",
        "review_owner": "DunderCode Engineering",
        "selected_ids": [entry["document_id"]],
        "boundaries": {
            "selected_source_documents": [entry["source"]],
            "excluded_changes": ["official package resources"],
        },
        "source_review": {
            "status": "APPROVED",
            "artifacts": [artifact],
            "dimensions": {
                dimension: _decision()
                for dimension in ("security", "privacy", "licensing", "editorial", "links", "identities")
            },
        },
        "package_review": {
            "generation_status": "GENERATED",
            "status": "APPROVED",
            "candidate": {
                "bundle_checksum": BUNDLE_CHECKSUM,
                "entries_checksum": ENTRIES_CHECKSUM,
                "descriptor": {"path": "bundle.yaml", "checksum": DESCRIPTOR_CHECKSUM},
                "entry_count": 42,
                "closure": {"status": "VALIDATED", "entry_count": 42},
                "selected_entries": [selected],
                "packaged_copies": [packaged],
            },
            "packaged_bytes": _decision(),
        },
        "open_issues": [],
        "approval_instruction": "Source and package review are both required before distribution.",
    }


def test_tracked_review_record_matches_versioned_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    record = load_review_record(REVIEW_PATH)

    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(public_record(record)))

    assert schema["$id"] == "urn:uuid:f26d2097-47aa-4f61-8a28-5c64acc93aa8"
    assert errors == []


def test_approved_dsk_entry_rejects_missing_review() -> None:
    with pytest.raises(ReviewError, match="exactly one exact approved"):
        validate_dsk_distribution_reviews({"entries": [_entry()]}, ())


def test_approved_decision_rejects_missing_approver_and_evidence() -> None:
    record = _record()
    record["source_review"]["dimensions"]["security"] = {
        "status": "APPROVED",
        "approver": None,
        "decided_at": None,
        "evidence": None,
    }

    with pytest.raises(ReviewError, match="requires approver, timestamp, and evidence"):
        validate_dsk_distribution_reviews({"entries": [_entry()]}, (record,))


def test_source_only_approval_cannot_authorize_distribution() -> None:
    record = _record()
    record["package_review"] = {
        "generation_status": "NOT GENERATED",
        "status": "PENDING",
        "candidate": None,
        "packaged_bytes": _decision("PENDING"),
    }

    with pytest.raises(ReviewError, match="exactly one exact approved"):
        validate_dsk_distribution_reviews({"entries": [_entry()]}, (record,))


def test_stale_review_fingerprint_cannot_authorize_distribution() -> None:
    record = _record()
    current = _entry(fingerprint="sha256:" + "5" * 64)

    with pytest.raises(ReviewError, match="exactly one exact approved"):
        validate_dsk_distribution_reviews({"entries": [current]}, (record,))


def test_package_approval_rejects_missing_candidate_binding() -> None:
    record = _record()
    record["package_review"]["candidate"] = None

    with pytest.raises(ReviewError, match="requires candidate binding"):
        validate_dsk_distribution_reviews({"entries": [_entry()]}, (record,))


def test_valid_synthetic_full_approval_authorizes_exact_entry() -> None:
    entry = _entry()

    validate_dsk_distribution_reviews({"entries": [entry]}, (_record(entry),))


def test_partial_governed_batch_distribution_is_rejected() -> None:
    approved = _entry()
    pending = _entry(distribution="pending", suffix="9998")
    record = _record(approved)
    pending_artifact = {
        key: pending[key]
        for key in (
            "document_id",
            "canonical_id",
            "source",
            "checksum",
            "review_fingerprint",
            "metadata_status",
        )
    }
    record["selected_ids"].append(pending["document_id"])
    record["boundaries"]["selected_source_documents"].append(pending["source"])
    record["source_review"]["artifacts"].append(pending_artifact)
    record["package_review"]["candidate"]["selected_entries"].append(
        {
            "source": pending["source"],
            "target": pending["target"],
            "checksum": pending["checksum"],
            "review_fingerprint": pending["review_fingerprint"],
        }
    )
    record["package_review"]["candidate"]["packaged_copies"].append(
        {"path": f"corpus-files/{pending['target']}", "checksum": pending["checksum"]}
    )

    with pytest.raises(ReviewError, match="all-or-none"):
        validate_dsk_distribution_reviews({"entries": [approved, pending]}, (record,))


def test_open_issue_blocks_approval() -> None:
    record = _record()
    record["open_issues"] = [
        {
            "issue_id": "browser-verification",
            "description": "Human browser verification is incomplete.",
            "disposition": "OPEN",
            "approver": None,
            "decided_at": None,
            "evidence": None,
            "rationale": None,
        }
    ]

    with pytest.raises(ReviewError, match="blocked by unresolved open issues"):
        validate_dsk_distribution_reviews({"entries": [_entry()]}, (record,))


def test_accepted_risk_issue_with_authorized_evidence_allows_approval() -> None:
    record = _record()
    record["open_issues"] = [
        {
            "issue_id": "browser-verification",
            "description": "Human browser verification cannot be completed.",
            "disposition": "ACCEPTED_RISK",
            "approver": "authorized-reviewer@example.test",
            "decided_at": "2026-08-30T12:00:00Z",
            "evidence": "review-evidence://browser-verification",
            "rationale": "The linked source is provenance-only and distribution accepts the documented limitation.",
        }
    ]

    validate_dsk_distribution_reviews({"entries": [_entry()]}, (record,))


def test_generic_checker_rejects_stale_pending_record(tmp_path: Path) -> None:
    current = _entry(fingerprint="sha256:" + "7" * 64, distribution="pending")
    record = _record(_entry(distribution="pending"))
    record["source_review"]["status"] = "PENDING"
    record["source_review"]["dimensions"] = {
        dimension: _decision("PENDING") for dimension in record["source_review"]["dimensions"]
    }
    record["package_review"] = {
        "generation_status": "NOT GENERATED",
        "status": "PENDING",
        "candidate": None,
        "packaged_bytes": _decision("PENDING"),
    }
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    with pytest.raises(ReviewError, match="does not match the current inventory"):
        check_review_records({"entries": [current]}, tmp_path, (record,), schema)


def test_approved_review_rejects_official_bundle_mismatch() -> None:
    config = load_config(Path("tools/desys_indexer.yaml"))
    assets = load_asset_config(Path("corpus/assets.yaml"), config.repository_root, config.sources)
    inventory = load_inventory(Path("corpus/inventory.yaml"))
    assert inventory is not None
    validate_inventory(inventory, config, assets)
    record = load_review_record(REVIEW_PATH)
    record["source_review"]["status"] = "APPROVED"
    record["source_review"]["dimensions"] = {
        dimension: _decision() for dimension in record["source_review"]["dimensions"]
    }
    record["open_issues"] = []
    _, _, report = build_review_candidate(inventory, config.repository_root, record, require_pending=True)
    record["package_review"] = {
        "generation_status": "GENERATED",
        "status": "APPROVED",
        "candidate": report["candidate"],
        "packaged_bytes": _decision(),
    }
    approved_inventory = deepcopy(inventory)
    selected = {artifact["source"] for artifact in record["source_review"]["artifacts"]}
    for entry in approved_inventory["entries"]:
        if entry["source"] in selected:
            entry["distribution"] = "approved"
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    check_review_records(approved_inventory, config.repository_root, (record,), schema)
    record["package_review"]["candidate"]["entries_checksum"] = "sha256:" + "0" * 64
    with pytest.raises(ReviewError, match="does not match the official bundle"):
        check_review_records(approved_inventory, config.repository_root, (record,), schema)


def test_review_candidate_is_deterministic_external_and_non_official(tmp_path: Path) -> None:
    config = load_config(Path("tools/desys_indexer.yaml"))
    assets = load_asset_config(Path("corpus/assets.yaml"), config.repository_root, config.sources)
    inventory = load_inventory(Path("corpus/inventory.yaml"))
    assert inventory is not None
    validate_inventory(inventory, config, assets)
    record = load_review_record(REVIEW_PATH)
    official_manifest, official_files = build_bundle(inventory, config.repository_root)
    package_root = Path("tools/reference_corpus_data")
    official_bytes = {path.relative_to(package_root): path.read_bytes() for path in package_root.rglob("*") if path.is_file()}

    candidate_manifest, candidate_files, report = build_review_candidate(
        inventory,
        config.repository_root,
        record,
        require_pending=True,
    )
    output = tmp_path / "candidate"
    validate_or_write_candidate(output, config.repository_root, candidate_files, report, check=False)
    validate_or_write_candidate(output, config.repository_root, candidate_files, report, check=True)

    assert len(official_manifest["entries"]) == 41
    assert len(official_files) == 42
    assert len(candidate_manifest["entries"]) == 46
    assert report["candidate"]["closure"] == {"status": "VALIDATED", "entry_count": 46}
    assert len(report["candidate"]["selected_entries"]) == 5
    assert official_bytes == {
        path.relative_to(package_root): path.read_bytes() for path in package_root.rglob("*") if path.is_file()
    }


def test_review_candidate_refuses_repository_output() -> None:
    with pytest.raises(ReviewError, match="outside the repository"):
        validate_or_write_candidate(
            Path("build/review-candidate"),
            Path.cwd(),
            {},
            {},
            check=False,
        )
