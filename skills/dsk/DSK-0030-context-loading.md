# DSK-0030 | Context Loading

## Metadata

Document Number: DSK-0030

Canonical ID: dsk.foundation.context-loading

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This document defines the standard context loading strategy used by AI agents operating within the DunderCode Engineering System (DESys).

Before any engineering reasoning begins, agents must construct an explicit, deterministic and minimal execution context.

The objective is to ensure that every engineering decision is based on the correct knowledge rather than implicit model memory.

---

# 2. Context Loading Philosophy

DESys follows one fundamental principle:

> Load only the knowledge required to solve the current engineering task.

Context should be:

* explicit;
* deterministic;
* minimal;
* traceable;
* reproducible.

Large context windows should never replace good engineering navigation.

---

# 3. Context Loading Pipeline

Every execution follows the same loading pipeline.

```text
User Request

↓

Intent Detection

↓

Skill Selection

↓

Knowledge Discovery (DSP)

↓

Dependency Resolution

↓

Context Assembly

↓

Engineering Reasoning
```

Each stage incrementally builds the execution context.

---

# 4. Context Sources

A complete engineering context may include information from:

* DES Engineering Standards
* DAR Assessments
* DEA Architecture
* DEP Processes
* DET Templates
* DSP Documentation Portal
* DSK Skills
* Project Documentation
* Generated Indexes
* User Request

All sources are treated as structured engineering knowledge.

---

# 5. Loading Priority

When multiple sources exist, they are loaded in the following order:

1. User Request
2. Active Skill
3. Required Canonical Documents
4. Required Dependencies
5. Supporting Documentation
6. Related Documents
7. Optional References

Mandatory engineering knowledge always has precedence.

---

# 6. Dependency Resolution

Dependencies should be recursively resolved.

Example:

```text
DET-PRD

↓

DEP Requirements Process

↓

DES Documentation Standards

↓

DEA Architecture Principles
```

The loading process stops when no additional required dependencies exist.

Circular dependencies must be detected and ignored.

---

# 7. Context Assembly

The execution context consists of four logical sections.

```text
Execution Context

├── User Intent

├── Active Skill

├── Engineering Knowledge

└── Constraints
```

Each section has a single responsibility.

---

# 8. Context Size

Agents should minimize unnecessary information.

The objective is not to maximize context size.

The objective is to maximize relevant engineering knowledge.

Unused documents should never be loaded.

---

# 9. Incremental Loading

Additional documentation should only be loaded when required.

Example:

```text
Architecture Review

↓

Architecture Documents

↓

Need Testing Information?

↓

Load DEP Testing Process

↓

Continue
```

Incremental loading reduces complexity while preserving reasoning quality.

---

# 10. Context Validation

Before reasoning begins, the agent verifies:

* required documents are available;
* dependencies were resolved;
* mandatory templates are present;
* engineering standards are accessible;
* active skill has sufficient knowledge.

Missing mandatory knowledge should interrupt execution.

---

# 11. Context Refresh

The context should be rebuilt whenever:

* user intent changes;
* active skill changes;
* project scope changes;
* new engineering artifacts become available.

Agents should avoid mixing obsolete context with current execution.

---

# 12. Engineering Constraints

Context loading must never:

* fabricate engineering knowledge;
* bypass required dependencies;
* ignore canonical references;
* overload the execution context with unrelated documentation.

Only relevant engineering knowledge should be loaded.

---

# 13. Design Principles

Context loading follows these principles:

* Documentation First
* Explicit Context
* Minimal Loading
* Incremental Expansion
* Deterministic Resolution
* Canonical References
* Dependency Awareness
* Engineering Traceability

---

# 14. Expected Outcomes

Following this strategy enables AI agents to:

* construct deterministic execution contexts;
* minimize hallucinations;
* improve engineering consistency;
* reduce unnecessary context size;
* maintain traceability across DESys;
* execute engineering workflows with predictable results.

Context Loading is the foundation upon which every DESys Skill performs reliable engineering reasoning.
