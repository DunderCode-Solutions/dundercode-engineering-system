---
metadata_schema: 1.0.0
document_id: DSK-1118
canonical_id: dsk.engineering.architecture.integration-architecture
title: Integration Architecture
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1118 | Integration Architecture

# 1. Purpose

This skill defines how AI agents design and document the Integration Architecture of a software system within the DunderCode Engineering System (DESys).

Integration Architecture specifies how architectural containers, internal components and external systems exchange information through well-defined communication mechanisms, contracts and integration patterns.

It establishes the communication topology of the software ecosystem while preserving loose coupling, scalability and maintainability.

---

# 2. Scope

This skill supports:

* Internal Integration Design
* External System Integration
* API Architecture
* Event-Driven Architecture
* Messaging Architecture
* Communication Pattern Selection
* Integration Contract Definition
* Integration Review

---

# 3. Skill Objectives

The Integration Architecture Skill aims to:

* define communication strategies;
* minimize coupling;
* maximize interoperability;
* improve scalability;
* simplify future integrations;
* establish reliable communication patterns.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* design system integrations;
* create API architecture;
* model messaging;
* define communication protocols;
* integrate external systems;
* design distributed systems.

This skill normally executes after Component Architecture.

---

# 5. Inputs

Typical inputs include:

* Container Architecture
* Component Architecture
* Context Model
* Bounded Contexts
* Functional Requirements
* Non-Functional Requirements
* Architecture Drivers
* Architecture Constraints

---

# 6. Outputs

Typical deliverables include:

* Integration Architecture
* Communication Diagram
* API Catalog
* Event Catalog
* Messaging Topology
* Integration Contracts
* Integration Review Report

---

# 7. Required Knowledge

### Required

```yaml
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - dea.integration-patterns
    - dea.event-driven-architecture
    - dea.api-design
```

---

# 8. Execution Workflow

1. Review architectural containers.
2. Review architectural components.
3. Identify communication requirements.
4. Select communication patterns.
5. Define integration protocols.
6. Define contracts.
7. Validate architectural consistency.
8. Produce the Integration Architecture.

---

# 9. Engineering Guidelines

Integration Architecture should:

* minimize coupling;
* maximize autonomy;
* define explicit contracts;
* document communication protocols;
* support asynchronous communication when appropriate;
* preserve engineering traceability.

Communication should be driven by business capabilities rather than infrastructure preferences.

---

# 10. Supported Integration Patterns

Typical patterns include:

* REST
* GraphQL
* gRPC
* Webhooks
* Publish / Subscribe
* Event Streaming
* Message Queue
* API Gateway
* Saga
* CQRS
* Anti-Corruption Layer
* Shared Database (discouraged unless justified)

Projects may adopt only the patterns appropriate to their architecture.

---

# 11. Integration Structure

Each integration should include:

* Identifier
* Source
* Destination
* Communication Pattern
* Protocol
* Contract
* Authentication Method
* Error Handling Strategy
* Related Requirements
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* communication paths are documented;
* contracts are explicit;
* protocols are identified;
* unnecessary coupling is avoided;
* external dependencies are documented;
* engineering traceability is preserved.

---

# 13. Dependencies

### Parent Skill

* DSK-1100 Architecture Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 14. Collaboration

The Integration Architecture Skill commonly collaborates with:

* Container Architecture
* Component Architecture
* Data Architecture
* Infrastructure Architecture
* Architecture Decision Records (ADR)

The Integration Architecture defines how the software ecosystem exchanges information while preserving modularity and architectural consistency.

---

# 15. Expected Outcomes

After execution, the Integration Architecture should provide:

* documented communication topology;
* explicit integration contracts;
* reliable messaging strategies;
* scalable integration patterns;
* reduced architectural coupling;
* a solid foundation for distributed software implementation.

The Integration Architecture Skill establishes the communication backbone of the software architecture, ensuring that containers, components and external systems interact through well-defined, maintainable and scalable integration mechanisms throughout the DESys engineering lifecycle.
