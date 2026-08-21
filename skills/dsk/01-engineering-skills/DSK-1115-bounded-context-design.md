---
metadata_schema: 1.0.0
document_id: DSK-1115
canonical_id: dsk.engineering.architecture.bounded-context-design
title: Bounded Context Design
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1115 | Bounded Context Design

# 1. Purpose

This skill defines how AI agents identify, design and document Bounded Contexts within the DunderCode Engineering System (DESys).

Bounded Context Design partitions the business domain into cohesive, autonomous contexts with explicit boundaries, responsibilities and business semantics.

Each Bounded Context represents a consistent business model with its own ubiquitous language and ownership.

---

# 2. Scope

This skill supports:

* Bounded Context Identification
* Context Boundary Definition
* Domain Partitioning
* Context Responsibility Definition
* Context Relationship Modeling
* Context Ownership
* Context Review

---

# 3. Skill Objectives

The Bounded Context Design Skill aims to:

* partition large domains into cohesive contexts;
* minimize coupling;
* maximize business cohesion;
* define ownership boundaries;
* establish clear responsibilities;
* prepare the architecture for scalable evolution.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify bounded contexts;
* partition the business domain;
* design domain boundaries;
* organize business capabilities;
* prepare modular architecture.

This skill normally executes after Context Modeling.

---

# 5. Inputs

Typical inputs include:

* Domain Model
* Context Model
* Business Rules
* Functional Requirements
* Architecture Vision
* Architecture Drivers
* Architecture Constraints

Missing business knowledge should trigger clarification before context partitioning begins.

---

# 6. Outputs

Typical deliverables include:

* Bounded Context Catalog
* Context Responsibilities
* Context Relationships
* Context Ownership
* Context Dependency Map
* Context Review Report

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
    - dea.domain-driven-design
    - dea.context-mapping
```

---

# 8. Execution Workflow

The Bounded Context Design Skill follows this workflow.

1. Review Domain Model.
2. Review Context Model.
3. Identify business capabilities.
4. Group related concepts.
5. Define Bounded Contexts.
6. Identify context ownership.
7. Define context relationships.
8. Validate cohesion and coupling.
9. Produce the Bounded Context Model.

---

# 9. Engineering Guidelines

Each Bounded Context should:

* represent a cohesive business capability;
* own its business terminology;
* minimize dependencies on other contexts;
* maximize internal cohesion;
* maintain explicit boundaries;
* preserve engineering traceability.

A Bounded Context should never be created based solely on technical considerations.

Business capability is the primary partitioning criterion.

---

# 10. Context Components

Each Bounded Context may include:

* Name
* Purpose
* Business Capability
* Owned Entities
* Owned Value Objects
* Domain Services
* Domain Events
* External Dependencies
* Upstream Contexts
* Downstream Contexts

---

# 11. Context Relationships

Relationships between contexts should be explicitly documented.

Typical relationship patterns include:

* Partnership
* Customer–Supplier
* Conformist
* Shared Kernel
* Open Host Service
* Published Language
* Anti-Corruption Layer

Projects may adopt only the patterns appropriate to their architectural style.

---

# 12. Validation

Before completion the skill verifies:

* every business concept belongs to a context;
* responsibilities are explicit;
* ownership is defined;
* excessive coupling is avoided;
* context boundaries are clear;
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

The Bounded Context Design Skill commonly collaborates with:

* Domain Modeling
* Context Modeling
* Container Architecture
* Integration Architecture
* Architecture Decision Records (ADR)

The Bounded Context Model establishes the organizational structure of the business domain and provides the foundation for subsequent architectural decomposition.

---

# 15. Expected Outcomes

After execution, the Bounded Context Model should provide:

* cohesive business partitions;
* explicit ownership boundaries;
* reduced architectural coupling;
* improved scalability;
* independent business evolution;
* a reliable foundation for containers, integrations and implementation.

The Bounded Context Design Skill transforms the conceptual business domain into autonomous business contexts, enabling modular architecture, clearer ownership and long-term maintainability throughout the DESys engineering lifecycle.
