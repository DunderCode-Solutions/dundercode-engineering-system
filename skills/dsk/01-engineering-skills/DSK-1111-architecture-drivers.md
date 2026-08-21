---
metadata_schema: 1.0.0
document_id: DSK-1111
canonical_id: dsk.engineering.architecture.architecture-drivers
title: Architecture Drivers
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1111 | Architecture Drivers

# 1. Purpose

This skill defines how AI agents identify, analyze and document Architecture Drivers within the DunderCode Engineering System (DESys).

Architecture Drivers represent the business, technical and operational forces that influence architectural decisions and shape the overall software architecture.

They provide the rationale behind architectural choices and establish priorities for architectural design.

---

# 2. Scope

This skill supports:

* Architecture Driver Identification
* Driver Classification
* Quality Attribute Prioritization
* Business Driver Analysis
* Technical Driver Analysis
* Constraint Identification
* Architectural Decision Support
* Driver Review

---

# 3. Skill Objectives

The Architecture Drivers Skill aims to:

* identify architectural influences;
* prioritize architectural concerns;
* align architecture with business strategy;
* support architectural decision making;
* reduce architectural ambiguity;
* establish objective decision criteria.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify architectural drivers;
* analyze architecture priorities;
* understand architecture decisions;
* define quality priorities;
* begin architectural design;
* prepare architecture documentation.

This skill normally executes after Architecture Vision.

---

# 5. Inputs

Typical inputs include:

* Architecture Vision
* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* Organizational Constraints
* Technical Constraints

Missing architectural information should trigger clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Architecture Drivers Catalog
* Driver Prioritization
* Quality Attribute Priorities
* Business Driver Summary
* Technical Driver Summary
* Driver Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="v7km31"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="w2ap9d"
knowledge:
  optional:
    - dea.quality-attributes
    - dea.reference-architectures
    - dea.architecture-principles
```

---

# 8. Execution Workflow

The Architecture Drivers Skill follows this workflow.

1. Review Architecture Vision.
2. Analyze business objectives.
3. Analyze quality requirements.
4. Identify architectural drivers.
5. Classify driver categories.
6. Prioritize architectural influences.
7. Validate engineering alignment.
8. Produce Architecture Drivers documentation.

---

# 9. Engineering Guidelines

Architecture Drivers should:

* represent forces that influence architecture;
* remain independent of implementation;
* be measurable whenever possible;
* support architectural decision making;
* preserve alignment with business objectives;
* remain traceable throughout the engineering lifecycle.

Architecture Drivers should explain **why** architectural decisions exist rather than **how** they are implemented.

---

# 10. Driver Categories

Typical Architecture Driver categories include:

* Business Drivers
* Quality Attribute Drivers
* Technical Drivers
* Regulatory Drivers
* Security Drivers
* Operational Drivers
* Integration Drivers
* Scalability Drivers
* Performance Drivers
* Availability Drivers
* Organizational Drivers

Projects may define additional driver categories according to business needs.

---

# 11. Driver Structure

Each Architecture Driver should include:

* Identifier
* Name
* Description
* Driver Category
* Business Motivation
* Expected Impact
* Priority
* Related Requirements
* Related Constraints
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* business alignment exists;
* quality attributes are represented;
* priorities are documented;
* duplicate drivers do not exist;
* implementation details are absent;
* traceability is preserved.

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

The Architecture Drivers Skill commonly collaborates with:

* Architecture Vision
* Architecture Constraints
* Domain Modeling
* Architecture Decision Records (ADR)
* Architecture Review

Architecture Drivers provide the rationale used to evaluate architectural alternatives and justify architectural decisions.

---

# 15. Expected Outcomes

After execution, the Architecture Drivers should provide:

* a prioritized set of architectural influences;
* documented business and technical motivations;
* explicit quality attribute priorities;
* improved architectural decision making;
* consistent engineering guidance;
* complete traceability between business objectives and architecture.

The Architecture Drivers Skill establishes the decision-making foundation of the software architecture, ensuring that every architectural choice remains aligned with business priorities, engineering standards and the long-term objectives of the DESys lifecycle.
