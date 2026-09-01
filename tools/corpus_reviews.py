"""Load and enforce governed review records for DSK corpus approvals."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from tools.desys_metadata import UniqueKeyLoader

REVIEW_RECORD_SCHEMA = "1.0.0"
SOURCE_DIMENSIONS = {"security", "privacy", "licensing", "editorial", "links", "identities"}
DSK_SOURCE_PREFIX = "skills/dsk/"


class ReviewError(ValueError):
    """Raised when a DSK review record cannot authorize distribution."""


def load_review_records(reviews_directory: Path) -> tuple[dict[str, Any], ...]:
    """Load versioned YAML review records in stable path order."""
    if not reviews_directory.is_dir():
        return ()
    return tuple(load_review_record(path) for path in sorted(reviews_directory.glob("*.yaml")))


def load_review_record(path: Path) -> dict[str, Any]:
    """Load one unique-key review record with path context."""
    if path.is_symlink() or not path.is_file():
        raise ReviewError(f"Review record must be a regular file: {path}")
    try:
        payload = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise ReviewError(f"Invalid review record YAML in {path}: {error}") from error
    if not isinstance(payload, dict):
        raise ReviewError(f"Review record must be a mapping: {path}")
    payload["_record_path"] = path.as_posix()
    return payload


def public_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a record without loader-only path context."""
    return {key: value for key, value in record.items() if key != "_record_path"}


def validate_dsk_distribution_reviews(
    inventory: dict[str, Any],
    records: tuple[dict[str, Any], ...],
) -> None:
    """Require exactly one fully approved exact review for every approved DSK entry."""
    record_ids: set[str] = set()
    for record in records:
        _validate_record(record)
        record_id = record["record_id"]
        if record_id in record_ids:
            raise ReviewError(f"Duplicate DSK review record_id: {record_id}")
        record_ids.add(record_id)

    entries = {entry["source"]: entry for entry in inventory["entries"]}
    for record in records:
        artifacts = record["source_review"]["artifacts"]
        selected = [entries.get(artifact["source"]) for artifact in artifacts]
        if any(
            entry is not None
            and entry.get("distribution") == "approved"
            and _artifact_matches_entry(artifact, entry)
            for artifact, entry in zip(artifacts, selected, strict=True)
        ) and any(
            entry is None
            or entry.get("distribution") != "approved"
            or not _artifact_matches_entry(artifact, entry)
            for artifact, entry in zip(artifacts, selected, strict=True)
        ):
            raise ReviewError(
                f"Governed DSK batch distribution must be all-or-none at exact fingerprints: {record['record_id']}"
            )

    for entry in inventory["entries"]:
        if entry.get("distribution") != "approved" or not _is_dsk_source(entry.get("source")):
            continue
        matches = [record for record in records if _record_authorizes_entry(record, entry)]
        if len(matches) != 1:
            raise ReviewError(
                f"Approved DSK entry requires exactly one exact approved source and package review: {entry['source']}"
            )


def validate_record_for_candidate(record: dict[str, Any], inventory: dict[str, Any], *, require_pending: bool) -> None:
    """Validate that one record selects exact current DSK entries for candidate rendering."""
    _validate_record(record)
    entries = {entry["source"]: entry for entry in inventory["entries"]}
    for artifact in record["source_review"]["artifacts"]:
        entry = entries.get(artifact["source"])
        if entry is None or not _artifact_matches_entry(artifact, entry):
            raise ReviewError(f"Review artifact does not match the current inventory: {artifact['source']}")
        if require_pending and entry["distribution"] != "pending":
            raise ReviewError(f"Review candidate selection must be pending: {artifact['source']}")


def _validate_record(record: dict[str, Any]) -> None:
    label = record.get("_record_path", record.get("record_id", "<review record>"))
    _require(record.get("review_record_schema") == REVIEW_RECORD_SCHEMA, f"Unsupported review schema: {label}")
    _require(isinstance(record.get("record_id"), str) and record["record_id"], f"Missing record_id: {label}")
    selected_ids = record.get("selected_ids")
    boundaries = record.get("boundaries")
    source_review = record.get("source_review")
    package_review = record.get("package_review")
    open_issues = record.get("open_issues")
    _require(isinstance(selected_ids, list) and selected_ids, f"selected_ids must be non-empty: {label}")
    _require(isinstance(boundaries, dict), f"boundaries must be a mapping: {label}")
    _require(isinstance(source_review, dict), f"source_review must be a mapping: {label}")
    _require(isinstance(package_review, dict), f"package_review must be a mapping: {label}")
    _require(isinstance(open_issues, list), f"open_issues must be a list: {label}")
    for issue in open_issues:
        _validate_issue(issue, label)

    artifacts = source_review.get("artifacts")
    _require(isinstance(artifacts, list) and artifacts, f"source_review.artifacts must be non-empty: {label}")
    artifact_sources: set[str] = set()
    for artifact in artifacts:
        _require(isinstance(artifact, dict), f"Source review artifacts must be mappings: {label}")
        required = {
            "document_id",
            "canonical_id",
            "source",
            "checksum",
            "review_fingerprint",
            "metadata_status",
        }
        _require(set(artifact) == required, f"Source review artifact fields are invalid: {label}")
        _require(_is_dsk_source(artifact["source"]), f"Review artifact is outside skills/dsk: {label}")
        _require(artifact["source"] not in artifact_sources, f"Duplicate source review artifact: {label}")
        artifact_sources.add(artifact["source"])
    _require(selected_ids == [artifact["document_id"] for artifact in artifacts], f"selected_ids are stale: {label}")
    _require(
        boundaries.get("selected_source_documents") == [artifact["source"] for artifact in artifacts],
        f"Selected source boundaries are stale: {label}",
    )

    dimensions = source_review.get("dimensions")
    _require(isinstance(dimensions, dict) and set(dimensions) == SOURCE_DIMENSIONS, f"Review dimensions invalid: {label}")
    for dimension, decision in dimensions.items():
        _validate_decision(decision, f"{label} source {dimension}")
    source_status = source_review.get("status")
    _require(source_status in {"PENDING", "APPROVED"}, f"Invalid source review status: {label}")
    if source_status == "APPROVED":
        _require(
            all(decision["status"] == "APPROVED" for decision in dimensions.values()),
            f"Approved source review has pending dimensions: {label}",
        )
        _require(_issues_closed(open_issues), f"Source approval is blocked by unresolved open issues: {label}")

    generation_status = package_review.get("generation_status")
    package_status = package_review.get("status")
    candidate = package_review.get("candidate")
    _require(generation_status in {"NOT GENERATED", "GENERATED"}, f"Invalid package generation status: {label}")
    _require(package_status in {"PENDING", "APPROVED"}, f"Invalid package review status: {label}")
    _validate_decision(package_review.get("packaged_bytes"), f"{label} packaged_bytes")
    if generation_status == "NOT GENERATED":
        _require(candidate is None and package_status == "PENDING", f"Ungenerated package review cannot approve: {label}")
    else:
        _validate_candidate_binding(candidate, artifacts, label)
    if package_status == "APPROVED":
        _require(source_status == "APPROVED", f"Package approval requires source approval: {label}")
        _require(generation_status == "GENERATED", f"Package approval requires a generated candidate: {label}")
        _require(
            package_review["packaged_bytes"]["status"] == "APPROVED",
            f"Package approval requires packaged_bytes approval: {label}",
        )
        _require(_issues_closed(open_issues), f"Package approval is blocked by unresolved open issues: {label}")


def _validate_decision(decision: Any, label: str) -> None:
    _require(isinstance(decision, dict), f"Decision must be a mapping: {label}")
    _require(set(decision) == {"status", "approver", "decided_at", "evidence"}, f"Decision fields invalid: {label}")
    status = decision.get("status")
    _require(status in {"PENDING", "APPROVED"}, f"Decision status invalid: {label}")
    evidence_fields = (decision.get("approver"), decision.get("decided_at"), decision.get("evidence"))
    if status == "APPROVED":
        _require(
            all(isinstance(value, str) and value.strip() for value in evidence_fields),
            f"Approved decision requires approver, timestamp, and evidence: {label}",
        )
    else:
        _require(all(value is None for value in evidence_fields), f"Pending decision cannot contain approval evidence: {label}")


def _validate_issue(issue: Any, label: str) -> None:
    _require(isinstance(issue, dict), f"Open issues must be mappings: {label}")
    required = {"issue_id", "description", "disposition", "approver", "decided_at", "evidence", "rationale"}
    _require(set(issue) == required, f"Open issue fields invalid: {label}")
    _require(isinstance(issue["issue_id"], str) and issue["issue_id"], f"Open issue ID invalid: {label}")
    _require(isinstance(issue["description"], str) and issue["description"], f"Open issue description invalid: {label}")
    disposition = issue["disposition"]
    _require(disposition in {"OPEN", "RESOLVED", "ACCEPTED_RISK"}, f"Open issue disposition invalid: {label}")
    decision_fields = (issue["approver"], issue["decided_at"], issue["evidence"], issue["rationale"])
    if disposition == "OPEN":
        _require(all(value is None for value in decision_fields), f"Open issue cannot contain disposition evidence: {label}")
    else:
        _require(
            all(isinstance(value, str) and value.strip() for value in decision_fields),
            f"Issue disposition requires approver, timestamp, evidence, and rationale: {label}",
        )


def _issues_closed(issues: list[dict[str, Any]]) -> bool:
    return all(issue["disposition"] in {"RESOLVED", "ACCEPTED_RISK"} for issue in issues)


def _validate_candidate_binding(candidate: Any, artifacts: list[dict[str, Any]], label: str) -> None:
    _require(isinstance(candidate, dict), f"Generated package review requires candidate binding: {label}")
    required = {
        "bundle_checksum",
        "entries_checksum",
        "descriptor",
        "entry_count",
        "closure",
        "selected_entries",
        "packaged_copies",
    }
    _require(set(candidate) == required, f"Candidate binding fields invalid: {label}")
    _require(_is_checksum(candidate["bundle_checksum"]), f"Candidate bundle checksum invalid: {label}")
    _require(_is_checksum(candidate["entries_checksum"]), f"Candidate entries checksum invalid: {label}")
    descriptor = candidate["descriptor"]
    _require(
        isinstance(descriptor, dict)
        and descriptor.get("path") == "bundle.yaml"
        and _is_checksum(descriptor.get("checksum")),
        f"Candidate descriptor binding invalid: {label}",
    )
    entry_count = candidate["entry_count"]
    closure = candidate["closure"]
    _require(isinstance(entry_count, int) and entry_count > 0, f"Candidate entry count invalid: {label}")
    _require(
        isinstance(closure, dict)
        and closure.get("status") == "VALIDATED"
        and closure.get("entry_count") == entry_count,
        f"Candidate closure binding invalid: {label}",
    )
    selected_entries = candidate["selected_entries"]
    packaged_copies = candidate["packaged_copies"]
    _require(
        isinstance(selected_entries, list) and len(selected_entries) == len(artifacts),
        f"Candidate selected entry binding is incomplete: {label}",
    )
    _require(
        isinstance(packaged_copies, list) and len(packaged_copies) == len(artifacts),
        f"Candidate packaged copy binding is incomplete: {label}",
    )
    for selected, packaged, artifact in zip(selected_entries, packaged_copies, artifacts, strict=True):
        _require(isinstance(selected, dict), f"Candidate selected entry is invalid: {label}")
        _require(isinstance(packaged, dict), f"Candidate packaged copy is invalid: {label}")
        _require(
            selected.get("source") == artifact["source"]
            and selected.get("checksum") == artifact["checksum"]
            and selected.get("review_fingerprint") == artifact["review_fingerprint"],
            f"Candidate selected entry is stale: {label}",
        )
        _require(packaged.get("checksum") == artifact["checksum"], f"Candidate packaged checksum is stale: {label}")
        _require(
            packaged.get("path") == f"corpus-files/{selected.get('target')}",
            f"Candidate packaged path does not match its selected target: {label}",
        )


def _record_authorizes_entry(record: dict[str, Any], entry: dict[str, Any]) -> bool:
    source_review = record["source_review"]
    package_review = record["package_review"]
    if source_review["status"] != "APPROVED" or package_review["status"] != "APPROVED":
        return False
    artifact = next(
        (item for item in source_review["artifacts"] if item["source"] == entry["source"]),
        None,
    )
    if artifact is None or not _artifact_matches_entry(artifact, entry):
        return False
    candidate = package_review["candidate"]
    selected = {item["target"]: item["checksum"] for item in candidate["selected_entries"]}
    packaged = {item["path"]: item["checksum"] for item in candidate["packaged_copies"]}
    return (
        selected.get(entry["target"]) == entry["checksum"]
        and packaged.get(f"corpus-files/{entry['target']}") == entry["checksum"]
    )


def _artifact_matches_entry(artifact: dict[str, Any], entry: dict[str, Any]) -> bool:
    return artifact == {
        "document_id": entry.get("document_id"),
        "canonical_id": entry.get("canonical_id"),
        "source": entry.get("source"),
        "checksum": entry.get("checksum"),
        "review_fingerprint": entry.get("review_fingerprint"),
        "metadata_status": entry.get("metadata_status"),
    }


def _is_dsk_source(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(DSK_SOURCE_PREFIX)


def _is_checksum(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        return False
    return all(character in "0123456789abcdef" for character in value[7:])


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewError(message)
