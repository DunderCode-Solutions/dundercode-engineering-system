# DSK-0050 | Prompt Construction

## Metadata

Document Number: DSK-0050

Canonical ID: dsk.foundation.prompt-construction

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This document defines how AI agents construct their internal execution prompts after completing knowledge discovery, context loading and knowledge resolution.

Prompt Construction is not responsible for discovering engineering knowledge.

Instead, it transforms an already validated engineering context into an executable reasoning plan.

The objective is to produce deterministic, explainable and reproducible AI behavior.

---

# 2. Prompt Construction Philosophy

DESys follows one fundamental principle:

> Prompts are generated from engineering knowledge, never from assumptions.

The prompt is the final representation of an already validated engineering context.

Engineering documentation always precedes prompt generation.

---

# 3. Construction Pipeline

Every execution follows the same construction sequence.

```text
User Request

↓

Intent Detection

↓

Skill Selection

↓

Knowledge Discovery

↓

Context Loading

↓

Knowledge Resolution

↓

Prompt Construction

↓

AI Reasoning

↓

Engineering Deliverable
```

Prompt Construction is therefore the last preparation stage before reasoning begins.

---

# 4. Prompt Components

Every execution prompt is composed of independent sections.

```text
Execution Prompt

├── Objective

├── Engineering Context

├── Constraints

├── Required Knowledge

├── Execution Instructions

├── Validation Rules

└── Expected Deliverables
```

Each component has a single responsibility.

---

# 5. Objective

The Objective describes what the agent must accomplish.

It should be:

* explicit;
* measurable;
* deterministic;
* engineering-oriented.

Objectives should never contain implementation details.

---

# 6. Engineering Context

The Engineering Context contains all resolved knowledge required for execution.

Typical elements include:

* project information;
* architecture;
* engineering processes;
* templates;
* engineering standards;
* project constraints.

Only validated knowledge should appear in this section.

---

# 7. Constraints

Constraints define execution boundaries.

Examples include:

* technology stack;
* architectural decisions;
* project rules;
* coding standards;
* regulatory requirements;
* user-specific restrictions.

Constraints always override general recommendations.

---

# 8. Required Knowledge

Every prompt explicitly references the engineering documentation used during construction.

Example:

```yaml
knowledge:

  required:

    - des.ai.prompt-engineering

    - dea.architecture.patterns

    - dep.process.testing

    - det.template.api
```

Prompt construction never duplicates engineering documentation.

It references canonical knowledge.

---

# 9. Execution Instructions

Execution Instructions describe how reasoning should occur.

Typical instructions include:

* analyze;
* compare;
* generate;
* validate;
* review;
* summarize;
* propose;
* explain.

Instructions should remain implementation independent.

---

# 10. Validation Rules

Every prompt includes explicit validation criteria.

Typical validations include:

* engineering process compliance;
* architecture consistency;
* template usage;
* standards compliance;
* output completeness.

Reasoning should never bypass validation.

---

# 11. Expected Deliverables

Prompt Construction explicitly defines expected outputs.

Examples include:

* PRD
* ADR
* RFC
* Architecture Review
* API Specification
* Test Plan
* Deployment Guide

Deliverables should be objective and verifiable.

---

# 12. Prompt Principles

Prompt Construction follows these principles:

* Documentation First
* Explicit Context
* Deterministic Reasoning
* Minimal Prompt
* Canonical References
* Structured Instructions
* Engineering Traceability
* Human Review Friendly

---

# 13. Vendor Independence

Prompt Construction is independent of any specific AI platform.

The generated reasoning structure should remain consistent across:

* ChatGPT
* Claude
* Gemini
* Cursor
* GitHub Copilot
* Semantic Kernel
* future AI execution engines

Execution syntax may vary.

Engineering intent must remain identical.

---

# 14. Anti-Patterns

Prompt Construction should avoid:

* embedding duplicated engineering knowledge;
* relying on undocumented assumptions;
* excessively large prompts;
* mixing unrelated engineering contexts;
* bypassing the Knowledge Resolution process;
* replacing canonical references with free-text explanations.

Prompt quality depends on engineering quality rather than prompt length.

---

# 15. Expected Outcomes

Following this strategy enables AI agents to:

* construct deterministic execution prompts;
* maximize engineering consistency;
* reduce hallucinations;
* improve explainability;
* preserve traceability to canonical documentation;
* maintain vendor-independent engineering reasoning.

Prompt Construction represents the final preparation layer before AI reasoning begins within the DESys execution pipeline.
