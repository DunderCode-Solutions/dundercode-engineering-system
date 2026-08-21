---
metadata_schema: 1.0.0
document_id: DSK-4011
canonical_id: dsk.software.coding-standards
title: Coding Standards
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Software Engineering
discipline: Engineering Coding Compliance
---

# DSK-4011 | Coding Standards

# 1. Purpose

This skill defines the **Engineering Coding Compliance (ECC)** model adopted by the DunderCode Engineering System (DESys).

Within DESys, coding standards are not formatting conventions.

They are engineering rules that ensure every software implementation preserves architecture, domain semantics, design decisions and engineering knowledge.

Every source file becomes an engineering artifact.

---

# 2. Scope

Engineering Coding Compliance governs:

* Source Code Standards
* Naming Standards
* Structural Standards
* Dependency Standards
* Documentation Standards
* Traceability Standards
* Implementation Consistency

---

# 3. Engineering Position

Coding Standards define how engineering knowledge is expressed through software.

```text id="coding-position"
Engineering Knowledge
        ↓
Coding Standards
        ↓
Source Code
        ↓
Executable Software
```

Source code SHALL faithfully represent approved engineering artifacts.

---

# 4. Engineering Objectives

Engineering Coding Compliance aims to:

* preserve engineering intent;
* standardize implementation;
* improve maintainability;
* simplify reviews;
* enable deterministic evolution;
* support AI-assisted analysis.

---

# 5. Engineering Coding Principles

Every implementation SHALL be:

* deterministic;
* readable;
* traceable;
* observable;
* composable;
* testable;
* evolvable.

Coding Standards exist to preserve engineering quality rather than personal coding preferences.

---

# 6. Engineering Standards

The following engineering standards SHALL be enforced.

## Naming Standards

Names SHALL:

* express business meaning;
* follow the ubiquitous language;
* avoid ambiguity;
* remain consistent across the project.

---

## Structural Standards

Source code SHALL preserve:

* architectural boundaries;
* module organization;
* layer separation;
* explicit responsibilities.

---

## Dependency Standards

Dependencies SHALL:

* be explicit;
* remain directional;
* avoid hidden coupling;
* preserve architectural integrity.

---

## Contract Standards

Implementations SHALL respect:

* software contracts;
* service contracts;
* public interfaces;
* versioning policies.

---

## Documentation Standards

Every engineering artifact SHALL contain sufficient documentation to support maintenance and AI reasoning.

---

## Traceability Standards

Every implementation SHALL maintain explicit links to:

* architecture decisions;
* design decisions;
* contracts;
* services;
* modules;
* reviews.

---

# 7. Engineering Coding Compliance (ECC)

DESys measures implementation quality through the Engineering Coding Compliance model.

Typical compliance dimensions include:

* Naming
* Structure
* Dependencies
* Contracts
* Documentation
* Traceability
* Complexity

The ECC score represents overall implementation compliance.

---

# 8. Source Code Registry (SCR)

Every implementation SHALL be represented within the Source Code Registry.

Example:

```yaml id="source-code-registry"
component:

  Customer Service

module:

  Customer

standard:

  ECC 2.0

status:

  Approved

review:

  CR-104
```

The Source Code Registry preserves implementation metadata.

---

# 9. Source Code Knowledge Graph (SCKG)

DESys represents implementation through the Source Code Knowledge Graph.

Example:

```text id="source-code-graph"
Coding Standard
        │ governs
        ▼
Source File
        │ belongs to
        ▼
Component
        │ belongs to
        ▼
Module
        │ assembled into
        ▼
Application
```

The Source Code Knowledge Graph enables:

* semantic navigation;
* engineering reasoning;
* dependency analysis;
* AI-assisted exploration.

---

# 10. Compliance Metrics

Typical Engineering Coding Compliance metrics include:

```yaml id="ecc-metrics"
compliance:

  98

naming:

  100

documentation:

  96

traceability:

  100

complexity:

  Low
```

All compliance metrics SHALL remain measurable.

---

# 11. AI-Assisted Compliance

AI MAY verify coding compliance automatically.

Typical automated checks include:

* naming consistency;
* architectural violations;
* dependency analysis;
* contract compliance;
* documentation quality;
* implementation traceability;
* structural complexity.

Recommendations SHALL remain deterministic and evidence-based.

---

# 12. Engineering Rules

Source code MUST:

* preserve engineering decisions;
* respect architecture;
* maintain explicit dependencies;
* remain reviewable;
* support deterministic evolution.

Source code MUST NOT:

* violate architectural boundaries;
* bypass contracts;
* introduce hidden dependencies;
* lose engineering traceability.

---

# 13. Inputs

Typical inputs include:

* Architecture Specifications
* Design Knowledge Network
* Software Contracts
* Module Definitions
* Engineering Policies
* Construction Knowledge Network

---

# 14. Outputs

Typical deliverables include:

* Source Code
* Compliance Report
* Source Code Registry
* Source Code Knowledge Graph
* Engineering Coding Compliance Score
* Implementation Traceability

---

# 15. Execution Workflow

1. Load engineering knowledge.
2. Apply coding standards.
3. Verify structural compliance.
4. Validate dependencies.
5. Verify contracts.
6. Calculate the Engineering Coding Compliance score.
7. Update engineering registries.
8. Publish compliant implementation artifacts.

---

# 16. Validation

Before completion the skill verifies:

* coding standards are satisfied;
* architecture remains preserved;
* dependencies remain explicit;
* contracts remain valid;
* traceability is complete;
* Engineering Coding Compliance is acceptable.

---

# 17. Dependencies

## Parent Skill

* DSK-4000 Software Engineering Overview

## Foundation Skills

* DSK-4010 Software Construction

Engineering Coding Compliance governs every implementation activity performed during Software Engineering.

---

# 18. Collaboration

The Coding Standards Skill collaborates with:

* Software Construction
* Security Engineering
* Quality Engineering
* Testing Engineering
* AI Reasoning Engine

Engineering Coding Compliance establishes the implementation quality model adopted by DESys.

---

# 19. Expected Outcomes

After execution, the Coding Standards Skill should provide:

* standardized engineering implementations;
* consistent software structure;
* preserved architectural integrity;
* measurable coding compliance;
* complete implementation traceability;
* AI-readable source code.

Engineering Coding Compliance concludes that every source file produced within DESys shall represent not only executable software, but also a faithful, traceable and governed expression of engineering knowledge accumulated throughout the Architecture, Domain and Design Engineering disciplines.
