# DSK-3021 | Code Smells

## Metadata

**Document Number:** DSK-3021

**Canonical ID:** dsk.design.code-smells

**Engineering Domain:** Design Engineering

**Engineering Discipline:** Engineering Smell Detection

**Document Class:** Engineering Skill

**Version:** 3.0.0

**Status:** Canonical

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines the **Engineering Smell Detection** model adopted by the DunderCode Engineering System (DESys).

Within DESys, smells are not limited to source code.

An Engineering Smell is any measurable symptom indicating deterioration of software quality, architectural consistency, business semantics or engineering knowledge.

Engineering Smell Detection provides the diagnostic layer that continuously monitors the health of engineering artifacts.

---

# 2. Scope

This specification governs:

* Engineering Smells
* Smell Detection
* Smell Classification
* Smell Severity
* Smell Registry
* Engineering Diagnostics
* Evolution Recommendations

---

# 3. Engineering Position

Engineering Smell Detection continuously analyzes engineering artifacts.

```text
Engineering Artifacts
        ↓
Pattern Detection
        ↓
Engineering Smells
        ↓
Severity Analysis
        ↓
Engineering Recommendations
        ↓
Evolution Planning
```

Smells become measurable engineering evidence.

---

# 4. Engineering Objectives

Engineering Smell Detection aims to:

* detect engineering degradation;
* preserve architectural quality;
* identify structural weaknesses;
* support evidence-driven evolution;
* improve maintainability;
* enable AI-assisted diagnostics.

---

# 5. Engineering Smell Categories

DESys classifies smells into multiple engineering domains.

## Code Smells

Examples include:

* Long Method
* Large Class
* Duplicate Code
* Feature Envy
* Primitive Obsession

---

## Contract Smells

Examples include:

* Fat Interface
* Leaky Contract
* Contract Drift
* Semantic Inconsistency
* Unstable Contract

---

## Service Smells

Examples include:

* God Service
* Chatty Service
* Cyclic Service
* Anemic Service
* Service Explosion

---

## Module Smells

Examples include:

* God Module
* Module Explosion
* Boundary Violation
* Shared Everything
* Circular Modules

---

## Architecture Smells

Examples include:

* Circular Dependencies
* Layer Violation
* Hidden Dependency
* Infrastructure Leakage
* Architecture Drift

---

## Domain Smells

Examples include:

* Wrong Aggregate
* Missing Domain Event
* Anemic Domain
* Broken Ubiquitous Language
* Invalid Business Boundary

---

## Knowledge Smells

Examples include:

* Knowledge Duplication
* Missing Traceability
* Orphan Artifact
* Registry Drift
* Knowledge Inconsistency

---

# 6. Engineering Smell Catalog (ESC)

DESys maintains a canonical Engineering Smell Catalog.

Each smell SHALL define:

* Canonical Identifier
* Category
* Description
* Detection Heuristics
* Severity
* Related Metrics
* Evolution Strategies
* Traceability References

The Engineering Smell Catalog becomes the authoritative reference for engineering diagnostics.

---

# 7. Smell Registry (SR)

Detected smells SHALL be stored within the Smell Registry.

Example:

```yaml
id:

  SMELL-102

category:

  Architecture

artifact:

  Billing Module

severity:

  High

status:

  Active

recommendation:

  Extract Payment Service
```

The Smell Registry preserves the complete diagnostic history of the project.

---

# 8. Smell Knowledge Graph (SKG)

DESys represents smells through a semantic Smell Knowledge Graph.

Example:

```text
Billing Module
        │ exhibits
        ▼
God Module
        │ recommends
        ▼
Extract Module
```

The Smell Knowledge Graph supports:

* dependency analysis;
* architectural diagnostics;
* AI reasoning;
* engineering navigation;
* impact analysis.

---

# 9. Smell Severity

Engineering Smells SHALL be classified according to severity.

Possible levels include:

| Severity | Meaning                                     |
| -------- | ------------------------------------------- |
| Low      | Minor improvement opportunity               |
| Medium   | Recommended improvement                     |
| High     | Significant architectural risk              |
| Critical | Immediate engineering intervention required |

Severity SHALL be supported by engineering evidence.

---

# 10. Detection Pipeline

Engineering Smell Detection follows a deterministic pipeline.

```text
Artifact
        ↓
Pattern Detection
        ↓
Smell Classification
        ↓
Severity Analysis
        ↓
Recommendation
        ↓
Evolution Planning
```

Every detected smell SHALL produce traceable engineering evidence.

---

# 11. Engineering Rules

Engineering Smells MUST:

* be measurable;
* remain reproducible;
* reference explicit engineering evidence;
* support architectural evolution.

Engineering Smells MUST NOT:

* rely on subjective opinions;
* generate inconsistent diagnostics;
* violate traceability.

---

# 12. Inputs

Typical inputs include:

* Source Code
* Software Contracts
* Service Registry
* Module Registry
* Knowledge Graphs
* Architecture Health Dashboard
* Engineering Metrics

---

# 13. Outputs

Typical deliverables include:

* Engineering Smell Report
* Smell Registry
* Smell Knowledge Graph
* Severity Report
* Engineering Recommendations
* Evolution Triggers

---

# 14. Execution Workflow

1. Analyze engineering artifacts.
2. Detect structural patterns.
3. Identify engineering smells.
4. Classify severity.
5. Register findings.
6. Produce engineering recommendations.
7. Update the Smell Knowledge Graph.
8. Trigger Engineering Evolution when necessary.

---

# 15. Validation

Before completion the skill verifies:

* smells are measurable;
* engineering evidence exists;
* severity is justified;
* recommendations are deterministic;
* engineering traceability is preserved.

---

# 16. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3020 Refactoring

---

# 17. Collaboration

The Code Smells Skill collaborates with:

* Architecture Engineering
* Software Construction
* Quality Engineering
* Engineering Evolution
* AI Reasoning Engine

Engineering Smell Detection provides the diagnostic foundation for continuous software evolution.

---

# 18. Expected Outcomes

After execution, the Code Smells Skill should provide:

* comprehensive engineering diagnostics;
* measurable degradation indicators;
* explicit engineering evidence;
* deterministic AI recommendations;
* complete smell traceability;
* automated evolution triggers.

Engineering Smell Detection establishes the diagnostic model adopted by DESys, enabling continuous identification, classification and governance of engineering degradation across code, contracts, services, modules, architecture, domain knowledge and semantic artifacts throughout the entire software engineering lifecycle.
