# DES-0910 — Prompt Engineering Standard

# Metadata

**Canonical ID:** des.ai.prompt-engineering

**Document Class:** Normative

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

**Applies To:** All prompts and prompt-driven interactions managed under DESys

---

# 1. Purpose

The Prompt Engineering Standard defines the engineering requirements for designing, organizing, maintaining, and governing prompts used within the DunderCode Engineering System (DESys).

Its purpose is to establish technology-independent engineering principles that ensure prompts remain clear, intentional, traceable, safe, reusable, and effective throughout their lifecycle.

Prompt engineering is considered an engineering discipline rather than a collection of ad hoc instructions.

---

# 2. Scope

This standard applies to every prompt, prompt template, system instruction, task instruction, and prompt-driven interaction managed under DESys.

It defines engineering expectations for prompt purpose, structure, clarity, context, safety, governance, traceability, and lifecycle management.

Implementation details related to model providers, prompt formatting tools, orchestration frameworks, or proprietary AI interfaces are intentionally excluded.

---

# 3. Audience

This standard is intended for:

* Solution Architects
* AI Architects
* Software Architects
* Data Architects
* Prompt Engineers
* Software Engineers
* Technical Leaders
* Governance Teams
* AI-assisted engineering systems

Every stakeholder responsible for designing, reviewing, or governing prompts SHALL understand and follow this standard.

---

# 4. Relationship with DESys

This standard derives its engineering philosophy from:

* DEC — DunderCode Engineering Canon
* DEM — DunderCode Engineering Method
* DCSG — DunderCode Canon Style Guide
* DES-0900 — AI Engineering Principles
* DES-0920 — Knowledge Engineering Standard
* DES-0940 — AI Evaluation Standard
* DES-0950 — AI Safety Standard

Prompt Engineering establishes the foundation for prompt-based AI interaction within DESys.

---

# 5. Prompt Engineering Principles

Prompt engineering SHALL follow the principles defined below.

## Intentionality

Every prompt SHALL have a clearly defined purpose.

Prompts MUST NOT exist without an explicit engineering objective.

---

## Clarity

Prompts SHOULD be written clearly, directly, and unambiguously.

Instructions SHOULD minimize interpretive ambiguity.

---

## Context Relevance

Prompts SHOULD provide only the context necessary to achieve the intended outcome.

Irrelevant information SHOULD be avoided.

---

## Constraint Definition

Prompts SHALL define relevant constraints when they are required for correct behavior.

Expected boundaries SHOULD be explicit.

---

## Output Orientation

Prompts SHOULD specify the desired form, structure, or behavior of the output when practical.

The intended result SHOULD be understandable from the prompt itself.

---

## Traceability

Prompts SHALL remain traceable to their purpose, version, and intended use.

Significant prompt changes SHOULD be documented.

---

## Reusability

Prompts SHOULD be reusable whenever practical.

Prompt templates SHOULD support controlled adaptation across similar use cases.

---

## Safety

Prompts SHALL be designed to avoid unsafe, misleading, or harmful outputs.

Safety considerations MUST be incorporated intentionally.

---

## Evolvability

Prompts SHALL evolve through controlled engineering processes.

Prompt refinements SHOULD preserve intended behavior and traceability.

---

# 6. Standard

Every DESys-compliant prompt SHALL define:

* Prompt purpose
* Intended audience
* Required context
* Output expectations
* Safety boundaries
* Ownership
* Version or revision expectations

Projects MAY use different prompt structures provided they remain consistent with the engineering principles established by this standard.

---

# 7. Mandatory Requirements

Every prompt managed under DESys MUST:

* Have a clearly defined purpose.
* Be understandable to its intended users or systems.
* Preserve traceability.
* Respect safety requirements.
* Define output expectations where applicable.
* Support revision control or version awareness.
* Be reviewed when behavior changes materially.

---

# 8. Prompt Engineering Lifecycle

Prompts SHALL follow a controlled lifecycle.

```text
Prompt Intent
      ↓
Design
      ↓
Review
      ↓
Implementation
      ↓
Validation
      ↓
Use
      ↓
Revision
```

Prompt behavior SHALL remain governed throughout its lifecycle.

---

# 9. Compliance

A project complies with this standard when its prompt engineering practices satisfy the requirements defined herein.

Compliance SHALL be verified during architecture reviews, AI assessments, safety reviews, governance reviews, engineering audits, and DunderCode Assessment Reports (DAR).

---

# 10. Relationship with Other AI Standards

Prompt Engineering establishes the foundation for all AI-related standards within DESys.

| Standard | Discipline                 |
| -------- | -------------------------- |
| DES-0900 | AI Engineering Principles  |
| DES-0910 | Prompt Engineering         |
| DES-0920 | Knowledge Engineering      |
| DES-0930 | Model Lifecycle Management |
| DES-0940 | AI Evaluation              |
| DES-0950 | AI Safety                  |
| DES-0960 | Human Oversight            |
| DES-0970 | AI Operations              |
| DES-0980 | AI Governance              |

Together, these standards define the AI Engineering Model adopted by DESys.

---

# 11. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES-0900 — AI Engineering Principles
* DES-0940 — AI Evaluation Standard
* DES-0950 — AI Safety Standard

---

# 12. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial Prompt Engineering Standard.
* Defined foundational engineering principles for prompt design.
* Established mandatory requirements for prompts and prompt templates.
* Introduced the Prompt Engineering Lifecycle.
* Defined the relationship between Prompt Engineering and the remaining AI Standards.
