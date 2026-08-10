---
metadata_schema: 1.0.0
document_id: DSK-3010
canonical_id: dsk.design.design-principles
title: Design Principles
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-3010 | Design Principles

# 1. Purpose

This skill defines the fundamental Design Principles adopted by the DunderCode Engineering System (DESys).

Design Principles guide software design decisions by establishing universal engineering concepts that promote maintainability, readability, modularity and long-term software evolution.

They provide the conceptual foundation upon which all subsequent design techniques, patterns and implementation practices are built.

---

# 2. Scope

This skill supports:

* Software Design Principles
* Design Decision Guidance
* Maintainability
* Modularity
* Readability
* Abstraction
* Encapsulation
* Engineering Consistency

---

# 3. Skill Objectives

The Design Principles Skill aims to:

* establish a common design philosophy;
* guide software design decisions;
* improve maintainability;
* encourage modular thinking;
* reduce accidental complexity;
* preserve engineering consistency.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* software design guidance;
* design best practices;
* software structure recommendations;
* engineering design decisions;
* implementation planning.

This skill normally executes before all other Design Skills.

---

# 5. Design Principles

DESys adopts the following foundational design principles:

* Simplicity
* Separation of Concerns
* High Cohesion
* Low Coupling
* Encapsulation
* Abstraction
* Explicit Dependencies
* Composition over Inheritance
* Information Hiding
* Readability
* Maintainability
* Evolvability

These principles should guide every software design decision independently of programming language or framework.

---

# 6. Inputs

Typical inputs include:

* Architecture Documentation
* Domain Model
* Business Requirements
* Engineering Standards
* Existing Design Decisions

---

# 7. Outputs

Typical deliverables include:

* Design Guidelines
* Design Decision Criteria
* Design Recommendations
* Engineering Review Inputs

---

# 8. Required Knowledge

### Required

```yaml id="dpk01"
knowledge:
  required:
    - des.engineering
    - des.design
```

### Optional

```yaml id="dpk02"
knowledge:
  optional:
    - dea.clean-architecture
    - dea.software-design
```

---

# 9. Execution Workflow

1. Review business and architectural context.
2. Identify design concerns.
3. Apply appropriate design principles.
4. Evaluate trade-offs.
5. Validate consistency with architecture.
6. Document design rationale.
7. Review with engineering stakeholders.
8. Publish design recommendations.

---

# 10. Engineering Guidelines

Design decisions should:

* express the domain rather than obscure it;
* minimize unnecessary complexity;
* maximize cohesion;
* minimize coupling;
* favor explicitness over implicit behavior;
* remain understandable by future engineers;
* preserve engineering traceability.

Good software design should make correct solutions easier than incorrect ones.

---

# 11. Validation

Before completion the skill verifies:

* design decisions follow established principles;
* unnecessary complexity has been avoided;
* architectural boundaries remain intact;
* domain concepts remain explicit;
* engineering traceability is preserved.

---

# 12. Dependencies

### Parent Skill

* DSK-3000 Design Skills Overview

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Design Principles Skill collaborates with every Design Skill and provides the conceptual foundation for:

* SOLID Principles
* Object-Oriented Design
* Design Patterns
* Dependency Injection
* API Design
* Refactoring
* Design Review

All design techniques should remain consistent with these principles.

---

# 14. Expected Outcomes

After execution, the Design Principles should provide:

* consistent software design decisions;
* improved maintainability;
* modular software structures;
* reduced accidental complexity;
* stronger alignment between domain and implementation;
* complete engineering traceability.

The Design Principles Skill establishes the conceptual foundation of DESys Design Engineering, ensuring that software structures remain expressive, maintainable and aligned with both architectural decisions and business intent throughout the software engineering lifecycle.
