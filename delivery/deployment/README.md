# Deployment

Deployment is the controlled introduction of a reviewed change into an execution
environment. This page navigates DESys deployment guidance and does not authorize
changes to a consumer environment.

Consumer projects define who may deploy, which controls apply, how credentials
are bounded, and what evidence permits continuation or requires abort.

## Principles

- **Automation:** automate repeatable steps when controls and observability are
  sufficient for the associated risk.
- **Controlled differences:** environments should make necessary differences
  explicit; they are not expected to be identical.
- **Provenance:** connect deployed artifacts to immutable source, build, and
  approval evidence.
- **Progressive validation:** limit exposure and evaluate defined health signals
  before expanding a change when architecture permits.
- **Recovery:** select and test rollback, roll-forward, restore, traffic-shift,
  or containment strategies appropriate to the change.
- **Least privilege:** deployment identities receive only the access and duration
  required for the approved operation.
- **Auditability:** retain the plan, operator or automation identity, timestamps,
  outcomes, and exceptions.

Availability is an objective constrained by service requirements, safety,
security, consistency, and cost. "Zero downtime" describes a desired outcome,
not a deployment strategy or universal guarantee.

## Strategy Selection

Common strategies include rolling replacement, blue-green switching, canary
release, recreate deployment, feature control, and other progressive-delivery
patterns. Selection depends on:

- state and data compatibility;
- reversibility and recovery time;
- capacity and traffic-management capability;
- user and regulatory impact;
- health signals and abort thresholds;
- operational complexity and cost.

Database and data migrations may not be safely reversible. Their plans should
address compatibility windows, backups, restore validation, forward recovery,
and partial-failure handling instead of assuming rollback is possible.

## Evidence Flow

```text
Approved change and artifact
          |
          v
Preflight and environment checks
          |
          v
Bounded rollout
          |
          v
Health and acceptance evaluation
          |
          +--> Continue or expand
          |
          `--> Abort, contain, or recover
```

The applicable project defines exact gates and human decision ownership.

## Standards Navigation

| Objective | Read |
| --- | --- |
| Understand deployment principles | [DES-0600](../../knowledge/des/deployment/DES-0600-deployment-engineering-principles.md) |
| Manage environment differences | [DES-0610](../../knowledge/des/deployment/DES-0610-environment-management.md) |
| Manage infrastructure as code | [DES-0620](../../knowledge/des/deployment/DES-0620-infrastructure-code.md) |
| Manage configuration | [DES-0630](../../knowledge/des/deployment/DES-0630-configuration-management.md) |
| Verify release artifacts and provenance | [DES-0640](../../knowledge/des/deployment/DES-0640-release-engineering.md) |
| Select a deployment strategy | [DES-0650](../../knowledge/des/deployment/DES-0650-deployment-strategies.md) |
| Plan rollback and recovery | [DES-0660](../../knowledge/des/deployment/DES-0660-rollback-recovery.md) |
| Assess operational readiness | [DES-0670](../../knowledge/des/deployment/DES-0670-operational-readiness.md) |
| Review deployment governance | [DES-0680](../../knowledge/des/deployment/DES-0680-deployment-governance.md) |
| Return to Delivery | [Delivery](../README.md) |

These standards are drafts and require their own editorial and lifecycle review
before public bundle inclusion.
