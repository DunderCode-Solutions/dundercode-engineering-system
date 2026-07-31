# DSK-2017 | Domain Services

## Metadata

Document Number: DSK-2017

Canonical ID: dsk.domain.domain-services

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, model and document Domain Services within the DunderCode Engineering System (DESys).

Domain Services encapsulate business operations that represent important domain behavior but do not naturally belong to a single Entity or Value Object.

They coordinate domain concepts while preserving a rich and expressive domain model.

---

# 2. Scope

This skill supports:

* Domain Service Identification
* Business Rule Coordination
* Cross-Entity Operations
* Domain Behavior Modeling
* Service Documentation
* Domain Responsibility Allocation

---

# 3. Skill Objectives

The Domain Services Skill aims to:

* identify domain behaviors without a natural owner;
* preserve cohesive domain models;
* avoid misplaced business logic;
* coordinate multiple domain concepts;
* improve maintainability;
* strengthen business-oriented design.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify domain services;
* organize business behavior;
* model complex business rules;
* coordinate multiple domain entities;
* refine the domain model.

This skill normally executes after Domain Events.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Business Capabilities
* Business Processes
* Domain Events
* Business Rules
* Ubiquitous Language

Only behaviors that cannot be naturally assigned to a single Entity or Value Object should become Domain Services.

---

# 6. Outputs

Typical deliverables include:

* Domain Service Catalog
* Service Definitions
* Business Responsibility Map
* Service Relationships
* Domain Behavior Documentation

---

# 7. Required Knowledge

### Required

```yaml
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - dea.domain-modeling
    - dea.software-design
```

---

# 8. Execution Workflow

1. Review business rules.
2. Identify behaviors spanning multiple domain concepts.
3. Evaluate ownership within Entities and Value Objects.
4. Create Domain Services only when no natural owner exists.
5. Define service responsibilities.
6. Document service interactions.
7. Validate with domain experts.
8. Publish the Domain Service Catalog.

---

# 9. Engineering Guidelines

Domain Services should:

* represent meaningful business behavior;
* remain stateless whenever possible;
* avoid infrastructure concerns;
* avoid persistence responsibilities;
* coordinate domain concepts without replacing them;
* preserve engineering traceability.

Entities and Value Objects should own their intrinsic behavior. Domain Services should only coordinate behavior that belongs to the domain as a whole.

---

# 10. Service Structure

Each Domain Service should include:

* Identifier
* Service Name
* Business Purpose
* Responsibilities
* Related Business Rules
* Related Entities
* Related Value Objects
* Related Domain Events
* Inputs
* Outputs
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* the service represents domain behavior;
* no Entity or Value Object is a better owner;
* infrastructure concerns are excluded;
* responsibilities are cohesive;
* engineering traceability is preserved.

---

# 12. Dependencies

### Parent Skill

* DSK-2000 Domain Skills

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Domain Services Skill commonly collaborates with:

* Domain Events
* Value Objects
* Aggregates
* Specifications
* Architecture Engineering

Domain Services provide business coordination while allowing Entities and Value Objects to remain focused on their own responsibilities.

---

# 14. Expected Outcomes

After execution, the Domain Services should provide:

* clear allocation of business responsibilities;
* coordinated domain behavior;
* reduced business logic duplication;
* improved domain cohesion;
* maintainable domain models;
* complete engineering traceability.

The Domain Services Skill establishes the coordination layer of the DESys domain model, ensuring that complex business behaviors are modeled explicitly, remain independent of infrastructure concerns and preserve the integrity of the domain throughout the software engineering lifecycle.
