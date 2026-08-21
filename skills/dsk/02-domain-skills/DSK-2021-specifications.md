---
metadata_schema: 1.0.0
document_id: DSK-2021
canonical_id: dsk.domain.specifications
title: Specifications
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-2021 | Specifications

# 1. Purpose

This skill defines how AI agents identify, model and document Specifications within the DunderCode Engineering System (DESys).

Specifications encapsulate reusable business predicates that determine whether domain objects satisfy specific business conditions.

They centralize business decision logic, improve expressiveness and support reusable domain rules without introducing duplication.

---

# 2. Scope

This skill supports:

* Business Predicate Modeling
* Eligibility Rules
* Validation Rules
* Decision Criteria
* Specification Composition
* Domain Rule Documentation

---

# 3. Skill Objectives

The Specifications Skill aims to:

* identify reusable business conditions;
* centralize business predicates;
* improve domain expressiveness;
* reduce duplicated decision logic;
* support composable business rules;
* strengthen domain consistency.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define business conditions;
* model decision rules;
* identify reusable predicates;
* organize validation logic;
* improve domain rule reuse.

This skill normally executes after Repositories.

---

# 5. Inputs

Typical inputs include:

* Business Rules
* Domain Services
* Aggregates
* Repositories
* Business Processes
* Domain Events

Specifications should represent reusable business conditions rather than executable workflows.

---

# 6. Outputs

Typical deliverables include:

* Specification Catalog
* Business Predicate Definitions
* Composition Rules
* Validation Criteria
* Specification Relationships

---

# 7. Required Knowledge

### Required

```yaml id="speck01"
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml id="speck02"
knowledge:
  optional:
    - dea.software-design
    - dea.clean-architecture
```

---

# 8. Execution Workflow

1. Review business rules.
2. Identify reusable predicates.
3. Define individual Specifications.
4. Identify composition opportunities.
5. Document business meaning.
6. Validate with domain experts.
7. Review reuse potential.
8. Publish the Specification Catalog.

---

# 9. Engineering Guidelines

Specifications should:

* represent business predicates;
* remain reusable;
* avoid infrastructure concerns;
* support logical composition (AND, OR, NOT);
* express business intent clearly;
* preserve engineering traceability.

Specifications answer **whether** a business condition is satisfied, not **how** a business operation is executed.

---

# 10. Specification Structure

Each Specification should include:

* Identifier
* Specification Name
* Business Meaning
* Evaluation Criteria
* Related Business Rules
* Related Aggregates
* Composition Rules
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* predicates represent business concepts;
* specifications are reusable;
* business meaning is explicit;
* logical composition is documented when applicable;
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

The Specifications Skill commonly collaborates with:

* Repositories
* Domain Services
* Policies
* Aggregates
* Requirements Engineering

Specifications provide reusable business decision logic that can be applied consistently across the domain model while remaining independent of infrastructure and application concerns.

---

# 14. Expected Outcomes

After execution, the Specifications should provide:

* reusable business predicates;
* centralized decision criteria;
* improved domain readability;
* composable business rules;
* reduced duplication of validation logic;
* complete engineering traceability.

The Specifications Skill establishes the reusable decision layer of the DESys domain model, ensuring that business conditions remain explicit, composable and consistently applied throughout the software engineering lifecycle.
