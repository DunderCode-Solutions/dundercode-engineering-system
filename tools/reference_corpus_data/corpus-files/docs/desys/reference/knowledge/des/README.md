# Engineering Standards Candidates

This collection navigates proposed DunderCode Engineering Standards (DES).
Standards in the current public-review scope are draft candidates, not approved
requirements. Their presence, metadata, indexing, or distribution does not
demonstrate compliance or grant approval.

## Authority and Lifecycle

Vendored DES documents are reference-only. A consumer project determines
applicability, exceptions, evidence, reviewers, and adoption through its own
governance. Consumer code, runtime evidence, approved decisions, policies, and
legal obligations take precedence for claims about that project.

Each candidate requires its own editorial, technical, security, distribution,
and lifecycle review. This README does not advance any candidate beyond its
recorded draft state or imply that review and approval have occurred.

## Current Navigation

| Candidate family | Scope | Reference |
| --- | --- | --- |
| Deployment | Environments, configuration, delivery strategies, recovery, readiness, and governance | [Deployment candidates](deployment/README.md) |
| Observability | Logging, metrics, tracing, alerting, incident detection, service health, telemetry, and governance | [Observability candidates](observability/README.md) |

For context, use the [Foundation authority model](../../foundation/README.md)
and the reviewed [Delivery guidance](../../delivery/README.md). These relative
paths preserve the source layout when vendored under `docs/desys/reference/`.
