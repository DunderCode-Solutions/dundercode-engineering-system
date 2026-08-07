# DSK-1114 | Context Modeling

## Metadata

Document Number: DSK-1114

Canonical ID: dsk.engineering.architecture.context-modeling

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, model and document the operational context of a software system within the DunderCode Engineering System (DESys).

Context Modeling describes the environment in which the system operates, including external actors, external systems, organizational boundaries and major interactions.

It establishes the architectural context before internal software structures are designed.

---

# 2. Scope

This skill supports:

* System Context Modeling
* External Actor Identification
* External System Identification
* Boundary Definition
* Context Relationship Modeling
* Context Review
* C4 Level 1 Modeling

---

# 3. Skill Objectives

The Context Modeling Skill aims to:

* define system boundaries;
* identify external interactions;
* document ecosystem relationships;
* support architectural communication;
* reduce integration ambiguity;
* prepare internal architectural design.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* create a context diagram;
* model the software ecosystem;
* identify external systems;
* define system boundaries;
* prepare architecture documentation.

This skill normally executes after Domain Modeling.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Business Rules
* Domain Model
* Architecture Vision
* Architecture Drivers
* Architecture Constraints

Missing ecosystem information should trigger clarification before context modeling begins.

---

# 6. Outputs

Typical deliverables include:

* System Context Model
* External Actors
* External Systems
* System Boundaries
* Context Relationships
* Context Diagram
* Context Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="m84k2r"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="y8tb3x"
knowledge:
  optional:
    - dea.c4-model
    - dea.integration-patterns
```

---

# 8. Execution Workflow

The Context Modeling Skill follows this workflow.

1. Review business objectives.
2. Review Domain Model.
3. Identify system boundaries.
4. Identify users and actors.
5. Identify external systems.
6. Identify major interactions.
7. Validate context consistency.
8. Produce the Context Model.

---

# 9. Engineering Guidelines

The Context Model should:

* describe the software ecosystem;
* remain technology independent;
* identify only significant interactions;
* avoid internal implementation details;
* define clear system boundaries;
* preserve engineering traceability.

The Context Model should describe **who interacts with the system**, not **how the system is internally implemented**.

---

# 10. Context Components

The Context Model typically includes:

* Primary Actors
* Secondary Actors
* External Systems
* Organizational Boundaries
* System Under Design (SuD)
* High-Level Relationships
* Major Information Flows

Projects may extend the model according to organizational standards.

---

# 11. Context Element Structure

Each context element should include:

* Identifier
* Name
* Category
* Description
* Responsibilities
* Related Requirements
* Related Domain Concepts
* Relationships
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* system boundaries are explicit;
* all major actors are represented;
* external systems are documented;
* unnecessary implementation details are absent;
* engineering traceability is preserved.

---

# 13. Dependencies

### Parent Skill

* DSK-1100 Architecture Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 14. Collaboration

The Context Modeling Skill commonly collaborates with:

* Domain Modeling
* Bounded Context Design
* Integration Architecture
* Component Architecture
* Architecture Review

The Context Model establishes the external perspective of the software architecture and serves as the foundation for subsequent architectural decomposition.

---

# 15. Expected Outcomes

After execution, the Context Model should provide:

* clearly defined system boundaries;
* identified external actors;
* documented external systems;
* simplified architectural communication;
* improved integration planning;
* a reliable foundation for architectural decomposition.

The Context Modeling Skill establishes the external architectural view of the software system, enabling architects, developers and AI agents to understand the operational ecosystem before designing the internal software structure.
