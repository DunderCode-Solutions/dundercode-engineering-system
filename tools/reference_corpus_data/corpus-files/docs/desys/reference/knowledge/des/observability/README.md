# Observability Reference Standards

This collection contains technology-neutral draft guidance for designing and
governing operational telemetry. It is eligible only for explicit, opt-in
reference distribution after the applicable corpus review. Installing or
reading it does not adopt it as consumer policy.

Consumer code, runtime evidence, law, contracts, approved decisions, security
and privacy policy, and local operating procedures take precedence. The
documents do not grant production access, authorize data collection or
automated action, prove compliance, or guarantee detection, availability, or
incident prevention.

## Use

Consumers should select only practices justified by an explicit operational
purpose and risk assessment. They should record ownership, data boundaries,
approvals, costs, failure modes, retention, and evidence before adoption.
Requirements written in uppercase are proposals for an adopting consumer; they
are not binding merely because this reference was distributed.

## Family

| ID | Draft reference |
| --- | --- |
| DES-0700 | [Observability Engineering Principles](DES-0700-observability-engineering-principles.md) |
| DES-0710 | [Logging](DES-0710-logging-standard.md) |
| DES-0720 | [Metrics](DES-0720-metrics-standard.md) |
| DES-0730 | [Distributed Tracing](DES-0730-distributed-tracing-standard.md) |
| DES-0740 | [Alerting](DES-0740-alerting-standard.md) |
| DES-0750 | [Incident Detection](DES-0750-incident-detection-standard.md) |
| DES-0760 | [Service Health](DES-0760-service-health-standard.md) |
| DES-0770 | [Operational Telemetry](DES-0770-operational-telemetry-standard.md) |
| DES-0780 | [Observability Governance](DES-0780-observability-governance.md) |

## Coverage

The family separates signal design from decisions made with those signals:

- logs address useful events, injection-safe encoding, privacy, access, and
  lifecycle controls;
- metrics address definitions, dimensions, cardinality, privacy, and cost;
- traces address sampling, propagation, and trust boundaries;
- alerts and incident detection address actionability, human confirmation, and
  bounded automation;
- service health addresses objectives, indicators, and dependencies;
- telemetry pipelines address schemas, backpressure, loss disclosure, and
  evidence quality;
- governance addresses ownership, approval, audit, retention, deletion, and
  emergency access.

No signal is complete or inherently trustworthy. Consumers should corroborate
material decisions and disclose missing, sampled, delayed, transformed, or
dropped evidence.

## Governing Context

This family is drafted for the opt-in, non-authoritative distribution model in
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
and the consumer authority hierarchy in
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
Its structure and normative language are aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
These documents provide governing context; lifecycle metadata alone is not
evidence of approval.
