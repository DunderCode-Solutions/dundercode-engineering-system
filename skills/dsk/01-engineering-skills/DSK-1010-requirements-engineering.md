---
metadata_schema: 1.0.0
document_id: DSK-1010
canonical_id: dsk.engineering.requirements-engineering
title: Requirements Engineering
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1010 | Requirements Engineering

# 1. Purpose

This skill defines how AI agents perform Requirements Engineering within the DunderCode Engineering System (DESys).

The objective is to transform business needs into complete, traceable and actionable engineering requirements while maintaining consistency with DESys standards, processes and templates.

This skill orchestrates engineering knowledge rather than replacing it.

---

# 2. Scope

This skill supports activities such as:

* Product Vision
* Business Goals
* Stakeholder Identification
* Functional Requirements
* Non-Functional Requirements
* User Stories
* Acceptance Criteria
* Product Backlog
* Epics
* Features
* PRD Generation
* Requirement Reviews
* Requirement Refinement

---

# 3. Skill Objectives

The Requirements Engineering Skill aims to:

* understand business needs;
* identify project objectives;
* organize engineering requirements;
* classify requirements correctly;
* preserve traceability;
* produce standardized engineering artifacts.

---

# 4. Activation Criteria

This skill should be activated when the user requests:

* create a PRD;
* define software requirements;
* organize business needs;
* write user stories;
* identify functional requirements;
* identify non-functional requirements;
* refine product scope;
* review existing requirements.

---

# 5. Inputs

Typical inputs include:

* business objectives;
* product ideas;
* stakeholder interviews;
* meeting notes;
* existing documentation;
* user constraints;
* organizational standards.

Incomplete inputs should trigger clarification before execution.

---

# 6. Outputs

Typical deliverables include:

* Product Requirements Document (PRD)
* User Stories
* Functional Requirements Specification
* Non-Functional Requirements Specification
* Product Backlog
* Acceptance Criteria
* Scope Definition
* Requirements Review Report

Deliverables should follow DESys engineering standards.

---

# 7. Required Knowledge

This skill should consume knowledge from the following DESys libraries.

### Required

```yaml
knowledge:
  required:
    - des.requirements.documentation
    - dep.requirements.process
    - det.prd.template
```

### Optional

```yaml
knowledge:
  optional:
    - dea.system-context
    - det.user-story.template
    - dep.architecture.process
```

---

# 8. Execution Workflow

The Requirements Engineering Skill follows this workflow:

1. Understand the business context.
2. Identify stakeholders.
3. Define project objectives.
4. Capture business needs.
5. Classify requirements.
6. Resolve ambiguities.
7. Produce structured requirements.
8. Validate completeness.
9. Generate engineering deliverables.

---

# 9. Engineering Rules

The skill should always:

* distinguish business requirements from technical solutions;
* separate functional and non-functional requirements;
* maintain requirement traceability;
* avoid implementation decisions during requirements analysis;
* identify assumptions explicitly;
* record unresolved questions.

---

# 10. Validation

Before completion, the skill verifies:

* objectives are defined;
* stakeholders are identified;
* requirements are complete;
* requirements are testable;
* acceptance criteria exist;
* ambiguities are documented;
* deliverables follow DESys templates.

---

# 11. Dependencies

This skill depends on:

### Processes

* DEP Requirements Process

### Templates

* PRD Template
* User Story Template

### Standards

* Requirements Documentation Standard

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 12. Collaboration

This skill commonly collaborates with:

* Architecture Engineering
* Documentation Engineering
* Engineering Review

Requirements should always precede architecture.

---

# 13. Expected Outcomes

After execution, the agent should be able to:

* understand the business problem;
* organize engineering requirements;
* generate standardized PRDs;
* produce traceable user stories;
* prepare the project for architectural design;
* reduce ambiguity before implementation.

The Requirements Engineering Skill establishes the engineering foundation upon which all subsequent software design and implementation activities are built.
