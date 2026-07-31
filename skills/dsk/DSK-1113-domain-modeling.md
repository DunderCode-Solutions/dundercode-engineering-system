# DSK-1113 | Domain Modeling

## Metadata

Document Number: DSK-1113

Canonical ID: dsk.engineering.architecture.domain-modeling

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, analyze and model the business domain within the DunderCode Engineering System (DESys).

Domain Modeling captures the core business concepts independently of implementation technologies, providing a shared understanding between business stakeholders, architects and software engineers.

The resulting Domain Model becomes the semantic foundation of the software architecture.

---

# 2. Scope

This skill supports:

* Business Domain Analysis
* Domain Modeling
* Entity Identification
* Value Object Identification
* Aggregate Identification
* Domain Relationship Modeling
* Ubiquitous Language Definition
* Domain Review

---

# 3. Skill Objectives

The Domain Modeling Skill aims to:

* represent the business domain accurately;
* establish a shared business vocabulary;
* reduce conceptual ambiguity;
* separate business concepts from technical implementation;
* support architectural consistency;
* prepare subsequent architectural models.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* model the business domain;
* identify business entities;
* create a domain model;
* organize business concepts;
* prepare software architecture.

This skill normally executes after Architecture Constraints.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Business Rules
* User Stories
* Product Backlog
* Architecture Vision
* Architecture Drivers
* Architecture Constraints

Incomplete business knowledge should trigger clarification before domain modeling begins.

---

# 6. Outputs

Typical deliverables include:

* Domain Model
* Ubiquitous Language
* Business Entities
* Value Objects
* Aggregates
* Domain Relationships
* Domain Glossary
* Domain Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="53bhn9"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="4apc9v"
knowledge:
  optional:
    - dea.domain-driven-design
    - dea.business-modeling
```

---

# 8. Execution Workflow

The Domain Modeling Skill follows this workflow.

1. Review business context.
2. Review engineering requirements.
3. Identify business concepts.
4. Define ubiquitous language.
5. Identify entities.
6. Identify value objects.
7. Identify aggregates.
8. Identify domain relationships.
9. Validate conceptual consistency.
10. Produce the Domain Model.

---

# 9. Engineering Guidelines

The Domain Model should:

* represent business reality;
* avoid technical implementation details;
* preserve business terminology;
* remain technology independent;
* emphasize conceptual clarity;
* support long-term maintainability.

Business concepts should not be influenced by frameworks, databases or programming languages.

---

# 10. Domain Components

The Domain Model may include:

* Business Concepts
* Entities
* Value Objects
* Aggregates
* Domain Services
* Domain Events
* Business Relationships
* Business Terminology

Projects may adopt only the concepts appropriate to their architectural style.

---

# 11. Domain Artifact Structure

Each domain element should include:

* Identifier
* Name
* Business Description
* Business Responsibility
* Related Business Rules
* Related Requirements
* Relationships
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* business terminology is consistent;
* duplicate concepts do not exist;
* business relationships are documented;
* implementation details are absent;
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

The Domain Modeling Skill commonly collaborates with:

* Context Modeling
* Bounded Context Design
* Component Architecture
* Data Architecture
* Architecture Decision Records (ADR)

The Domain Model provides the conceptual foundation for all subsequent architectural models.

---

# 15. Expected Outcomes

After execution, the Domain Model should provide:

* a shared business vocabulary;
* clear business concepts;
* implementation-independent domain knowledge;
* consistent architectural terminology;
* improved communication between business and engineering;
* a reliable conceptual foundation for software architecture.

The Domain Modeling Skill establishes the semantic foundation of the software architecture, ensuring that all architectural models remain aligned with the real business domain and the engineering principles defined by DESys.
