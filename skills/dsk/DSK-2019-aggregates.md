# DSK-2019 | Aggregates

## Metadata

Document Number: DSK-2019

Canonical ID: dsk.domain.aggregates

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, model and document Aggregates within the DunderCode Engineering System (DESys).

Aggregates establish consistency boundaries within the domain model by grouping related Entities and Value Objects under a single Aggregate Root responsible for enforcing business invariants.

They ensure that business consistency is preserved while enabling scalable and maintainable domain models.

---

# 2. Scope

This skill supports:

* Aggregate Identification
* Aggregate Root Definition
* Consistency Boundary Modeling
* Business Invariant Protection
* Aggregate Documentation
* Domain Consistency

---

# 3. Skill Objectives

The Aggregates Skill aims to:

* identify aggregate boundaries;
* define Aggregate Roots;
* protect business invariants;
* organize related domain concepts;
* improve consistency;
* support scalable domain modeling.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify aggregates;
* organize domain consistency;
* define Aggregate Roots;
* model transactional boundaries;
* improve domain integrity.

This skill normally executes after Value Objects.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Domain Services
* Value Objects
* Business Rules
* Domain Events
* Ubiquitous Language

Aggregate boundaries should be driven by business consistency requirements rather than database structure.

---

# 6. Outputs

Typical deliverables include:

* Aggregate Catalog
* Aggregate Root Definitions
* Consistency Boundaries
* Aggregate Relationships
* Invariant Documentation

---

# 7. Required Knowledge

### Required

```yaml id="aggk01"
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml id="aggk02"
knowledge:
  optional:
    - dea.domain-modeling
    - dea.software-design
```

---

# 8. Execution Workflow

1. Review Entities and Value Objects.
2. Identify business consistency requirements.
3. Define Aggregate boundaries.
4. Select the Aggregate Root.
5. Identify protected invariants.
6. Define relationships with other Aggregates.
7. Validate with domain experts.
8. Publish the Aggregate Catalog.

---

# 9. Engineering Guidelines

Aggregates should:

* protect business invariants;
* expose a single Aggregate Root;
* minimize boundary size;
* avoid unnecessary coupling;
* remain independent of persistence technology;
* preserve engineering traceability.

Aggregate boundaries should reflect transactional consistency, not implementation convenience.

---

# 10. Aggregate Structure

Each Aggregate should include:

* Identifier
* Aggregate Name
* Aggregate Root
* Business Purpose
* Internal Entities
* Value Objects
* Business Invariants
* Related Domain Events
* External Relationships
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* exactly one Aggregate Root exists;
* business invariants are protected;
* consistency boundaries are explicit;
* aggregate responsibilities are cohesive;
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

The Aggregates Skill commonly collaborates with:

* Value Objects
* Repositories
* Specifications
* Domain Services
* Architecture Engineering

Aggregates provide the structural consistency model that supports persistence, transactional integrity and domain evolution while remaining independent of infrastructure concerns.

---

# 14. Expected Outcomes

After execution, the Aggregates should provide:

* clearly defined consistency boundaries;
* explicit Aggregate Roots;
* protected business invariants;
* cohesive domain structures;
* improved scalability of the domain model;
* complete engineering traceability.

The Aggregates Skill establishes the consistency structure of the DESys domain model, ensuring that related business concepts evolve together under explicit business rules while preserving domain integrity throughout the software engineering lifecycle.
