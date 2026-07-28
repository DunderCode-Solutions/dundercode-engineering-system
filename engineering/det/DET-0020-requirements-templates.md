# DET-0020 — Requirements Templates

# Metadata

**Canonical ID:** det.requirements.templates

**Document Class:** Engineering Templates

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

**Applies To:** All requirements documentation developed within DESys

---

# 1. Purpose

The Requirements Templates Standard defines the engineering principles and reusable templates used to capture, organize, validate, and maintain software requirements within the DunderCode Engineering System (DESys).

Its purpose is to establish a standardized approach for documenting business, functional, non-functional, and technical requirements while preserving consistency, traceability, and engineering quality.

Requirements templates transform business needs into engineering-ready specifications.

---

# 2. Scope

This standard applies to every requirements artifact produced within DET.

It covers reusable templates for:

* Business Requirements
* Functional Requirements
* Non-Functional Requirements
* User Stories
* Epics
* Features
* Use Cases
* Acceptance Criteria
* Business Rules
* Requirement Specifications

Requirements prioritization methodologies are intentionally outside the scope of this document.

---

# 3. Audience

This document is intended for:

* Product Managers
* Product Owners
* Business Analysts
* Software Architects
* Solution Architects
* Software Engineers
* QA Engineers
* Engineering Managers
* AI-assisted engineering systems

---

# 4. Relationship with DESys

Requirements Templates translate business needs into engineering specifications.

```text id="r8q3tm"
Project Templates
        ↓
Requirements Templates
        ↓
Architecture Templates
        ↓
Implementation
```

Requirements documentation serves as the contractual bridge between business expectations and engineering execution.

---

# 5. Engineering Principles

Every Requirements Template SHALL follow the principles below.

## Clarity

Requirements SHALL be written using clear, precise, and unambiguous language.

---

## Atomicity

Each requirement SHOULD describe a single capability or behavior.

---

## Testability

Every requirement SHALL be objectively verifiable.

---

## Traceability

Requirements SHALL remain traceable throughout the engineering lifecycle.

---

## Consistency

Requirements SHALL not contradict other approved requirements.

---

## Completeness

Requirements SHOULD provide sufficient context for engineering implementation.

---

## Business Alignment

Every requirement SHALL support an identifiable business objective.

---

## Independence

Requirements SHOULD minimize unnecessary dependencies.

---

## Evolvability

Requirements SHALL support controlled evolution throughout the project lifecycle.

---

## Governance

Requirements SHALL support engineering governance and future audits.

---

# 6. Standard Template Structure

Requirements templates SHOULD include, when applicable:

* Metadata
* Identifier
* Requirement Name
* Description
* Business Objective
* Stakeholders
* Priority
* Dependencies
* Constraints
* Acceptance Criteria
* Business Rules
* Traceability
* Notes
* References
* Changelog

Additional sections MAY be included depending on the complexity of the requirement.

---

# 7. Mandatory Requirements

Every requirements template MUST:

* Define a unique identifier.
* Describe the intended behavior.
* Include acceptance criteria.
* Support traceability.
* Align with business objectives.
* Follow DET documentation standards.
* Support future maintenance.

---

# 8. Requirements Lifecycle

Requirements SHALL evolve through a controlled engineering lifecycle.

```text id="v6m2ph"
Business Need
        ↓
Requirement Definition
        ↓
Validation
        ↓
Approval
        ↓
Implementation
        ↓
Verification
        ↓
Evolution
```

Requirements SHALL remain synchronized with the evolving product.

---

# 9. Compliance

A Requirements Template complies with this standard when it:

* Clearly specifies the requirement.
* Supports engineering implementation.
* Includes measurable acceptance criteria.
* Preserves engineering traceability.
* Aligns with DES engineering standards.

---

# 10. Relationship with Other DET Documents

Requirements Templates connect project planning with architecture and implementation.

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

Requirements Templates provide the engineering specifications consumed by architecture, implementation, testing, and operations.

---

# 11. Recommended Template Catalog

The following templates are recommended within this family.

| Template                   | Purpose                             |
| -------------------------- | ----------------------------------- |
| Business Requirement       | Business objective specification    |
| Functional Requirement     | Functional behavior specification   |
| Non-Functional Requirement | Quality attribute specification     |
| Epic                       | High-level capability               |
| Feature                    | Deliverable functionality           |
| User Story                 | User-centered requirement           |
| Use Case                   | Interaction specification           |
| Acceptance Criteria        | Verification rules                  |
| Business Rule              | Organizational policy or constraint |
| Requirement Specification  | Comprehensive requirement document  |

Organizations MAY extend this catalog while preserving DET principles.

---

# 12. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES — DunderCode Engineering Standards
* DEA — DunderCode Engineering Architecture
* DET-0000 — Engineering Templates Overview
* DET-0010 — Project Templates

---

# 13. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Requirements Templates Standard.
* Defined engineering principles for requirements documentation.
* Established the standard structure for requirements templates.
* Introduced the Requirements Lifecycle.
* Included the recommended catalog of reusable requirements templates.
* Positioned Requirements Templates as the specification layer between project planning and software architecture.
