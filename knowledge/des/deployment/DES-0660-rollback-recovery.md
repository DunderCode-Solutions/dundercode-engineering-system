---
metadata_schema: 1.0.0
document_id: DES-0660
canonical_id: des.deployment.rollback-recovery
title: Rollback & Recovery Standard
node_type: standard
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Consumer deployment-recovery practices that explicitly adopt this draft guidance
relationships:
- type: references
  target: rfc.corpus.reference-distribution
- type: references
  target: adr.corpus.layout-and-authority
- type: references
  target: dcsg.canon.style-guide
---

# DES-0660 - Rollback & Recovery Standard

## 1. Status and Authority

This standard is draft, reference-only guidance. Opt-in distribution under
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
and the authority boundaries in
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md)
do not authorize rollback, restore, failover, or data modification. The consumer
project owns recovery objectives, decision authority, and acceptance of data
loss or service impact. This draft is aligned with and reviewed against the draft
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md),
which does not grant lifecycle approval.

## 2. Purpose and Scope

This document supports recovery from a deployment that is harmful, incomplete,
or unable to meet its objectives. Recovery may contain impact, shift traffic,
disable a feature, restore state, roll back code or configuration, or roll
forward with a corrective change.

Rollback is one option, not a universal guarantee. Data and externally visible
effects can make returning to an earlier artifact unsafe or impossible.

## 3. Recovery Decision

A project-owned recovery plan should define:

- detection signals and who may declare a recovery event;
- immediate containment and user or stakeholder communication;
- dependencies, state, and compatibility assumptions;
- decision criteria for rollback, restore, failover, or roll-forward;
- authorized identities, tools, targets, and concurrency bounds;
- validation criteria, escalation, and stopping conditions;
- accepted recovery time, data loss, and residual-risk objectives;
- evidence and post-event review ownership.

During an event, preserve evidence without delaying urgent containment. If the
documented plan conflicts with observed conditions, the authorized incident role
should reassess rather than let automation continue from stale assumptions.

## 4. Data and Schema Changes

Data migration planning should address schema and application compatibility,
ordering, long-running work, retries, duplicate processing, partial completion,
and concurrent old and new versions. Expand-and-contract and other compatibility
patterns can reduce coupling but do not make a migration automatically safe.

Before an irreversible or destructive step, identify:

| Concern | Evidence |
| --- | --- |
| Backup | Scope, completion, protection, age, and owner |
| Restore | Tested procedure, target, duration, integrity checks, and dependencies |
| Rollback | Which code, schema, configuration, and data effects are reversible |
| Roll-forward | Corrective path, required compatibility, build time, and authority |
| Partial failure | Resume, compensate, quarantine, or reconcile behavior |
| Data loss | Maximum accepted loss and who may accept it |

A backup is not evidence of recoverability until restoration is tested at a
frequency and scale appropriate to project risk. Restore testing should avoid
exposing protected data and should verify application-level consistency, not
only file or storage completion.

Down migrations can lose information or fail after new writes. Plans should not
advertise rollback when the actual recovery path is restore or roll-forward.

## 5. Execution and Validation

Recovery automation should verify the incident, target, artifact or backup
identity, authorization, and current state before acting. Retries, destructive
steps, and cross-region or cross-environment actions should be explicitly
bounded. Automation should stop on conflicting state, unexpected writes, missing
evidence, or exhausted limits.

Validation should cover service behavior, data integrity, security controls,
dependencies, queued or duplicated work, and user impact. Recovery closure may
record partial restoration and follow-up actions; it should not claim success
solely because an older version is running.

## 6. Evidence and Learning

Record the trigger, decision owner, chosen path, identities, artifacts or backup,
timestamps, commands or automation references, observed outcomes, data effects,
exceptions, and validation. Protect secrets and sensitive incident data, and
retain evidence under project policy. Review material events without treating
the review as proof that recurrence is impossible.

## 7. Related Guidance

- [Deployment strategies](DES-0650-deployment-strategies.md)
- [Operational readiness](DES-0670-operational-readiness.md)
- [Deployment governance](DES-0680-deployment-governance.md)

## 8. Limitations

Recovery plans age as systems and dependencies change. Exercises and restore
tests reduce uncertainty but cannot guarantee recovery time, completeness, or
absence of data loss during a real event.
