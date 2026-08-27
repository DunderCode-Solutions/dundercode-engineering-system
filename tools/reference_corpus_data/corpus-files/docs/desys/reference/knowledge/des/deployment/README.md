# Deployment Standards

This collection contains draft, technology-neutral reference guidance for moving
reviewed changes into controlled environments. It is eligible for opt-in
reference distribution only after the review and allowlisting required by
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
and
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).

These documents do not become a consumer project's policy when copied or
indexed. The project owns its architecture, risk acceptance, deployment
authority, evidence requirements, and applicable legal or contractual duties.
Adoption requires a project-owned decision. Metadata and links support discovery;
they do not grant approval authority or demonstrate compliance.

## Coverage

| ID | Topic |
| --- | --- |
| [DES-0600](DES-0600-deployment-engineering-principles.md) | Risk-based deployment principles and bounded automation |
| [DES-0610](DES-0610-environment-management.md) | Purposeful environments and controlled differences |
| [DES-0620](DES-0620-infrastructure-code.md) | Reviewed infrastructure definitions, state, secrets, and dependencies |
| [DES-0630](DES-0630-configuration-management.md) | Configuration and secret boundaries |
| [DES-0640](DES-0640-release-engineering.md) | Artifact provenance, integrity, and promotion evidence |
| [DES-0650](DES-0650-deployment-strategies.md) | Progressive exposure and health gates |
| [DES-0660](DES-0660-rollback-recovery.md) | Rollback, roll-forward, restore, and data migration recovery |
| [DES-0670](DES-0670-operational-readiness.md) | Readiness evidence and accountable decisions |
| [DES-0680](DES-0680-deployment-governance.md) | Access, approvals, emergencies, audit, and retention |

## Use

Start with DES-0600, then select the guidance relevant to the project's change
and operating model. The documents form a control system, not a mandatory linear
process. A low-risk configuration correction and an irreversible data migration
may require different evidence, approvers, rollout limits, and recovery plans.

Automation is appropriate only where scope, credentials, concurrency, stop
conditions, observability, and human ownership are defined. No document in this
family guarantees availability, successful recovery, security, or compliance.

## Lifecycle

Every document in this collection is `draft` and reference-only. The family is
aligned with and reviewed against the draft
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md);
that guide does not grant lifecycle approval. RFC-0001 and ADR-0001 define the
opt-in distribution model and the boundary between DESys references and project
authority.
