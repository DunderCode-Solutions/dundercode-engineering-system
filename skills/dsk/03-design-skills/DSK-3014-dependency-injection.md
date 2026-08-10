---
metadata_schema: 1.0.0
document_id: DSK-3014
canonical_id: dsk.design.dependency-injection
title: Dependency Injection
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-3014 | Dependency Injection

# 1. Purpose

This skill defines the Dependency Engineering model adopted by the DunderCode Engineering System (DESys).

Dependency Injection (DI) is the implementation mechanism used to materialize dependency relationships previously defined during software design.

Within DESys, Dependency Injection is not an architectural pattern, framework feature or programming technique.

It is the engineering process responsible for managing software dependencies while preserving abstraction, modularity, maintainability and architectural integrity.

---

# 2. Scope

This specification governs:

* Dependency Engineering
* Dependency Modeling
* Dependency Resolution
* Dependency Ownership
* Dependency Lifetime
* Injection Strategies
* Dependency Validation
* Dependency Traceability

---

# 3. Engineering Position

Dependency Injection is the final step of Dependency Engineering.

The engineering workflow is:

```text
Business

↓

Domain Model

↓

Architecture

↓

Object Model

↓

Dependency Model

↓

Dependency Resolution

↓

Dependency Injection

↓

Implementation
```

Software dependencies SHALL be engineered before they are injected.

---

# 4. Engineering Objectives

Dependency Engineering aims to:

* minimize coupling;
* maximize modularity;
* preserve abstractions;
* improve maintainability;
* improve testability;
* support software evolution;
* preserve architectural consistency.

---

# 5. Dependency Model

Every dependency SHALL explicitly define:

* Consumer
* Abstraction
* Provider
* Owner
* Lifetime
* Resolution Strategy
* Scope

Example:

```yaml
dependency:

  consumer:

    OrderService

  abstraction:

    IRepository

  provider:

    PostgresRepository

  owner:

    Application Layer

  lifetime:

    Singleton

  scope:

    Request
```

---

# 6. Dependency Resolution

Every dependency SHALL define how it is resolved.

Typical resolution mechanisms include:

* Constructor Injection
* Method Injection
* Factory Resolution
* Composition Root

Dependency Resolution SHALL remain independent of framework implementation.

---

# 7. Injection Strategies

DESys recognizes three injection strategies.

## Constructor Injection

Preferred.

Dependencies are fully initialized during object creation.

---

## Method Injection

Accepted when dependencies are operation-specific.

---

## Property Injection

Discouraged.

Property Injection SHOULD only be used when required by framework constraints.

---

# 8. Dependency Ownership

Every dependency SHALL have a single owner.

Ownership defines:

* who creates the dependency;
* who controls its lifecycle;
* who disposes of it.

Multiple ownership SHALL be avoided.

---

# 9. Dependency Lifetime

Every dependency SHALL define its lifecycle.

Typical lifetimes include:

* Singleton
* Scoped
* Transient
* Pooled

Lifetime decisions SHALL be explicitly documented.

---

# 10. Dependency Resolution Matrix (DRM)

Every dependency SHALL produce a Dependency Resolution Matrix.

Example:

```yaml
dependency:

  consumer:

    OrderService

  abstraction:

    IRepository

  provider:

    PostgresRepository

  resolution:

    Constructor Injection

  owner:

    Application Layer

  lifetime:

    Scoped
```

The DRM becomes part of the Engineering Knowledge Base.

---

# 11. Dependency Lifecycle Graph (DLG)

DESys represents dependency lifecycles as a semantic graph.

Example:

```text
Application

↓

creates

↓

OrderService

↓

owns

↓

Repository

↓

owns

↓

Database Connection

↓

disposed_by

↓

Pool
```

The DLG supports:

* lifecycle reasoning;
* ownership analysis;
* dependency validation;
* impact analysis;
* AI context retrieval.

---

# 12. Engineering Rules

Dependencies MUST:

* depend on abstractions whenever possible;
* preserve architectural boundaries;
* define ownership;
* define lifetime;
* define resolution strategy.

Dependencies MUST NOT:

* introduce cyclic dependencies;
* instantiate collaborators internally when external resolution is appropriate;
* hide dependency relationships;
* violate architectural layering.

---

# 13. Dependency Anti-patterns

DESys explicitly discourages:

* Service Locator
* Hidden Dependencies
* Static Singletons
* Runtime Lookup
* Circular Dependencies
* Multiple Ownership
* Temporal Coupling
* Global Dependency Containers

These anti-patterns reduce software maintainability and engineering transparency.

---

# 14. Inputs

Typical inputs include:

* Object Model
* Design Patterns
* Architecture Documentation
* Dependency Requirements

---

# 15. Outputs

Typical deliverables include:

* Dependency Model
* Dependency Resolution Matrix
* Dependency Lifecycle Graph
* Dependency Validation Report
* Dependency Traceability

---

# 16. Execution Workflow

1. Review software structure.
2. Identify dependency relationships.
3. Separate abstractions from implementations.
4. Define ownership.
5. Define lifecycle.
6. Select resolution strategy.
7. Build the Dependency Resolution Matrix.
8. Build the Dependency Lifecycle Graph.
9. Validate dependency consistency.

---

# 17. Validation

Before completion the skill verifies:

* dependencies remain explicit;
* abstractions are respected;
* ownership is unique;
* lifecycles are documented;
* dependency cycles are absent;
* engineering traceability is preserved.

---

# 18. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3010 Design Principles
* DSK-3011 SOLID Principles
* DSK-3012 Object-Oriented Design
* DSK-3013 Design Patterns

---

# 19. Collaboration

The Dependency Injection Skill collaborates with:

* Package Organization
* Modularity
* Refactoring
* Architecture Engineering
* Software Construction

Dependency Engineering connects software components while preserving abstraction, ownership and architectural consistency.

---

# 20. Expected Outcomes

After execution, the Dependency Injection Skill should provide:

* explicit dependency models;
* abstraction-oriented software structures;
* documented dependency ownership;
* well-defined dependency lifecycles;
* reusable dependency engineering artifacts;
* semantic dependency graphs;
* complete engineering traceability.

The Dependency Injection Skill establishes the Dependency Engineering model of DESys by ensuring that software dependencies are explicitly modeled, resolved, governed and documented before implementation, enabling maintainable, testable and architecture-compliant software systems throughout the engineering lifecycle.
