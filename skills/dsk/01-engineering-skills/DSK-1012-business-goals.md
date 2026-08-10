---
metadata_schema: 1.0.0
document_id: DSK-1012
canonical_id: dsk.engineering.requirements.business-goals
title: Business Goals
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1012 | Business Goals

# 1. Purpose

This skill defines how AI agents identify, organize and validate Business Goals within the DunderCode Engineering System (DESys).

Business Goals describe the measurable organizational outcomes that justify the existence of a software product or engineering initiative.

They provide the strategic foundation upon which product requirements, architecture and implementation decisions are built.

---

# 2. Scope

This skill supports:

* Business Goal definition
* Business Objective refinement
* Strategic alignment
* Goal prioritization
* Success criteria definition
* KPI identification
* Value assessment
* Goal review

---

# 3. Skill Objectives

The Business Goals Skill aims to:

* identify organizational objectives;
* align software initiatives with business strategy;
* define measurable outcomes;
* establish product success criteria;
* support prioritization of engineering activities;
* improve stakeholder alignment.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define business objectives;
* organize strategic goals;
* justify a software initiative;
* establish product success criteria;
* prioritize business outcomes;
* begin a new product or project.

This skill normally executes immediately after Product Vision.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Strategy
* Organizational Objectives
* Market Opportunities
* Customer Needs
* Stakeholder Expectations
* Existing Business Documentation

Missing strategic information should trigger clarification before execution.

---

# 6. Outputs

Typical deliverables include:

* Business Goals
* Strategic Objectives
* Expected Business Outcomes
* Key Performance Indicators (KPIs)
* Success Metrics
* Goal Prioritization
* Goal Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.requirements.process
    - des.requirements.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - det.prd.template
    - dea.business-context
```

---

# 8. Execution Workflow

The Business Goals Skill follows this workflow.

1. Understand organizational strategy.
2. Identify the business problem.
3. Define expected business outcomes.
4. Establish measurable objectives.
5. Define success indicators.
6. Prioritize goals.
7. Validate strategic alignment.
8. Produce structured business goals.

---

# 9. Engineering Guidelines

Business Goals should:

* describe outcomes rather than solutions;
* be measurable whenever possible;
* support product prioritization;
* remain technology independent;
* align with organizational strategy;
* remain understandable by both business and engineering teams.

Business Goals should never describe implementation details.

---

# 10. Validation

Before completion the skill verifies:

* every goal is clearly defined;
* goals are measurable;
* business value is explicit;
* goals align with Product Vision;
* priorities are documented;
* success criteria exist.

---

# 11. Dependencies

### Parent Skill

* DSK-1010 Requirements Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 12. Collaboration

The Business Goals Skill commonly collaborates with:

* Product Vision
* Stakeholder Analysis
* Requirements Engineering
* Architecture Engineering

Business Goals provide strategic guidance for all subsequent engineering activities.

---

# 13. Expected Outcomes

After execution, the Business Goals should provide:

* clearly defined organizational objectives;
* measurable business outcomes;
* explicit success criteria;
* prioritized strategic goals;
* alignment between business and engineering;
* a stable foundation for requirements engineering.

The Business Goals Skill ensures that every engineering initiative within DESys is driven by measurable organizational value rather than isolated technical decisions.
