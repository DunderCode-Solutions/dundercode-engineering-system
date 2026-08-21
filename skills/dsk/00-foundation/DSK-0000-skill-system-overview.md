---
metadata_schema: 1.0.0
document_id: DSK-0000
canonical_id: dsk.foundation.skill-system-overview
title: Skill System Overview
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-0000 | Skill System Overview

# 1. Purpose

The DunderCode Skills (DSK) library defines the operational intelligence layer of the DunderCode Engineering System (DESys).

While engineering documentation describes standards, architectures, processes and templates, DSK defines **how AI agents should consume and execute that knowledge**.

A skill is not a prompt.

A skill is an executable reasoning specification.

It determines:

* what the agent must accomplish;
* when the skill should be activated;
* which engineering knowledge must be consulted;
* how reasoning should occur;
* which validations must be performed;
* what constitutes a successful result.

The DSK library transforms static engineering documentation into reusable AI capabilities.

---

# 2. AI Runtime Layer

DESys separates engineering knowledge from AI execution.

Engineering documentation defines **what exists**.

The Documentation Portal (DSP) defines **where knowledge can be found**.

The Skills library (DSK) defines **how knowledge should be consumed**.

Together they form the complete AI Engineering Runtime.

```text
Engineering Knowledge
        │
        ▼
Documentation Portal (DSP)
        │
Knowledge Discovery
        │
        ▼
DunderCode Skills (DSK)
        │
AI Reasoning
        │
        ▼
Engineering Deliverables
```

---

# 3. Objectives

The DSK library aims to:

* standardize AI reasoning;
* provide deterministic engineering workflows;
* reduce hallucinations through explicit knowledge routing;
* maximize reuse of engineering knowledge;
* separate engineering documentation from operational AI behavior;
* provide versioned and maintainable AI capabilities;
* enable consistent execution across different AI platforms.

---

# 4. Scope

DSK defines reusable engineering skills covering:

* software architecture;
* requirements engineering;
* software development;
* documentation;
* code review;
* testing;
* DevOps;
* governance;
* project management;
* AI engineering;
* domain-specific engineering activities.

The DSK library never replaces engineering documentation.

Instead, it orchestrates how documentation should be consumed.

---

# 5. Relationship with DESys

Each DESys library has a different responsibility.

| Library | Responsibility          |
| ------- | ----------------------- |
| DES     | Engineering standards   |
| DAR     | Engineering assessments |
| DEA     | Architecture knowledge  |
| DEP     | Engineering processes   |
| DET     | Engineering templates   |
| DSP     | Documentation discovery |
| DSK     | AI execution layer      |

---

# 6. Skill Architecture

Every skill follows the same architectural structure.

A skill defines:

* identity;
* purpose;
* activation criteria;
* required inputs;
* expected outputs;
* required engineering knowledge;
* execution workflow;
* reasoning strategy;
* validation rules;
* completion criteria.

Skills must remain modular, reusable and deterministic.

---

# 7. Skill Anatomy

Every DSK skill should contain the following components:

1. Identity
2. Purpose
3. Activation Criteria
4. Inputs
5. Outputs
6. Required Knowledge
7. Execution Workflow
8. Constraints
9. Validation Rules
10. Completion Criteria

This standardization guarantees consistent behavior across all engineering agents.

---

# 8. Knowledge Routing

A skill acts as an intelligent knowledge router.

Instead of embedding engineering knowledge, it determines:

* which DESys libraries must be consulted;
* which canonical documents are required;
* the order in which information should be consumed;
* validation checkpoints;
* expected engineering artifacts.

Knowledge routing minimizes duplicated information and simplifies long-term maintenance.

---

# 9. Knowledge Dependencies

Every skill explicitly declares its engineering dependencies.

Example:

```yaml
depends_on:

- des.ai.prompt-engineering

- dep.process.requirements

- det.template.prd
```

Dependency declarations enable:

* impact analysis;
* automatic validation;
* documentation traceability;
* skill maintenance;
* engineering governance.

---

# 10. Skill Composition

Skills may invoke other skills.

Complex engineering activities are built by composing smaller reusable capabilities.

Example:

```text
Create PRD

│

├── Requirements Skill

├── Architecture Skill

├── Template Skill

└── Review Skill
```

Skill composition promotes modularity, reuse and maintainability.

---

# 11. Skill Lifecycle

Every skill follows a controlled lifecycle.

1. Design
2. Review
3. Approval
4. Publication
5. Versioning
6. Continuous Improvement
7. Retirement

This lifecycle guarantees engineering quality and long-term maintainability.

---

# 12. Versioning

Skills are versioned independently from engineering documentation.

Engineering documentation may evolve without requiring immediate modifications to every skill.

Likewise, reasoning workflows may improve while consuming the same engineering knowledge.

This separation reduces maintenance costs and increases long-term stability.

---

# 13. Vendor Independence

The DSK library is platform agnostic.

Skills are designed to execute consistently across different AI ecosystems, including:

* ChatGPT
* Claude
* Gemini
* Cursor
* GitHub Copilot
* Semantic Kernel
* future LLM platforms

The execution engine may change.

Engineering reasoning must remain stable.

---

# 14. Design Principles

The DSK library follows the following principles:

* Single Responsibility
* Explicit Knowledge Routing
* Canonical References
* Modular Skills
* Reusable Reasoning
* Version Independence
* Deterministic Execution
* Human Review Friendly
* AI Vendor Neutrality
* Engineering First

---

# 15. Expected Outcomes

The DSK library enables AI agents to:

* discover the correct engineering knowledge;
* execute standardized engineering workflows;
* generate deterministic outputs;
* maintain engineering consistency;
* reuse organizational knowledge;
* support engineering governance;
* continuously improve reasoning quality.

DSK represents the operational intelligence layer of the DunderCode Engineering System (DESys), bridging engineering knowledge and AI execution while remaining independent of any specific AI platform or execution engine.
