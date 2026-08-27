import json
import re
from pathlib import Path

import pytest
import yaml

from tools.desys_metadata import (
    DOCUMENT_CLASSES,
    NODE_TYPES,
    OPTIONAL_FIELDS,
    RELATIONSHIP_TYPES,
    REQUIRED_FIELDS,
    STATUSES,
    FrontMatterError,
    parse_front_matter,
    validate_document_metadata,
    validate_repository,
)
from tools.migrate_metadata import migrate_document

VALID_METADATA = {
    "metadata_schema": "1.0.0",
    "document_id": "DES-0200",
    "canonical_id": "des.quality.code-quality",
    "title": "Code Quality Standard",
    "node_type": "standard",
    "document_class": "normative",
    "version": "1.0.0",
    "status": "draft",
    "language": "en",
    "owner": "DunderCode Engineering",
}


class TestFrontMatter:
    def test_parses_front_matter_and_body(self) -> None:
        markdown = "---\nmetadata_schema: 1.0.0\ntitle: Test\n---\n# Test\n"

        metadata, body = parse_front_matter(markdown)

        assert metadata["metadata_schema"] == "1.0.0"
        assert body == "# Test\n"

    def test_rejects_body_metadata(self) -> None:
        with pytest.raises(FrontMatterError):
            parse_front_matter("# Test\n\n# Metadata\n")

    def test_rejects_duplicate_yaml_keys(self) -> None:
        markdown = "---\ntitle: First\ntitle: Second\n---\n# Test\n"

        with pytest.raises(FrontMatterError):
            parse_front_matter(markdown)


class TestMetadataValidation:
    def test_json_schema_has_stable_resource_id(self) -> None:
        schema_path = Path("knowledge/architecture/metadata/desys-metadata.schema.json")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        assert schema["$id"] == "urn:uuid:22eb6a5c-efb9-5581-9ee5-e52435153086"

    def test_json_schema_matches_validator_contract(self) -> None:
        schema_path = Path("knowledge/architecture/metadata/desys-metadata.schema.json")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        properties = schema["properties"]
        assert set(schema["required"]) == set(REQUIRED_FIELDS)
        assert set(properties) == set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)
        assert schema["properties"]["metadata_schema"]["const"] == "1.0.0"
        assert set(properties["node_type"]["enum"]) == NODE_TYPES
        assert set(properties["document_class"]["enum"]) == DOCUMENT_CLASSES
        assert set(properties["status"]["enum"]) == STATUSES
        relationship_enum = schema["$defs"]["relationship"]["properties"]["type"]["enum"]
        assert set(relationship_enum) == RELATIONSHIP_TYPES

    def test_json_schema_patterns_reject_newline_terminated_values_under_search_semantics(self) -> None:
        schema_path = Path("knowledge/architecture/metadata/desys-metadata.schema.json")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        relationship_target = definitions["relationship"]["properties"]["target"]

        assert relationship_target == {"$ref": "#/$defs/canonicalId"}
        cases = (
            (schema["properties"]["document_id"]["pattern"], "DES-0200"),
            (definitions["canonicalId"]["pattern"], "des.quality.code-quality"),
            (definitions["legacyCanonicalId"]["pattern"], "des.code-quality"),
            (definitions["canonicalId"]["pattern"], "des.quality.relationship-target"),
            (schema["properties"]["version"]["pattern"], "1.0.0"),
        )

        for pattern, valid_value in cases:
            assert re.search(pattern, valid_value) is not None
            assert re.search(pattern, f"{valid_value}\n") is None

    def test_accepts_valid_metadata(self) -> None:
        issues = validate_document_metadata(
            VALID_METADATA,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert issues == []

    def test_rejects_unknown_fields(self) -> None:
        metadata = {**VALID_METADATA, "unexpected": True}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert any("unknown field 'unexpected'" in issue.message for issue in issues)

    def test_rejects_non_string_key_without_crashing(self) -> None:
        metadata = {**VALID_METADATA, 1: "unexpected"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert any("must be a string" in issue.message for issue in issues)

    def test_accepts_identifier_only_filename(self) -> None:
        issues = validate_document_metadata(VALID_METADATA, Path("knowledge/des/DES-0200.md"))

        assert issues == []

    def test_warns_about_legacy_canonical_status(self) -> None:
        metadata = {**VALID_METADATA, "status": "canonical", "legacy_status": True}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert [issue.severity for issue in issues] == ["warning"]

    def test_rejects_unmarked_canonical_status(self) -> None:
        metadata = {**VALID_METADATA, "status": "canonical"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert any("requires legacy_status" in issue.message for issue in issues)

    def test_rejects_invalid_optional_container_without_crashing(self) -> None:
        metadata = {**VALID_METADATA, "aliases": None, "relationships": None}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert any("aliases must be a non-empty list" in issue.message for issue in issues)
        assert any("relationships must be a list" in issue.message for issue in issues)

    def test_rejects_non_english_canonical_language_in_v1(self) -> None:
        metadata = {**VALID_METADATA, "language": "pt-BR"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert any("must be 'en'" in issue.message for issue in issues)

    def test_accepts_legacy_two_segment_alias(self) -> None:
        metadata = {**VALID_METADATA, "aliases": ["des.code-quality"]}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        assert issues == []

    def test_detects_duplicate_ids_in_repository(self, tmp_path: Path) -> None:
        for document_id in ("DES-0200", "DES-0210"):
            path = tmp_path / f"{document_id}-test.md"
            metadata = {**VALID_METADATA, "document_id": document_id}
            front_matter = "\n".join(f"{key}: {value}" for key, value in metadata.items())
            path.write_text(f"---\n{front_matter}\n---\n# Test\n", encoding="utf-8")

        report = validate_repository(tmp_path)

        assert any("duplicate canonical_id" in issue.message for issue in report.errors)

    def test_alias_collision_identifies_canonical_owner(self, tmp_path: Path) -> None:
        first = tmp_path / "DES-0200-first.md"
        first_metadata = VALID_METADATA
        first.write_text(
            f"---\n{yaml.safe_dump(first_metadata, sort_keys=False)}---\n# First\n",
            encoding="utf-8",
        )
        second = tmp_path / "DES-0210-second.md"
        second_metadata = {
            **VALID_METADATA,
            "document_id": "DES-0210",
            "canonical_id": "des.quality.second",
            "aliases": [VALID_METADATA["canonical_id"]],
        }
        second.write_text(
            f"---\n{yaml.safe_dump(second_metadata, sort_keys=False)}---\n# Second\n",
            encoding="utf-8",
        )

        report = validate_repository(tmp_path)

        collision = next(issue for issue in report.errors if "conflicts with a canonical_id" in issue.message)
        assert collision.path == Path("DES-0210-second.md")
        assert "DES-0200-first.md" in collision.message


class TestMetadataMigration:
    def test_derives_document_id_from_identifier_only_filename(self) -> None:
        legacy = """# DES-0200 \u2014 Code Quality

Canonical ID: des.quality.code-quality
Document Class: Normative
Version: 1.0.0 (Draft)
Status: Draft
Canonical Language: English
Owner: DunderCode Engineering
---

# 1. Purpose

Body.
"""

        migrated = migrate_document(Path("DES-0200.md"), legacy)
        metadata, _ = parse_front_matter(migrated)

        assert metadata["document_id"] == "DES-0200"
