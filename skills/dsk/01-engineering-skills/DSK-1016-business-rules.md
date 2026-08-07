# DSK-1016 | Business Rules

## Metadata

Document Number: DSK-1016

Canonical ID: dsk.engineering.requirements.business-rules

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, document, organize and validate Business Rules within the DunderCode Engineering System (DESys).

Business Rules describe the organizational policies, constraints and decision logic that govern how the business operates independently of software implementation.

These rules become authoritative engineering knowledge used throughout analysis, design, implementation and validation.

---

# 2. Scope

This skill supports:

* Business Rule Identification
* Business Policy Definition
* Decision Rule Specification
* Constraint Definition
* Validation Rule Definition
* Workflow Rule Definition
* Rule Classification
* Rule Review

---

# 3. Skill Objectives

The Business Rules Skill aims to:

* identify organizational policies;
* separate business logic from system behavior;
* preserve business knowledge;
* reduce ambiguity;
* improve engineering traceability;
* support consistent implementation.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define business rules;
* document company policies;
* specify validation logic;
* identify organizational constraints;
* model business decisions;
* prepare detailed requirements.

This skill normally executes after Functional and Non-Functional Requirements.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Organizational Policies
* Regulatory Requirements
* Existing Business Processes

Incomplete business logic should trigger clarification before execution.

---

# 6. Outputs

Typical deliverables include:

* Business Rules Catalog
* Business Policy Specification
* Decision Rules
* Validation Rules
* Operational Constraints
* Rule Dependency Mapping
* Business Rule Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.requirements.process
    - des.requirements.documentation
    - det.prd.template
```

### Optional

```yaml
knowledge:
  optional:
    - dea.business-context
    - dea.domain-model
    - det.business-rule.template
```

---

# 8. Execution Workflow

The Business Rules Skill follows this workflow.

1. Analyze business context.
2. Review organizational objectives.
3. Identify governing policies.
4. Identify decision logic.
5. Classify business rules.
6. Define rule dependencies.
7. Validate consistency.
8. Produce structured business rule documentation.

---

# 9. Engineering Guidelines

Business Rules should:

* represent organizational knowledge;
* remain independent of software implementation;
* avoid technology references;
* use business terminology;
* remain testable;
* support traceability.

Business Rules should describe **why** a decision exists rather than **how** software implements it.

---

# 10. Business Rule Categories

Typical categories include:

* Validation Rules
* Calculation Rules
* Authorization Rules
* Eligibility Rules
* Approval Rules
* Workflow Rules
* Regulatory Rules
* Financial Rules
* Operational Rules
* Compliance Rules

Projects may define additional rule categories.

---

# 11. Rule Structure

Each Business Rule should include:

* Identifier
* Name
* Description
* Business Justification
* Rule Category
* Trigger
* Expected Outcome
* Exceptions
* Related Requirements
* Traceability Reference

This structure standardizes rule documentation across DESys.

---

# 12. Validation

Before completion the skill verifies:

* rules are independent of implementation;
* organizational policies are preserved;
* rules are unambiguous;
* duplicate rules do not exist;
* dependencies are documented;
* traceability is maintained.

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

The Business Rules Skill commonly collaborates with:

* Functional Requirements
* User Stories
* Architecture Engineering
* Testing Engineering
* Documentation Engineering

Business Rules become authoritative references for implementation and validation.

---

# 15. Expected Outcomes

After execution, the Business Rules should provide:

* documented organizational knowledge;
* standardized decision logic;
* explicit operational policies;
* implementation-independent business constraints;
* complete traceability to engineering requirements;
* a stable foundation for architecture, development and testing.

The Business Rules Skill preserves the organization's business knowledge as reusable engineering assets, ensuring that software implementations remain aligned with business policies throughout the DESys engineering lifecycle.
