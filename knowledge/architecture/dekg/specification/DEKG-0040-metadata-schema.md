---
metadata_schema: 1.0.0
document_id: DEKG-0040
canonical_id: dekg.specification.metadata-schema
title: Metadata Schema
node_type: specification
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All indexable DESys documents
---

# DEKG-0040 - Metadata Schema

# 1. Purpose

This specification defines the canonical metadata contract for documents represented as nodes in the DunderCode Engineering Knowledge Graph (DEKG).

The contract provides one machine-readable representation for identity, classification, lifecycle, governance, scope, and semantic relationships.

# 2. Scope

This specification applies to every non-empty, identifier-bearing DESys Markdown document.

README files are navigation surfaces and are not DEKG nodes. Empty placeholders are not nodes, do not reserve identifiers, and are ignored with a validation warning until content is added.

# 3. Serialization

Metadata MUST be serialized as YAML front matter at the beginning of the Markdown file.

```yaml
---
metadata_schema: 1.0.0
document_id: DES-0200
canonical_id: des.quality.code-quality
title: Code Quality Standard
node_type: standard
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All software projects developed under DESys
---
```

The opening delimiter MUST be the first line of the file. Metadata sections embedded in the Markdown body are not canonical metadata.

# 4. Required Fields

| Field | Purpose |
| --- | --- |
| `metadata_schema` | Selects the metadata contract version. |
| `document_id` | Provides the stable human-readable identifier. |
| `canonical_id` | Provides the stable semantic identifier used by DEKG. |
| `title` | Names the asset without its document identifier. |
| `node_type` | Defines the role of the asset in DEKG. |
| `document_class` | Defines whether the asset is normative, informative, operational, or reference material. |
| `version` | Records a SemVer value without lifecycle qualifiers. |
| `status` | Records the document lifecycle state. |
| `language` | Records the canonical language; schema v1 accepts `en`. |
| `owner` | Identifies the accountable team or role. |

# 5. Optional Fields

The schema supports `domain`, `discipline`, `architecture_model`, `authors`, `reviewers`, `applies_to`, `tags`, `aliases`, `legacy_status`, and `relationships`.

Unknown fields MUST be rejected. Schema evolution MUST occur through a new `metadata_schema` version rather than ungoverned field additions.

# 6. Identity Rules

`document_id` MUST match the identifier at the start of the filename. Both `document_id` and `canonical_id` MUST be globally unique.

Canonical identifiers MUST:

- contain at least a library, domain, and slug segment;
- use lowercase ASCII letters, digits, hyphens, and periods;
- start with the lowercase library represented by `document_id`;
- remain stable when a title, file, or directory changes.

When a canonical identifier changes, the previous identifier MUST be retained in `aliases`. Aliases MAY retain a legacy two-segment identifier that would not be valid for a new `canonical_id`.

# 7. Lifecycle Rules

`version` MUST contain only a SemVer value. Lifecycle labels such as `(Draft)` MUST NOT be appended to it.

The normal lifecycle is `draft`, `review`, `approved`, `published`, and `deprecated`.

`canonical` is accepted temporarily as a legacy status only when `legacy_status: true` records an explicit migration exception. New or updated documents MUST NOT introduce this status. Migration from `canonical` requires governance evidence and MUST NOT be inferred automatically.

# 8. Relationship Rules

Relationships MUST use a supported relationship type and a canonical ID as their target. Relationship targets MUST resolve to a canonical ID or alias in the repository.

Narrative references in document bodies remain informative until they are deliberately represented in `relationships`.

# 9. Validation

The normative machine-readable contract is `knowledge/architecture/metadata/desys-metadata.schema.json`.

Repository validation additionally enforces:

- document and canonical ID uniqueness;
- agreement between filename, document ID, and canonical ID library;
- alias uniqueness;
- relationship target resolution;
- explicit warnings for legacy statuses and empty placeholders.

Run validation with:

```bash
python3 tools/validate_metadata.py
```

Use `--show-warnings` to list legacy statuses and empty placeholders. Use `--strict-placeholders` when identifier-bearing placeholders must fail validation.

# 10. Governance

Changes to required fields, meanings, enums, or validation behavior require a new metadata schema version and a documented migration path.

The JSON Schema, this specification, the validator, and migration tooling MUST evolve together.
