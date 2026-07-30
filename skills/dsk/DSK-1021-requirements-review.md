# DSK-1021 | Requirements Review

## Metadata

Document Number: DSK-1021

Canonical ID: dsk.engineering.requirements.requirements-review

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents review, validate and assess Requirements Engineering artifacts within the DunderCode Engineering System (DESys).

The Requirements Review ensures that engineering artifacts are complete, consistent, unambiguous and ready for architecture, implementation and testing.

This skill performs engineering quality assurance rather than generating new requirements.

---

# 2. Scope

This skill supports:

* Requirements Review
* PRD Review
* User Story Review
* Business Rule Review
* Requirement Consistency Analysis
* Requirement Completeness Analysis
* Engineering Quality Assessment
* Review Report Generation

---

# 3. Skill Objectives

The Requirements Review Skill aims to:

* identify incomplete requirements;
* detect inconsistencies;
* verify engineering quality;
* validate requirement traceability;
* reduce implementation risks;
* improve engineering documentation quality.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* review software requirements;
* validate a PRD;
* audit User Stories;
* inspect Business Rules;
* verify engineering completeness;
* prepare documentation for architecture.

This skill normally executes after PRD Generation.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Stakeholder Analysis
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* User Stories
* Acceptance Criteria
* Product Backlog
* Product Requirements Document (PRD)

If engineering artifacts are incomplete, the review should document missing information rather than attempting to invent it.

---

# 6. Outputs

Typical deliverables include:

* Requirements Review Report
* Quality Assessment Report
* Engineering Findings
* Missing Information Report
* Risk Assessment
* Improvement Recommendations
* Review Summary

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.requirements.process
    - des.requirements.documentation
    - det.review-checklist
```

### Optional

```yaml
knowledge:
  optional:
    - det.prd.template
    - det.user-story.template
    - det.acceptance-criteria.template
```

---

# 8. Execution Workflow

The Requirements Review Skill follows this workflow.

1. Load engineering artifacts.
2. Verify document completeness.
3. Validate internal consistency.
4. Verify traceability.
5. Detect ambiguity.
6. Identify duplicated information.
7. Evaluate engineering quality.
8. Produce review findings.
9. Generate the final review report.

---

# 9. Engineering Review Guidelines

The review should verify:

* completeness;
* correctness;
* consistency;
* uniqueness;
* traceability;
* testability;
* feasibility;
* business alignment.

The review should never modify engineering artifacts directly.

Instead, it should recommend improvements.

---

# 10. Review Checklist

The review evaluates whether:

* Product Vision is defined.
* Business Goals are measurable.
* Stakeholders are identified.
* Functional Requirements are complete.
* Non-Functional Requirements are measurable.
* Business Rules are documented.
* User Stories deliver business value.
* Acceptance Criteria are objective.
* Product Backlog is organized.
* PRD is internally consistent.

---

# 11. Validation

Before completion the skill verifies:

* every engineering artifact was reviewed;
* review findings are evidence-based;
* recommendations are actionable;
* unresolved issues are documented;
* traceability remains intact.

---

# 12. Dependencies

### Parent Skill

* DSK-1010 Requirements Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Requirements Review Skill commonly collaborates with:

* PRD Generation
* Architecture Engineering
* Testing Engineering
* Documentation Engineering
* Engineering Governance

The review serves as the quality gate before architectural design begins.

---

# 14. Expected Outcomes

After execution, the Requirements Review should provide:

* verified engineering documentation;
* identified quality issues;
* documented improvement opportunities;
* reduced implementation risks;
* validated engineering consistency;
* approval readiness for architecture and development.

The Requirements Review Skill establishes the engineering quality gate for Requirements Engineering, ensuring that downstream engineering activities begin with complete, consistent and verifiable documentation.
