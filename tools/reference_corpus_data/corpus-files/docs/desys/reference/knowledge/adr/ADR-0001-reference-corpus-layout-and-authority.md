---
metadata_schema: 1.0.0
document_id: ADR-0001
canonical_id: adr.corpus.layout-and-authority
title: Reference Corpus Layout and Authority
node_type: decision
document_class: normative
version: 1.0.0
status: approved
language: en
owner: DunderCode Engineering
applies_to:
- DESys reference corpus installations in consumer repositories
tags:
- corpus
- architecture
- authority
- vendoring
relationships:
- type: derives_from
  target: rfc.corpus.reference-distribution
---

# ADR-0001 - Reference Corpus Layout and Authority

# 1. Status

Approved for the DESys v0.2 implementation cycle.

# 2. Context

DESys tooling can initialize consumer documentation collections and generate
deterministic indexes, but the v0.1 package does not distribute the DESys source
knowledge corpus. Adding this capability introduces decisions about package
boundaries, target paths, content ownership, updates, conflicts, and authority.

Copying reference material into the same collections as project ADRs, PRDs, and
RFCs would make origin and governance ambiguous. Resolving mutable remote
content during initialization would weaken reproducibility. Overwriting copied
documents would violate the non-destructive initializer contract.

# 3. Decision Drivers

The architecture must provide:

- immutable and reproducible distribution;
- clear separation between reference and project authority;
- explicit consumer consent during the alpha lifecycle;
- operation without a DESys source checkout;
- deterministic package and index contents;
- idempotent installation and safe upgrades;
- conflict detection before writes;
- traceable provenance for every copied file;
- compatibility with existing v0.1 consumers.

# 4. Decision

DESys will distribute an explicitly curated reference corpus as package
resources in the same wheel as the compatible tooling version.

The curated resources will include the repository license and applicable
third-party notices. These legal assets must be explicit inventory entries,
package resources, installed files, and manifest records; they must not be
inferred from wheel metadata.

Corpus installation will be opt-in through
`desys-project-init --with-reference-corpus`. The initializer will copy approved
reference resources into `docs/desys/reference/`, place required legal notices
under `docs/desys/`, and record provenance and checksums in
`docs/desys/corpus-manifest.yaml`.

The original collection hierarchy below the five source roots will be preserved.
The package build will use an allowlist inventory and will not include source
directories through an unrestricted wildcard.

# 5. Target Ownership Boundaries

The following paths are project-owned:

- `docs/adr/`;
- `docs/prd/`;
- `docs/rfc/`;
- project policies, source code, and configuration outside DESys-managed blocks.

The following paths are DESys-managed when corpus installation is enabled:

- `docs/desys/reference/`;
- `docs/desys/LICENSE`;
- `docs/desys/THIRD_PARTY_NOTICES.md`;
- `docs/desys/corpus-manifest.yaml`;
- the existing explicitly marked DESys blocks and generated integration files.

`docs/generated/` contains derived artifacts. Generated artifacts are neither
project authority nor corpus source and may be regenerated from configured
sources.

# 6. Authority Hierarchy

For facts about a consumer project, evidence is evaluated in this order:

1. Consumer source code and runtime behavior.
2. Consumer-approved policies and architecture decisions.
3. Consumer PRDs, RFCs, and maintained operational documentation.
4. Vendored DESys reference guidance.
5. Generated discovery artifacts.

This order does not grant approval authority to metadata fields or relationships.
When project evidence contradicts the reference corpus, tooling and agents must
report the conflict and follow the consumer's documented authority.

# 7. Installation Semantics

The initializer performs a complete preflight before writing corpus files. It
rejects unsafe paths, symlinks, existing unmanaged files at managed targets, and
manifest inconsistencies.

On first installation, all planned files are either safe to create or no corpus
file is written. The existing project scaffold remains subject to its current
non-destructive behavior.

Rerunning the same package and corpus version must be idempotent.

# 8. Update Semantics

The first v0.2 alpha implements first installation and same-snapshot
reconciliation. It rejects a manifest from another bundle checksum before using
that manifest as ownership evidence. Cross-snapshot reconciliation remains
deferred until the package can validate the complete prior manifest against a
trusted predecessor descriptor. This fail-closed limitation preserves the
non-destructive boundary while the update mechanism is incomplete.

The recorded installed checksum is the baseline for update decisions:

- unchanged managed files may be updated;
- locally modified managed files are conflicts and must not be overwritten;
- locally deleted files require explicit resolution and are not recreated
  silently;
- upstream removals delete local files only when they remain unchanged;
- any blocking conflict prevents all corpus writes;
- `--dry-run` reports the same operation plan without modifying the repository.

The implementation may add an explicit conflict-resolution mechanism later. The
first version must prefer refusal over implicit recovery.

# 9. Indexing Decision

Installed corpus directories will be configured as additional index sources.
Project and corpus documents share one identifier namespace so relationships can
be resolved consistently.

Identifier or alias collisions are validation errors. Index generation must not
rename either source automatically.

Navigation-only README files may be present for humans but remain excluded from
DEKG nodes. Skills are indexed as reference documents and are not activated or
executed by this decision.

# 10. Versioning Decision

One DESys package version carries one corpus snapshot. The manifest separately
versions its own schema so future reconciliation behavior can evolve safely.

The release tag, package version, corpus inventory, and manifest metadata must be
aligned. Runtime retrieval from mutable branches is prohibited.

Splitting the corpus into a separate distribution requires a future decision and
a demonstrated need for independent release cadence.

# 11. Security Decision

Only content marked for public distribution may enter package resources. Review
must cover credentials, confidential references, personal data, licensing,
unsafe instructions, external links, and the complete generated search content.

The packaging gate also requires approved, checksum-matched license and
third-party notice entries. The initializer must install those notices beside
the manifest so their obligations remain visible after corpus files are copied
out of the wheel.

The packaging gate validates inventory coverage and checksums. The initializer
rejects path traversal and does not preserve executable permissions from corpus
resources.

# 12. Compatibility Decision

The default initializer behavior remains corpus-free for the v0.2 alpha. Existing
commands, generated project collections, and tool-source isolation remain
compatible with v0.1.

Omitting the corpus option on a later rerun does not remove an already installed
corpus. Removal requires an explicit future operation or documented manual
procedure.

# 13. Consequences

## Positive

- Consumers gain local, searchable, versioned DESys reference material.
- Package resolution also resolves a compatible corpus snapshot.
- Provenance and conflict behavior are auditable.
- Project authority remains distinguishable from reusable guidance.
- The implementation can reuse existing initializer preflight and idempotency
  principles.

## Negative

- The wheel and consumer repository become larger.
- Corpus updates require checksum reconciliation logic.
- One identifier namespace can expose collisions in consumer documents.
- Editorial and security review become release-blocking activities.
- Tooling and corpus share a release cadence until another decision changes it.

# 14. Rejected Alternatives

## Place Corpus Documents in Local ADR, PRD, and RFC Collections

Rejected because it obscures ownership and could make reusable guidance appear
to be a project decision.

## Resolve Documents from a Git Branch at Runtime

Rejected because branches are mutable and network resolution weakens
reproducibility and offline use.

## Use a Git Submodule

Rejected for the first version because it imposes extra Git lifecycle operations
on every consumer and complicates non-Git installation tests.

## Overwrite Local Corpus Modifications During Upgrade

Rejected because it violates the initializer's non-destructive contract and can
destroy consumer annotations.

## Enable the Corpus by Default

Rejected during alpha because the repository-size, search-quality, and agent
behavior impacts must first be measured through pilots.

# 15. Validation Requirements

The first alpha portion of this decision is considered implemented only when
automated tests demonstrate:

- exact inventory-to-package coverage;
- exact legal-notice inventory, package, manifest, and installation coverage;
- package installation without a source checkout;
- opt-in and default compatibility behavior;
- dry-run accuracy;
- idempotent reruns;
- same-snapshot reconciliation and fail-closed rejection of other bundle checksums;
- atomic refusal on modified and deleted files;
- no changes to consumer-owned documentation;
- deterministic index artifacts;
- identifier collision diagnostics;
- public-tag installation on supported platforms.

The cross-snapshot portion remains unimplemented until trusted predecessor
descriptors are packaged and automated tests demonstrate safe unchanged-file
updates, additions, removals, provenance continuity, and atomic refusal for all
consumer modifications.

# 16. Follow-Up Decisions

Future ADRs may be required for:

- a corpus distribution independent from the tooling package;
- explicit corpus removal and conflict-resolution commands;
- selective installation by domain or collection;
- automatic skill activation;
- remote or organization-specific private corpus layers.
