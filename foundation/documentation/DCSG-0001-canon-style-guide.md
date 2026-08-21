---
metadata_schema: 1.0.0
document_id: DCSG-0001
canonical_id: dcsg.canon.style-guide
title: DunderCode Canon Style Guide
node_type: style-guide
document_class: normative
version: 1.1.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All documentation produced within the DunderCode Engineering System (DESys)
---

# DCSG-0001 — DunderCode Canon Style Guide

# 1. Purpose

The DunderCode Canon Style Guide (DCSG) defines the official standards for creating, maintaining, reviewing, and evolving documentation within the DunderCode Engineering System (DESys).

Its purpose is to ensure that every document produced by DunderCode is clear, consistent, traceable, reusable, and maintainable throughout its lifecycle.

Documentation is considered an engineering asset and therefore follows the same level of discipline applied to software development.

---

# 2. Audience

This guide is intended for everyone involved in the creation, review, maintenance, and evolution of documentation within DESys.

This includes:

- Software Engineers
- Solution Architects
- Technical Writers
- Reviewers
- Engineering Managers
- AI-assisted documentation systems

---

# 3. Philosophy

Documentation is not a by-product of development.

Documentation is development.

Within DESys, documentation is the primary source of truth from which architecture, standards, implementations, and products are derived.

Every engineering decision must be documented before it is implemented.

Knowledge always precedes implementation.

---

# 4. Scope

This guide applies to every official engineering artifact, including but not limited to:

* DEC — DunderCode Engineering Canon
* DEM — DunderCode Engineering Method
* DES — DunderCode Engineering Standards
* DSB — DunderCode Solution Blueprints
* ADR — Architecture Decision Records
* RFC — Request for Comments
* PRD — Product Requirements Documents
* DTL — DunderCode Tools
* Repository documentation
* Technical documentation
* User documentation

---

# 5. Non-Goals

This guide does not define engineering practices, software architecture, programming standards, or development methodologies.

Those responsibilities belong to the corresponding DES, DEM, DEC, ADR, and RFC documents.

The sole purpose of DCSG is to define how engineering knowledge is documented.

---

# 6. Documentation Principles

Every document produced by DunderCode shall follow these principles.

## 6.1 Clarity

Documents must communicate ideas unambiguously.

Readers should never need to infer the intended meaning.

---

## 6.2 Simplicity

Complex ideas should be explained using simple language whenever possible.

---

## 6.3 Consistency

Terminology, formatting, and document organization shall remain consistent across the entire engineering system.

---

## 6.4 Traceability

Every engineering decision shall be traceable to its origin.

Documents must explicitly reference related principles, standards, methods, ADRs, RFCs, and products whenever applicable.

---

## 6.5 Reusability

Documentation should be written to maximize reuse across projects.

---

## 6.6 Evolvability

Documentation is expected to evolve continuously.

Every document may be improved while preserving its historical traceability.

---

# 7. Documentation Lifecycle

Every official document progresses through the following lifecycle:

Draft

↓

Review

↓

Approved

↓

Published

↓

Deprecated

Each state represents a well-defined stage in the engineering process.

---

# 8. Canonical Language

English is the canonical language of DESys.

Translations are derived documents and shall never replace the canonical version.

Whenever inconsistencies exist between translated and canonical versions, the English version prevails.

---

# 9. Writing Style

Documentation shall be:

* Professional
* Objective
* Educational
* Precise
* Timeless whenever possible

Marketing language, exaggerated claims, and ambiguous wording should be avoided.

The objective is to teach rather than persuade.

---

# 10. Normative Language

Normative documents within the DunderCode Engineering System (DESys) SHALL use standardized requirement keywords to express engineering requirements consistently.

DESys adopts the normative language defined by RFC 2119 to ensure consistency across engineering standards, methods, governance documents, and architectural specifications.

The following keywords SHALL be interpreted as follows.

| Keyword | Meaning |
|----------|---------|
| **MUST** | Indicates an absolute requirement. |
| **MUST NOT** | Indicates an absolute prohibition. |
| **SHOULD** | Indicates a strong recommendation unless a justified reason exists not to follow it. |
| **SHOULD NOT** | Indicates a practice that is generally discouraged. |
| **MAY** | Indicates an optional behavior or implementation choice. |

Normative keywords SHALL appear in uppercase whenever they define engineering requirements.

These keywords are mandatory for normative documents, including but not limited to:

- DEC — DunderCode Engineering Canon
- DEM — DunderCode Engineering Method
- DES — DunderCode Engineering Standard
- DAR — DunderCode Assessment Report
- ADR — Architecture Decision Record (when defining mandatory decisions)
- RFC — Request for Comments (when defining proposed engineering standards)

Documents intended solely for explanation, guidance, or reference (such as guides, tutorials, examples, and README files) MAY use ordinary language instead of normative keywords.

---

# 11. Voice and Tone

Documents should be written using:

* Active voice
* Direct language
* Consistent terminology

Whenever possible:

Explain why.

Then explain what.

Finally explain how.

---

# 12. Document Structure

Every official document SHOULD follow a consistent organizational structure appropriate to its document type.

Common sections include:

- Purpose
- Scope
- Audience
- Motivation
- Standard
- Requirements
- Recommendations
- Exceptions
- Compliance
- References
- Revision History

Not every document is required to include all sections.

Each document type defines its own canonical structure while following the editorial principles established by this guide.

Examples:

- README documents describe domains and provide navigation.
- DES documents define engineering standards.
- DEM documents define engineering methods.
- DEC documents establish canonical engineering principles.
- DAR documents define assessment and review criteria.
- ADR documents record architectural decisions.

---

# 13. Metadata

Every non-empty, identifier-bearing DESys document MUST include canonical YAML front matter to support traceability, knowledge management, automation, and semantic indexing.

The canonical fields, enums, syntax, and validation rules are defined by DEKG-0040 and `knowledge/architecture/metadata/desys-metadata.schema.json`.

README files are navigation surfaces and do not require canonical metadata. Empty placeholders are not engineering assets and are not indexed.

Metadata embedded as a Markdown section is not machine-readable canonical metadata and MUST NOT be introduced in new documents.

---

# 14. Cross References

Documents shall reference related engineering assets whenever relationships exist.

References should be explicit rather than implied.

This enables complete engineering traceability across the DESys knowledge graph.

Cross references should create explicit engineering relationships rather than simple hyperlinks.

---

# 15. Examples

Examples are mandatory whenever they improve understanding.

Good examples are:

* Short
* Realistic
* Complete
* Easy to reproduce

Examples should demonstrate engineering concepts rather than isolated syntax.

---

# 16. Diagrams

Diagrams should prioritize understanding over artistic presentation.

Every diagram must communicate a single concept clearly.

---

# 17. Tables

Tables should be used whenever structured comparison improves readability.

Avoid tables for purely narrative content.

---

# 18. Code Blocks

Code examples shall:

* Be complete whenever practical.
* Follow official engineering standards.
* Represent production-quality examples.

Pseudo-code should be explicitly identified.

---

# 19. AI-Assisted Documentation

Documentation shall be written to maximize comprehension by both humans and AI systems.

Authors should:

* Use explicit terminology.
* Avoid unnecessary ambiguity.
* Prefer short sections.
* Define concepts before using them.
* Maintain consistent naming conventions.

AI is considered an engineering assistant rather than an authority.

The documentation remains the single source of truth.

Normative keywords, standardized metadata, and consistent document structures improve semantic indexing, automated validation, AI-assisted retrieval, and integration with the DunderCode Engineering Knowledge Graph (DEKG).

AI systems should interpret engineering requirements according to the normative language defined by this guide while preserving document traceability and canonical structure.

---

# 20. Documentation Quality Model (DQM)

Every document shall be evaluated using the following quality model.

Purpose

↓

Clarity

↓

Consistency

↓

Traceability

↓

Completeness

↓

Maintainability

↓

Reusability

A document should satisfy each level before progressing to the next.

---

# 21. Governance

Changes to official documentation follow the DESys engineering workflow.

Proposal

↓

Discussion

↓

Review

↓

Approval

↓

Publication

↓

Assessment (DAR)

↓

Continuous Improvement

Major structural changes shall be proposed through an RFC.

---

# 22. Guiding Principle

Every document must teach, not merely describe.

Documentation exists to transfer engineering knowledge.

The success of a document is measured by the reader's ability to understand, apply, and evolve the knowledge it contains.

---

# 23. Closing Statement

The DunderCode Canon Style Guide is the editorial foundation of the DunderCode Engineering System.

It establishes the principles that transform documentation into structured engineering knowledge.

By standardizing documentation, DESys standardizes engineering communication, preserves organizational knowledge, and enables continuous software evolution.

---

# 24. Changelog

## Version 1.0.0

Initial release.

## Version 1.1.0 (Draft)

### Added

- Introduced the **Normative Language** section based on RFC 2119.
- Expanded the standardized Metadata Schema.
- Updated Document Structure to support multiple document types.
- Added support for Canonical IDs and Document Types.
- Formalized editorial support for DEKG integration.
- Improved AI-readability through standardized document semantics.

### Changed

- Clarified the distinction between informational and normative documents.
- Improved guidance for engineering specifications.
- Enhanced document interoperability across the DESys ecosystem.


---

**Think First. Build Better.**

---
