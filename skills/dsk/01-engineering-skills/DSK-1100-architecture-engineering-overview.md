# DSK-1100 | Architecture Engineering

## Metadata

Document Number: DSK-1100

Canonical ID: dsk.engineering.architecture

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents perform Architecture Engineering within the DunderCode Engineering System (DESys).

Architecture Engineering transforms validated software requirements into a coherent, scalable and maintainable technical solution while preserving complete engineering traceability.

This skill orchestrates architectural knowledge rather than replacing architectural design activities.

---

# 2. Scope

This skill supports:

* Architecture Vision
* Architecture Analysis
* Domain Modeling
* Context Modeling
* Component Design
* Integration Design
* Data Architecture
* Infrastructure Architecture
* Security Architecture
* Architecture Decision Records (ADR)
* Architecture Review
* Architecture Traceability

---

# 3. Skill Objectives

The Architecture Engineering Skill aims to:

* transform business requirements into technical architecture;
* support engineering decision making;
* preserve architectural consistency;
* improve scalability and maintainability;
* reduce technical risks;
* establish implementation guidance.

---

# 4. Activation Criteria

This skill should be activated when the user requests:

* design software architecture;
* create system architecture;
* define components;
* define integrations;
* model domains;
* prepare implementation architecture;
* review architecture.

This skill normally executes after Requirements Engineering.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* Product Backlog
* Product Requirements Document (PRD)
* Requirements Traceability

Incomplete engineering artifacts should trigger clarification before architectural design begins.

---

# 6. Outputs

Typical deliverables include:

* Software Architecture
* Architecture Views
* Domain Model
* Context Model
* Component Model
* Integration Model
* Architecture Decision Records (ADR)
* Architecture Review Report
* Architecture Traceability

---

# 7. Required Knowledge

This skill should consume knowledge from the following DESys libraries.

### Required

```yaml
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
    - det.architecture.template
```

### Optional

```yaml
knowledge:
  optional:
    - dea.reference-architectures
    - dea.domain-model
    - dea.integration-patterns
```

---

# 8. Execution Workflow

The Architecture Engineering Skill follows this workflow.

1. Understand business context.
2. Review engineering requirements.
3. Identify architectural drivers.
4. Analyze constraints.
5. Produce architectural models.
6. Validate architectural consistency.
7. Record architectural decisions.
8. Produce architecture documentation.

---

# 9. Engineering Rules

Architecture should always:

* satisfy business requirements;
* preserve traceability;
* remain implementation independent when possible;
* document architectural decisions;
* minimize unnecessary complexity;
* maximize maintainability;
* support future evolution.

Architecture should never introduce functionality not supported by validated requirements.

---

# 10. Validation

Before completion the skill verifies:

* architectural drivers are identified;
* requirements are covered;
* constraints are respected;
* architectural decisions are documented;
* traceability is preserved;
* documentation follows DESys standards.

---

# 11. Dependencies

### Processes

* DEP Architecture Process

### Templates

* Architecture Template
* ADR Template

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 12. Collaboration

This skill commonly collaborates with:

* Requirements Engineering
* Development Engineering
* Testing Engineering
* Deployment Engineering

Architecture Engineering acts as the bridge between Requirements Engineering and Software Implementation.

---

# 13. Expected Outcomes

After execution, the Architecture Engineering Skill should provide:

* coherent software architecture;
* documented architectural decisions;
* complete engineering traceability;
* implementation guidance;
* scalable technical solutions;
* a reliable foundation for software development.

Architecture Engineering establishes the technical foundation of the software product while preserving alignment with business objectives and engineering standards throughout the DESys lifecycle.
