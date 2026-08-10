---
metadata_schema: 1.0.0
document_id: DAR-1060
canonical_id: dar.assessment.quality-scoring
title: Quality Scoring
node_type: assessment
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All Documentation Assessment Reports (DAR) performed within DESys
aliases:
- dar.quality-scoring
---

# DAR-1060 — Quality Scoring

# 1. Purpose

The Quality Scoring Standard defines the engineering requirements for assigning structured quality scores to assessed engineering assets within the DunderCode Engineering System (DESys).

Its purpose is to establish a consistent, transparent, and traceable scoring model that supports assessment interpretation, prioritization, governance, and continuous improvement.

Quality scoring is considered an engineering classification mechanism rather than a subjective rating preference.

---

# 2. Scope

This standard applies to every DAR performed under DESys.

It defines engineering expectations for score definition, score interpretation, score assignment, consistency, traceability, and lifecycle management.

Implementation details related to numeric formulas, automated ranking systems, visualization tools, or organization-specific rating conventions are intentionally excluded.

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

Every stakeholder responsible for assigning or interpreting quality scores SHALL understand and follow this standard.

---

# 4. Relationship with DESys

This standard derives its engineering philosophy from:

* DEC — DunderCode Engineering Canon
* DEM — DunderCode Engineering Method
* DCSG — DunderCode Canon Style Guide
* DAR-1000 — Assessment Principles
* DAR-1010 — Assessment Methodology
* DAR-1020 — Assessment Criteria
* DAR-1030 — Assessment Levels
* DAR-1040 — Evidence Collection
* DAR-1050 — Findings & Recommendations

Quality Scoring defines how assessment outcomes are summarized and compared in a consistent way.

---

# 5. Quality Scoring Principles

Quality scoring SHALL follow the principles defined below.

## Clarity

Quality scores SHALL communicate assessment outcomes clearly.

Stakeholders SHOULD understand what the score represents.

---

## Consistency

Equivalent assessment outcomes SHOULD produce equivalent scores.

Scoring practices SHALL remain stable across assessments.

---

## Traceability

Every score SHALL remain traceable to the underlying evidence, criteria, and findings.

Score history SHOULD be preserved for future review.

---

## Relevance

Scores SHALL reflect the actual quality condition of the assessed engineering asset.

Scores MUST NOT be assigned arbitrarily.

---

## Actionability

Scores SHOULD support prioritization and decision-making.

Scores SHOULD help stakeholders determine whether action is required.

---

## Objectivity

Scoring SHALL be based on evidence and defined rules rather than reviewer preference.

Subjective judgment MUST NOT replace scoring discipline.

---

## Comparability

Scores SHOULD support comparison across reviews, assets, and time periods whenever practical.

Equivalent scoring models SHOULD remain comparable.

---

## Evolvability

Scoring models SHALL evolve through controlled engineering processes.

Changes SHOULD preserve interpretability and continuity.

---

# 6. Standard

Every DAR SHALL define:

* Scoring model
* Score interpretation
* Score assignment rules
* Traceability source
* Review responsibilities
* Revision process
* Comparison expectations

Projects MAY define specialized scoring models provided they remain consistent with the principles established by this standard.

---

# 7. Mandatory Requirements

Every assessment conducted under DESys MUST:

* Use a defined quality scoring model.
* Apply scoring consistently.
* Preserve traceability to criteria and evidence.
* Communicate the meaning of each score.
* Support future reassessment.
* Align scoring with assessment objectives.
* Distinguish scoring from qualitative findings.

---

# 8. Quality Scoring Lifecycle

Quality scoring SHALL follow a controlled lifecycle.

```text id="4q2n7x"
Score Model Definition
      ↓
Review
      ↓
Approval
      ↓
Application
      ↓
Interpretation
      ↓
Revision
      ↓
Retirement
```

Quality scoring SHALL remain governed throughout its lifecycle.

---

# 9. Compliance

An assessment complies with this standard when its quality scoring model satisfies the requirements defined herein.

Compliance SHALL be verified during governance reviews, documentation reviews, engineering audits, and DAR quality checks.

---

# 10. Relationship with Other DAR Standards

Quality Scoring operates within the complete DAR Engineering Assessment Model.

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
* DAR-1020 — Assessment Criteria
* DAR-1030 — Assessment Levels
* DAR-1050 — Findings & Recommendations

---

# 12. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Quality Scoring Standard.
* Defined engineering requirements for assessment scoring.
* Established mandatory requirements for traceable and comparable scores.
* Introduced the Quality Scoring Lifecycle.
* Positioned quality scoring as the summarization layer of the DAR Engineering Model.
