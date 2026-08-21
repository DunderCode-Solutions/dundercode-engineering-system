---
metadata_schema: 1.0.0
document_id: DSK-1018
canonical_id: dsk.engineering.requirements.acceptance-criteria
title: Acceptance Criteria
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1018 | Acceptance Criteria

# 1. Purpose

This skill defines how AI agents create, organize and validate Acceptance Criteria within the DunderCode Engineering System (DESys).

Acceptance Criteria establish the observable conditions that determine whether a User Story has been successfully implemented.

They serve as the contractual agreement between business stakeholders, engineering teams and quality assurance.

---

# 2. Scope

This skill supports:

* Acceptance Criteria Definition
* Acceptance Criteria Refinement
* Story Validation
* Business Rule Validation
* Test Scenario Preparation
* Requirement Verification
* Acceptance Review

---

# 3. Skill Objectives

The Acceptance Criteria Skill aims to:

* define objective completion conditions;
* reduce ambiguity during implementation;
* support software testing;
* preserve requirement traceability;
* improve communication between business and engineering;
* establish measurable delivery expectations.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define acceptance criteria;
* complete a User Story;
* prepare stories for implementation;
* prepare test scenarios;
* validate software requirements;
* refine backlog items.

This skill normally executes after User Stories.

---

# 5. Inputs

Typical inputs include:

* User Stories
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* Product Vision
* Existing Test Scenarios

If story objectives are unclear, the skill should request clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Acceptance Criteria
* Acceptance Checklist
* Validation Scenarios
* Story Completion Conditions
* Requirement Verification Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.requirements.process
    - det.acceptance-criteria.template
    - des.requirements.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - det.user-story.template
    - det.test-case.template
```

---

# 8. Execution Workflow

The Acceptance Criteria Skill follows this workflow.

1. Review User Story.
2. Review related requirements.
3. Review Business Rules.
4. Identify expected outcomes.
5. Define measurable acceptance conditions.
6. Verify completeness.
7. Validate traceability.
8. Produce structured acceptance criteria.

---

# 9. Engineering Guidelines

Acceptance Criteria should:

* describe observable behavior;
* remain measurable;
* avoid implementation details;
* reference related requirements;
* reference applicable business rules;
* support objective verification.

Acceptance Criteria should answer:

> "How do we know this User Story has been completed successfully?"

---

# 10. Recommended Structure

Each Acceptance Criterion should include:

* Identifier
* Description
* Expected Outcome
* Related User Story
* Related Functional Requirement
* Related Business Rule
* Validation Method
* Traceability Reference

---

# 11. Recommended Formats

The preferred formats are:

### Given / When / Then

```text
Given ...

When ...

Then ...
```

or

### Checklist

* [ ] Condition 1
* [ ] Condition 2
* [ ] Condition 3

Projects may adopt one or both approaches according to organizational standards.

---

# 12. Validation

Before completion the skill verifies:

* every criterion is measurable;
* expected behavior is explicit;
* business rules are covered;
* user story objectives are satisfied;
* ambiguity has been eliminated;
* traceability is preserved.

---

# 13. Dependencies

### Parent Skill

* DSK-1010 Requirements Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 14. Collaboration

The Acceptance Criteria Skill commonly collaborates with:

* User Stories
* Testing Engineering
* Development Engineering
* Product Backlog
* Engineering Review

Acceptance Criteria become primary inputs for software verification and testing.

---

# 15. Expected Outcomes

After execution, the Acceptance Criteria should provide:

* objective completion conditions;
* measurable validation rules;
* improved communication between business and engineering;
* complete requirement traceability;
* test-ready implementation specifications;
* reduced delivery ambiguity.

The Acceptance Criteria Skill establishes the objective definition of completion for software features, ensuring that engineering deliverables satisfy business expectations and can be verified consistently throughout the DESys engineering lifecycle.
