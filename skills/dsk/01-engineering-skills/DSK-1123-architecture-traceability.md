# DSK-1123 | Architecture Traceability

## Metadata

Document Number: DSK-1123

Canonical ID: dsk.engineering.architecture.architecture-traceability

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents establish, maintain and validate Architecture Traceability within the DunderCode Engineering System (DESys).

Architecture Traceability connects architectural artifacts with business objectives, requirements, engineering decisions and implementation elements, enabling complete impact analysis throughout the software lifecycle.

It preserves architectural continuity from business intent to software implementation.

---

# 2. Scope

This skill supports:

* Architecture Traceability
* Artifact Relationships
* Impact Analysis
* Dependency Mapping
* Architecture Governance
* Traceability Validation
* Traceability Reporting

---

# 3. Skill Objectives

The Architecture Traceability Skill aims to:

* preserve engineering continuity;
* support impact analysis;
* improve architectural governance;
* simplify architectural evolution;
* increase engineering transparency;
* enable end-to-end traceability.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* establish traceability;
* connect architectural artifacts;
* analyze architectural impact;
* validate engineering continuity;
* perform governance activities.

This skill normally executes after Architecture Review.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* User Stories
* Architecture Drivers
* Architecture Decision Records
* Domain Model
* Context Model
* Bounded Contexts
* Container Architecture
* Component Architecture
* Integration Architecture
* Data Architecture
* Infrastructure Architecture
* Architecture Review

---

# 6. Outputs

Typical deliverables include:

* Architecture Traceability Matrix
* Dependency Graph
* Impact Analysis Report
* Traceability Report
* Engineering Relationship Catalog

---

# 7. Required Knowledge

### Required

```yaml id="yrq4tm"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="itlgx5"
knowledge:
  optional:
    - dea.traceability
    - dea.impact-analysis
    - dea.software-governance
```

---

# 8. Execution Workflow

1. Collect engineering artifacts.
2. Identify artifact relationships.
3. Create traceability links.
4. Validate relationship consistency.
5. Detect missing traceability.
6. Produce dependency graph.
7. Generate impact analysis.
8. Publish the Architecture Traceability.

---

# 9. Engineering Guidelines

Architecture Traceability should:

* preserve end-to-end engineering relationships;
* avoid orphan architectural artifacts;
* support automated impact analysis;
* remain technology independent;
* evolve continuously throughout the project lifecycle;
* preserve engineering traceability.

Every significant architectural artifact should be traceable to its originating business motivation.

---

# 10. Typical Traceability Relationships

Typical relationships include:

* Business Goal → Requirement
* Requirement → Business Rule
* Requirement → User Story
* Requirement → Architecture Driver
* Architecture Driver → ADR
* ADR → Container
* ADR → Component
* Bounded Context → Container
* Container → Component
* Component → Integration
* Integration → Data Architecture
* Data Architecture → Infrastructure
* Architecture Review → ADR
* Architecture Review → Recommendations

Projects may extend these relationships according to organizational standards.

---

# 11. Traceability Structure

Each traceability relationship should include:

* Source Artifact
* Target Artifact
* Relationship Type
* Description
* Justification
* Status
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* all architectural artifacts are connected;
* orphan artifacts are identified;
* relationship consistency is preserved;
* impact analysis is possible;
* engineering traceability is complete.

---

# 13. Dependencies

### Parent Skill

* DSK-1100 Architecture Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 14. Collaboration

The Architecture Traceability Skill commonly collaborates with:

* Requirements Traceability
* Architecture Decision Records
* Architecture Review
* Engineering Governance
* Quality Assurance

Architecture Traceability provides the engineering relationships required for governance, auditing, maintenance and impact analysis throughout the software lifecycle.

---

# 15. Expected Outcomes

After execution, the Architecture Traceability should provide:

* complete engineering relationships;
* reliable impact analysis;
* transparent architectural evolution;
* improved governance;
* simplified maintenance;
* full architectural accountability.

The Architecture Traceability Skill establishes the end-to-end engineering relationship network of the DESys architecture, ensuring that every architectural decision, component and infrastructure element remains traceable to its originating business objectives throughout the complete software engineering lifecycle.
