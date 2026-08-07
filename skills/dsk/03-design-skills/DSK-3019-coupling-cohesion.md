# DSK-3019 | Coupling & Cohesion

## Metadata

**Document Number:** DSK-3019

**Canonical ID:** dsk.design.coupling-cohesion

**Engineering Domain:** Design Engineering

**Engineering Discipline:** Structural Relationship Engineering

**Document Class:** Engineering Skill

**Version:** 2.0.0

**Status:** Canonical

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines the **Structural Relationship Engineering** model adopted by the DunderCode Engineering System (DESys).

Within DESys, coupling and cohesion are measurable engineering properties rather than subjective design guidelines.

The purpose of this skill is to evaluate the structural quality of relationships between software elements and provide objective indicators that support architectural evolution and governance.

---

# 2. Scope

This specification governs:

* Coupling Analysis
* Cohesion Analysis
* Structural Relationships
* Dependency Quality
* Relationship Metrics
* Architectural Recommendations
* Structural Traceability

---

# 3. Engineering Position

Structural Relationship Engineering evaluates how software elements collaborate.

```text id="relationship-flow"
Software Elements
        ↓
Relationships
        ↓
Coupling Analysis
        ↓
Cohesion Analysis
        ↓
Structural Relationship Index
        ↓
Architectural Recommendations
```

Unlike Modularity Engineering, which evaluates modules as architectural units, Structural Relationship Engineering evaluates the quality of the relationships between those units.

---

# 4. Engineering Objectives

Structural Relationship Engineering aims to:

* maximize cohesion;
* minimize unnecessary coupling;
* preserve architectural boundaries;
* improve maintainability;
* simplify evolution;
* enable AI-assisted architectural reasoning.

---

# 5. Cohesion Model

DESys evaluates multiple cohesion dimensions.

Typical dimensions include:

* Structural Cohesion
* Behavioral Cohesion
* Semantic Cohesion
* Functional Cohesion
* Data Cohesion

Higher cohesion indicates that software elements collaborate toward a single business responsibility.

---

# 6. Coupling Model

DESys evaluates multiple coupling dimensions.

Typical coupling categories include:

* Content Coupling
* Common Coupling
* External Coupling
* Control Coupling
* Data Coupling

Lower coupling improves modularity and independent evolution.

---

# 7. Cohesion Index (CI)

Each architectural element SHALL receive a Cohesion Index.

Example:

```yaml id="cohesion-index"
module:

  Customer

cohesion:

  structural: 92

  behavioral: 90

  semantic: 95

overall:

  92
```

The Cohesion Index represents internal architectural consistency.

---

# 8. Coupling Index (CPI)

Each architectural element SHALL receive a Coupling Index.

Example:

```yaml id="coupling-index"
module:

  Customer

coupling:

  content: 0

  control: 5

  external: 8

  data: 12

overall:

  25
```

The Coupling Index represents external dependency intensity.

---

# 9. Structural Relationship Index (SRI)

DESys defines the **Structural Relationship Index (SRI)**.

The SRI combines:

* Cohesion Index
* Coupling Index

The resulting score reflects the overall structural quality of an architectural element.

Possible classifications include:

| Classification | Meaning                 |
| -------------- | ----------------------- |
| A              | Excellent               |
| B              | Good                    |
| C              | Acceptable              |
| D              | Refactoring Recommended |

---

# 10. Coupling Knowledge Graph (CKG)

DESys represents dependencies through a semantic Coupling Knowledge Graph.

Example:

```text id="coupling-graph"
Customer Module
        │ depends on
        ▼
Billing Module
        │ depends on
        ▼
Payment Module
        │ depends on
        ▼
Accounting Module
```

The Coupling Knowledge Graph enables:

* dependency navigation;
* impact analysis;
* architectural reasoning;
* AI context retrieval.

---

# 11. Cohesion Knowledge Graph (CHG)

DESys represents internal module composition through a semantic Cohesion Knowledge Graph.

Example:

```text id="cohesion-graph"
Customer Module
        │ owns
        ▼
Customer Aggregate
        │ owns
        ▼
Customer Policy
        │ owns
        ▼
Customer Repository
        │ owns
        ▼
Customer Service
```

The Cohesion Knowledge Graph evaluates whether responsibilities remain properly grouped.

---

# 12. Engineering Rules

Architectural elements MUST:

* maximize cohesion;
* minimize unnecessary coupling;
* expose explicit contracts;
* preserve architectural boundaries.

Architectural elements MUST NOT:

* introduce hidden dependencies;
* accumulate unrelated responsibilities;
* depend unnecessarily on implementation details.

---

# 13. Architectural Anti-patterns

DESys explicitly discourages:

* God Objects
* Feature Scattering
* Shotgun Surgery
* Circular Dependencies
* Hidden Coupling
* Semantic Fragmentation

These anti-patterns reduce structural quality and architectural maintainability.

---

# 14. AI Architectural Recommendations

Structural Relationship Engineering SHALL produce automated recommendations.

Example:

```text id="recommendation"
Billing Module

Coupling Index: 71

Recommendation:

- Extract Payment Service

- Reduce Direct Dependencies

- Introduce Service Contract
```

Recommendations SHALL remain deterministic and traceable.

---

# 15. Inputs

Typical inputs include:

* Module Registry
* Module Knowledge Graph
* Dependency Graph
* Service Registry
* Architecture Documentation

---

# 16. Outputs

Typical deliverables include:

* Cohesion Report
* Coupling Report
* Structural Relationship Index
* Coupling Knowledge Graph
* Cohesion Knowledge Graph
* Engineering Recommendations
* Traceability Report

---

# 17. Execution Workflow

1. Analyze structural relationships.
2. Measure cohesion.
3. Measure coupling.
4. Calculate Cohesion Index.
5. Calculate Coupling Index.
6. Calculate Structural Relationship Index.
7. Update structural knowledge graphs.
8. Produce architectural recommendations.

---

# 18. Validation

Before completion the skill verifies:

* cohesion remains acceptable;
* coupling remains controlled;
* architectural boundaries are preserved;
* structural metrics remain valid;
* engineering traceability is complete.

---

# 19. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3017 Package Organization
* DSK-3018 Modularity

---

# 20. Collaboration

The Coupling & Cohesion Skill collaborates with:

* Architecture Engineering
* Quality Engineering
* Software Construction
* Integration Engineering
* AI Reasoning Engine

Structural Relationship Engineering provides continuous evaluation of architectural relationships throughout DESys.

---

# 21. Expected Outcomes

After execution, the Coupling & Cohesion Skill should provide:

* measurable structural quality;
* explicit relationship governance;
* architectural recommendations;
* semantic relationship knowledge;
* AI-assisted structural analysis;
* complete engineering traceability.

Structural Relationship Engineering establishes the continuous evaluation model for software relationships adopted by DESys, ensuring that architectural elements remain cohesive, loosely coupled, semantically consistent and continuously governed throughout the entire software engineering lifecycle.
