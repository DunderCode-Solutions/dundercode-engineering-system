---
metadata_schema: 1.0.0
document_id: RFC-0001
canonical_id: rfc.corpus.reference-distribution
title: Reference Corpus Distribution
node_type: proposal
document_class: informative
version: 1.0.0
status: approved
language: en
owner: DunderCode Engineering
applies_to:
- DESys reference corpus distribution beginning with v0.2
tags:
- corpus
- distribution
- documentation
- project-initialization
relationships:
- type: produces
  target: adr.corpus.layout-and-authority
---

# RFC-0001 - Reference Corpus Distribution

# 1. Summary

This RFC proposes a versioned and non-destructive mechanism for distributing a
curated DESys reference corpus into consumer repositories.

The corpus consists of approved documents selected from `delivery/`,
`engineering/`, `foundation/`, `knowledge/`, and `skills/`. Consumer projects
may opt in during initialization. The selected documents are copied into a
dedicated reference area, indexed alongside project-owned documentation, and
tracked through a manifest containing provenance and checksums.

The proposal does not activate skills, infer project decisions, or grant DESys
reference material authority over consumer-owned ADRs, PRDs, and RFCs.

# 2. Motivation

DESys v0.1 provides metadata validation, deterministic indexing, project
scaffolding, and quality automation. The Python distribution contains the
tooling, but it does not distribute the source knowledge corpus. A newly
initialized consumer repository therefore starts with an empty local document
corpus.

Projects may benefit from access to reusable engineering standards, guides,
templates, and skills. Copying these documents manually would lose provenance,
make updates unsafe, and blur the boundary between DESys guidance and project
authority.

A governed distribution mechanism is required before the corpus can be made
available through `desys-project-init`.

# 3. Goals

The proposal has the following goals:

- distribute only reviewed and explicitly public documents;
- preserve source version, path, and checksum provenance;
- separate DESys reference material from project-owned documentation;
- keep the capability opt-in during the alpha lifecycle;
- support dry-run, conflict detection, and idempotent reruns;
- index vendored references together with local ADRs, PRDs, and RFCs;
- preserve deterministic generated artifacts;
- permit safe corpus updates without overwriting consumer changes;
- work from an installed package without requiring a DESys source checkout;
- preserve the behavior of v0.1 when corpus distribution is not requested.

# 4. Non-Goals

The first implementation will not:

- activate or execute skills;
- dynamically download unpinned content at initialization time;
- make DESys documents authoritative for project-specific decisions;
- edit consumer-owned ADRs, PRDs, RFCs, or other existing content;
- provide bidirectional synchronization with the DESys repository;
- publish the corpus as an independently versioned remote service;
- convert every README or placeholder into an indexable document;
- guarantee stable corpus APIs before a non-alpha release.

# 5. Current State

The repository indexer currently scans all five source trees and produces five
artifacts under `skills/generated/`. The package itself includes only Python
tooling. The consumer scaffold configures sources under `docs/adr`, `docs/prd`,
and `docs/rfc`, and writes generated artifacts under `docs/generated`.

The current corpus contains valid indexable material, navigation-only README
files, empty placeholders, and documents with governed legacy metadata. These
classes must not be treated as equally ready for public distribution.

# 6. Proposed User Experience

The existing command remains unchanged:

```bash
desys-project-init
```

Consumers explicitly request the reference corpus with:

```bash
desys-project-init --with-reference-corpus
```

Dry-run reports every planned corpus operation without writing files:

```bash
desys-project-init --with-reference-corpus --dry-run
```

Rerunning the same command reconciles the installed corpus against its manifest.
An unchanged installation produces zero writes. A safe upgrade updates only
files whose local checksum still matches the checksum previously recorded by
DESys.

# 7. Target Layout

The proposed consumer layout is:

```text
docs/
|-- adr/
|-- prd/
|-- rfc/
|-- desys/
|   |-- README.md
|   |-- corpus-manifest.yaml
|   `-- reference/
|       |-- delivery/
|       |-- engineering/
|       |-- foundation/
|       |-- knowledge/
|       `-- skills/
`-- generated/
```

The original source hierarchy is preserved below `docs/desys/reference/` to
retain stable relative paths and make provenance inspection straightforward.

# 8. Corpus Selection

Distribution is allowlist-based. A document is eligible only when it:

- passes canonical metadata validation when it is an indexable node;
- contains substantive content;
- has completed editorial review;
- is approved for public distribution;
- contains no credentials, private paths, personal data, or confidential names;
- has compatible licensing and attribution;
- does not require automatic execution or skill activation;
- has an explicit target path in the corpus inventory.

README files may be distributed as navigation surfaces without becoming DEKG
nodes. Empty placeholders are excluded until they receive approved content.
Legacy metadata must be migrated or explicitly excluded from the first bundle.

# 9. Distribution Artifact

The initial implementation should package the curated corpus as immutable
package resources in the same wheel as the compatible DESys tooling. The build
must derive the package resources from an explicit inventory rather than include
entire source directories implicitly.

Each published DESys version therefore carries one compatible corpus snapshot.
Installation remains self-contained and does not require a network request after
the package has been resolved.

An independently versioned corpus package may be considered later if corpus and
tooling release cadences diverge significantly.

# 10. Manifest

`docs/desys/corpus-manifest.yaml` records at least:

- manifest schema version;
- DESys package version;
- release tag and source commit;
- corpus version;
- installation timestamp;
- source and target path for every distributed file;
- document identifier when applicable;
- classification and distribution status;
- original content checksum;
- installed content checksum.

The manifest is authoritative for ownership and reconciliation. The generated
search and graph artifacts remain derived outputs and are never used as a
replacement for source documents.

# 11. Update and Conflict Policy

For every managed corpus file, the initializer applies these rules:

| Local state | Required behavior |
| --- | --- |
| File absent on first install | Create it after preflight succeeds. |
| File matches the recorded checksum | Keep it or replace it with the new version. |
| File differs from the recorded checksum | Report a conflict and do not overwrite it. |
| File was deleted locally | Report the deletion and require explicit resolution. |
| File was removed from the new corpus | Remove it only when its local checksum is unchanged. |
| File is new in the corpus | Create it after the complete preflight succeeds. |

Preflight is atomic at the operation-planning level: any blocking conflict stops
all corpus writes. Existing non-corpus initializer guarantees remain in force.

# 12. Index Integration

When corpus distribution is enabled, the generated indexer configuration adds
the eligible reference directories to its sources. Local project collections
remain separate sources.

The indexer must preserve globally unique document and canonical identifiers
across both local and vendored documents. A consumer document that collides with
a corpus identifier fails validation with an actionable source-path diagnostic.

`search-index.json` contains document bodies. Public-distribution review is
therefore mandatory before a document enters the bundle.

# 13. Authority Model

Authority follows the source of the claim:

- consumer ADRs, PRDs, RFCs, policies, and code describe the consumer project;
- vendored DESys documents provide reusable reference guidance;
- generated indexes provide discovery and do not create authority;
- metadata relationships provide traceability and do not infer approval rights;
- conflicts between project evidence and reference guidance must be reported,
  not silently resolved in favor of the reference corpus.

The generated `AGENTS.md` and `docs/desys/README.md` must explain this hierarchy.

# 14. Compatibility

Projects that do not pass `--with-reference-corpus` receive the v0.1 scaffold
behavior. Existing projects can opt in later. Removal of the option from a rerun
does not implicitly delete an installed corpus.

The manifest schema must be versioned independently from document metadata. An
unsupported manifest version must fail before writes occur.

# 15. Security and Supply Chain

The implementation must:

- build the inventory deterministically;
- fail when an inventory checksum differs from packaged content;
- reject symlinks and paths escaping the target root;
- avoid executable permissions on corpus documents;
- avoid runtime downloads from branches or mutable tags;
- preserve the immutable package source already recorded by the initializer;
- scan the final bundle, not only the source repository;
- expose provenance in a human-readable form.

# 16. Delivery Plan

Implementation is divided into the following gates:

1. Approve this RFC and the related architecture decision.
2. Build a complete inventory and public-distribution classification.
3. Resolve placeholders and governed legacy metadata.
4. Implement deterministic corpus packaging and manifest validation.
5. Extend the initializer, generated configuration, and authority guidance.
6. Add install, update, conflict, compatibility, and platform tests.
7. Run security, licensing, and editorial review on the final bundle.
8. Execute new-project and existing-project pilots.
9. Publish the accepted capability as `v0.2.0-alpha.1`.

# 17. Alternatives Considered

## Git Submodule

Rejected for the initial implementation because it introduces Git-specific
operational complexity, mutable branch risks, and poor onboarding ergonomics.

## Clone the DESys Repository

Rejected because consumers should not require a complete source checkout or
inherit internal repository structure.

## Download a Branch at Runtime

Rejected because mutable sources weaken reproducibility and offline operation.

## Copy All Markdown Automatically

Rejected because navigation files, placeholders, legacy metadata, and content
classification require deliberate curation.

## Index DESys Remotely Without Copying Sources

Deferred because current artifact validation requires source paths inside the
consumer repository, and remote content would complicate authority and
availability guarantees.

# 18. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Consumer mistakes guidance for project policy | Separate paths and explicit authority instructions. |
| Wheel size increases | Curated allowlist and measured release budget. |
| Consumer edits vendored content | Checksum conflicts and no silent overwrite. |
| Stale guidance remains installed | Versioned manifest and documented update workflow. |
| Identifier collisions occur | Repository-wide validation before generation. |
| Confidential content enters search output | Public classification and final-bundle scanning. |
| Alpha behavior changes unexpectedly | Opt-in flag and regression coverage for v0.1 behavior. |

# 19. Acceptance Criteria

The RFC implementation is complete when:

- a clean package contains exactly the approved corpus inventory;
- install and dry-run work without a DESys checkout;
- rerunning the same version produces zero changes;
- safe upgrades preserve provenance and update unchanged files;
- modified or deleted local corpus files block writes with clear diagnostics;
- project-owned files remain byte-identical;
- generated indexes cover all configured local and corpus sources exactly;
- generated artifacts remain deterministic;
- anonymous installation from an immutable public tag succeeds;
- Linux, macOS, and Windows gates pass;
- both planned consumer pilots pass;
- release documentation states the alpha limitations and authority model.

# 20. Open Questions

- What maximum wheel-size increase is acceptable for the first corpus bundle?
- Should navigation-only READMEs be included in every distributed collection?
- Which current legacy-status skills are approved for the first public bundle?
- Should later versions expose a dedicated corpus synchronization command?
- What retention policy applies to corpus files removed by a future release?

# 21. Decision Request

The proposed opt-in model, package-resource distribution, target layout,
manifest responsibilities, conflict policy, and delivery gates are approved.
The resulting architecture decisions are recorded in ADR-0001.
