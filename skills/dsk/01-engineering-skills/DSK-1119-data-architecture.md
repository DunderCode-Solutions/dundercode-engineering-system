# DSK-1119 | Data Architecture

## Metadata

Document Number: DSK-1119

Canonical ID: dsk.engineering.architecture.data-architecture

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents design and document the Data Architecture of a software system within the DunderCode Engineering System (DESys).

Data Architecture establishes how business information is organized, stored, governed, shared and protected across the software ecosystem.

It defines the strategic data landscape independently of implementation details such as schemas, ORM mappings or SQL scripts.

---

# 2. Scope

This skill supports:

* Data Domain Definition
* Data Ownership
* Data Storage Strategy
* Data Distribution
* Data Governance
* Data Lifecycle
* Data Security
* Data Architecture Review

---

# 3. Skill Objectives

The Data Architecture Skill aims to:

* organize enterprise information;
* define data ownership;
* improve consistency;
* support scalability;
* preserve data integrity;
* establish governance policies.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* design data architecture;
* organize enterprise data;
* define storage strategy;
* establish data governance;
* prepare software architecture.

This skill normally executes after Integration Architecture.

---

# 5. Inputs

Typical inputs include:

* Domain Model
* Bounded Contexts
* Container Architecture
* Component Architecture
* Integration Architecture
* Functional Requirements
* Non-Functional Requirements
* Business Rules

Missing business information should trigger clarification before data modeling begins.

---

# 6. Outputs

Typical deliverables include:

* Data Architecture
* Data Ownership Map
* Storage Strategy
* Data Flow Overview
* Data Governance Guidelines
* Data Lifecycle Definition
* Data Architecture Review Report

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
    - dea.data-management
    - dea.database-patterns
    - dea.data-governance
```

---

# 8. Execution Workflow

1. Review Domain Model.
2. Review Bounded Contexts.
3. Identify data domains.
4. Define ownership boundaries.
5. Select storage strategies.
6. Define data lifecycle.
7. Define governance rules.
8. Validate consistency.
9. Produce the Data Architecture.

---

# 9. Engineering Guidelines

The Data Architecture should:

* align with business capabilities;
* preserve ownership boundaries;
* minimize data duplication;
* support scalability;
* define governance policies;
* remain implementation independent.

Technology selection should support business requirements rather than dictate architectural decisions.

---

# 10. Architectural Topics

Typical topics include:

* Transactional Data
* Analytical Data
* Operational Data
* Event Data
* Master Data
* Reference Data
* File Storage
* Object Storage
* Search Indexes
* Cache Strategy
* Backup Strategy
* Retention Policies

Projects may extend these topics according to organizational needs.

---

# 11. Data Architecture Structure

Each data domain should include:

* Identifier
* Name
* Description
* Business Owner
* Storage Strategy
* Lifecycle
* Security Classification
* Related Bounded Context
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* ownership is explicit;
* storage responsibilities are documented;
* governance policies exist;
* unnecessary duplication is minimized;
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

The Data Architecture Skill commonly collaborates with:

* Integration Architecture
* Infrastructure Architecture
* Architecture Decision Records (ADR)
* Security Architecture
* Architecture Review

The Data Architecture defines the strategic organization and governance of enterprise information throughout the software lifecycle.

---

# 15. Expected Outcomes

After execution, the Data Architecture should provide:

* well-defined data ownership;
* consistent storage strategy;
* scalable information organization;
* explicit governance policies;
* improved data integrity;
* a reliable foundation for software implementation.

The Data Architecture Skill establishes the information architecture of the software ecosystem, ensuring that business data remains organized, governed and aligned with architectural principles throughout the DESys engineering lifecycle.
