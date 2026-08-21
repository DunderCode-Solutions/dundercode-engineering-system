---
metadata_schema: 1.0.0
document_id: DSK-0020
canonical_id: dsk.foundation.agent-navigation
title: Agent Navigation
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-0020 | Agent Navigation

# 1. Purpose

This document defines the standard navigation strategy used by AI agents operating inside the DunderCode Engineering System (DESys).

Rather than relying on implicit model knowledge, every engineering task should begin by discovering and consuming the appropriate DESys documentation.

Agent Navigation standardizes how engineering knowledge is located, traversed and consumed.

---

# 2. Navigation Philosophy

DESys follows the principle:

> Never answer from memory when engineering knowledge exists.

Every engineering decision should originate from canonical documentation.

The agent should always prefer:

Engineering Documentation

over

Model Memory.

---

# 3. Navigation Layers

Navigation occurs through successive layers.

```text
User Request

↓

Intent Detection

↓

Skill Selection

↓

Knowledge Discovery (DSP)

↓

Document Selection

↓

Knowledge Consumption

↓

Engineering Reasoning

↓

Validation

↓

Engineering Deliverable
```

Each layer has a distinct responsibility.

---

# 4. Intent Detection

The first responsibility of the agent is understanding user intent.

Typical intents include:

* architecture
* implementation
* documentation
* testing
* deployment
* review
* governance
* prompt engineering

Intent detection determines which skill should be activated.

---

# 5. Skill Selection

Once intent is identified, the appropriate DSK Skill is selected.

Examples:

| Intent              | Skill              |
| ------------------- | ------------------ |
| Architecture Design | Architecture Skill |
| Create PRD          | Requirements Skill |
| Code Review         | Review Skill       |
| API Design          | API Skill          |

Skills should remain specialized and reusable.

---

# 6. Knowledge Discovery

Skills never search documentation directly.

Instead they delegate discovery to the Documentation Portal (DSP).

DSP identifies:

* relevant libraries;
* canonical documents;
* related references;
* dependency chains.

---

# 7. Canonical Navigation

Navigation is always performed using Canonical IDs.

Example:

```text
des.ai.prompt-engineering

↓

dep.process.requirements

↓

det.template.prd
```

Canonical navigation guarantees deterministic engineering reasoning.

---

# 8. Dependency Traversal

Agents may traverse document dependencies.

Example:

```text
Architecture Review

↓

dea.architecture.review

↓

depends_on

↓

dep.process.architecture

↓

depends_on

↓

des.architecture.principles
```

Dependencies provide complete engineering context.

---

# 9. Knowledge Consumption

After locating documentation, the agent consumes knowledge in the following order:

1. Required documents
2. Supporting documents
3. Related documents
4. Optional references

Mandatory engineering knowledge always takes precedence.

---

# 10. Validation

Before producing outputs the agent verifies:

* required documents were consulted;
* engineering processes were respected;
* templates were applied;
* architectural constraints were satisfied;
* reasoning remains consistent.

Validation is mandatory.

---

# 11. Navigation Constraints

Agents should never:

* invent engineering standards;
* bypass required documentation;
* ignore canonical references;
* replace DESys knowledge with model assumptions.

Whenever documentation exists, documentation becomes the source of truth.

---

# 12. Fallback Strategy

If required documentation cannot be located, the agent should:

1. report missing knowledge;
2. identify missing dependencies;
3. request clarification if necessary;
4. avoid unsupported engineering conclusions.

Engineering uncertainty must be explicit.

---

# 13. Navigation Principles

Every agent should follow:

* Documentation First
* Skill Before Reasoning
* Canonical Navigation
* Explicit Dependencies
* Deterministic Knowledge Routing
* Engineering Traceability
* Human Review Friendly

---

# 14. Expected Outcomes

Following this navigation strategy enables AI agents to:

* locate the correct engineering knowledge;
* minimize hallucinations;
* produce deterministic outputs;
* maintain consistency across DESys;
* remain independent from any AI vendor;
* generate engineering artifacts aligned with organizational standards.

Agent Navigation represents the standardized entry point into the DESys knowledge ecosystem.
