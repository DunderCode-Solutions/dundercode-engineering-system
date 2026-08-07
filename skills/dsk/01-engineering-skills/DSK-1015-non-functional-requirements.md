# DSK-1015 | Non-Functional Requirements

## Metadata

Document Number: DSK-1015

Canonical ID: dsk.engineering.requirements.non-functional-requirements

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, organize and validate Non-Functional Requirements (NFRs) within the DunderCode Engineering System (DESys).

Non-Functional Requirements define the quality attributes, operational constraints and performance expectations that govern how a software system should behave.

These requirements provide essential inputs for architecture, infrastructure, security and operational decisions.

---

# 2. Scope

This skill supports:

* Quality Attribute Identification
* Performance Requirements
* Security Requirements
* Availability Requirements
* Reliability Requirements
* Scalability Requirements
* Maintainability Requirements
* Compliance Requirements
* Operational Constraints
* NFR Review

---

# 3. Skill Objectives

The Non-Functional Requirements Skill aims to:

* identify quality expectations;
* define measurable quality attributes;
* document operational constraints;
* support architectural decisions;
* reduce implementation risks;
* establish objective acceptance criteria.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define quality requirements;
* specify performance expectations;
* establish security requirements;
* define operational constraints;
* prepare software architecture;
* complete software requirements.

This skill normally executes after Functional Requirements.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Regulatory Requirements
* Organizational Standards
* Business Constraints
* Operational Environment

Missing quality information should trigger clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Non-Functional Requirements Specification
* Quality Attribute Catalog
* Performance Requirements
* Security Requirements
* Operational Constraints
* Compliance Requirements
* NFR Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="ehhj6t"
knowledge:
  required:
    - dep.requirements.process
    - des.requirements.documentation
    - det.prd.template
```

### Optional

```yaml id="u6tql5"
knowledge:
  optional:
    - dea.architecture.principles
    - dea.quality-attributes
    - dea.security
```

---

# 8. Execution Workflow

The Non-Functional Requirements Skill follows this workflow.

1. Analyze business context.
2. Review Functional Requirements.
3. Identify quality attributes.
4. Define measurable NFRs.
5. Identify operational constraints.
6. Classify NFR categories.
7. Validate completeness.
8. Produce structured NFR documentation.

---

# 9. Engineering Guidelines

Non-Functional Requirements should:

* describe quality attributes rather than functionality;
* be measurable whenever possible;
* remain implementation independent;
* support architectural decision making;
* be individually testable;
* remain traceable to business objectives.

Whenever possible, NFRs should define objective acceptance thresholds.

Examples include:

* maximum response time;
* minimum availability;
* recovery objectives;
* security standards;
* supported concurrent users.

---

# 10. Requirement Categories

Typical Non-Functional Requirement categories include:

* Performance
* Scalability
* Availability
* Reliability
* Security
* Privacy
* Maintainability
* Observability
* Accessibility
* Usability
* Portability
* Compliance
* Disaster Recovery
* Interoperability

Projects may define additional categories when required.

---

# 11. Validation

Before completion the skill verifies:

* quality attributes are measurable;
* constraints are documented;
* requirements are testable;
* architectural implications are identified;
* duplicate NFRs do not exist;
* traceability is preserved.

---

# 12. Dependencies

### Parent Skill

* DSK-1010 Requirements Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Non-Functional Requirements Skill commonly collaborates with:

* Functional Requirements
* Business Rules
* Architecture Engineering
* Testing Engineering
* Deployment Engineering

Non-Functional Requirements directly influence architectural and infrastructure decisions.

---

# 14. Expected Outcomes

After execution, the Non-Functional Requirements should provide:

* measurable quality expectations;
* documented operational constraints;
* complete quality attribute specifications;
* architectural guidance;
* objective validation criteria;
* a reliable foundation for architecture, testing and operations.

The Non-Functional Requirements Skill establishes the quality expectations of the software system, ensuring that engineering decisions consider not only what the system must do, but also how well it must perform throughout its lifecycle.
