import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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


class FrontMatterTests(unittest.TestCase):
    def test_parses_front_matter_and_body(self) -> None:
        markdown = "---\nmetadata_schema: 1.0.0\ntitle: Test\n---\n# Test\n"

        metadata, body = parse_front_matter(markdown)

        self.assertEqual(metadata["metadata_schema"], "1.0.0")
        self.assertEqual(body, "# Test\n")

    def test_rejects_body_metadata(self) -> None:
        with self.assertRaises(FrontMatterError):
            parse_front_matter("# Test\n\n# Metadata\n")

    def test_rejects_duplicate_yaml_keys(self) -> None:
        markdown = "---\ntitle: First\ntitle: Second\n---\n# Test\n"

        with self.assertRaises(FrontMatterError):
            parse_front_matter(markdown)


class MetadataValidationTests(unittest.TestCase):
    def test_json_schema_matches_validator_contract(self) -> None:
        schema_path = Path("knowledge/architecture/metadata/desys-metadata.schema.json")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        properties = schema["properties"]
        self.assertEqual(set(schema["required"]), set(REQUIRED_FIELDS))
        self.assertEqual(set(properties), set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS))
        self.assertEqual(schema["properties"]["metadata_schema"]["const"], "1.0.0")
        self.assertEqual(set(properties["node_type"]["enum"]), NODE_TYPES)
        self.assertEqual(set(properties["document_class"]["enum"]), DOCUMENT_CLASSES)
        self.assertEqual(set(properties["status"]["enum"]), STATUSES)
        relationship_enum = schema["$defs"]["relationship"]["properties"]["type"]["enum"]
        self.assertEqual(set(relationship_enum), RELATIONSHIP_TYPES)

    def test_accepts_valid_metadata(self) -> None:
        issues = validate_document_metadata(
            VALID_METADATA,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertEqual(issues, [])

    def test_rejects_unknown_fields(self) -> None:
        metadata = {**VALID_METADATA, "unexpected": True}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertTrue(any("unknown field 'unexpected'" in issue.message for issue in issues))

    def test_rejects_non_string_key_without_crashing(self) -> None:
        metadata = {**VALID_METADATA, 1: "unexpected"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertTrue(any("must be a string" in issue.message for issue in issues))

    def test_accepts_identifier_only_filename(self) -> None:
        issues = validate_document_metadata(VALID_METADATA, Path("knowledge/des/DES-0200.md"))

        self.assertEqual(issues, [])

    def test_warns_about_legacy_canonical_status(self) -> None:
        metadata = {**VALID_METADATA, "status": "canonical", "legacy_status": True}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertEqual([issue.severity for issue in issues], ["warning"])

    def test_rejects_unmarked_canonical_status(self) -> None:
        metadata = {**VALID_METADATA, "status": "canonical"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertTrue(any("requires legacy_status" in issue.message for issue in issues))

    def test_rejects_invalid_optional_container_without_crashing(self) -> None:
        metadata = {**VALID_METADATA, "aliases": None, "relationships": None}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertTrue(any("aliases must be a non-empty list" in issue.message for issue in issues))
        self.assertTrue(any("relationships must be a list" in issue.message for issue in issues))

    def test_rejects_non_english_canonical_language_in_v1(self) -> None:
        metadata = {**VALID_METADATA, "language": "pt-BR"}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertTrue(any("must be 'en'" in issue.message for issue in issues))

    def test_accepts_legacy_two_segment_alias(self) -> None:
        metadata = {**VALID_METADATA, "aliases": ["des.code-quality"]}

        issues = validate_document_metadata(
            metadata,
            Path("knowledge/des/quality/DES-0200-code-quality-standard.md"),
        )

        self.assertEqual(issues, [])

    def test_detects_duplicate_ids_in_repository(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for document_id in ("DES-0200", "DES-0210"):
                path = root / f"{document_id}-test.md"
                metadata = {**VALID_METADATA, "document_id": document_id}
                front_matter = "\n".join(f"{key}: {value}" for key, value in metadata.items())
                path.write_text(f"---\n{front_matter}\n---\n# Test\n", encoding="utf-8")

            report = validate_repository(root)

        self.assertTrue(any("duplicate canonical_id" in issue.message for issue in report.errors))


class MetadataMigrationTests(unittest.TestCase):
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

        self.assertEqual(metadata["document_id"], "DES-0200")

if __name__ == "__main__":
    unittest.main()
