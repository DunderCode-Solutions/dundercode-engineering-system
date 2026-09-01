# DESys Skills Compatibility Delivery Roadmap

Status: APPROVED FOR IMPLEMENTATION

Roadmap date: 2026-08-27

## 1. Objective

Deliver future DESys Skills without breaking repositories initialized from
`v0.2.0-alpha.1`. Work is governed by
[`ADR-0002`](../knowledge/adr/ADR-0002-cross-snapshot-migration-and-skill-boundaries.md)
and must preserve the fail-closed ownership model established by `ADR-0001`.

This roadmap authorizes implementation work. It does not approve the current
DSK collection for distribution and does not authorize active Skill execution.

## 2. Baseline

| Contract | Current baseline |
| --- | --- |
| Package | `0.2.0a1` / `v0.2.0-alpha.1` |
| Corpus | `0.1.0` |
| Inventory schema | `1.2.0` |
| Bundle schema | `1.1.0` |
| Consumer manifest schema | `1.1.0` |
| Approved bundle | 41 resources / 24 indexable documents |
| DSK inventory | 166 entries: 165 pending, 1 excluded, 0 approved |
| DSK legacy metadata | 105 documents using `status: canonical` |
| Supported reconciliation | First install and same-snapshot only |

## 3. Delivery Principles

- Each PR must preserve fail-closed behavior and pass the complete quality gate.
- Schema and behavior changes must include fixtures for supported and rejected
  versions.
- No PR may approve DSK content incidentally.
- Reference Skills and Active Skills remain separate workstreams.
- Migration tests must assert bytes, manifests, plans, and rollback state rather
  than relying only on command exit status.
- Compatibility claims require evidence from exact immutable artifacts.

## 4. Planned PR Sequence

### PR 1 - Versioned Compatibility Contracts

Status: COMPLETE

Deliverables:

- formal JSON Schemas for bundle and consumer manifest;
- machine-readable compatibility matrix;
- validation of package, corpus, release, and schema alignment;
- fixtures for supported and unsupported contract versions.

Exit gate:

- current `v0.2.0-alpha.1` manifests validate without semantic relaxation;
- unsupported major versions fail before ownership is trusted;
- documentation and runtime validation agree on the same matrix.

### PR 2 - Trusted Predecessor Descriptors

Status: COMPLETE

Deliverables:

- immutable predecessor descriptors packaged with the target release;
- complete predecessor manifest and provenance validation;
- explicit direct-migration declarations;
- fail-closed diagnostics for unknown, skipped, or forged snapshots.

Exit gate:

- a valid v0.2 predecessor is accepted only through its exact descriptor;
- any entry, checksum, release, source, or schema mismatch prevents planning.

### PR 3 - Cross-Snapshot Planner and Preflight

Status: COMPLETE

Deliverables:

- deterministic `ADD`, `UPDATE`, `REMOVE`, `UNCHANGED`, and `CONFLICT` plans;
- checksum-based local modification and deletion detection;
- repository-wide identity and alias collision preflight;
- portable path and future Skill identifier collision checks;
- dry-run parity for every operation type.

Exit gate:

- every conflict prevents all writes;
- diagnostics name both sides of identity conflicts;
- repeated planning produces byte-identical output.

### PR 4 - Transactional Apply and Rollback

Status: COMPLETE

Deliverables:

- same-filesystem staging for target content and manifest;
- verified backup or predecessor restoration data;
- transaction journal or equivalent recoverable state;
- failure injection at each mutation boundary;
- explicit recovery behavior and operator documentation.

Exit gate:

- every injected apply failure automatically restores the exact predecessor
  bytes and manifest before returning;
- an interrupted rollback leaves a recovery record that blocks every operation
  except recovery, and recovery restores the exact predecessor state;
- no partial migration is accepted as managed state;
- successful apply publishes the target manifest last.

### PR 5 - Compatibility Publication

Status: COMPLETE

Deliverables:

- human-readable compatibility matrix in release documentation;
- generated or validated matrix values from package contracts;
- supported predecessor, exact Python version, operating-system image or
  version, architecture, and immutable artifact declarations;
- upgrade, refusal, recovery, and rollback procedures.

Exit gate:

- stale release documentation fails CI;
- each supported migration path links to automated evidence.

Exit gate state: COMPLETE. The versioned release-evidence contract and canonical
documentation checker passed Linux, macOS, and Windows CI and merged through
[PR #17](https://github.com/DunderCode-Solutions/dundercode-engineering-system/pull/17)
at `4d544a8acc5e0c7e249884feb56d4acde29cd86f`. Canonical candidate details are in
[`DESYS-V0.3-COMPATIBILITY.md`](DESYS-V0.3-COMPATIBILITY.md).

### PR 6 - Reference Skill Remediation Batches

Deliverables:

- bounded DSK batches with reference-only and non-activation framing;
- explicit human authority and deny-by-default boundaries;
- migration of legacy lifecycle metadata;
- resolution of links, relationships, duplicate concepts, and filenames;
- security, privacy, licensing, and editorial review per exact checksum.

Exit gate:

- only reviewed checksums become `approved`;
- an altered approved document returns to `pending`;
- no Skill claims automatic approval, deployment, remediation, or credentials.

### PR 7A - Active Skill Architecture

Deliverables:

- separate ADR or RFC for active capability packaging;
- versioned Skill schema covering tools, permissions, inputs, outputs, runtime,
  and lifecycle;
- canonical source and generated adapter boundaries;
- ownership, update, removal, conflict, and rollback semantics;
- threat model for execution, credentials, network, and supply chain.

Exit gate:

- no active file or mutable state is placed in `docs/desys/reference/`;
- activation remains explicit, least-privileged, and deny-by-default;
- vendor adapters cannot silently expand canonical permissions.

This PR authorizes implementation work only. It cannot authorize an Active
Skills release.

### PR 7B - Active Skill Contract Implementation

Deliverables:

- runtime validation for the approved Active Skill schema;
- explicit install, activation, update, deactivation, removal, and rollback
  commands;
- canonical-to-vendor adapter generation with permission non-expansion checks;
- ownership manifests for active definitions and generated adapters;
- failure injection and security tests for credentials, tools, network access,
  path boundaries, and adapter tampering;
- platform and isolated-package tests for every supported adapter.

Exit gate:

- each lifecycle operation is transactional, idempotent where applicable, and
  fails closed on unknown state;
- active definitions, generated adapters, credentials, and runtime state use
  their approved separate namespaces;
- no adapter can activate capabilities beyond the canonical declaration;
- security review and explicit engineering-owner approval are recorded for the
  exact implementation checksums.

### PR 8 - Consumer Upgrade Pilot and Release Gate

Deliverables:

- sanitized fixture or disposable clone representative of the SaaS consumer;
- upgrade from the exact public v0.2 tag to the Skills candidate;
- positive addition, update, removal, and idempotency scenarios;
- negative modification, deletion, collision, forged-manifest, and interrupted
  apply scenarios;
- anonymous immutable-tag validation and platform evidence.

Exit gate:

- the fixture contains application source, package and lock files, local ADR,
  PRD, and RFC documents, generated indexes, existing CI, the v0.2 manifest, at
  least one locally modified managed file, and controlled identity collisions;
- fixture scale, file counts, and managed-byte checksums are recorded so the
  scenario is reproducible;
- consumer-owned files remain byte-identical;
- rollback restores the exact predecessor snapshot;
- all required scenarios pass on Linux, macOS, and Windows;
- no critical or high defect remains open.

## 5. Required Test Matrix

| Area | Mandatory scenarios |
| --- | --- |
| Predecessor trust | Exact match, unknown bundle, forged entry, wrong provenance, unsupported schema |
| Planning | Add, update, remove, unchanged, rename-as-remove/add, deterministic ordering |
| Consumer changes | Modified managed file, deleted managed file, unmanaged target, local ID and alias collision |
| Paths | Traversal, symlink, hardlink, executable, case collision, Windows reserved name, Unicode normalization |
| Transaction | Failure before first write, between each write, before manifest commit, during rollback, recovery rerun |
| Skills | Reference-only install, no activation, no mutable reference paths, permission denial for active adapters |
| Platforms | Linux, macOS, Windows, isolated wheel, anonymous public tag |

## 6. SaaS Adoption Protocol

Until all gates pass, a consumer SaaS must:

1. pin DESys to `v0.2.0-alpha.1` rather than a mutable branch or `latest`;
2. retain `docs/desys/corpus-manifest.yaml` and installed checksums;
3. keep project-specific documents outside `docs/desys/reference/`;
4. avoid manually creating Skill files inside the managed reference namespace;
5. test upgrades only in a disposable branch or clone;
6. capture a repository backup before migration;
7. promote the upgrade only after dry-run, apply, quality, and rollback evidence
   pass for the exact source and target snapshots.

## 7. Go/No-Go Decision

A Skills release is GO only when:

- PRs 1 through 6 and PR 8 are complete for Reference Skills;
- PRs 7A and 7B are also complete if the release includes Active Skills;
- the compatibility matrix names `v0.2.0-alpha.1` as a tested predecessor;
- the real-consumer migration pilot passes;
- final editorial, security, licensing, and platform reviews pass;
- the release candidate has no uncommitted regeneration or checksum drift;
- anonymous validation succeeds against the exact immutable candidate tag.

Any unmet gate is NO-GO. A new-project installation passing does not compensate
for a failed existing-project migration.

## 8. Traceability

| Adopted requirement | Delivery location |
| --- | --- |
| Cross-snapshot migration | PRs 2 and 3 |
| Compatibility matrix | PRs 1 and 5 |
| Consumer modification detection | PR 3 |
| Migration and rollback plan | PR 4 |
| Real SaaS clone upgrade | PR 8 |
| Reference versus Active Skill separation | PRs 6, 7A, and 7B |
| Editorial and safety remediation | PR 6 |
