---
metadata_schema: 1.0.0
document_id: DES-0730
canonical_id: des.observability.distributed-tracing
title: Distributed Tracing Standard
node_type: standard
document_class: normative
version: 1.1.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Consumer distributed systems that explicitly adopt this draft through their governance
relationships:
- type: references
  target: rfc.corpus.reference-distribution
- type: references
  target: adr.corpus.layout-and-authority
- type: references
  target: dcsg.canon.style-guide
---

# DES-0730 - Distributed Tracing Standard

## 1. Status and Authority

This is draft, reference-only guidance for opt-in consumer use. It does not
authorize cross-system tracking or require end-to-end tracing. Distribution is
defined by
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md),
while consumer privacy, security, architecture, and operational decisions take
precedence under
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
This draft is aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
Uppercase terms apply only if locally adopted.

## 2. Purpose and Limits

Tracing can relate selected operations across asynchronous and service
boundaries to support latency and failure diagnosis. Sampling, missing
instrumentation, clock error, retries, fan-out, and broken propagation produce
partial views. A trace is not proof of causation, completeness, or identity.

## 3. Trace and Span Design

An adopting consumer:

- MUST document traced boundaries, operation names, attributes, status
  semantics, ownership, and expected overhead;
- SHOULD use bounded, stable attributes and avoid payload capture;
- MUST NOT place credentials, customer content, or personal identifiers in
  trace context, baggage, names, events, or attributes by default;
- SHOULD represent links, retries, queues, and asynchronous work without
  inventing parent-child relationships;
- MUST expose whether a view is complete, partial, sampled, or delayed.

## 4. Sampling

Sampling policy MUST state where decisions occur, target volume, selection
criteria, retention, and expected bias. Head, tail, adaptive, and error-focused
sampling each omit different evidence; consumers SHOULD validate policy against
both ordinary and failure traffic.

Sampling MUST have overload behavior and cost limits. Changes that affect trend
comparison or alert interpretation SHOULD be recorded. Sensitive traces MUST NOT
be retained merely because a sampling rule selected them.

## 5. Context and Trust Boundaries

Inbound trace identifiers, flags, and baggage are untrusted. At each trust
boundary, a consumer MUST validate format and size, remove disallowed fields,
apply local sampling and access policy, and prevent external callers from
forcing costly collection or privileged correlation.

Context propagated to another organization, region, tenant, or sensitivity zone
MUST be minimized and explicitly allowed. Locally generated correlation values
SHOULD be non-secret, non-semantic, bounded in lifetime, and unsuitable as
authentication or authorization evidence.

## 6. Security and Validation

Trace access and export SHOULD reveal no more topology or tenant activity than
the operational purpose requires. Validation SHOULD cover malformed context,
oversized baggage, spoofed sampling flags, partial paths, clock skew, duplicate
spans, high fan-out, pipeline loss, and deletion across linked stores.

## 7. Family References

- [Observability Engineering Principles](DES-0700-observability-engineering-principles.md)
- [Logging](DES-0710-logging-standard.md)
- [Operational Telemetry](DES-0770-operational-telemetry-standard.md)
- [Observability Governance](DES-0780-observability-governance.md)

## 8. Revision History

### 1.1.0 - Draft

- Added explicit sampling bias, context validation, trust-boundary, privacy,
  overload, and trace-completeness guidance.
