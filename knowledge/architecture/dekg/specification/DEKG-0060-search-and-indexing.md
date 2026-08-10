---
metadata_schema: 1.0.0
document_id: DEKG-0060
canonical_id: dekg.specification.search-and-indexing
title: Search and Indexing
node_type: specification
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- DESys index generation and consumers
---

# DEKG-0060 - Search and Indexing

# 1. Purpose

This specification defines the deterministic projection of canonical DESys documents into machine-readable index artifacts.

# 2. Source Of Truth

Canonical Markdown documents and their YAML front matter are the source of truth. Generated indexes MUST NOT introduce identity, lifecycle, or relationship information that is absent from canonical metadata.

README files, unnumbered Markdown files, empty placeholders, generated output, and narrative references are not indexed as DEKG nodes.

# 3. Pipeline

The index pipeline MUST:

1. load and validate its configuration;
2. validate canonical metadata across the repository;
3. discover configured, non-empty, identifier-bearing documents;
4. parse metadata and Markdown bodies;
5. render every requested artifact in memory;
6. write artifacts through same-directory atomic replacement.

Any metadata or configuration error MUST stop generation before artifacts are replaced.

# 4. Determinism

Generated output MUST NOT contain timestamps, random identifiers, absolute paths, modification times, or environment-specific values.

Every artifact MUST contain the same deterministic `build_id`. The build ID is the SHA-256 digest of canonical JSON representing all five semantic artifact payloads before the build ID is assigned. Changes to source documents, artifact schemas, or renderer projections therefore produce a different build ID.

Documents, nodes, relationships, aliases, and navigation groups MUST use stable lexical ordering.

# 5. Common Envelope

Every artifact contains:

| Field | Purpose |
| --- | --- |
| `schema_version` | Selects the generated artifact contract. |
| `build_id` | Identifies one coherent generation of all artifacts. |

Consumers MUST reject or refresh a mixed set of artifacts with different build IDs.

# 6. Index Artifact

`index.yaml` is the normalized document catalog. It contains `document_count` and a `documents` list ordered by canonical ID.

Each entry contains the canonical metadata, repository-relative path, normalized optional fields, relationships, and extracted summary.

# 7. Graph Artifact

`graph.yaml` contains `nodes` and `edges`.

Nodes represent indexed documents. Edges are produced only by explicit `relationships` metadata. Relationship targets expressed through aliases are resolved to their current canonical IDs. Inverse edges are not inferred.

# 8. Navigation Artifact

`navigation.yaml` groups documents by repository directory. Groups are ordered by path, and documents within each group are ordered by canonical ID.

This projection provides structural navigation without treating filesystem location as semantic identity.

# 9. Alias Artifact

`aliases.yaml` maps every historical canonical ID to its current canonical ID. Alias keys are globally unique and ordered lexically.

# 10. Search Artifact

`search-index.json` contains a technology-neutral search corpus. Each entry includes identity, classification, scope, summary, aliases, tags, and the Markdown body without front matter.

The artifact does not prescribe tokenization, ranking, stemming, embedding, or a search engine.

# 11. Paths And Security

Generated artifacts MUST contain only POSIX repository-relative paths.

Sources, output directories, exclusions, and artifacts MUST be validated to prevent absolute paths, path traversal, and writes outside the repository root.

# 12. Commands

Validate and render without writing:

```bash
python3 tools/build_index.py --dry-run
```

Generate configured artifacts:

```bash
python3 tools/build_index.py
```
