---
metadata_schema: 1.0.0
document_id: DES-0740
canonical_id: des.observability.alerting
title: Alerting Standard
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

# DES-0740 - Alerting Standard

## 1. Status and Authority

This draft is reference-only and requires explicit consumer adoption. It does
not define local paging obligations, severity, staffing, or response authority.
Distribution follows
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md),
and consumer governance remains authoritative under
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
This draft is aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
Uppercase terms are proposed requirements only after adoption.

## 2. Purpose and Limits

An alert requests attention for a condition with a defined response. It is not
proof of an incident or root cause. Not every anomaly needs notification, and
not every notification should interrupt a person.

## 3. Actionable Alert Definition

Each interrupting alert MUST identify:

- the affected service or objective and observed condition;
- user or operational impact, with uncertainty stated;
- severity and routing rationale;
- a current owner and expected first action;
- supporting evidence, freshness, and known blind spots;
- suppression, escalation, and resolution behavior;
- a safe investigation reference maintained by the consumer.

An alert without a timely human action or separately approved automated response
SHOULD be a dashboard, report, or recorded event instead. Notification content
MUST minimize sensitive data because delivery channels may have broader access.

## 4. Anti-Fatigue Controls

Consumers SHOULD group related symptoms, deduplicate repeated notifications,
route by ownership, and use delays or persistence windows appropriate to impact.
Maintenance, testing, and known dependency failure SHOULD have explicit handling
rather than ad hoc silencing.

Owners MUST review alert volume, repeated pages, false positives, false
negatives, unowned alerts, time-to-acknowledge, and actions taken. Chronic noisy
alerts SHOULD be repaired, downgraded, or retired. Fatigue and unsafe workload
are design failures, not operator shortcomings.

## 5. Testing and Change

Before enabling an interrupting route, consumers SHOULD test signal absence,
staleness, threshold boundaries, recovery, notification failure, duplicate
delivery, ownership gaps, and dependency-wide events. Tests MUST avoid sending
real secrets or causing unapproved production changes.

Material changes to thresholds, severity, routing, or automation SHOULD be
reviewed and reversible. Alert evaluation SHOULD disclose sampled, delayed, or
dropped telemetry that could suppress or trigger notifications.

## 6. Evidence and Limits

Useful evidence includes the definition, owner acceptance, test results,
notification history, response outcomes, suppression history, and review
decisions. Alert counts alone do not demonstrate reliability or preparedness.

## 7. Family References

- [Metrics](DES-0720-metrics-standard.md)
- [Incident Detection](DES-0750-incident-detection-standard.md)
- [Service Health](DES-0760-service-health-standard.md)
- [Observability Governance](DES-0780-observability-governance.md)

## 8. Revision History

### 1.1.0 - Draft

- Added actionable-alert content, anti-fatigue controls, sensitive notification
  handling, ownership, and failure-mode testing.
