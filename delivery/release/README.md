# Release Management

A release is a versioned and traceable set of changes or artifacts made available
for distribution, deployment, or adoption. A release does not require one
packaging technology, versioning scheme, or deployment model.

This page provides DESys reference guidance. Consumer projects define release
authority, version policy, validation evidence, publication channels, and
acceptable residual risk.

## Principles

- **Provenance:** connect a release to immutable source, build inputs, artifacts,
  and validation evidence.
- **Integrity:** publish checksums or signatures appropriate to the distribution
  channel and threat model.
- **Version policy:** use a documented scheme suitable for the artifact and its
  compatibility commitments.
- **Reproducibility:** control inputs and document environmental factors; do not
  promise byte-identical output unless the build demonstrates it.
- **Approval:** identify the human or organizational authority responsible for
  accepting residual risk.
- **Communication:** publish relevant changes, compatibility effects,
  limitations, and recovery guidance.
- **Immutability:** do not move or silently replace a published immutable release
  identifier.

## Release Evidence

A release record should identify, when applicable:

- source revision and build identity;
- artifact names, checksums, and signatures;
- dependency and toolchain versions;
- test and review results;
- known limitations and unresolved risks;
- migration, rollback, roll-forward, or restoration guidance;
- approver and publication timestamp;
- support and deprecation expectations.

Emergency releases may use an expedited process defined by project governance.
They should preserve essential authorization and evidence and record deferred
review work explicitly.

## Reference Flow

```text
Reviewed change
      |
      v
Version and artifact creation
      |
      v
Integrity and validation evidence
      |
      v
Authorized publication
      |
      v
Deployment or consumer adoption
```

This flow is not a universal approval gate. Projects tailor it according to the
artifact, risk, distribution channel, and operational context.

## Navigation

| Objective | Read |
| --- | --- |
| Review the release engineering standard | [DES-0640](../../knowledge/des/deployment/DES-0640-release-engineering.md) |
| Select deployment strategies | [Deployment](../deployment/README.md) |
| Review runtime evidence | [Observability](../observability/README.md) |
| Return to Delivery | [Delivery](../README.md) |

DES-0640 is currently a draft and requires its own editorial and lifecycle review
before public bundle inclusion.
