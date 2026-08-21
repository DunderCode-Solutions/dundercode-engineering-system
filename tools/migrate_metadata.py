#!/usr/bin/env python3
"""Migrate legacy DESys metadata blocks to canonical YAML front matter."""

from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.desys_metadata import (
    MANAGED_FILENAME_PATTERN,
    managed_documents,
    parse_front_matter,
    validate_document_metadata,
)

FIELD_PATTERN = re.compile(
    r"^\s*(?:\*\*)?([A-Za-z][A-Za-z ]+?):(?:\*\*)?\s*(.*?)\s*$"
)
TITLE_PATTERN = re.compile(r"^#\s+[A-Z]+-[0-9]{4}\s*(?:\u2014|\|)\s*(.+?)\s*$")

NODE_TYPES = {
    "ADR": "decision",
    "DAR": "assessment",
    "DCSG": "style-guide",
    "DEA": "architecture",
    "DEC": "canon",
    "DEKG": "specification",
    "DEM": "method",
    "DES": "standard",
    "DET": "template",
    "DEP": "process",
    "DSB": "architecture",
    "DSK": "skill",
    "DSP": "specification",
    "GUIDE": "guide",
    "PRD": "product-requirement",
    "RFC": "proposal",
}

SPECIAL_CANONICAL_IDS = {
    "DEC-0001": "dec.foundation.engineering-manifesto",
    "DEM-0001": "dem.foundation.engineering-method",
}

RENAMED_CANONICAL_IDS = {
    "dar.evidence-collection": "dar.assessment.evidence-collection",
    "dar.findings-recommendations": "dar.assessment.findings-recommendations",
    "dar.quality-scoring": "dar.assessment.quality-scoring",
    "dar.continuous-improvement": "dar.assessment.continuous-improvement",
    "dar.assessment-governance": "dar.assessment.governance",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--write", action="store_true", help="Write migrated documents.")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    root = arguments.root.resolve()
    migrated: list[Path] = []
    skipped_placeholders: list[Path] = []
    updates: list[tuple[Path, str]] = []

    for path in managed_documents(root):
        markdown = path.read_text(encoding="utf-8")
        if not markdown.strip():
            skipped_placeholders.append(path.relative_to(root))
            continue
        if _has_front_matter(markdown):
            continue

        updated = migrate_document(path, markdown)
        updated_metadata, _ = parse_front_matter(updated)
        errors = [
            issue
            for issue in validate_document_metadata(updated_metadata, path)
            if issue.severity == "error"
        ]
        if errors:
            messages = "; ".join(issue.message for issue in errors)
            raise ValueError(f"Migrated metadata is invalid for {path}: {messages}")
        migrated.append(path.relative_to(root))
        updates.append((path, updated))

    if arguments.write:
        for path, updated in updates:
            path.write_text(updated, encoding="utf-8")

    action = "Migrated" if arguments.write else "Would migrate"
    print(f"{action} {len(migrated)} document(s).")
    print(f"Skipped {len(skipped_placeholders)} empty placeholder(s).")
    return 0


def migrate_document(path: Path, markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines:
        raise ValueError(f"Cannot migrate empty document: {path}")

    delimiter_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if delimiter_index is None:
        raise ValueError(f"Legacy metadata delimiter not found: {path}")

    heading = next(
        (line.strip() for line in lines[:delimiter_index] if line.strip().startswith("# ")),
        None,
    )
    if heading is None:
        raise ValueError(f"Document title not found: {path}")

    fields = _parse_legacy_fields(lines[:delimiter_index])
    filename_match = MANAGED_FILENAME_PATTERN.fullmatch(path.name)
    filename_document_id = filename_match.group("document_id") if filename_match else None
    document_id = fields.get("Document Number") or fields.get("Document ID") or filename_document_id
    if document_id is None:
        raise ValueError(f"Document ID cannot be derived: {path}")
    prefix = document_id.split("-", 1)[0]
    title = _extract_title(heading)

    old_canonical_id = fields.get("Canonical ID") or SPECIAL_CANONICAL_IDS.get(document_id)
    if old_canonical_id is None:
        raise ValueError(f"Canonical ID cannot be derived: {path}")
    canonical_id = RENAMED_CANONICAL_IDS.get(old_canonical_id, old_canonical_id)

    metadata: dict[str, Any] = OrderedDict()
    metadata["metadata_schema"] = "1.0.0"
    metadata["document_id"] = document_id
    metadata["canonical_id"] = canonical_id
    metadata["title"] = title
    metadata["node_type"] = NODE_TYPES[prefix]
    metadata["document_class"] = "operational" if prefix == "DSK" else "normative"
    metadata["version"] = _normalize_version(fields["Version"])
    metadata["status"] = fields["Status"].lower()
    if metadata["status"] == "canonical":
        metadata["legacy_status"] = True
    metadata["language"] = _normalize_language(fields["Canonical Language"])
    metadata["owner"] = fields["Owner"]

    optional_mapping = {
        "Engineering Domain": "domain",
        "Engineering Discipline": "discipline",
        "Architecture Model": "architecture_model",
    }
    for legacy_field, canonical_field in optional_mapping.items():
        if value := fields.get(legacy_field):
            metadata[canonical_field] = value

    if applies_to := fields.get("Applies To"):
        metadata["applies_to"] = [applies_to]
    if canonical_id != old_canonical_id:
        metadata["aliases"] = [old_canonical_id]
    depends_on = fields.get("Depends On")
    if depends_on == "DEC-0001":
        metadata["relationships"] = [
            {"type": "depends_on", "target": SPECIAL_CANONICAL_IDS["DEC-0001"]}
        ]
    elif depends_on is not None:
        raise ValueError(f"Unsupported legacy Depends On value '{depends_on}': {path}")

    body_lines = lines[delimiter_index + 1 :]
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    front_matter = yaml.safe_dump(
        dict(metadata),
        sort_keys=False,
        allow_unicode=False,
        default_flow_style=False,
    ).rstrip()
    body = "\n".join([heading, "", *body_lines]).rstrip() + "\n"
    return f"---\n{front_matter}\n---\n\n{body}"


def _parse_legacy_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in lines:
        match = FIELD_PATTERN.match(line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def _extract_title(heading: str) -> str:
    match = TITLE_PATTERN.match(heading)
    if match is None:
        raise ValueError(f"Document title has an unsupported format: {heading}")
    return match.group(1)


def _normalize_version(value: str) -> str:
    return re.sub(r"\s*\(Draft\)\s*$", "", value, flags=re.IGNORECASE)


def _normalize_language(value: str) -> str:
    if value.lower() == "english":
        return "en"
    return value


def _has_front_matter(markdown: str) -> bool:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    parse_front_matter(markdown)
    return True


if __name__ == "__main__":
    raise SystemExit(main())
