---
metadata_schema: 1.0.0
document_id: ADR-0002
canonical_id: adr.corpus.cross-snapshot-and-skill-boundaries
title: Cross-Snapshot Migration and Skill Boundaries
node_type: decision
document_class: normative
version: 1.0.0
status: approved
language: en
owner: DunderCode Engineering
applies_to:
- DESys corpus upgrades and future skill distribution
tags:
- corpus
- migration
- compatibility
- skills
- rollback
relationships:
- type: extends
  target: adr.corpus.layout-and-authority
- type: derives_from
  target: rfc.corpus.reference-distribution
---

# ADR-0002 - Cross-Snapshot Migration and Skill Boundaries

# 1. Status

Approved for implementation planning after `v0.2.0-alpha.1`.

This decision approves the safety and compatibility prerequisites for a future
DESys Skills release. It does not approve any current DSK document for public
distribution and does not authorize automatic skill activation.

# 2. Context

The first v0.2 alpha installs an immutable reference corpus and safely
reconciles the same snapshot. It rejects a consumer manifest whose bundle
checksum differs from the package bundle before trusting that manifest as
ownership evidence.

Adding any approved DSK document changes the bundle descriptor and checksum.
Consequently, a consumer pinned to `v0.2.0-alpha.1` cannot adopt a later bundle
without cross-snapshot migration support. The current per-file application also
has no repository-wide rollback if an operating-system failure occurs after one
or more writes.

The repository's DSK collection is currently documentation. It does not contain
Agent Skills packages, `SKILL.md` contracts, vendor adapters, runtime state, or
activation logic. Treating reference documents and active capabilities as the
same distribution would blur authority, ownership, permissions, and lifecycle
boundaries.

# 3. Decision Drivers

The next distribution architecture must provide:

- non-destructive upgrades from an explicitly supported prior snapshot;
- provenance continuity from the installed bundle to the target bundle;
- conflict detection for local changes, deletions, identities, and target paths
  before any write;
- an all-or-restored application boundary for managed files;
- explicit compatibility across package, corpus, bundle, manifest, metadata,
  and Skill contracts;
- a vendor-neutral distinction between reference guidance and active Skills;
- evidence from upgrading a realistic existing consumer;
- continued fail-closed behavior for unknown or unsupported snapshots.

# 4. Decision

DESys will not distribute DSK documents to existing corpus consumers until the
cross-snapshot, compatibility, preflight, rollback, and consumer-pilot gates in
this decision pass.

DESys will maintain two distinct capability classes:

1. **Reference Skills** are immutable, indexed DSK documents installed under
   `docs/desys/reference/skills/`. Vendoring them grants no execution authority,
   installs no tools, and performs no activation.
2. **Active Skills** are executable or tool-bearing capabilities. They require a
   separate versioned schema, ownership model, permission model, lifecycle, and
   installation decision. No active Skill path is authorized by this ADR.

Active Skill files, generated state, caches, credentials, and vendor adapters
must not be placed inside `docs/desys/reference/`. A later ADR or RFC must define
their canonical source, generated targets, conflict policy, and removal
semantics before implementation.

# 5. Trusted Predecessor Model

Each package that supports an upgrade must carry immutable descriptors for every
directly supported predecessor bundle. A predecessor descriptor must include:

- bundle schema and checksum;
- corpus version, release tag, and source commit;
- complete target, identity, classification, and original-checksum records;
- the manifest schema versions accepted for that predecessor;
- the target bundle to which migration is authorized.

The initializer must validate the complete installed manifest against a bundled
predecessor descriptor before using it as ownership evidence. A matching
checksum without matching entries or provenance is insufficient.

Only explicitly declared direct migrations are supported. Skipping snapshots
requires either a declared direct migration or sequential execution of every
trusted migration. Unknown, mutable, or network-retrieved predecessor data must
fail closed.

# 6. Cross-Snapshot Planning

After predecessor validation, the initializer must calculate a complete plan:

- `ADD` for a target present only in the new bundle;
- `UPDATE` for a target whose approved content changed and whose installed bytes
  still match the predecessor manifest;
- `REMOVE` for a predecessor target absent from the new bundle whose installed
  bytes remain unchanged;
- `UNCHANGED` for identical entries;
- `CONFLICT` for local modifications, local deletion, unsafe paths, identity
  collisions, unmanaged targets, or inconsistent provenance.

Renames are represented as a checksum-verified removal and addition unless a
future schema defines a first-class rename with equivalent safety guarantees.

Any conflict must prevent every managed write. `--dry-run` must produce the same
ordered plan and diagnostics as apply without changing bytes, timestamps, or
repository state.

# 7. Consumer Modification and Identity Preflight

The preflight must compare every predecessor-owned target against its recorded
installed checksum. It must also scan consumer-owned indexable documents before
writing and reject collisions involving:

- `document_id`;
- `canonical_id`;
- aliases;
- case-insensitive portable paths;
- any future Skill identifier namespace.

The diagnostic must identify both conflicting sources and must not infer that a
DESys reference overrides consumer authority.

# 8. Transaction and Rollback

Applying a migration must be recoverable as one operation. The implementation
must stage new content and the target manifest before mutating managed targets.
It must retain enough verified predecessor content or backups to restore every
changed target if any operation fails.

The target manifest is the commit marker and must become visible only after all
target operations succeed. Automatic rollback must restore the complete
predecessor snapshot and manifest before the failed command returns.

If rollback itself is interrupted by an external failure, a recoverable
transaction record must remain. While that record exists, every DESys operation
except explicit recovery must fail closed. Recovery must restore the complete
predecessor snapshot before migration can be retried; a recovery record is not a
valid release end state and does not satisfy rollback acceptance by itself.

Per-file atomic replacement alone does not satisfy this requirement.

# 9. Compatibility Matrix

Every release that changes a distribution contract must publish a compatibility
matrix covering:

- DESys package version;
- corpus version and bundle checksum;
- inventory, bundle, and consumer-manifest schema versions;
- metadata schema version;
- Reference Skill content version where applicable;
- Active Skill schema and adapter versions where applicable;
- supported direct predecessor snapshots;
- exact Python versions, host operating-system images or versions,
  architectures, and immutable artifact identifiers used for validation.

Compatibility is exact and evidence-based. A release must not claim backward or
forward compatibility solely because two schemas parse successfully.

# 10. Skill Distribution Gates

Reference Skills may enter a public bundle only after:

- reference-only and non-activation language is consistent across the selected
  batch;
- human authority, deny-by-default execution, bounded credentials, privacy,
  safety, and production constraints are explicit where applicable;
- legacy lifecycle metadata and unresolved references are remediated;
- links, relationships, identifiers, licenses, and final packaged bytes pass
  review;
- exact reviewed checksums are marked `approved` in bounded batches.

Active Skills require a separate approval after their own schema, permission,
adapter, installation, update, removal, and rollback contracts are implemented.

# 11. Consumer Migration Pilot

Before a Skills release, DESys must upgrade a disposable clone of a realistic
consumer that was initialized from `v0.2.0-alpha.1`. The pilot must include
consumer code, local documents, CI, an unchanged corpus, controlled local
modifications, an identity collision, and an injected mid-apply failure.

Evidence must prove:

- unchanged consumer-owned files remain byte-identical;
- safe additions, updates, and removals match the target bundle;
- every conflict prevents all writes;
- rollback restores the exact predecessor state;
- rerunning the target snapshot is idempotent;
- generated indexes remain deterministic;
- Linux, macOS, and Windows gates pass.

Private SaaS content must not be committed to DESys evidence. The pilot may use a
sanitized fixture or record only non-sensitive checksums and outcomes.

# 12. Consequences

## Positive

- Existing consumers can adopt future corpus releases without silent overwrite.
- Skills cannot acquire execution authority merely by being indexed.
- Compatibility claims become explicit and testable.
- Failed migrations have a defined recovery boundary.
- A real consumer upgrade becomes a release gate rather than post-release
  discovery.

## Negative

- The package must retain trusted predecessor data for supported migrations.
- Migration logic and platform tests become materially more complex.
- DSK remediation must be delivered in bounded editorial batches.
- Active Skills require another architecture and security decision.

# 13. Rejected Alternatives

## Continue Rejecting Every Prior Bundle Indefinitely

Rejected because existing consumers would need manual deletion and
reinstallation, losing safe ownership and provenance continuity.

## Trust Only the Prior Bundle Checksum

Rejected because a checksum alone does not prove that the complete consumer
manifest and installed files match the trusted predecessor.

## Install Active Skills Beside Reference Documents

Rejected because mutable or executable state would violate the closed,
immutable reference namespace and confuse guidance with authority.

## Resolve Migration Descriptors from a Branch

Rejected because mutable network state weakens reproducibility and supply-chain
integrity.

# 14. Implementation and Release Gates

This decision is implemented only when automated tests and release evidence
demonstrate:

1. trusted predecessor validation and fail-closed unknown snapshots;
2. deterministic `ADD`, `UPDATE`, `REMOVE`, `UNCHANGED`, and `CONFLICT` plans;
3. pre-write local-modification and identity-collision detection;
4. transaction rollback under injected failure at every mutation boundary;
5. a published compatibility matrix validated against package metadata;
6. explicit Reference Skill and Active Skill boundaries;
7. exact-checksum editorial and security approval for selected Skills;
8. successful upgrade of a realistic v0.2 consumer clone;
9. anonymous immutable-tag installation and migration;
10. Linux, macOS, and Windows quality gates on the exact candidate.
