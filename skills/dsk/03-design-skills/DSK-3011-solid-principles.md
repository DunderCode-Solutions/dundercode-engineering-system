# DSK-3011 | SOLID Principles

## Metadata

**Document Number:** DSK-3011

**Canonical ID:** dsk.design.solid-principles

**Document Class:** Engineering Skill

**Version:** 1.0.0

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents apply the SOLID Principles within the DunderCode Engineering System (DESys).

SOLID is the primary object-oriented design framework adopted by DESys to produce software that is maintainable, extensible, testable and resilient to change.

It operationalizes the Design Principles established by DSK-3010 and provides practical guidance for designing software components while preserving architectural boundaries and domain integrity.

---

# 2. Scope

This skill governs:

* Object-Oriented Design
* Class Responsibilities
* Interface Design
* Dependency Management
* Extensibility
* Maintainability
* Testability
* Refactoring Guidance

---

# 3. Relationship with Design Principles

Design Principles define **how engineers should think**.

SOLID defines **how object-oriented software should be structured**.

```text
Design Principles
        ↓
SOLID
        ↓
Object-Oriented Design
        ↓
Design Patterns
        ↓
Dependency Injection
```

SOLID complements, but does not replace, the Design Principles.

---

# 4. Objectives

The SOLID Principles aim to:

* improve maintainability;
* reduce coupling;
* increase cohesion;
* support extensibility;
* improve testability;
* reduce technical debt;
* preserve architectural integrity.

---

# 5. SOLID Principles

## Single Responsibility Principle (SRP)

Every software component should have a single primary responsibility and a single reason to change.

---

## Open/Closed Principle (OCP)

Software should be open for extension while remaining closed for modification.

---

## Liskov Substitution Principle (LSP)

Derived types must remain behaviorally compatible with their base types.

---

## Interface Segregation Principle (ISP)

Clients should depend only on the interfaces they actually require.

---

## Dependency Inversion Principle (DIP)

High-level policies should depend upon abstractions rather than concrete implementations.

---

# 6. Inputs

Typical inputs include:

* Design Principles
* Architecture Documentation
* Domain Model
* Existing Software Design
* Engineering Standards

---

# 7. Outputs

Typical deliverables include:

* SOLID Assessment
* Refactoring Recommendations
* Dependency Improvements
* Interface Improvements
* Design Quality Report

---

# 8. Required Knowledge

### Required

```yaml
knowledge:
  required:
    - des.design
    - des.engineering
```

### Optional

```yaml
knowledge:
  optional:
    - dea.clean-architecture
    - dea.object-oriented-design
```

---

# 9. Execution Workflow

1. Review software structure.
2. Evaluate responsibilities.
3. Evaluate extensibility.
4. Evaluate inheritance.
5. Evaluate interfaces.
6. Evaluate dependency direction.
7. Identify violations.
8. Produce recommendations.

---

# 10. SOLID Trade-offs

SOLID principles should not be applied mechanically.

Typical engineering trade-offs include:

| Principle | Possible Trade-off                   |
| --------- | ------------------------------------ |
| SRP       | Excessive class fragmentation        |
| OCP       | Over-engineering through abstraction |
| LSP       | Complex inheritance hierarchies      |
| ISP       | Too many small interfaces            |
| DIP       | Unnecessary abstraction layers       |

Engineering decisions should balance maintainability, simplicity and business value.

---

# 11. Engineering Guidelines

Software designed under DESys should:

* prioritize readability;
* avoid unnecessary abstraction;
* minimize coupling;
* maximize cohesion;
* preserve architectural boundaries;
* express domain concepts clearly;
* remain easy to evolve.

SOLID exists to improve software quality—not to increase complexity.

---

# 12. Validation

Before completion the skill verifies:

* responsibilities remain cohesive;
* dependencies point toward abstractions where appropriate;
* interfaces remain focused;
* inheritance preserves behavior;
* extensibility does not introduce unnecessary complexity;
* architectural boundaries remain intact;
* engineering traceability is preserved.

---

# 13. Dependencies

### Parent Skill

* DSK-3000 Design Skills Overview

### Foundation Skills

* DSK-3010 Design Principles

---

# 14. Collaboration

The SOLID Principles Skill collaborates with:

* Object-Oriented Design
* Design Patterns
* Dependency Injection
* Refactoring
* Code Review
* Design Review

SOLID provides the object-oriented foundation upon which the remaining Design Skills are applied.

---

# 15. Expected Outcomes

After execution, the SOLID Principles should provide:

* cohesive software components;
* extensible software structures;
* improved dependency management;
* stronger maintainability;
* improved testability;
* reduced technical debt;
* consistent object-oriented design;
* complete engineering traceability.

The SOLID Principles Skill establishes the object-oriented design foundation of DESys, ensuring that software remains maintainable, adaptable and aligned with architectural decisions throughout the engineering lifecycle.
