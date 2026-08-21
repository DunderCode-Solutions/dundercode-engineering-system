---
metadata_schema: 1.0.0
document_id: DET-0010
canonical_id: det.project.templates
title: Project Templates
node_type: template
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All project documentation developed within DESys
---

# DET-0010 — Project Templates

# 1. Purpose

The Project Templates Standard defines the engineering principles and reusable templates used to document software projects within the DunderCode Engineering System (DESys).

Its purpose is to establish consistent project documentation that supports planning, communication, governance, execution, and long-term maintainability throughout the engineering lifecycle.

Project templates standardize how engineering initiatives are described before implementation begins.

---

# 2. Scope

This standard applies to all project-level documentation.

It covers reusable templates for:

* Project Charter
* Product Vision
* Product Requirement Document (PRD)
* Business Case
* Project Proposal
* Roadmap
* Release Plan
* Milestone Plan
* Stakeholder Register
* Project Summary

Project management methodologies (Agile, Scrum, Kanban, Waterfall, etc.) are intentionally outside the scope of this document.

---

# 3. Audience

This document is intended for:

* Product Managers
* Product Owners
* Project Managers
* Engineering Managers
* Software Architects
* Technical Leaders
* Business Analysts
* AI-assisted engineering systems

---

# 4. Relationship with DESys

Project Templates initiate the engineering lifecycle.

```text id="q3m7ha"
Engineering Standards
        ↓
Engineering Architecture
        ↓
Project Templates
        ↓
Engineering Execution
```

Project documentation transforms business intent into structured engineering work.

---

# 5. Engineering Principles

Every Project Template SHALL follow the principles below.

## Clarity

Project objectives SHALL be clearly defined.

---

## Business Alignment

Every project SHALL identify the business problem it intends to solve.

---

## Engineering Alignment

Project documentation SHALL remain aligned with DES standards and DEA architectures whenever applicable.

---

## Traceability

Requirements, decisions, and deliverables SHALL remain traceable throughout the project lifecycle.

---

## Simplicity

Project documentation SHOULD communicate essential information without unnecessary complexity.

---

## Reusability

Templates SHOULD be reusable across different engineering initiatives.

---

## Completeness

Project templates SHOULD provide sufficient information for engineering planning and execution.

---

## Maintainability

Project documentation SHOULD remain easy to update throughout the project lifecycle.

---

## Evolvability

Project artifacts SHALL evolve alongside the project while preserving historical traceability.

---

## Governance

Project documentation SHALL support engineering governance and decision-making.

---

# 6. Standard Template Structure

Project templates SHOULD include, when applicable:

* Metadata
* Executive Summary
* Business Context
* Problem Statement
* Objectives
* Scope
* Stakeholders
* Assumptions
* Constraints
* Functional Overview
* Non-Functional Expectations
* Success Metrics
* Risks
* Timeline
* Deliverables
* References
* Changelog

Additional sections MAY be introduced depending on project complexity.

---

# 7. Mandatory Requirements

Every project template MUST:

* Clearly define project objectives.
* Describe business value.
* Identify stakeholders.
* Define project scope.
* Preserve engineering traceability.
* Follow DET documentation standards.
* Support future project evolution.

---

# 8. Template Lifecycle

Project Templates SHALL evolve throughout the engineering lifecycle.

```text id="u6r2cn"
Project Idea
        ↓
Project Definition
        ↓
Planning
        ↓
Execution
        ↓
Monitoring
        ↓
Delivery
        ↓
Project Evolution
```

Project documentation SHALL remain synchronized with project reality.

---

# 9. Compliance

A Project Template complies with this standard when it:

* Clearly defines project intent.
* Supports engineering planning.
* Preserves traceability.
* Aligns with DES engineering standards.
* Supports governance and execution.

---

# 10. Relationship with Other DET Documents

Project Templates establish the foundation for all subsequent engineering documentation.

| Document | Relationship                   |
| -------- | ------------------------------ |
| DET-0000 | Engineering Templates Overview |
| DET-0010 | Project Templates              |
| DET-0020 | Requirements Templates         |
| DET-0030 | Architecture Templates         |
| DET-0040 | API Templates                  |
| DET-0050 | Testing Templates              |
| DET-0060 | Operational Templates          |
| DET-0070 | AI Templates                   |
| DET-0080 | Template Governance            |

Project Templates provide the business and planning context consumed by the remaining engineering artifacts.

---

# 11. Recommended Template Catalog

The following templates are recommended within this family.

| Template                           | Purpose                              |
| ---------------------------------- | ------------------------------------ |
| Project Charter                    | Formal project authorization         |
| Product Vision                     | Product direction and goals          |
| Product Requirement Document (PRD) | Functional and business requirements |
| Business Case                      | Business justification               |
| Project Proposal                   | Initial project presentation         |
| Product Roadmap                    | Strategic delivery planning          |
| Release Plan                       | Planned releases and milestones      |
| Milestone Plan                     | Project scheduling                   |
| Stakeholder Register               | Stakeholder identification           |
| Executive Summary                  | High-level project overview          |

Organizations MAY extend this catalog while preserving DET principles.

---

# 12. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES — DunderCode Engineering Standards
* DEA — DunderCode Engineering Architecture
* DET-0000 — Engineering Templates Overview

---

# 13. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Project Templates Standard.
* Defined engineering principles for project documentation.
* Established the standard structure for project templates.
* Introduced the Project Template Lifecycle.
* Included the recommended catalog of reusable project templates.
* Positioned Project Templates as the entry point for engineering documentation within DET.
