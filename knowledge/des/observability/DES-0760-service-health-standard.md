---
metadata_schema: 1.0.0
document_id: DES-0760
canonical_id: des.observability.service-health
title: Service Health Standard
node_type: standard
document_class: normative
version: 1.1.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Consumer systems that explicitly adopt this draft through their governance
relationships:
- type: references
  target: rfc.corpus.reference-distribution
- type: references
  target: adr.corpus.layout-and-authority
- type: references
  target: dcsg.canon.style-guide
---

# DES-0760 - Service Health Standard

## 1. Status and Authority

This is draft, reference-only guidance for optional consumer adoption. It does
not define a consumer's service commitments, health claims, or incident policy.
Distribution follows
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md),
while local evidence and approval remain authoritative under
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
This draft is aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
Uppercase terms are proposed requirements only after adoption.

## 2. Purpose and Limits

Service health is an evidence-based view of whether a service is delivering an
explicitly defined outcome. A process being reachable is not equivalent to user
success. A green dashboard does not guarantee health, and an internal component
failure does not necessarily imply material user impact.

## 3. Objectives and Indicators

For each material service, an adopting consumer SHOULD define:

- the users, journeys, interfaces, and operating periods in scope;
- service indicators and how valid events are counted;
- objectives, evaluation windows, exclusions, and error-budget policy;
- freshness and missing-data behavior;
- owners for the objective, measurement, and response;
- review criteria when architecture or user needs change.

Objectives MUST be distinguished from contractual commitments and public claims.
No target guarantees an outcome. Indicators SHOULD measure user-observable
results where practical and SHOULD disclose known blind spots and low-volume
uncertainty.

## 4. Health Views

Health views SHOULD represent relevant states such as healthy, degraded,
unavailable, unknown, and under maintenance rather than forcing binary status.
They MUST identify scope, timestamp or freshness, evidence source, and whether
the view is internal or approved for external communication.

Rollups MUST NOT hide material tenant, region, feature, or journey impact. Views
containing sensitive topology or customer-specific status require appropriate
access. Public status requires separate communications approval and evidence.

## 5. Dependencies

Service owners SHOULD maintain a dependency view covering critical upstream,
downstream, platform, identity, data, and third-party dependencies. The view
SHOULD record ownership, expected failure effect, observability gap, and fallback
or escalation path.

Dependency signals are untrusted inputs across organizational boundaries.
Health aggregation MUST distinguish direct evidence from inferred dependency
state and avoid asserting a root cause before confirmation.

## 6. Validation and Review

Consumers SHOULD test indicator calculations, partial degradation, dependency
failure, stale data, low traffic, planned maintenance, regional splits, and the
health system's own failure. Review evidence SHOULD compare stated health with
user reports and confirmed incidents and record mismatches.

## 7. Family References

- [Metrics](DES-0720-metrics-standard.md)
- [Alerting](DES-0740-alerting-standard.md)
- [Incident Detection](DES-0750-incident-detection-standard.md)
- [Operational Telemetry](DES-0770-operational-telemetry-standard.md)

## 8. Revision History

### 1.1.0 - Draft

- Added service objectives and indicators, nuanced health views, dependency
  evidence, public-claim boundaries, and health-system failure tests.
