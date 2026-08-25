---
metadata_schema: 1.0.0
document_id: DES-0710
canonical_id: des.observability.logging
title: Logging Standard
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

# DES-0710 - Logging Standard

## 1. Status and Authority

This is draft, reference-only guidance for voluntary consumer adoption. It is
not approved policy and does not authorize logging. Its distribution follows
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md),
and it remains subordinate to the consumer authority boundaries in
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md).
Its structure and normative language are aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
The uppercase terms are proposed requirements only after adoption.

## 2. Purpose and Limits

Logs can provide event-level evidence for diagnosis, security investigation,
audit support, and operational learning. They do not establish complete history,
causation, user intent, or compliance. Logging MAY be omitted where another
signal answers the need with less risk or cost.

## 3. Event Design

An adopting consumer:

- MUST define useful event categories, severity semantics, ownership, and the
  questions each category supports;
- SHOULD use stable, documented fields for time, event type, component,
  environment, outcome, and non-sensitive correlation where relevant;
- MUST distinguish event time from collection time and disclose uncertain clock
  ordering where material;
- SHOULD avoid repetitive success events, unbounded payloads, and debug output
  without a time-limited purpose;
- MUST treat log text and fields as untrusted data.

Changing field meaning or severity SHOULD follow schema review and preserve a
version or migration note when consumers depend on it.

## 4. Privacy and Redaction

Logs MUST NOT contain credentials, authentication material, encryption keys, or
raw secret values. Personal data, customer content, request bodies, headers,
query values, and stable person or device identifiers MUST be excluded by
default and included only with documented necessity and approval.

Redaction SHOULD occur before data leaves the producing trust boundary. It MUST
fail safely: uncertain values are omitted or replaced rather than emitted in
full. Teams SHOULD test redaction against encoded, nested, multiline, oversized,
and malformed input and review derived fields that could permit re-identification.

## 5. Injection and Integrity

Untrusted values MUST be encoded as data rather than allowed to create fields,
lines, control sequences, or executable markup. Renderers and export paths MUST
escape content for their destination. Consumers SHOULD limit record size and
field count and preserve an explicit truncation indicator.

Logs SHOULD carry integrity and provenance appropriate to their use. Operators
MUST NOT infer authenticity merely from a source label; compromised producers
and pipeline transformations can create misleading records.

## 6. Access and Lifecycle

Access MUST be least-privileged, purpose-bound, reviewed, and auditable where
risk warrants. Search, bulk export, support access, and administrative access
SHOULD be governed separately. Shared public links and unrestricted production
log access SHOULD NOT be enabled by default.

Retention MUST have an approved duration by data category and storage tier.
Deletion, legal hold, backup expiry, export, and downstream-copy behavior MUST be
defined and tested. Longer retention is not automatically safer or more useful.

## 7. Validation Evidence

Useful evidence includes sample records with synthetic data, schema tests,
redaction and injection tests, access reviews, retention/deletion results, volume
and cost limits, and documented loss or truncation behavior. Passing these tests
does not establish legal or regulatory compliance.

## 8. Family References

- [Observability Engineering Principles](DES-0700-observability-engineering-principles.md)
- [Operational Telemetry](DES-0770-operational-telemetry-standard.md)
- [Observability Governance](DES-0780-observability-governance.md)

## 9. Revision History

### 1.1.0 - Draft

- Added opt-in authority limits, privacy and redaction controls, injection-safe
  handling, access governance, and tested retention and deletion.
