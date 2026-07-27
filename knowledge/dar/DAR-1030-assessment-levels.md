# DAR-1030 — Assessment Levels

# Metadata

**Canonical ID:** dar.assessment.levels

**Document Class:** Normative

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

**Applies To:** All Documentation Assessment Reports (DAR) performed within DESys

---

# 1. Purpose

The Assessment Levels Standard defines the engineering requirements for classifying the outcome of assessments performed within the DunderCode Engineering System (DESys).

Its purpose is to establish a consistent and transparent model for expressing assessment outcomes in a way that supports objective review, prioritization, governance, and continuous improvement.

Assessment levels are considered an engineering classification mechanism rather than a subjective rating preference.

---

# 2. Scope

This standard applies to every DAR performed under DESys.

It defines engineering expectations for assessment classification, severity interpretation, outcome normalization, traceability, and review consistency.

Implementation details related to numeric scales, scoring algorithms, visualization tools, or organizational rating systems are intentionally excluded.

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

Every stakeholder responsible for interpreting or assigning assessment outcomes SHALL understand and follow this standard.

---

# 4. Relationship with DESys

This standard derives its engineering philosophy from:

* DEC — DunderCode Engineering Canon
* DEM — DunderCode Engineering Method
* DCSG — DunderCode Canon Style Guide
* DAR-1000 — Assessment Principles
* DAR-1010 — Assessment Methodology
* DAR-1020 — Assessment Criteria

Assessment Levels define how the result of a DAR is classified and communicated.

---

# 5. Assessment Level Principles

Assessment levels SHALL follow the principles defined below.

## Clarity

Assessment levels SHALL communicate outcomes clearly.

Stakeholders SHOULD understand the significance of each level without ambiguity.

---

## Consistency

Equivalent assessment outcomes SHOULD receive equivalent levels.

Level assignment MUST remain consistent across reviewers.

---

## Relevance

Assessment levels SHALL reflect the actual quality condition of the evaluated engineering asset.

Levels MUST NOT be assigned arbitrarily.

---

## Traceability

Each assessment level SHALL be traceable to the criteria and evidence that support it.

Level history SHOULD remain documented.

---

## Actionability

Assessment levels SHOULD help stakeholders determine what actions are needed next.

Each level SHOULD imply an appropriate response path.

---

## Prioritization

Assessment levels SHOULD help prioritize improvement work, review effort, or governance attention.

Higher-severity findings SHOULD receive more urgent attention when appropriate.

---

## Objectivity

Level assignment SHOULD be based on evidence and defined criteria.

Subjective preference MUST NOT replace evaluation discipline.

---

## Evolvability

Assessment level models SHALL evolve through controlled engineering processes.

Changes SHOULD preserve continuity and interpretability.

---

# 6. Standard

Every DAR SHALL define:

* Available assessment levels
* Level semantics
* Assignment rules
* Severity interpretation
* Response expectations
* Review responsibilities
* Revision process

Projects MAY define specialized level models provided they remain consistent with the principles established by this standard.

---

# 7. Mandatory Requirements

Every assessment conducted under DESys MUST:

* Use defined assessment levels.
* Assign levels consistently.
* Preserve traceability to criteria and evidence.
* Communicate the meaning of each level.
* Support follow-up action where required.
* Be reviewable and repeatable.
* Align levels with assessment objectives.

---

# 8. Assessment Level Lifecycle

Assessment levels SHALL follow a controlled lifecycle.

```text id="4v9k3p"
Level Definition
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

Assessment levels SHALL remain governed throughout their lifecycle.

---

# 9. Compliance

An assessment complies with this standard when its level classification model satisfies the requirements defined herein.

Compliance SHALL be verified during governance reviews, documentation reviews, engineering audits, and DAR quality checks.

---

# 10. Relationship with Other DAR Standards

Assessment Levels operate within the complete DAR Engineering Assessment Model.

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

---

# 12. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Assessment Levels Standard.
* Defined engineering requirements for assessment classification.
* Established mandatory requirements for clear and consistent levels.
* Introduced the Assessment Level Lifecycle.
* Positioned Assessment Levels as the outcome classification layer of the DAR Engineering Model.
