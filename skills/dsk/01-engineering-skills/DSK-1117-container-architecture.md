---
metadata_schema: 1.0.0
document_id: DSK-1117
canonical_id: dsk.engineering.architecture.container-architecture
title: Container Architecture
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
architecture_model: C4 Model (Level 2)
---

# DSK-1117 | Container Architecture

# 1. Purpose

This skill defines how AI agents design and document the Container Architecture of a software system within the DunderCode Engineering System (DESys).

Container Architecture identifies the major executable applications, data stores and runtime services that compose the software solution.

Each container represents an independently deployable or executable unit with clearly defined responsibilities and interactions.

The resulting architecture corresponds to the C4 Model – Level 2 (Container Diagram).

---

# 2. Scope

This skill supports:

* Container Identification
* Runtime Architecture
* Deployment-Oriented Architecture
* Container Responsibilities
* Container Communication
* Container Dependencies
* Container Review
* C4 Level 2 Modeling

---

# 3. Skill Objectives

The Container Architecture Skill aims to:

* identify executable units;
* organize runtime responsibilities;
* define communication paths;
* simplify deployment planning;
* improve scalability;
* support implementation architecture.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* design application architecture;
* create container diagrams;
* organize runtime applications;
* define deployment architecture;
* prepare implementation architecture.

This skill normally executes after Bounded Context Design.

---

# 5. Inputs

Typical inputs include:

* Domain Model
* Context Model
* Bounded Contexts
* Functional Requirements
* Non-Functional Requirements
* Architecture Vision
* Architecture Drivers
* Architecture Constraints

---

# 6. Outputs

Typical deliverables include:

* Container Diagram
* Container Catalog
* Container Responsibilities
* Runtime Communication Model
* Technology Summary
* Container Review Report

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
    - dea.c4-model
    - dea.reference-architectures
    - dea.deployment-patterns
```

---

# 8. Execution Workflow

1. Review Context Model.
2. Review Bounded Contexts.
3. Identify executable applications.
4. Identify data stores.
5. Identify infrastructure services.
6. Define container responsibilities.
7. Define communication paths.
8. Validate runtime architecture.
9. Produce the Container Architecture.

---

# 9. Engineering Guidelines

Each container should:

* own a clear responsibility;
* expose explicit interfaces;
* communicate through defined protocols;
* minimize coupling;
* maximize cohesion;
* remain independently deployable whenever possible.

Containers should represent runtime applications rather than business concepts.

---

# 10. Typical Container Types

Typical containers include:

* Web Application
* REST API
* Mobile Application
* Desktop Application
* Worker
* Scheduler
* Authentication Service
* Notification Service
* Message Broker
* Database
* Cache
* File Storage
* Search Engine

Projects may define additional container types according to architectural needs.

---

# 11. Container Structure

Each container should include:

* Identifier
* Name
* Description
* Responsibility
* Technology
* Runtime
* Interfaces
* Dependencies
* Related Bounded Context
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* containers have explicit responsibilities;
* communication paths are documented;
* unnecessary coupling is minimized;
* runtime boundaries are clear;
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

The Container Architecture Skill commonly collaborates with:

* Component Architecture
* Integration Architecture
* Data Architecture
* Infrastructure Architecture
* Architecture Decision Records (ADR)

The Container Architecture defines the runtime structure that supports software deployment and execution.

---

# 15. Expected Outcomes

After execution, the Container Architecture should provide:

* clearly identified runtime applications;
* explicit runtime responsibilities;
* documented communication paths;
* scalable deployment structure;
* implementation guidance;
* a reliable foundation for Component Architecture.

The Container Architecture Skill transforms business-oriented architectural contexts into executable runtime structures, providing the architectural bridge between business modeling and software implementation within the DESys engineering lifecycle.
