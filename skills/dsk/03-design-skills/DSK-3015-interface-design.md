---
metadata_schema: 1.0.0
document_id: DSK-3015
canonical_id: dsk.design.interface-design
title: Interface Design
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Design Engineering
---

# DSK-3015 | Interface Design

# 1. Purpose

This skill defines the **Software Contract Engineering** model adopted by the DunderCode Engineering System (DESys).

Within DESys, interfaces are software contracts that formally define collaboration between independent software components.

A software contract specifies responsibilities, operations, constraints, compatibility and evolution while remaining completely independent from implementation details.

Software contracts are first-class engineering artifacts.

Implementations are merely realizations of those contracts.

---

# 2. Scope

This specification governs:

* Software Contract Engineering
* Contract Design
* Contract Modeling
* Contract Ownership
* Contract Lifecycle
* Contract Compatibility
* Contract Governance
* Contract Traceability

---

# 3. Engineering Position

Software Contracts represent the collaboration layer of the software architecture.

They separate responsibilities from implementations and establish stable communication boundaries between components.

```text id="contract-engineering-flow"
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

Software Contracts

↓

Implementations
```

DESys adopts **Contract-First Engineering**.

Software contracts SHALL exist before software implementations.

---

# 4. Engineering Objectives

Software Contract Engineering aims to:

* preserve abstraction;
* reduce coupling;
* maximize modularity;
* enable independent implementations;
* improve maintainability;
* support long-term evolution;
* strengthen engineering governance.

---

# 5. Software Contract Model

Every software contract SHALL explicitly define:

* Contract Identifier
* Contract Name
* Purpose
* Responsibilities
* Operations
* Inputs
* Outputs
* Preconditions
* Postconditions
* Invariants
* Version
* Stability
* Owner

Contracts define expected behavior.

They never define implementation.

---

# 6. Contract Ownership

Every software contract SHALL define ownership.

Ownership includes:

* Contract Owner
* Technical Maintainer
* Primary Providers
* Primary Consumers
* Version Owner

Ownership SHALL remain unique.

Ownership SHALL remain traceable.

---

# 7. Contract Lifecycle

Every software contract SHALL evolve through controlled lifecycle stages.

```text id="contract-lifecycle"
Draft

↓

Experimental

↓

Stable

↓

Deprecated

↓

Retired
```

Lifecycle transitions SHALL be documented.

---

# 8. Contract Compatibility

Every contract evolution SHALL classify changes as:

* Compatible
* Breaking

Compatible changes MAY preserve the current major version.

Breaking changes SHALL increment the major version.

Example:

```text id="contract-versioning"
v1

↓

Compatible

↓

v1.1

↓

Compatible

↓

v1.2

↓

Breaking

↓

v2
```

---

# 9. Interface Contract Matrix (ICM)

Every software contract SHALL produce an Interface Contract Matrix.

Example:

```yaml id="icm"
contract:

  identifier:

    CTR-001

  name:

    IRepository

  owner:

    Persistence Team

  providers:

    - PostgresRepository

  consumers:

    - OrderService

    - InvoiceService

  version:

    v1

  lifecycle:

    Stable

  compatibility:

    Compatible
```

The Interface Contract Matrix becomes part of the Engineering Knowledge Base.

---

# 10. Interface Knowledge Graph (IKG)

DESys represents software contracts through a semantic Interface Knowledge Graph.

Example:

```text id="ikg"
OrderService

↓

consumes

↓

IRepository

↑

implemented_by

↓

PostgresRepository
```

The Interface Knowledge Graph enables:

* semantic navigation;
* contract discovery;
* dependency analysis;
* impact analysis;
* engineering reasoning;
* AI context retrieval.

---

# 11. Contract Registry (CR)

All software contracts SHALL be registered within the DESys Contract Registry.

The Contract Registry maintains:

* Canonical Identifier
* Current Version
* Lifecycle Status
* Ownership
* Providers
* Consumers
* Compatibility History
* Traceability References

The Contract Registry becomes the authoritative source of software contracts throughout DESys.

---

# 12. Contract Quality Attributes

Every software contract SHOULD be:

* Cohesive
* Stable
* Minimal
* Predictable
* Discoverable
* Versionable
* Testable
* Backward Compatible whenever possible

Quality SHALL be continuously evaluated during software evolution.

---

# 13. Engineering Rules

Software contracts MUST:

* expose responsibilities only;
* preserve abstraction;
* hide implementation details;
* remain cohesive;
* remain stable;
* evolve predictably;
* support independent implementations.

Software contracts MUST NOT:

* expose implementation;
* become excessively broad;
* violate architectural boundaries;
* introduce cyclic contracts;
* depend on concrete implementations.

---

# 14. Contract Anti-patterns

DESys explicitly discourages:

* Fat Interfaces
* God Interfaces
* Marker Interfaces
* Leaky Contracts
* Chatty Interfaces
* Cyclic Contracts
* Implementation-Centric Contracts

These anti-patterns reduce software quality and engineering transparency.

---

# 15. Inputs

Typical inputs include:

* Object Model
* Dependency Model
* Architecture Documentation
* Business Requirements

---

# 16. Outputs

Typical deliverables include:

* Software Contracts
* Interface Contract Matrix
* Interface Knowledge Graph
* Contract Registry
* Compatibility Report
* Contract Documentation
* Engineering Traceability

---

# 17. Execution Workflow

1. Review collaboration boundaries.
2. Identify software contracts.
3. Define responsibilities.
4. Define ownership.
5. Define operations.
6. Define lifecycle.
7. Define compatibility.
8. Produce the Interface Contract Matrix.
9. Update the Contract Registry.
10. Update the Interface Knowledge Graph.
11. Validate engineering consistency.

---

# 18. Validation

Before completion the skill verifies:

* responsibilities remain cohesive;
* ownership is explicit;
* lifecycle is documented;
* compatibility is documented;
* abstraction is preserved;
* implementation remains hidden;
* engineering traceability is preserved.

---

# 19. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3010 Design Principles
* DSK-3011 SOLID Principles
* DSK-3012 Object-Oriented Design
* DSK-3013 Design Patterns
* DSK-3014 Dependency Injection

---

# 20. Collaboration

The Interface Design Skill collaborates with:

* API Design
* Package Organization
* Modularity
* Architecture Engineering
* Software Construction

Software Contract Engineering establishes the canonical collaboration model used throughout DESys.

---

# 21. Expected Outcomes

After execution, the Interface Design Skill should provide:

* explicit software contracts;
* stable collaboration boundaries;
* controlled contract evolution;
* documented ownership;
* semantic contract knowledge;
* reusable engineering contracts;
* governed contract registry;
* complete engineering traceability.

Software Contracts become the canonical collaboration mechanism of DESys, enabling AI agents, software components and engineering artifacts to communicate through explicit, versioned, semantically governed and fully traceable engineering agreements throughout the entire software engineering lifecycle.
