---
metadata_schema: 1.0.0
document_id: DES-0720
canonical_id: des.observability.metrics
title: Metrics Standard
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

# DES-0720 - Metrics Standard

## 1. Status and Authority

This is draft, reference-only guidance. Distribution under
[RFC-0001 - Reference Corpus Distribution](../../rfc/RFC-0001-reference-corpus-distribution.md)
does not adopt it, prove compliance, or require metrics collection.
[ADR-0001 - Reference Corpus Layout and Authority](../../adr/ADR-0001-reference-corpus-layout-and-authority.md)
leaves applicability with consumer governance. This draft is aligned with
[DCSG-0001 - DunderCode Canon Style Guide](../../../foundation/documentation/DCSG-0001-canon-style-guide.md).
Uppercase terms are proposed requirements only for an adopting consumer.

## 2. Purpose and Limits

Metrics summarize selected behavior over time for health evaluation, capacity,
trends, and alert inputs. Aggregation loses detail, and missing series, stale
scrapes, retries, resets, and selection bias can change interpretation. A metric
does not by itself explain cause or user impact.

## 3. Definitions and Quality

Each adopted metric SHOULD define:

- name, purpose, owner, unit, type, and calculation;
- event population, exclusions, aggregation, dimensions, and time basis;
- expected range, freshness, reset behavior, and missing-data semantics;
- known biases, sampling, and decisions for which it is unsuitable;
- review and retirement criteria.

Units and semantics MUST NOT change silently. Derived rates and ratios MUST
identify valid denominators and behavior when input is absent or delayed.

## 4. Cardinality and Cost

Dimensions MUST come from a bounded, reviewed set. Raw user, request, session,
device, payload, timestamp, error text, and other effectively unique values MUST
NOT be dimensions by default. Consumers SHOULD estimate the product of dimension
values, growth under failure, and worst-case tenant behavior before release.

Collection SHOULD have budgets for series count, ingestion, storage, query,
transfer, producer overhead, and operator attention. Limits MUST degrade safely:
drop or aggregate according to a disclosed policy rather than exhausting the
observed service or telemetry pipeline. Owners SHOULD review unused and costly
series for removal.

## 5. Privacy and Access

Aggregation does not automatically anonymize data. Small groups, rare labels,
stable identifiers, and cross-dataset joins can reveal individuals or sensitive
operations. Consumers MUST minimize dimensions, restrict sensitive breakdowns,
and apply privacy review where re-identification or inference is plausible.

Access, export, retention, and deletion MUST follow the classification of both
metric values and dimensions. Public dashboards SHOULD use separately reviewed
aggregates and MUST NOT expose internal identifiers or confidential topology.

## 6. Validation Evidence

Consumers SHOULD test metric calculations with known inputs, counter resets,
missing intervals, boundary values, dimension growth, and pipeline loss. Reviews
SHOULD include actual cardinality and cost against budget and evidence that
alerts handle stale or absent data explicitly.

## 7. Family References

- [Observability Engineering Principles](DES-0700-observability-engineering-principles.md)
- [Alerting](DES-0740-alerting-standard.md)
- [Service Health](DES-0760-service-health-standard.md)
- [Operational Telemetry](DES-0770-operational-telemetry-standard.md)

## 8. Revision History

### 1.1.0 - Draft

- Added metric semantics, cardinality controls, cost budgets, privacy limits, and
  missing-data validation.
