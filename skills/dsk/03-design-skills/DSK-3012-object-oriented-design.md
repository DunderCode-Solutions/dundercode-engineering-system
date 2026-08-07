# DSK-3012 | Object-Oriented Design

## Metadata

**Document Number:** DSK-3012

**Canonical ID:** dsk.design.object-oriented-design

**Document Class:** Engineering Skill

**Version:** 1.0.0

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines the engineering rules that AI agents MUST follow when constructing Object-Oriented software models inside DESys.

Object-Oriented Design is responsible for translating the Domain Model into implementation-ready software objects while preserving business semantics, architectural boundaries and engineering consistency.

Within DESys, software objects are engineering representations of domain concepts.

They are never created from technical convenience alone.

---

# 2. Scope

This specification governs:

* Object Modeling
* Responsibility Assignment
* Class Design
* Identity Modeling
* State Modeling
* Behavior Modeling
* Collaboration Modeling
* Composition
* Inheritance
* Polymorphism
* Object Lifecycle

---

# 3. Engineering Position

Object-Oriented Design does not create business behavior.

Business behavior originates in Domain Engineering.

OOD expresses that behavior through software objects.

```text id="ood01"
Business

↓

Domain Model

↓

Object Model

↓

Implementation
```

This separation is mandatory within DESys.

---

# 4. Engineering Objectives

Every Object Model produced by DESys should:

* faithfully represent business concepts;
* preserve ubiquitous language;
* maximize cohesion;
* minimize coupling;
* encapsulate business behavior;
* support maintainability;
* support future evolution.

---

# 5. Object Definition

Every software object MUST define:

* Identity
* Responsibilities
* State
* Behavior
* Collaborations
* Lifecycle
* Invariants
* Dependencies

Objects SHOULD represent one business concept.

Objects MUST NOT exist only to transport data.

---

# 6. Object Responsibility Matrix (ORMx)

Every object SHOULD be documented using the Object Responsibility Matrix.

Example:

```yaml id="ormx01"
object:

  name: Customer

  responsibilities:

    - Manage Customer Lifecycle

  owns:

    - Orders

  collaborates_with:

    - InvoiceService

  publishes:

    - CustomerCreated

  consumes:

    - CreditApproved

  invariants:

    - CreditLimit
```

ORMx becomes part of the Engineering Knowledge Base.

---

# 7. Object Collaboration

Software objects collaborate through explicit contracts.

Valid collaboration mechanisms include:

* Method Calls
* Interfaces
* Domain Events
* Domain Services
* Repositories

Objects SHOULD collaborate rather than manipulate each other's internal state.

---

# 8. Object Lifecycle Model (OLM)

Objects possessing meaningful lifecycle transitions SHOULD document their lifecycle.

Example:

```text id="olm01"
Created

↓

Active

↓

Suspended

↓

Archived
```

Lifecycle transitions SHOULD preserve domain invariants.

---

# 9. Inputs

Typical inputs include:

* Domain Model
* Aggregates
* Value Objects
* Domain Services
* Architecture Documentation
* SOLID Assessment

---

# 10. Outputs

Typical deliverables include:

* Object Model
* Object Responsibility Matrix
* Object Collaboration Graph
* Object Lifecycle Model
* Design Recommendations

---

# 11. Execution Workflow

1. Review the Domain Model.
2. Identify business concepts.
3. Create software objects.
4. Assign responsibilities.
5. Define collaborations.
6. Model lifecycle.
7. Validate object cohesion.
8. Publish the Object Model.

---

# 12. Engineering Rules

DESys adopts the following mandatory rules:

* every object MUST represent a domain concept;
* behavior MUST remain close to the state it manipulates;
* responsibilities MUST remain cohesive;
* collaborations SHOULD remain explicit;
* composition SHOULD be preferred over inheritance;
* inheritance MUST be justified;
* implementation details MUST remain encapsulated.

These rules apply independently of programming language.

---

# 13. Validation

Before completion the skill verifies:

* every object maps to a business concept;
* responsibilities remain cohesive;
* behavior is encapsulated;
* collaborations remain explicit;
* lifecycle preserves invariants;
* engineering traceability is preserved.

---

# 14. Dependencies

### Parent Skill

* DSK-3000 Design Skills Overview

### Foundation Skills

* DSK-3010 Design Principles
* DSK-3011 SOLID Principles

---

# 15. Collaboration

The Object-Oriented Design Skill collaborates with:

* Design Patterns
* Dependency Injection
* Refactoring
* Domain Engineering
* Architecture Engineering

OOD transforms business concepts into implementation-ready software structures.

---

# 16. Expected Outcomes

After execution, Object-Oriented Design should produce:

* expressive software objects;
* cohesive responsibilities;
* explicit collaborations;
* well-defined object lifecycles;
* maintainable software structures;
* implementation-ready object models;
* complete engineering traceability.

The Object-Oriented Design Skill establishes the canonical Object Model of DESys, ensuring that business concepts are consistently represented through cohesive software objects capable of evolving with both the business domain and the software architecture throughout the engineering lifecycle.
