---
metadata_schema: 1.0.0
document_id: DES-0620
canonical_id: des.deployment.infrastructure-as-code
title: Infrastructure as Code Standard
node_type: standard
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Consumer infrastructure-as-code practices that explicitly adopt this draft guidance
relationships:
- type: references
  target: rfc.corpus.reference-distribution
- type: references
  target: adr.corpus.layout-and-authority
- type: references
  target: dcsg.canon.style-guide
---

# DES-0620 - Infrastructure as Code Standard

## 1. Status and Authority

This standard is draft, reference-only guidance. Its opt-in distribution under
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
and the authority boundaries in
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md)
do not authorize infrastructure changes or select a tool for a consumer. The
project owns adoption, provider choices, access, review, and risk decisions. This
draft is aligned with and reviewed against the draft
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md),
which does not grant lifecycle approval.

## 2. Purpose and Scope

Infrastructure as code (IaC) means managing relevant infrastructure intent as
reviewable definitions and controlled inputs. This document covers definitions,
dependencies, execution plans, state, secrets, review, drift, and evidence. It
supports declarative and imperative approaches and does not require one provider,
language, state backend, or versioning scheme.

## 3. Source and Dependency Control

Material definitions should be version-controlled and linked to an accountable
owner. Generated files and reusable modules should have reviewable sources.
Provider, module, image, package, and plugin dependencies should be constrained
to project-approved versions or immutable identities, with integrity verification
where supported. Updates should be deliberate and reviewed rather than resolved
from an unbounded mutable source during deployment.

Pinning reduces unintended change but can retain defects. Projects should define
how dependency updates, compatibility review, and urgent fixes are handled.

## 4. State and Secrets

When an IaC system uses state, the project should define:

- authoritative location and environment boundary;
- access control, encryption, locking or concurrency protection, and backup;
- retention, recovery, migration, and disposal procedures;
- handling for partial writes, stale locks, imports, and state repair;
- controls preventing state content from entering logs or public artifacts.

State can contain credentials or other sensitive values even when definitions do
not. Secrets should be referenced through a project-approved secret channel, not
stored in source, plan artifacts, state, or logs unless the chosen system cannot
avoid it and compensating controls are recorded. Secret values should not be used
as stable identifiers when rotation would force unsafe replacement.

## 5. Review and Execution

A material infrastructure change should separate, where practical:

1. validation of syntax, policy, dependencies, and target context;
2. generation of a change plan against a known state revision;
3. human or policy review of additions, replacements, deletions, access changes,
   data effects, cost, and blast radius;
4. approval by project-designated authority;
5. bounded execution of the reviewed revision;
6. post-change validation and evidence capture.

If the platform cannot guarantee that the reviewed plan equals execution, the
project should revalidate material differences before proceeding. Plan files may
contain sensitive data and should receive corresponding access and retention.

Destructive operations, broad target selection, imports, and state repair need
explicit scope confirmation and a recovery decision. Automation should limit
concurrency, retries, duration, and credentials, and stop when state, target, or
approval assumptions no longer hold.

## 6. Drift and Exceptions

Drift is a difference between intended and observed state. Detection should
report enough context for an owner to classify it as expected, unauthorized,
emergency, externally managed, or stale definition. Automatic reconciliation is
appropriate only within preapproved resource, impact, and timing bounds.

Emergency or manual changes should be recorded and then imported, represented,
or removed according to a project decision. Ignoring drift indefinitely weakens
the source of truth; automatically overwriting it may worsen an incident.

## 7. Evidence

Useful evidence includes the reviewed definition revision, dependency lock or
resolution record, target and state identity, redacted plan summary, reviewers
and approval, executor identity, timestamps, outcome, validation, drift status,
and exceptions. Evidence should not duplicate secret values.

## 8. Related Guidance

- [Deployment principles](DES-0600-deployment-engineering-principles.md)
- [Environment management](DES-0610-environment-management.md)
- [Configuration management](DES-0630-configuration-management.md)
- [Rollback and recovery](DES-0660-rollback-recovery.md)
- [Deployment governance](DES-0680-deployment-governance.md)

## 9. Limitations

IaC improves reviewability and repeatability but does not guarantee convergence,
security, recoverability, or absence of provider-side change. Runtime evidence
and project-owned controls remain necessary.
