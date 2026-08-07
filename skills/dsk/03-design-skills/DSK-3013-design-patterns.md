# DSK-3013 | Design Patterns

## Metadata

**Document Number:** DSK-3013

**Canonical ID:** dsk.design.design-patterns

**Document Class:** Engineering Skill

**Version:** 1.0.0

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

---

# 1. Purpose

This skill defines the engineering methodology used by DESys AI agents to evaluate, justify, select and govern Design Patterns.

Within DESys, Design Patterns are engineering decisions.

They are not implementation goals.

They are not architectural replacements.

They are reusable engineering solutions applied only after a recurring software design problem has been identified.

---

# 2. Scope

This specification governs:

* Pattern Engineering
* Pattern Selection
* Pattern Evaluation
* Pattern Justification
* Pattern Documentation
* Pattern Governance
* Pattern Traceability

---

# 3. Engineering Position

Patterns refine software design.

They do not define:

* business behavior;
* software architecture;
* object-oriented modeling.

```text id="engpat01"
Business

↓

Domain

↓

Architecture

↓

OOD

↓

Pattern Engineering

↓

Implementation
```

Patterns improve software structures while preserving the previous engineering layers.

---

# 4. Engineering Objectives

Pattern Engineering aims to:

* solve recurring software design problems;
* improve maintainability;
* improve extensibility;
* improve readability;
* standardize engineering decisions;
* preserve engineering consistency.

---

# 5. Engineering Decision Process

Pattern selection SHALL follow the Engineering Decision Process.

```text id="engpat02"
Engineering Problem

↓

Engineering Analysis

↓

Candidate Patterns

↓

Trade-off Analysis

↓

Engineering Decision

↓

Documentation

↓

Validation
```

Patterns SHALL NOT be selected directly.

The engineering problem MUST always be evaluated first.

---

# 6. Pattern Categories

DESys classifies patterns into:

### Creational

Object creation.

### Structural

Software organization.

### Behavioral

Object interaction.

The complete catalog of patterns is implementation-specific and maintained separately from this skill.

---

# 7. Pattern Decision Matrix (PDM)

Every adopted pattern SHALL produce a Pattern Decision Matrix.

Example:

```yaml id="pdm02"
problem:

  Runtime Algorithm Selection

candidate_patterns:

  - Strategy

  - State

selected_pattern:

  Strategy

engineering_reason:

  Algorithms vary independently

business_reason:

  Pricing policy changes

tradeoffs:

  Additional abstraction

affected_components:

  PricingService
```

The PDM becomes part of the Engineering Knowledge Base.

---

# 8. Pattern Knowledge Graph (PKG)

DESys represents Pattern Engineering as a semantic graph.

Example:

```text id="engpat03"
PricingService

↓

uses

↓

Strategy

↓

solves

↓

Runtime Algorithm Selection

↓

related_to

↓

Dependency Injection
```

The PKG supports:

* engineering reasoning;
* dependency analysis;
* AI context retrieval;
* impact analysis;
* software evolution.

---

# 9. Engineering Rules

Patterns MUST:

* solve a validated engineering problem;
* preserve domain clarity;
* preserve architectural consistency;
* improve maintainability.

Patterns MUST NOT:

* compensate for poor architecture;
* compensate for poor object-oriented design;
* introduce unnecessary abstraction;
* be selected because they are popular.

---

# 10. Engineering Trade-offs

Every engineering decision SHALL document:

* benefits;
* disadvantages;
* implementation cost;
* maintenance cost;
* architectural impact;
* domain impact.

Engineering trade-offs become part of the Pattern Decision Matrix.

---

# 11. Inputs

Typical inputs include:

* Object Model
* Architecture Documentation
* Design Principles
* SOLID Assessment
* Existing Software Design

---

# 12. Outputs

Typical deliverables include:

* Pattern Decision Matrix
* Pattern Knowledge Graph
* Engineering Decision Record
* Pattern Traceability

---

# 13. Execution Workflow

1. Review software design.
2. Identify recurring engineering problems.
3. Evaluate candidate patterns.
4. Compare engineering trade-offs.
5. Select the engineering solution.
6. Produce Pattern Decision Matrix.
7. Update Pattern Knowledge Graph.
8. Validate engineering consistency.

---

# 14. Validation

Before completion the skill verifies:

* engineering problem is explicit;
* selected pattern addresses the problem;
* trade-offs are documented;
* architecture remains consistent;
* domain clarity is preserved;
* engineering traceability is preserved.

---

# 15. Dependencies

## Parent Skill

* DSK-3000 Design Skills Overview

## Foundation Skills

* DSK-3010 Design Principles
* DSK-3011 SOLID Principles
* DSK-3012 Object-Oriented Design

---

# 16. Collaboration

The Design Patterns Skill collaborates with:

* Dependency Injection
* Refactoring
* Package Organization
* Modularity
* Architecture Engineering

Pattern Engineering provides reusable engineering decisions while preserving software consistency.

---

# 17. Expected Outcomes

After execution, the Design Patterns Skill should provide:

* justified engineering decisions;
* reusable software solutions;
* documented trade-offs;
* standardized pattern selection;
* semantic pattern knowledge;
* complete engineering traceability.

The Design Patterns Skill establishes the Pattern Engineering process of DESys by ensuring that reusable software solutions are selected through explicit engineering analysis, documented decision-making and complete semantic traceability rather than by convention or familiarity alone.
