# DunderCode Skills (DSK)

The **DunderCode Skills (DSK)** library defines the operational intelligence layer of the **DunderCode Engineering System (DESys)**.

While the DESys engineering libraries define standards, architecture, processes, templates and governance, the DSK library defines **how AI agents should consume and execute that engineering knowledge**.

A DSK Skill is **not** a prompt.

A DSK Skill is a reusable engineering capability that combines:

* knowledge routing;
* reasoning workflows;
* execution rules;
* validation criteria;
* quality gates;
* engineering best practices.

The DSK library enables deterministic, reusable and vendor-independent AI execution.

---

# Purpose

The DSK library exists to:

* standardize AI engineering behavior;
* provide reusable engineering capabilities;
* minimize hallucinations through explicit knowledge routing;
* maximize engineering consistency;
* support modular AI reasoning;
* remain independent from any specific AI platform.

---

# DSK Inside DESys

The DSK library operates as the execution layer of the DESys ecosystem.

```text
                 DESys

Engineering Knowledge Libraries

DES
DAR
DEA
DEP
DET

        │

        ▼

Documentation Portal (DSP)

Knowledge Discovery

        │

        ▼

DunderCode Skills (DSK)

AI Execution Layer

        │

        ▼

Engineering Deliverables
```

Engineering documentation defines **what** exists.

The DSP defines **where** knowledge can be found.

The DSK defines **how** engineering knowledge should be executed.

---

# Library Organization

| Document | Description               |
| -------- | ------------------------- |
| DSK-0000 | Skill System Overview     |
| DSK-0010 | Skill Architecture        |
| DSK-0020 | Skill Lifecycle           |
| DSK-0030 | Knowledge Routing         |
| DSK-0040 | Prompt Engineering Skills |
| DSK-0050 | Engineering Review Skills |
| DSK-0060 | Development Skills        |
| DSK-0070 | AI Collaboration Patterns |
| DSK-0080 | Skill Governance          |

---

# What is a Skill?

Within DESys, a Skill is an executable engineering specification.

Every Skill defines:

* its purpose;
* activation criteria;
* required engineering knowledge;
* execution workflow;
* validation rules;
* completion criteria;
* expected engineering outputs.

Skills orchestrate engineering knowledge rather than duplicating it.

---

# Skill Principles

Every DSK Skill follows the same engineering principles:

* Single Responsibility
* Explicit Knowledge Routing
* Canonical References
* Modular Composition
* Deterministic Execution
* Engineering Traceability
* Human Review Friendly
* Vendor Independence

These principles guarantee consistent AI behavior across projects and platforms.

---

# Relationship with Other Libraries

The DSK library consumes knowledge from the entire DESys ecosystem.

| Library | Responsibility           |
| ------- | ------------------------ |
| DES     | Engineering Standards    |
| DAR     | Engineering Assessments  |
| DEA     | Architecture Engineering |
| DEP     | Engineering Processes    |
| DET     | Engineering Templates    |
| DSP     | Documentation Discovery  |
| DSK     | AI Execution             |

---

# Recommended Reading Order

AI agents and engineers should explore the DSK library in the following order:

1. DSK-0000 — Skill System Overview
2. DSK-0010 — Skill Architecture
3. DSK-0020 — Skill Lifecycle
4. DSK-0030 — Knowledge Routing
5. Specialized Skills (DSK-0040 onward)

This sequence provides a consistent understanding of the DSK architecture before introducing specialized engineering capabilities.

---

# Target Audience

The DSK library is intended for:

* AI Agents
* Software Engineers
* Software Architects
* Technical Leads
* Engineering Managers
* AI Platform Developers
* Engineering Teams adopting DESys

---

# Engineering Philosophy

Engineering knowledge should remain centralized.

Skills should remain reusable.

AI execution should remain deterministic.

The DSK library never replaces engineering documentation.

Instead, it transforms engineering knowledge into reusable execution capabilities while preserving traceability, maintainability and long-term governance.

---

# Vendor Independence

The DSK architecture is platform agnostic.

Skills are designed to execute consistently across multiple AI ecosystems, including:

* ChatGPT
* Claude
* Gemini
* Cursor
* GitHub Copilot
* Microsoft Semantic Kernel
* Future LLM platforms

Execution engines may evolve.

Engineering reasoning must remain stable.

---

# Related Libraries

* DES — Engineering Standards
* DAR — Engineering Assessments
* DEA — Architecture Engineering
* DEP — Engineering Processes
* DET — Engineering Templates
* DSP — Documentation Portal

Together these libraries form the complete **DunderCode Engineering System (DESys)**, providing a unified, modular and scalable engineering framework for both humans and AI agents.
