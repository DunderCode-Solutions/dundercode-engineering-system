# DSK-1011 | Product Vision

## Metadata

Document Number: DSK-1011

Canonical ID: dsk.engineering.requirements.product-vision

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents create and refine a Product Vision within the DunderCode Engineering System (DESys).

The Product Vision establishes the strategic direction of a software product before detailed requirements, architecture or implementation activities begin.

It provides a shared understanding of the product's purpose, business value and long-term objectives.

---

# 2. Scope

This skill supports:

* Product Vision creation
* Product Vision refinement
* Vision review
* Vision validation
* Business objective definition
* Product positioning
* Value proposition definition
* Success criteria definition

---

# 3. Skill Objectives

The Product Vision Skill aims to:

* understand the business problem;
* define the product purpose;
* identify target users;
* establish business value;
* align stakeholders around a common vision;
* create a stable foundation for Requirements Engineering.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* create a new product;
* define a product vision;
* organize an idea;
* start a software project;
* clarify business objectives;
* refine product strategy.

This skill should normally execute before Requirements Engineering.

---

# 5. Inputs

Typical inputs include:

* business idea;
* problem statement;
* customer needs;
* organizational objectives;
* market opportunity;
* stakeholder expectations.

If essential information is missing, the skill should request clarification before continuing.

---

# 6. Outputs

Typical deliverables include:

* Product Vision Statement
* Product Purpose
* Target Audience
* Business Goals
* Value Proposition
* Success Metrics
* Product Scope Summary
* Vision Review Report

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

The Product Vision Skill follows this workflow.

1. Understand the business context.
2. Identify the problem to be solved.
3. Identify stakeholders.
4. Define target users.
5. Describe the expected value.
6. Define business objectives.
7. Identify project boundaries.
8. Produce the Product Vision.
9. Validate stakeholder alignment.

---

# 9. Engineering Guidelines

The Product Vision should answer:

* Why does the product exist?
* Who benefits from it?
* Which problem does it solve?
* Why is it valuable?
* What differentiates it?
* How will success be measured?

The Product Vision should avoid implementation details.

Technology decisions belong to later engineering phases.

---

# 10. Validation

Before completion the skill verifies:

* business problem is clearly defined;
* target audience exists;
* business value is explicit;
* objectives are measurable;
* scope is understandable;
* assumptions are documented;
* vision is internally consistent.

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

The Product Vision Skill commonly collaborates with:

* Stakeholder Analysis
* Requirements Engineering
* Architecture Engineering

The resulting Product Vision becomes an input for subsequent engineering activities.

---

# 13. Expected Outcomes

After execution, the Product Vision should provide:

* a shared understanding of the product;
* clearly defined business objectives;
* explicit value proposition;
* identified target users;
* strategic alignment among stakeholders;
* a solid foundation for requirements engineering.

The Product Vision Skill establishes the strategic direction of the product and serves as the starting point for all subsequent engineering activities within DESys.
