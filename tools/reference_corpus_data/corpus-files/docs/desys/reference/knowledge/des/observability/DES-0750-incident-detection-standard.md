---
metadata_schema: 1.0.0
document_id: DES-0750
canonical_id: des.observability.incident-detection
title: Incident Detection Standard
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

# DES-0750 - Incident Detection Standard

## 1. Status and Authority

This document is draft, reference-only guidance. It does not declare events to
be incidents, authorize response actions, or replace consumer incident policy.
Distribution follows
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md),
and consumer governance controls adoption and authority under
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
This draft is aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
Uppercase terms are proposals only for an adopting consumer.

## 2. Purpose and Limits

Incident detection combines telemetry, user reports, dependency information,
and operational context to identify conditions that may require coordinated
response. Detection can be late, wrong, incomplete, or manipulated. Absence of
an alert is not evidence that no incident exists.

## 3. Recognition and Confirmation

Consumers SHOULD define recognition criteria based on observed impact, affected
scope, duration, safety or security implications, and uncertainty. Severity MUST
reflect current evidence and be revisable as facts change.

Automated classifiers and alerts MAY create a candidate incident. A designated
human SHOULD confirm the incident, severity, and response context before
high-impact action. Immediate containment MAY precede confirmation only within a
separately approved emergency policy with bounded authority and retained
evidence.

Reports from users, support, partners, and dependencies SHOULD remain valid
detection inputs even when telemetry does not corroborate them.

## 4. Bounded Automation

Automated detection or response MUST have:

- a named owner and approved purpose;
- defined inputs, confidence limits, and fail-safe behavior;
- least-privileged scope, rate and duration limits, and protected credentials;
- idempotency or a documented recovery path;
- human override, stop conditions, and escalation;
- durable records of input, decision, action, and outcome.

Automation MUST NOT infer authorization from telemetry context. Destructive,
irreversible, cross-tenant, or broad production action requires explicit human
confirmation unless an approved risk decision defines narrower safe conditions.

## 5. Detection Quality

Owners SHOULD review missed incidents, false candidates, delayed confirmation,
severity changes, correlated failures, and dependence on unavailable pipelines.
Tests SHOULD include stale and conflicting evidence, notification failure,
partial outages, clock error, and loss of the detection system itself.

Records SHOULD distinguish observations, hypotheses, decisions, and confirmed
facts. Post-incident learning MUST NOT retroactively present uncertain detection
as certainty.

## 6. Family References

- [Alerting](DES-0740-alerting-standard.md)
- [Service Health](DES-0760-service-health-standard.md)
- [Operational Telemetry](DES-0770-operational-telemetry-standard.md)
- [Observability Governance](DES-0780-observability-governance.md)

## 7. Revision History

### 1.1.0 - Draft

- Added candidate-versus-confirmed incident handling, non-telemetry inputs,
  uncertainty, and strict boundaries for automated response.
