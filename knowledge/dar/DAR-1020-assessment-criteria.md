---
metadata_schema: 1.0.0
document_id: DAR-1020
canonical_id: dar.assessment.criteria
title: Assessment Criteria
node_type: assessment
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All Documentation Assessment Reports (DAR) performed within DESys
---

# DAR-1020 — Assessment Criteria

# 1. Purpose

The Assessment Criteria Standard defines the engineering requirements for establishing the criteria used to evaluate engineering assets within the DunderCode Engineering System (DESys).

Its purpose is to ensure that assessments are conducted against explicit, relevant, and consistent criteria that support objective evaluation, repeatability, and traceable governance.

Assessment criteria are considered an engineering instrument rather than an informal judgment aid.

---

# 2. Scope

This standard applies to every DAR performed under DESys.

It defines engineering expectations for criterion definition, relevance, consistency, applicability, traceability, and lifecycle management.

Implementation details related to scoring tools, templates, or reviewer-specific preferences are intentionally excluded.

---

# 3. Audience

This standard is intended for:

* Engineering Reviewers
* Solution Architects
* Software Architects
* Technical Leaders
* Engineering Managers
* Documentation Engineers
* Governance Teams
* AI-assisted engineering systems

Every stakeholder responsible for defining or applying assessment criteria SHALL understand and follow this standard.

---

# 4. Relationship with DESys

This standard derives its engineering philosophy from:

* DEC — DunderCode Engineering Canon
* DEM — DunderCode Engineering Method
* DCSG — DunderCode Canon Style Guide
* DAR-1000 — Assessment Principles
* DAR-1010 — Assessment Methodology

Assessment Criteria define what is evaluated during a DAR and how evaluation remains consistent.

---

# 5. Assessment Criteria Principles

Assessment criteria SHALL follow the principles defined below.

## Relevance

Criteria SHALL be relevant to the engineering asset being assessed.

Irrelevant criteria MUST NOT be introduced.

---

## Explicitness

Criteria SHALL be stated clearly and unambiguously.

Implicit evaluation standards SHOULD be avoided.

---

## Consistency

Equivalent assets SHOULD be assessed using equivalent criteria whenever practical.

Criteria application MUST remain consistent across assessments.

---

## Traceability

Every criterion SHALL remain traceable to a governing standard, policy, or evaluation objective.

Criterion history SHOULD be documented.

---

## Applicability

Criteria SHALL be applied only when they are relevant to the type and scope of the assessed asset.

Criteria MUST NOT be used outside their intended context.

---

## Objectivity

Criteria SHOULD be framed in a way that supports evidence-based evaluation.

Subjective interpretation SHOULD be minimized.

---

## Completeness

Assessment criteria SHOULD cover the quality dimensions relevant to the review objective.

Missing critical criteria SHOULD be identified and corrected.

---

## Evolvability

Criteria SHALL evolve through controlled engineering processes.

Changes SHOULD preserve continuity and traceability.

---

# 6. Standard

Every DAR SHALL define:

* Assessment objective
* Applicable criteria set
* Criterion definitions
* Evaluation intent
* Traceability source
* Review responsibilities
* Revision process

Projects MAY define specialized criteria sets provided they remain consistent with the principles established by this standard.

---

# 7. Mandatory Requirements

Every assessment conducted under DESys MUST:

* Use explicitly defined criteria.
* Apply criteria consistently.
* Preserve traceability to source standards.
* Avoid irrelevant criteria.
* Document changes to criteria over time.
* Support future reassessment.
* Align criteria with the assessment objective.

---

# 8. Assessment Criteria Lifecycle

Assessment criteria SHALL follow a controlled lifecycle.

```text id="b9n4qx"
Criterion Definition
      ↓
Review
      ↓
Approval
      ↓
Application
      ↓
Evaluation
      ↓
Revision
      ↓
Retirement
```

Criteria SHALL remain governed throughout their lifecycle.

---

# 9. Compliance

An assessment complies with this standard when its criteria definition and application satisfy the requirements defined herein.

Compliance SHALL be verified during governance reviews, documentation reviews, engineering audits, and DAR quality checks.

---

# 10. Relationship with Other DAR Standards

Assessment Criteria operate within the complete DAR Engineering Assessment Model.

| Standard | Discipline                 |
| -------- | -------------------------- |
| DAR-1000 | Assessment Principles      |
| DAR-1010 | Assessment Methodology     |
| DAR-1020 | Assessment Criteria        |
| DAR-1030 | Assessment Levels          |
| DAR-1040 | Evidence Collection        |
| DAR-1050 | Findings & Recommendations |
| DAR-1060 | Quality Scoring            |
| DAR-1070 | Continuous Improvement     |
| DAR-1080 | Assessment Governance      |

Together, these standards define the Documentation Assessment Report (DAR) Engineering Model adopted by DESys.

---

# 11. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DAR-1000 — Assessment Principles
* DAR-1010 — Assessment Methodology

---

# 12. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Assessment Criteria Standard.
* Defined engineering requirements for assessment criteria.
* Established mandatory requirements for relevant and traceable criteria.
* Introduced the Assessment Criteria Lifecycle.
* Positioned Assessment Criteria as the evaluation layer of the DAR Engineering Model.
