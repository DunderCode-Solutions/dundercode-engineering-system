---
metadata_schema: 1.0.0
document_id: DET-0030
canonical_id: det.architecture.templates
title: Architecture Templates
node_type: template
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All architecture documentation developed within DESys
---

# DET-0030 — Architecture Templates

# 1. Purpose

The Architecture Templates Standard defines the engineering principles and reusable templates used to document software architectures within the DunderCode Engineering System (DESys).

Its purpose is to establish a standardized structure for capturing architectural knowledge, decisions, system designs, and technical strategies while preserving consistency, traceability, maintainability, and engineering quality.

Architecture templates transform engineering architecture into structured documentation suitable for implementation, review, and long-term evolution.

---

# 2. Scope

This standard applies to every architecture document produced within DET.

It covers reusable templates for:

* Architecture Decision Records (ADR)
* Request for Comments (RFC)
* Software Architecture Documents (SAD)
* Solution Architecture Documents
* System Context Diagrams
* C4 Model Documentation
* Component Specifications
* Deployment Architecture
* Integration Architecture
* Technical Design Documents

Architecture governance processes are defined by DEA and are outside the scope of this document.

---

# 3. Audience

This document is intended for:

* Enterprise Architects
* Solution Architects
* Software Architects
* Technical Leaders
* Platform Engineers
* Engineering Managers
* Software Engineers
* AI-assisted engineering systems

---

# 4. Relationship with DESys

Architecture Templates document engineering architectures defined within DEA.

```text id="d7v8pk"
Engineering Standards
        ↓
Engineering Architecture
        ↓
Architecture Templates
        ↓
Engineering Documentation
        ↓
Implementation
```

Architecture documentation provides the communication layer between architectural design and software implementation.

---

# 5. Engineering Principles

Every Architecture Template SHALL follow the principles below.

## Architectural Fidelity

Documentation SHALL accurately represent the approved architecture.

---

## Clarity

Architectural concepts SHALL be described clearly and unambiguously.

---

## Traceability

Architecture documents SHALL remain traceable to DES standards, DEA assets, requirements, and implementation.

---

## Consistency

Equivalent architectures SHOULD produce equivalent documentation structures.

---

## Completeness

Documentation SHOULD contain sufficient information to support implementation, review, and maintenance.

---

## Technology Neutrality

Architecture documentation SHOULD emphasize engineering concepts rather than framework-specific details whenever practical.

---

## Evolvability

Architecture documents SHALL support continuous architectural evolution.

---

## Maintainability

Architecture documentation SHOULD remain simple to maintain throughout the system lifecycle.

---

## Reusability

Architecture templates SHOULD maximize reuse across engineering projects.

---

## Governance

Architecture documentation SHALL support engineering reviews and governance activities.

---

# 6. Standard Template Structure

Architecture templates SHOULD include, when applicable:

* Metadata
* Purpose
* Scope
* Audience
* Business Context
* System Context
* Architectural Goals
* Architectural Principles
* Architecture Overview
* Component View
* Data View
* Integration View
* Deployment View
* Security View
* Operational Considerations
* Architectural Decisions
* Assumptions
* Constraints
* Risks
* References
* Changelog

Additional sections MAY be introduced according to project complexity.

---

# 7. Mandatory Requirements

Every architecture template MUST:

* Clearly identify the architectural scope.
* Preserve engineering traceability.
* Document architectural assumptions.
* Describe architectural components.
* Record significant architectural decisions.
* Support implementation and future evolution.
* Follow DET documentation standards.

---

# 8. Architecture Documentation Lifecycle

Architecture documentation SHALL evolve throughout the engineering lifecycle.

```text id="h2n6rm"
Architecture Need
        ↓
Architecture Design
        ↓
Documentation
        ↓
Technical Review
        ↓
Publication
        ↓
Implementation
        ↓
Architecture Evolution
```

Architecture documentation SHALL remain synchronized with the implemented architecture.

---

# 9. Compliance

An Architecture Template complies with this standard when it:

* Accurately documents the approved architecture.
* Supports engineering implementation.
* Preserves engineering traceability.
* Aligns with DEA architectural principles.
* Supports governance and continuous improvement.

---

# 10. Relationship with Other DET Documents

Architecture Templates connect engineering requirements with implementation guidance.

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

Architecture Templates provide the standardized documentation used to communicate engineering architectures across the software lifecycle.

---

# 11. Recommended Template Catalog

The following templates are recommended within this family.

| Template                             | Purpose                                      |
| ------------------------------------ | -------------------------------------------- |
| Architecture Decision Record (ADR)   | Architectural decision documentation         |
| Request for Comments (RFC)           | Technical proposal and discussion            |
| Software Architecture Document (SAD) | Complete software architecture specification |
| Solution Architecture Document       | Solution-level architecture                  |
| System Context Diagram               | External system relationships                |
| C4 Model Documentation               | Multi-level architecture visualization       |
| Component Specification              | Component responsibilities                   |
| Deployment Architecture              | Infrastructure and deployment topology       |
| Integration Architecture             | Communication between systems                |
| Technical Design Document            | Detailed technical solution                  |

Organizations MAY extend this catalog while preserving DET principles.

---

# 12. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES — DunderCode Engineering Standards
* DEA — DunderCode Engineering Architecture
* DET-0000 — Engineering Templates Overview
* DET-0020 — Requirements Templates

---

# 13. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Architecture Templates Standard.
* Defined engineering principles for architecture documentation.
* Established the standard structure for architecture templates.
* Introduced the Architecture Documentation Lifecycle.
* Included the recommended catalog of reusable architecture templates.
* Positioned Architecture Templates as the documentation layer connecting DEA architectures to engineering implementation.
