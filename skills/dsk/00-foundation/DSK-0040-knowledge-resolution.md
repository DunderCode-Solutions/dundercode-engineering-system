---
metadata_schema: 1.0.0
document_id: DSK-0040
canonical_id: dsk.foundation.knowledge-resolution
title: Knowledge Resolution
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-0040 | Knowledge Resolution

# 1. Purpose

This document defines how AI agents resolve engineering knowledge within the DunderCode Engineering System (DESys).

Engineering knowledge may originate from multiple libraries, project documentation, generated artifacts and user requests.

Knowledge Resolution establishes deterministic rules for selecting the correct engineering source.

---

# 2. Resolution Philosophy

DESys follows one fundamental principle:

> Engineering decisions must always originate from the highest-authority canonical knowledge available.

Knowledge resolution prioritizes authoritative engineering documentation over model assumptions.

---

# 3. Resolution Pipeline

Every engineering request follows the same resolution process.

```text
User Request

↓

Context Loading

↓

Knowledge Sources

↓

Conflict Detection

↓

Priority Resolution

↓

Engineering Context

↓

Reasoning
```

---

# 4. Knowledge Sources

Knowledge may originate from:

* User Request
* Project Documentation
* DES Standards
* DAR Assessments
* DEA Architecture
* DEP Processes
* DET Templates
* DSP Documentation Portal
* DSK Skills
* Generated Engineering Artifacts

Each source has a predefined authority level.

---

# 5. Authority Hierarchy

When conflicts occur, knowledge is resolved according to the following priority.

| Priority | Source                    |
| -------- | ------------------------- |
| 1        | Explicit User Constraints |
| 2        | Project Documentation     |
| 3        | DET Templates             |
| 4        | DEP Processes             |
| 5        | DEA Architecture          |
| 6        | DES Standards             |
| 7        | DAR Assessments           |
| 8        | DSK Skills                |
| 9        | Model Internal Knowledge  |

Internal model knowledge should only be used when no canonical engineering knowledge exists.

---

# 6. Conflict Detection

Conflicts occur when two engineering sources provide incompatible guidance.

Typical examples include:

* different architecture patterns;
* conflicting process definitions;
* obsolete templates;
* project-specific overrides;
* outdated engineering standards.

Every detected conflict must be resolved explicitly.

---

# 7. Resolution Rules

The following rules apply:

1. Prefer project-specific documentation.
2. Prefer canonical DESys documents.
3. Prefer the newest approved document version.
4. Prefer documents with explicit governance.
5. Never merge conflicting engineering guidance implicitly.

---

# 8. Canonical Resolution

Canonical IDs are the primary mechanism for resolving engineering knowledge.

Agents should always resolve documentation through Canonical IDs rather than filenames or directory structures.

Example:

```text
dea.architecture.patterns

↓

Current Approved Version

↓

Engineering Context
```

---

# 9. Version Resolution

When multiple document versions exist:

* Approved versions take precedence.
* Stable releases take precedence over drafts.
* Drafts may be loaded only when explicitly requested.
* Deprecated documents should never be selected automatically.

---

# 10. Project Overrides

Projects may intentionally override DESys recommendations.

Such overrides must:

* be documented;
* be traceable;
* remain local to the project;
* never modify canonical DESys documentation.

Project overrides always require explicit justification.

---

# 11. Missing Knowledge

When required knowledge cannot be resolved, the agent should:

1. identify the missing document;
2. report the unresolved dependency;
3. avoid unsupported conclusions;
4. request clarification when appropriate.

Unknown knowledge must never be fabricated.

---

# 12. Resolution Principles

Knowledge Resolution follows these principles:

* Documentation First
* Canonical Authority
* Explicit Traceability
* Deterministic Selection
* Conflict Transparency
* Version Awareness
* Engineering Governance

---

# 13. Vendor Independence

Knowledge Resolution is independent of any AI platform.

Whether executed by ChatGPT, Claude, Gemini, Cursor, Copilot or future AI systems, the same engineering knowledge must be selected for identical inputs.

Execution engines may differ.

Knowledge resolution must remain identical.

---

# 14. Expected Outcomes

Applying these rules enables AI agents to:

* consistently resolve engineering knowledge;
* eliminate ambiguity between documentation sources;
* minimize hallucinations;
* preserve engineering governance;
* maintain reproducible engineering decisions;
* ensure every deliverable is grounded in authoritative DESys documentation.

Knowledge Resolution is the decision layer that guarantees engineering consistency across the entire DESys ecosystem.
