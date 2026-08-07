# DSK-3016 | API Design

## Metadata

**Document Number:** DSK-3016

**Canonical ID:** dsk.design.api-design

**Engineering Domain:** Design Engineering

**Engineering Discipline:** Service Engineering

**Document Class:** Engineering Skill

**Version:** 2.0.0

**Status:** Canonical

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines the **Service Engineering** methodology adopted by the DunderCode Engineering System (DESys).

Within DESys, an API is not the primary engineering artifact.

The primary engineering artifact is the **Service Contract**.

A Service Contract models an externally consumable business capability.

API technologies (REST, GraphQL, gRPC, Events, SDKs, CLI, etc.) are transport-specific projections derived from the Service Contract.

---

# 2. Scope

This specification governs:

* Service Engineering
* Service Contracts
* API Projections
* Service Registry
* Service Evolution
* Service Compatibility
* Service Governance
* Service Traceability

---

# 3. Engineering Position

Service Engineering transforms business capabilities into reusable integration services.

```text
Business Capability
        ↓
Application Service
        ↓
Service Contract
        ↓
API Projection
        ↓
Transport Technology
        ↓
Runtime Implementation
```

DESys adopts a **Contract-First Service Engineering** approach.

Service Contracts SHALL exist before API implementations.

---

# 4. Engineering Principles

Service Engineering SHALL:

* expose business capabilities;
* preserve ubiquitous language;
* remain protocol-independent;
* maximize interoperability;
* minimize transport coupling;
* support long-term evolution.

---

# 5. Service Contract Model

Every Service Contract SHALL define:

* Canonical Identifier
* Service Name
* Business Capability
* Purpose
* Operations
* Request Contracts
* Response Contracts
* Published Events
* Error Contracts
* Version
* Compatibility
* Ownership

Service Contracts SHALL never contain transport-specific details.

---

# 6. API Projection Model

API Projections are realizations of Service Contracts.

Supported projections include:

* REST
* GraphQL
* gRPC
* Event Streaming
* Message Bus
* CLI
* SDK

Multiple API Projections MAY expose the same Service Contract.

All projections SHALL preserve semantic consistency.

---

# 7. API Contract Matrix (ACM)

Every Service Contract SHALL produce an API Contract Matrix.

Example:

```yaml
service:

  CustomerService

operation:

  createCustomer

projection:

  REST

request:

  CustomerRequest

response:

  CustomerResponse

events:

  CustomerCreated

version:

  v1
```

The API Contract Matrix documents the mapping between service operations and transport-specific projections.

---

# 8. Service Registry (SR)

All Service Contracts SHALL be maintained within the DESys Service Registry.

The Service Registry SHALL contain:

* Canonical Identifier
* Service Owner
* Current Version
* Compatibility Status
* API Projections
* Consumers
* Providers
* Published Events
* Traceability References

The Service Registry becomes the canonical catalog of externally exposed services.

---

# 9. Service Knowledge Graph (SKG)

DESys represents services through a semantic Service Knowledge Graph.

Example:

```text
CustomerService
        │ exposes
        ▼
createCustomer
        │ consumes
        ▼
CustomerRequest
        │ returns
        ▼
CustomerResponse
        │ publishes
        ▼
CustomerCreated
```

The Service Knowledge Graph enables:

* service discovery;
* dependency analysis;
* impact analysis;
* semantic navigation;
* AI reasoning;
* contextual retrieval.

---

# 10. Service Evolution

Service Contracts evolve independently of transport technologies.

Compatible changes preserve interoperability.

Breaking changes SHALL increment the major version.

```text
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

# 11. Engineering Rules

Service Contracts MUST:

* expose business capabilities;
* remain transport-independent;
* preserve domain semantics;
* remain cohesive;
* evolve predictably.

API Projections MUST:

* implement the Service Contract faithfully;
* preserve compatibility rules;
* avoid introducing business behavior.

---

# 12. Anti-patterns

DESys explicitly discourages:

* RPC over REST
* Transport-Oriented Design
* God APIs
* Leaky DTOs
* Hidden Versioning
* Verb-Based Resources
* Inconsistent Error Models
* Business Logic in Transport Layer

---

# 13. Inputs

Typical inputs include:

* Business Capabilities
* Use Cases
* Domain Model
* Software Contracts
* Architecture Documentation

---

# 14. Outputs

Typical deliverables include:

* Service Contracts
* API Contract Matrix
* Service Registry
* Service Knowledge Graph
* Compatibility Report
* API Documentation
* Engineering Traceability

---

# 15. Execution Workflow

1. Identify business capability.
2. Define application service.
3. Model the Service Contract.
4. Define operations.
5. Define request and response contracts.
6. Define event contracts.
7. Generate API Projections.
8. Update the Service Registry.
9. Update the Service Knowledge Graph.
10. Validate engineering consistency.

---

# 16. Validation

Before completion the skill verifies:

* business capabilities remain explicit;
* Service Contracts remain protocol-independent;
* API Projections preserve semantics;
* compatibility is documented;
* ownership is defined;
* engineering traceability is complete.

---

# 17. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3015 Interface Design

---

# 18. Collaboration

The API Design Skill collaborates with:

* Architecture Engineering
* Integration Engineering
* Security Engineering
* Event Engineering
* Software Construction

Service Engineering provides the canonical external collaboration model adopted by DESys.

---

# 19. Expected Outcomes

After execution, the API Design Skill should provide:

* explicit Service Contracts;
* protocol-independent service definitions;
* governed API Projections;
* reusable service capabilities;
* semantic service knowledge;
* complete engineering traceability.

Service Contracts become the canonical representation of externally exposed business capabilities, while API Projections provide protocol-specific realizations that remain versioned, governed, semantically consistent and fully traceable throughout the entire software engineering lifecycle.
