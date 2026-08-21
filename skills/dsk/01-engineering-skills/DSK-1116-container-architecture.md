---
metadata_schema: 1.0.0
document_id: DSK-1116
canonical_id: dsk.engineering.architecture.component-architecture
title: Component Architecture
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1116 | Component Architecture

# 1. Purpose

This skill defines how AI agents design and document the high-level Component Architecture of a software system within the DunderCode Engineering System (DESys).

Component Architecture decomposes the solution into cohesive architectural components with clearly defined responsibilities, interfaces and dependencies.

It transforms business-oriented architectural models into an implementation-oriented structural view while remaining independent of specific technologies whenever possible.

---

# 2. Scope

This skill supports:

* Component Identification
* Component Decomposition
* Component Responsibility Definition
* Interface Definition
* Dependency Modeling
* Component Collaboration
* Architectural Layering
* Component Review

---

# 3. Skill Objectives

The Component Architecture Skill aims to:

* organize the software into cohesive components;
* reduce coupling between architectural elements;
* maximize cohesion within components;
* define explicit responsibilities;
* simplify future implementation;
* improve maintainability and scalability.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* design software components;
* decompose the architecture;
* organize application modules;
* define architectural layers;
* prepare implementation architecture.

This skill normally executes after Bounded Context Design.

---

# 5. Inputs

Typical inputs include:

* Domain Model
* Context Model
* Bounded Contexts
* Functional Requirements
* Non-Functional Requirements
* Architecture Vision
* Architecture Drivers
* Architecture Constraints

Missing architectural information should trigger clarification before component decomposition begins.

---

# 6. Outputs

Typical deliverables include:

* Component Architecture
* Component Catalog
* Component Responsibilities
* Component Interfaces
* Dependency Diagram
* Architectural Layers
* Component Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - dea.c4-model
    - dea.architecture-patterns
    - dea.component-design
```

---

# 8. Execution Workflow

The Component Architecture Skill follows this workflow.

1. Review Domain Model.
2. Review Context Model.
3. Review Bounded Contexts.
4. Identify architectural components.
5. Define component responsibilities.
6. Define public interfaces.
7. Define dependencies.
8. Validate cohesion and coupling.
9. Produce the Component Architecture.

---

# 9. Engineering Guidelines

Each architectural component should:

* have a single primary responsibility;
* expose explicit interfaces;
* minimize dependencies;
* maximize internal cohesion;
* remain independently understandable;
* preserve engineering traceability.

Component boundaries should be driven by business capabilities rather than implementation convenience.

---

# 10. Component Categories

Typical architectural components include:

* User Interface
* Application Services
* Domain Services
* Infrastructure Services
* Persistence Components
* Integration Components
* Messaging Components
* Authentication Components
* Reporting Components
* Background Processing Components

Projects may define additional component categories according to architectural style.

---

# 11. Component Structure

Each component should include:

* Identifier
* Name
* Description
* Responsibility
* Public Interfaces
* Consumed Interfaces
* Dependencies
* Related Requirements
* Related Bounded Context
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* every component has a clear responsibility;
* dependencies are explicit;
* circular dependencies are identified;
* interfaces are documented;
* cohesion is high;
* coupling is minimized;
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

The Component Architecture Skill commonly collaborates with:

* Bounded Context Design
* Integration Architecture
* Data Architecture
* Infrastructure Architecture
* Architecture Decision Records (ADR)

Component Architecture provides the structural decomposition required for implementation planning and technical design.

---

# 15. Expected Outcomes

After execution, the Component Architecture should provide:

* a modular architectural structure;
* explicit component responsibilities;
* well-defined interfaces;
* controlled dependencies;
* improved maintainability;
* a reliable foundation for software implementation.

The Component Architecture Skill transforms business-oriented architectural models into a cohesive structural architecture, enabling scalable implementation while preserving alignment with business capabilities and DESys engineering standards.
