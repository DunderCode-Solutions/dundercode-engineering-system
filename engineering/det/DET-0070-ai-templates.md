---
metadata_schema: 1.0.0
document_id: DET-0070
canonical_id: det.ai.templates
title: AI Templates
node_type: template
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All AI documentation developed within DESys
---

# DET-0070 — AI Templates

# 1. Purpose

The AI Templates Standard defines the engineering principles and reusable templates used to document Artificial Intelligence systems within the DunderCode Engineering System (DESys).

Its purpose is to standardize AI engineering documentation, ensuring consistency, transparency, traceability, safety, governance, and maintainability throughout the AI lifecycle.

AI templates transform AI engineering practices into reusable documentation assets.

---

# 2. Scope

This standard applies to every AI-related artifact produced within DET.

It covers reusable templates for:

* Prompt Specifications
* Prompt Libraries
* RAG Context Specifications
* Knowledge Base Specifications
* AI Model Cards
* AI Evaluation Reports
* AI Benchmark Reports
* AI Safety Reviews
* Human Review Checklists
* AI Operational Runbooks
* AI Deployment Documentation
* AI Governance Reports

Model implementation and training procedures are intentionally outside the scope of this document.

---

# 3. Audience

This document is intended for:

* AI Engineers
* Machine Learning Engineers
* Software Architects
* Solution Architects
* Knowledge Engineers
* Prompt Engineers
* AI Product Managers
* Engineering Managers
* AI-assisted engineering systems

---

# 4. Relationship with DESys

AI Templates document the engineering artifacts used throughout the AI lifecycle.

```text id="v7p2xm"
AI Engineering Standards
        ↓
AI Architecture
        ↓
AI Templates
        ↓
AI Systems
        ↓
Continuous Improvement
```

AI documentation supports reproducible, governable, and maintainable AI engineering.

---

# 5. Engineering Principles

Every AI Template SHALL follow the principles below.

## Transparency

AI documentation SHALL clearly describe system behavior, assumptions, and limitations.

---

## Traceability

AI artifacts SHALL remain traceable to knowledge sources, prompts, models, evaluations, and governance decisions.

---

## Reproducibility

Templates SHOULD enable AI behavior to be reproduced consistently.

---

## Safety

Documentation SHALL capture applicable safety controls and operational constraints.

---

## Human Oversight

Templates SHALL identify where human review or approval is required.

---

## Maintainability

AI documentation SHOULD evolve alongside prompts, models, and knowledge bases.

---

## Explainability

Templates SHOULD document the reasoning, objectives, and expected behavior of AI systems.

---

## Governance

AI documentation SHALL support engineering governance, audits, and compliance.

---

## Reusability

Templates SHOULD maximize reuse across AI projects.

---

## Continuous Improvement

AI documentation SHALL improve through operational experience and evaluation feedback.

---

# 6. Standard Template Structure

AI templates SHOULD include, when applicable:

* Metadata
* Purpose
* Scope
* AI Objective
* Business Context
* Inputs
* Outputs
* Prompt or Model Description
* Knowledge Sources
* Evaluation Criteria
* Limitations
* Risks
* Safety Considerations
* Human Review Requirements
* Operational Notes
* References
* Changelog

Additional sections MAY be introduced according to AI system complexity.

---

# 7. Mandatory Requirements

Every AI template MUST:

* Clearly define its purpose.
* Describe the intended AI behavior.
* Identify applicable knowledge sources.
* Document evaluation criteria.
* Describe limitations and risks.
* Preserve engineering traceability.
* Follow DET documentation standards.

---

# 8. AI Documentation Lifecycle

AI documentation SHALL evolve alongside AI systems.

```text id="p4k8zr"
AI Need
        ↓
Prompt / Model Design
        ↓
Documentation
        ↓
Evaluation
        ↓
Deployment
        ↓
Operational Feedback
        ↓
Continuous Improvement
```

AI documentation SHALL remain synchronized with production AI behavior.

---

# 9. Compliance

An AI Template complies with this standard when it:

* Clearly documents the AI artifact.
* Supports reproducibility.
* Preserves engineering traceability.
* Aligns with DES AI standards.
* Supports governance and responsible AI practices.

---

# 10. Relationship with Other DET Documents

AI Templates document engineering artifacts used throughout the AI lifecycle.

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

AI Templates provide standardized documentation for AI engineering, complementing traditional software engineering artifacts.

---

# 11. Recommended Template Catalog

The following templates are recommended within this family.

| Template                     | Purpose                                 |
| ---------------------------- | --------------------------------------- |
| Prompt Specification         | Prompt definition and expected behavior |
| Prompt Library Entry         | Reusable prompt catalog                 |
| RAG Context Specification    | Retrieval context definition            |
| Knowledge Base Specification | Knowledge source documentation          |
| AI Model Card                | Model characteristics and limitations   |
| AI Evaluation Report         | Evaluation results                      |
| AI Benchmark Report          | Comparative performance analysis        |
| AI Safety Review             | Safety assessment                       |
| Human Review Checklist       | Human oversight guidance                |
| AI Operational Runbook       | AI operational procedures               |
| AI Deployment Document       | AI deployment guidance                  |
| AI Governance Report         | Governance and compliance evidence      |

Organizations MAY extend this catalog while preserving DET principles.

---

# 12. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES — DunderCode Engineering Standards
* DEA — DunderCode Engineering Architecture
* DAR — Documentation Assessment Reports
* DET-0000 — Engineering Templates Overview
* DET-0030 — Architecture Templates
* DET-0060 — Operational Templates

---

# 13. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial AI Templates Standard.
* Defined engineering principles for AI documentation.
* Established the standard structure for AI templates.
* Introduced the AI Documentation Lifecycle.
* Included the recommended catalog of reusable AI engineering templates.
* Positioned AI Templates as the standardized documentation layer supporting AI engineering, governance, and operational excellence within DESys.
