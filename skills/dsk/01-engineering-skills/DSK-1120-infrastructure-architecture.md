---
metadata_schema: 1.0.0
document_id: DSK-1120
canonical_id: dsk.engineering.architecture.infrastructure-architecture
title: Infrastructure Architecture
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1120 | Infrastructure Architecture

# 1. Purpose

This skill defines how AI agents design and document the Infrastructure Architecture of a software system within the DunderCode Engineering System (DESys).

Infrastructure Architecture specifies the operational platform responsible for executing, deploying, monitoring, securing and maintaining the software ecosystem.

It establishes the runtime environment while remaining independent of infrastructure-as-code or deployment implementation.

---

# 2. Scope

This skill supports:

* Cloud Architecture
* Deployment Architecture
* Networking
* Container Orchestration
* Compute Resources
* Storage Infrastructure
* Observability
* Security Infrastructure
* High Availability
* Disaster Recovery
* Infrastructure Review

---

# 3. Skill Objectives

The Infrastructure Architecture Skill aims to:

* define the operational platform;
* improve reliability;
* maximize availability;
* support scalability;
* simplify operations;
* establish infrastructure governance.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* design infrastructure;
* define deployment platform;
* organize cloud architecture;
* prepare operational architecture;
* define hosting strategy.

This skill normally executes after Data Architecture.

---

# 5. Inputs

Typical inputs include:

* Container Architecture
* Component Architecture
* Integration Architecture
* Data Architecture
* Non-Functional Requirements
* Architecture Drivers
* Architecture Constraints

Infrastructure uncertainties should trigger clarification before platform definition begins.

---

# 6. Outputs

Typical deliverables include:

* Infrastructure Architecture
* Deployment Topology
* Infrastructure Components
* Networking Overview
* Operational Architecture
* Availability Strategy
* Infrastructure Review Report

---

# 7. Required Knowledge

### Required

```yaml id="d3t0zr"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="ytm72k"
knowledge:
  optional:
    - dea.cloud-architecture
    - dea.infrastructure-patterns
    - dea.observability
    - dea.platform-engineering
```

---

# 8. Execution Workflow

1. Review Container Architecture.
2. Review Integration Architecture.
3. Review Data Architecture.
4. Define deployment platform.
5. Define networking.
6. Define operational services.
7. Define observability.
8. Define availability strategy.
9. Validate infrastructure consistency.
10. Produce the Infrastructure Architecture.

---

# 9. Engineering Guidelines

Infrastructure Architecture should:

* support business objectives;
* remain scalable;
* maximize availability;
* support operational simplicity;
* document platform dependencies;
* preserve engineering traceability.

Infrastructure decisions should be driven by business and operational requirements rather than vendor preference alone.

---

# 10. Infrastructure Topics

Typical infrastructure topics include:

* Cloud Provider
* Compute Platform
* Container Platform
* Networking
* Load Balancing
* API Gateway
* Service Discovery
* Storage
* Object Storage
* Backup
* Disaster Recovery
* Monitoring
* Logging
* Metrics
* Distributed Tracing
* Secrets Management
* Identity Management
* CDN
* WAF

Projects may extend these topics according to organizational needs.

---

# 11. Infrastructure Structure

Each infrastructure element should include:

* Identifier
* Name
* Description
* Responsibility
* Platform
* Availability Level
* Security Considerations
* Operational Dependencies
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* deployment topology is documented;
* infrastructure responsibilities are explicit;
* operational dependencies are identified;
* availability strategy is defined;
* observability is documented;
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

The Infrastructure Architecture Skill commonly collaborates with:

* Data Architecture
* Architecture Decision Records (ADR)
* Security Architecture
* Architecture Review
* Architecture Traceability

Infrastructure Architecture provides the operational foundation that enables the software architecture to execute reliably in production environments.

---

# 15. Expected Outcomes

After execution, the Infrastructure Architecture should provide:

* a well-defined operational platform;
* scalable deployment architecture;
* reliable availability strategy;
* comprehensive observability;
* secure operational environment;
* a complete architectural foundation for implementation and operations.

The Infrastructure Architecture Skill establishes the operational foundation of the DESys software architecture, ensuring that applications, integrations and data services execute in a secure, scalable, resilient and maintainable infrastructure throughout the engineering lifecycle.
