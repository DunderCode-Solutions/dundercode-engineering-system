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
- Identifier-bearing DESys documents that adopt metadata schema 1.0.0
---

# DEKG-0040 - Metadata Schema

## 1. Status and Authority

This document is a draft normative specification for DESys metadata schema
version `1.0.0`. It describes the accompanying machine-readable validation
artifact but is not an approved policy merely because its metadata class is
`normative` or because the schema validates an instance.

When installed through the opt-in reference corpus, this specification and its
schema are reference material. They do not govern consumer-owned documents or
override consumer code, runtime evidence, approved decisions, or local policy.
A consumer project may adopt the contract through its own governance.

## 2. Purpose and Scope

The proposed contract represents identity, classification, lifecycle, scope,
and semantic relationships for documents represented as DEKG nodes. Within
DESys, it is intended for non-empty Markdown files whose filenames begin with a
supported document identifier.

README files are navigation surfaces rather than DEKG nodes. Empty placeholders
are not nodes and do not reserve identifiers. The repository validator reports
them as warnings by default or errors in strict-placeholder mode.

The JSON Schema validates one metadata mapping. It cannot by itself inspect a
Markdown filename, prove repository-wide uniqueness, resolve a relationship,
or establish that a lifecycle transition was authorized.

## 3. Serialization

For documents using this contract, metadata is serialized as YAML front matter
at the beginning of the Markdown file.

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

The opening delimiter is the first line of a managed document. Metadata sections
embedded in the Markdown body are not parsed as canonical front matter.

## 4. Machine-Readable Contract

The [DESys metadata JSON Schema](../../metadata/desys-metadata.schema.json) uses
JSON Schema Draft 2020-12 and rejects unknown properties.

### 4.1 Required Fields

| Field | Actual schema constraint |
| --- | --- |
| `metadata_schema` | The string constant `1.0.0`. |
| `document_id` | A supported uppercase library, a hyphen, and four digits. |
| `canonical_id` | A supported lowercase library plus at least two dot-separated, lowercase alphanumeric or hyphenated segments. |
| `title` | A string containing at least one non-whitespace character. |
| `node_type` | One value from the node-type enum below. |
| `document_class` | `informative`, `normative`, `operational`, or `reference`. |
| `version` | Three dot-separated non-negative integers without leading zeroes except `0`. |
| `status` | `approved`, `canonical`, `deprecated`, `draft`, `published`, or `review`. |
| `language` | The string constant `en`. |
| `owner` | A string containing at least one non-whitespace character. |

Supported document libraries are `ADR`, `DAR`, `DCSG`, `DEA`, `DEC`, `DEKG`,
`DEM`, `DES`, `DET`, `DEP`, `DSB`, `DSK`, `DSP`, `GUIDE`, `PRD`, and `RFC`.

Supported node types are `architecture`, `assessment`, `canon`, `decision`,
`guide`, `method`, `process`, `product-requirement`, `proposal`, `skill`,
`specification`, `standard`, `style-guide`, and `template`.

### 4.2 Optional Fields

| Field | Actual schema constraint |
| --- | --- |
| `domain`, `discipline`, `architecture_model` | A string containing at least one non-whitespace character. |
| `authors`, `reviewers`, `applies_to`, `tags` | A non-empty array of unique, non-empty strings. |
| `aliases` | A non-empty array of unique legacy canonical IDs; two-segment IDs are accepted. |
| `legacy_status` | The constant `true`; valid only with `status: canonical`, which also requires it. |
| `relationships` | An array of strict relationship objects; the array may be empty. |

Unknown fields fail schema validation because `additionalProperties` is `false`.

JSON Schema applies `pattern` as a search. The identifier and version patterns
therefore use the ECMAScript-compatible terminal assertion `(?![\s\S])` rather
than `$`, which can match before a final line terminator. This rejects
newline-terminated values and aligns the machine-readable artifact with the
repository validator's already-stricter full-match behavior.

### 4.3 Relationship Objects

Each relationship contains only `type` and `target`. Both fields are required.
The target uses the canonical-ID syntax, including at least three total
segments. Supported types are:

`belongs_to`, `child`, `consumes`, `depends_on`, `derives_from`, `defines`,
`explains`, `extends`, `implements`, `owns`, `parent`, `produces`, `realizes`,
`references`, `related`, `specializes`, `supersedes`, `triggers`, and
`validates`.

## 5. Document Identity Rules

The repository validator, rather than JSON Schema alone, checks that
`document_id` matches the identifier at the start of the filename, that the
lowercase library in `canonical_id` matches `document_id`, and that document
IDs, canonical IDs, and aliases are unique across the validated sources.

Each canonical-ID segment contains lowercase ASCII letters or digits, optionally
separated by single hyphens. Canonical IDs remain stable across title or path
changes. A reviewed identifier migration may retain the prior value in
`aliases`; metadata alone does not authorize that migration. The repository
validator also rejects an alias equal to its document's canonical ID.

## 6. Schema Resource Identity and Loading

The schema resource identifier is exactly:

```text
urn:uuid:22eb6a5c-efb9-5581-9ee5-e52435153086
```

This `$id` identifies the JSON Schema resource and supplies the base URI for its
internal references. It is not a retrieval URL, a DEKG canonical ID, evidence
of document approval, or release provenance. The `metadata_schema: 1.0.0`
instance value identifies the metadata contract version separately.

For alpha artifacts, this UUID URN replaces
`https://dundercode.dev/schemas/desys-metadata-1.0.0.json` as the schema resource
identifier. The earlier identifier used an NXDOMAIN host and was not a reliable
retrieval location. Consumers of the alpha schema should update cached or
configured identifiers to the UUID URN; the earlier value is not an alternate
identity for this resource.

Load the schema from the local artifact, not by dereferencing `$id` or using the
network. Its source-repository path is:

```text
knowledge/architecture/metadata/desys-metadata.schema.json
```

The approved distribution design requires a future packaged corpus to install
the schema at:

```text
docs/desys/reference/knowledge/architecture/metadata/desys-metadata.schema.json
```

A future packaged implementation must include that local artifact and must not
depend on network retrieval. A validator that uses a schema registry should
associate the exact UUID URN with the locally loaded resource. All current
`$ref` values are fragments within that resource.

## 7. Lifecycle Rules

`version` contains only the SemVer-shaped value accepted by the schema; a label
such as `(Draft)` is not accepted. The normal lifecycle is `draft`, `review`,
`approved`, `published`, and `deprecated`.

`canonical` is a legacy status accepted only with `legacy_status: true`. The
repository validator warns on that combination. New lifecycle transitions and
migrations require governance evidence; a valid metadata value is not proof of
an authorized transition.

## 8. Relationship Resolution

JSON Schema validates relationship shape, type, and target syntax. Repository
validation additionally requires each target to resolve to a canonical ID or a
syntactically compatible alias in the validated sources, rejects a relationship
to the same document, and rejects identifier collisions.

A Markdown link supports navigation and a metadata relationship supports graph
semantics. Neither one grants approval authority.

## 9. Validation

`tools/validate_metadata.py` parses YAML front matter and applies the repository
validator's implementation of the metadata contract. It does not fetch the JSON
Schema by `$id`. Direct JSON Schema consumers should load the local artifact as
described in Section 6.

Repository validation checks:

- required and supported fields and values;
- agreement between filename, document ID, and canonical ID library;
- document ID, canonical ID, and alias uniqueness;
- relationship shape, target resolution, and self-reference;
- legacy-status and empty-placeholder warnings.

Run the packaged validator from a DESys source checkout or installed tooling:

```bash
desys-metadata-validate
```

When using the repository's locked development environment, use:

```bash
uv run desys-metadata-validate
```

Use `--show-warnings` to list legacy statuses and empty placeholders. Use
`--strict-placeholders` when identifier-bearing placeholders must fail
validation.

## 10. Release Provenance

The approved design for future opt-in distribution under the
[reference corpus RFC](../../../rfc/RFC-0001-reference-corpus-distribution.md)
and [authority ADR](../../../adr/ADR-0001-reference-corpus-layout-and-authority.md)
requires the schema to be an explicitly inventoried package resource. Before
such a package is released, release evidence must record the manifest schema
version, DESys package version, immutable release tag, source commit, corpus
version, and installation timestamp. The schema entry must record its exact
source and installed paths, classification and distribution status, and original
and installed content checksums. These values must align with the immutable
package resource and approved inventory.

A conforming future corpus manifest must supply that provenance. The schema
`$id`, file path, lifecycle metadata, or successful validation cannot replace
it. A schema content change produces a new checksum and requires the applicable
editorial, security, licensing, dependency-closure, and release review before
public distribution.

## 11. Governance and Compatibility

A change to the intended accepted fields, meanings, enums, or validation
behavior requires a new `metadata_schema` version and a documented migration
path. Version `1.0.0` is retained for two alpha corrections: Section 6 replaces
an unusable schema resource identifier, and Section 4 rejects final line
terminators that the shipped repository validator already rejected. These
changes align the machine artifact with the existing intended contract; they do
not change the repository validator's accepted metadata.

The JSON Schema, this specification, repository validator, tests, and migration
tooling should remain aligned. Passing automated validation does not establish
editorial approval or consumer-project authority. Editorial conventions and the
draft authority model are described by the
[Canon Style Guide](../../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
