---
metadata_schema: 1.0.0
document_id: DSK-1013
canonical_id: dsk.engineering.requirements.stakeholder-analysis
title: Stakeholder Analysis
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1013 | Stakeholder Analysis

# 1. Purpose

This skill defines how AI agents identify, classify and analyze stakeholders within the DunderCode Engineering System (DESys).

Stakeholder Analysis ensures that engineering decisions consider the interests, responsibilities and expectations of all relevant participants before requirements are defined.

The resulting analysis becomes an essential input for Requirements Engineering and subsequent engineering activities.

---

# 2. Scope

This skill supports:

* Stakeholder Identification
* Stakeholder Classification
* Role Definition
* Responsibility Mapping
* Interest Analysis
* Influence Analysis
* Communication Planning
* Stakeholder Review

---

# 3. Skill Objectives

The Stakeholder Analysis Skill aims to:

* identify all relevant stakeholders;
* understand stakeholder expectations;
* classify stakeholders according to their influence;
* document stakeholder responsibilities;
* support engineering prioritization;
* reduce communication risks.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify project stakeholders;
* organize project participants;
* understand user groups;
* define decision makers;
* map responsibilities;
* begin Requirements Engineering.

This skill normally executes after Product Vision and Business Goals.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Organizational Structure
* Customer Information
* Existing Documentation
* Project Scope
* Business Context

If stakeholder information is incomplete, the skill should request clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Stakeholder Register
* Stakeholder Matrix
* Stakeholder Roles
* Responsibility Mapping
* Influence Assessment
* Interest Assessment
* Communication Recommendations
* Stakeholder Review Report

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml id="z2m94h"
knowledge:
  required:
    - dep.requirements.process
    - des.requirements.documentation
```

### Optional

```yaml id="v8q6pm"
knowledge:
  optional:
    - det.prd.template
    - dea.business-context
```

---

# 8. Execution Workflow

The Stakeholder Analysis Skill follows this workflow.

1. Understand the project context.
2. Identify stakeholder groups.
3. Classify stakeholders.
4. Define responsibilities.
5. Assess influence.
6. Assess interests.
7. Identify communication needs.
8. Validate stakeholder coverage.
9. Produce structured stakeholder documentation.

---

# 9. Engineering Guidelines

Stakeholders should be analyzed according to:

* organizational role;
* business responsibility;
* decision authority;
* influence on the project;
* expected benefits;
* communication needs.

The analysis should distinguish clearly between:

* Business Stakeholders
* End Users
* Product Owners
* Technical Stakeholders
* Regulatory Stakeholders
* External Partners

---

# 10. Validation

Before completion the skill verifies:

* all stakeholder groups are represented;
* responsibilities are documented;
* decision makers are identified;
* communication needs are defined;
* stakeholder expectations are explicit;
* no relevant stakeholder has been omitted.

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

The Stakeholder Analysis Skill commonly collaborates with:

* Product Vision
* Business Goals
* Functional Requirements
* Non-Functional Requirements
* Requirements Engineering

Stakeholder information directly influences requirement prioritization and engineering decisions.

---

# 13. Expected Outcomes

After execution, the Stakeholder Analysis should provide:

* a complete stakeholder inventory;
* clearly defined stakeholder roles;
* documented responsibilities;
* influence and interest assessments;
* communication recommendations;
* a reliable foundation for Requirements Engineering.

The Stakeholder Analysis Skill ensures that engineering decisions reflect the needs, expectations and responsibilities of all relevant participants within the DESys engineering lifecycle.
