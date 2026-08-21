---
metadata_schema: 1.0.0
document_id: DSK-1110
canonical_id: dsk.engineering.architecture.architecture-vision
title: Architecture Vision
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1110 | Architecture Vision

# 1. Purpose

This skill defines how AI agents create and refine an Architecture Vision within the DunderCode Engineering System (DESys).

The Architecture Vision establishes the strategic direction of the software architecture before detailed architectural models and implementation decisions are produced.

It aligns technical decisions with business objectives while defining the architectural principles that will guide the entire engineering lifecycle.

---

# 2. Scope

This skill supports:

* Architecture Vision creation
* Architecture Vision refinement
* Architectural principle definition
* Quality attribute prioritization
* Technical strategy definition
* Architecture alignment
* Vision review

---

# 3. Skill Objectives

The Architecture Vision Skill aims to:

* establish architectural direction;
* align architecture with business objectives;
* define architectural principles;
* identify architectural priorities;
* support future architectural decisions;
* provide a stable foundation for architectural modeling.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define software architecture;
* start architecture design;
* establish architecture principles;
* define technical strategy;
* prepare architecture documentation.

This skill normally executes immediately after Requirements Engineering has been completed.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* Product Requirements Document (PRD)
* Requirements Traceability

Missing business or engineering information should trigger clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Architecture Vision Statement
* Architectural Principles
* Technical Strategy
* Quality Attribute Priorities
* Architecture Goals
* Architecture Scope
* Architecture Vision Review

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="mf27st"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="qx7l6r"
knowledge:
  optional:
    - dea.reference-architectures
    - dea.architecture-principles
```

---

# 8. Execution Workflow

The Architecture Vision Skill follows this workflow.

1. Review business objectives.
2. Review engineering requirements.
3. Identify architectural priorities.
4. Define architecture principles.
5. Define quality attribute priorities.
6. Establish technical direction.
7. Validate alignment with business goals.
8. Produce the Architecture Vision.

---

# 9. Engineering Guidelines

The Architecture Vision should:

* remain technology independent whenever possible;
* align with Product Vision;
* support business objectives;
* prioritize quality attributes;
* define architectural principles;
* guide future engineering decisions.

The Architecture Vision should avoid implementation details.

Specific architectural models belong to subsequent Architecture Engineering skills.

---

# 10. Architecture Vision Contents

The Architecture Vision should include:

* Architecture Purpose
* Architecture Goals
* Architecture Scope
* Architectural Principles
* Quality Attribute Priorities
* Technical Strategy
* Constraints Summary
* Expected Outcomes

---

# 11. Validation

Before completion the skill verifies:

* architectural objectives are defined;
* business alignment exists;
* quality priorities are documented;
* architectural principles are consistent;
* implementation details have been avoided.

---

# 12. Dependencies

### Parent Skill

* DSK-1100 Architecture Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Architecture Vision Skill commonly collaborates with:

* Architecture Drivers
* Architecture Constraints
* Domain Modeling
* Context Modeling
* Architecture Review

The Architecture Vision serves as the strategic reference for all subsequent architectural activities.

---

# 14. Expected Outcomes

After execution, the Architecture Vision should provide:

* a clearly defined architectural direction;
* documented architectural principles;
* alignment between business and architecture;
* prioritized quality attributes;
* a consistent foundation for architectural design;
* guidance for subsequent architecture decisions.

The Architecture Vision Skill establishes the strategic architectural direction of the software product, ensuring that all future architectural decisions remain aligned with business objectives and the engineering standards defined by DESys.
