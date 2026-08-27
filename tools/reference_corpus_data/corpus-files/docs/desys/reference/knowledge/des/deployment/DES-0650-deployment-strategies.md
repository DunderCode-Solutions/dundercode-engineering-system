---
metadata_schema: 1.0.0
document_id: DES-0650
canonical_id: des.deployment.deployment-strategies
title: Deployment Strategies Standard
node_type: standard
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Consumer deployment-strategy practices that explicitly adopt this draft guidance
relationships:
- type: references
  target: rfc.corpus.reference-distribution
- type: references
  target: adr.corpus.layout-and-authority
- type: references
  target: dcsg.canon.style-guide
---

# DES-0650 - Deployment Strategies Standard

## 1. Status and Authority

This standard is draft, reference-only guidance. Opt-in distribution under
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
and the authority boundaries in
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md)
do not select or approve a deployment strategy for a consumer. The project owns
rollout authority, health criteria, user impact, and risk acceptance. This draft
is aligned with and reviewed against the draft
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md),
which does not grant lifecycle approval.

## 2. Purpose and Scope

This document supports selection and control of how a verified change is exposed
to an environment or users. It covers recreate, rolling, parallel-environment,
canary, traffic-shift, feature-control, and other approaches without prescribing
a platform or claiming that one strategy is universally safer.

"Zero downtime" is an objective, not a strategy or guarantee. State, data,
capacity, dependency, and client compatibility can dominate strategy choice.

## 3. Strategy Selection

Select a strategy using project evidence about:

- impact and blast radius of failure;
- statefulness, data compatibility, and migration order;
- artifact, API, protocol, and client compatibility windows;
- capacity needed to run old and new versions concurrently;
- traffic control, session behavior, and background work;
- observability quality and time needed to detect harm;
- rollback, restore, roll-forward, and containment feasibility;
- operator load, cost, timing, and external obligations.

A complex progressive strategy can add more failure modes than it removes. A
simple outage window may be safer when explicitly approved and communicated.

## 4. Progressive Rollout Plan

Where architecture and risk justify progressive exposure, define stages before
execution. Each stage should state:

| Element | Decision |
| --- | --- |
| Exposure | Targets, users, traffic, regions, tenants, or workload share |
| Entry | Preconditions and evidence required to begin |
| Health | Service, dependency, data, security, and user-impact signals |
| Threshold | Continue, pause, abort, or investigate criteria |
| Observation | Minimum period and known signal delay |
| Authority | Who evaluates evidence and who may override or stop |
| Recovery | Containment and validated rollback or roll-forward option |

Health gates should combine leading deployment signals with user-visible and
business-relevant outcomes where available. A single process check or average
metric can hide localized harm. Missing, delayed, contradictory, or low-quality
telemetry should have a defined response rather than be treated as success.

Expansion should be deliberate. Automation may advance only within approved
exposure, timing, threshold, and concurrency bounds. It should pause on ambiguous
target selection, failed prerequisites, breached gates, evidence loss, or expired
approval. A project-owned role retains authority to stop or contain the rollout.

## 5. Execution and Closure

Before execution, verify artifact identity, target, current state, configuration,
capacity, access, dependencies, migration prerequisites, and recovery readiness.
Record stage decisions and exceptions without exposing secrets.

After final exposure, continue observation for the period required to detect
delayed effects. Closure should record the actual scope, health evaluation,
remaining old versions or feature states, follow-up work, and recovery status.
Completion of automation alone does not establish acceptance.

## 6. Related Guidance

- [Release engineering](DES-0640-release-engineering.md)
- [Rollback and recovery](DES-0660-rollback-recovery.md)
- [Operational readiness](DES-0670-operational-readiness.md)
- [Deployment governance](DES-0680-deployment-governance.md)

## 7. Limitations

Progressive exposure limits some blast radius but does not eliminate correlated,
delayed, or data-dependent failures. Strategy evidence must be interpreted in the
project's operating context.
