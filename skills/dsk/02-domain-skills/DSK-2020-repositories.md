---
metadata_schema: 1.0.0
document_id: DSK-2020
canonical_id: dsk.domain.repositories
title: Repositories
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-2020 | Repositories

# 1. Purpose

This skill defines how AI agents identify, model and document Repositories within the DunderCode Engineering System (DESys).

Repositories provide the domain-facing abstraction responsible for retrieving and persisting Aggregates while hiding persistence mechanisms from the domain model.

They expose collection-like interfaces that operate exclusively on Aggregate Roots and preserve domain purity.

---

# 2. Scope

This skill supports:

* Repository Identification
* Aggregate Persistence Contracts
* Repository Interfaces
* Domain Persistence Modeling
* Repository Documentation
* Repository Governance

---

# 3. Skill Objectives

The Repositories Skill aims to:

* identify Aggregate persistence needs;
* define repository contracts;
* isolate persistence concerns;
* preserve domain independence;
* improve maintainability;
* strengthen architectural consistency.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define repositories;
* model persistence abstractions;
* organize Aggregate access;
* specify repository contracts;
* prepare domain persistence.

This skill normally executes after Aggregates.

---

# 5. Inputs

Typical inputs include:

* Aggregates
* Aggregate Roots
* Business Rules
* Domain Services
* Domain Events
* Ubiquitous Language

Repositories should be created only for Aggregate Roots.

---

# 6. Outputs

Typical deliverables include:

* Repository Catalog
* Repository Interfaces
* Repository Responsibilities
* Aggregate Persistence Map
* Repository Contracts

---

# 7. Required Knowledge

### Required

```yaml id="repok01"
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml id="repok02"
knowledge:
  optional:
    - dea.clean-architecture
    - dea.hexagonal-architecture
```

---

# 8. Execution Workflow

1. Review Aggregate Roots.
2. Identify persistence requirements.
3. Define repository responsibilities.
4. Specify repository operations.
5. Validate Aggregate ownership.
6. Review repository cohesion.
7. Validate with architects.
8. Publish the Repository Catalog.

---

# 9. Engineering Guidelines

Repositories should:

* manage Aggregate Roots only;
* expose business-oriented operations;
* remain independent of persistence technology;
* avoid business logic;
* avoid infrastructure implementation details;
* preserve engineering traceability.

Repositories represent domain collections rather than database access layers.

---

# 10. Repository Structure

Each Repository should include:

* Identifier
* Repository Name
* Aggregate Root
* Responsibilities
* Supported Operations
* Query Intent
* Business Constraints
* Related Aggregates
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* repositories manage only Aggregate Roots;
* persistence details are abstracted;
* operations are business-oriented;
* business logic is excluded;
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

The Repositories Skill commonly collaborates with:

* Aggregates
* Specifications
* Factories
* Architecture Engineering
* Infrastructure Architecture

Repositories define the domain contract that infrastructure implementations must satisfy while keeping the domain model isolated from technical persistence concerns.

---

# 14. Expected Outcomes

After execution, the Repositories should provide:

* clear persistence abstractions;
* Aggregate-oriented repository interfaces;
* technology-independent contracts;
* improved domain isolation;
* stronger architectural consistency;
* complete engineering traceability.

The Repositories Skill establishes the persistence abstraction layer of the DESys domain model, ensuring that Aggregate lifecycle management remains independent of infrastructure technologies while preserving the integrity of the domain throughout the software engineering lifecycle.
