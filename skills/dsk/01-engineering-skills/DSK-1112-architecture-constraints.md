# DSK-1112 | Architecture Constraints

## Metadata

Document Number: DSK-1112

Canonical ID: dsk.engineering.architecture.architecture-constraints

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, document and validate Architecture Constraints within the DunderCode Engineering System (DESys).

Architecture Constraints represent the technical, organizational, operational and regulatory limitations that restrict architectural decisions.

These constraints define the solution space within which the software architecture must be designed.

---

# 2. Scope

This skill supports:

* Architecture Constraint Identification
* Technical Constraint Analysis
* Organizational Constraint Analysis
* Regulatory Constraint Analysis
* Infrastructure Constraint Analysis
* Constraint Classification
* Constraint Validation
* Constraint Review

---

# 3. Skill Objectives

The Architecture Constraints Skill aims to:

* identify architectural limitations;
* document mandatory restrictions;
* reduce architectural risks;
* improve architectural consistency;
* support realistic architectural decisions;
* preserve engineering traceability.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify architecture constraints;
* document technical limitations;
* analyze solution restrictions;
* define implementation boundaries;
* prepare architecture design.

This skill normally executes after Architecture Drivers.

---

# 5. Inputs

Typical inputs include:

* Architecture Vision
* Architecture Drivers
* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Organizational Policies
* Infrastructure Standards
* Regulatory Requirements

Missing organizational information should trigger clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Architecture Constraints Catalog
* Technical Constraints
* Organizational Constraints
* Regulatory Constraints
* Infrastructure Constraints
* Constraint Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

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
    - dea.infrastructure
    - dea.security
    - dea.reference-architectures
```

---

# 8. Execution Workflow

The Architecture Constraints Skill follows this workflow.

1. Review Architecture Vision.
2. Review Architecture Drivers.
3. Identify technical constraints.
4. Identify business constraints.
5. Identify organizational constraints.
6. Identify regulatory constraints.
7. Validate engineering consistency.
8. Produce Architecture Constraints documentation.

---

# 9. Engineering Guidelines

Architecture Constraints should:

* represent mandatory limitations;
* remain implementation independent whenever possible;
* distinguish restrictions from preferences;
* remain traceable;
* support realistic architectural decisions.

Constraints should describe **what cannot be changed** without modifying business, organizational or technical assumptions.

---

# 10. Constraint Categories

Typical Architecture Constraint categories include:

* Technical Constraints
* Infrastructure Constraints
* Organizational Constraints
* Budget Constraints
* Team Constraints
* Regulatory Constraints
* Security Constraints
* Technology Constraints
* Vendor Constraints
* Legacy System Constraints
* Operational Constraints

Projects may define additional categories according to organizational needs.

---

# 11. Constraint Structure

Each Architecture Constraint should include:

* Identifier
* Name
* Description
* Constraint Category
* Source
* Business Justification
* Expected Impact
* Mandatory Level
* Related Drivers
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* constraints are explicitly documented;
* business justification exists;
* duplicate constraints do not exist;
* related architecture drivers are identified;
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

The Architecture Constraints Skill commonly collaborates with:

* Architecture Vision
* Architecture Drivers
* Domain Modeling
* Infrastructure Architecture
* Architecture Decision Records (ADR)

Architecture Constraints define the boundaries within which architectural decisions must be made.

---

# 15. Expected Outcomes

After execution, the Architecture Constraints should provide:

* documented architectural limitations;
* explicit implementation boundaries;
* reduced architectural uncertainty;
* realistic engineering expectations;
* complete traceability between constraints and architecture;
* a reliable foundation for architectural modeling.

The Architecture Constraints Skill establishes the mandatory boundaries of the software architecture, ensuring that architectural decisions remain feasible, compliant and aligned with organizational, technical and regulatory realities throughout the DESys engineering lifecycle.
