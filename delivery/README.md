# Delivery

The Delivery collection provides navigation from engineering output to release,
deployment, and operational evidence. It describes reusable DESys guidance; it
does not automatically define a consumer project's production policy.

Consumer projects identify their own release approvers, service objectives,
environments, security controls, incident processes, and acceptable risk. When
project evidence conflicts with vendored DESys guidance, the project's code,
runtime behavior, and approved decisions take precedence.

## Current Scope

The first reviewed Delivery reference set provides navigation for:

| Area | Purpose | Navigation |
| --- | --- | --- |
| Release | Version, provenance, validation, and publication | [Release](release/README.md) |
| Deployment | Controlled change to an execution environment | [Deployment](deployment/README.md) |
| Observability | Telemetry, service health, diagnosis, and feedback | [Observability](observability/README.md) |

The `ci-cd/`, `operations/`, and `support/` directories do not yet contain
substantive reviewed assets. Their current README files are excluded from the
public corpus rather than presented as complete guidance.

## Delivery Flow

```text
Reviewed change
      |
      v
Versioned release
      |
      v
Controlled deployment
      |
      v
Runtime evidence and feedback
```

This flow is descriptive, not a universal approval sequence. Projects tailor
activities according to change risk, urgency, architecture, and governance.

## Cross-Cutting Requirements

Delivery decisions should identify:

- accountable human or organizational owners;
- immutable source and artifact provenance;
- validation evidence and acceptance criteria;
- security, privacy, and compliance constraints;
- rollout, abort, recovery, and communication plans;
- service objectives and observable outcomes;
- retained evidence for later review.

Automation may execute an approved plan, but automation does not grant approval
authority or determine acceptable business risk.

## Related Standards

- [Deployment standards](../knowledge/des/deployment/README.md)
- [Observability standards](../knowledge/des/observability/README.md)
- [Engineering processes](../engineering/dep/README.md)
- [Foundation authority model](../foundation/README.md)

The linked standards are currently drafts. They are reference candidates until
their own lifecycle and distribution reviews are complete.
