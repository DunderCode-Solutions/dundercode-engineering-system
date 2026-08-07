# DSK-1020 | PRD Generation

## Metadata

Document Number: DSK-1020

Canonical ID: dsk.engineering.requirements.prd-generation

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents generate a Product Requirements Document (PRD) within the DunderCode Engineering System (DESys).

Rather than creating requirements from scratch, this skill consolidates previously validated engineering artifacts into a standardized, complete and traceable Product Requirements Document.

The generated PRD becomes the authoritative specification for architecture, development, testing and project planning.

---

# 2. Scope

This skill supports:

* PRD Generation
* PRD Assembly
* PRD Validation
* PRD Review
* PRD Regeneration
* PRD Consistency Verification
* PRD Traceability Validation
* Engineering Documentation Packaging

---

# 3. Skill Objectives

The PRD Generation Skill aims to:

* consolidate engineering knowledge;
* generate standardized documentation;
* preserve complete traceability;
* eliminate duplicated information;
* validate engineering consistency;
* prepare projects for architecture and implementation.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* generate a PRD;
* create product documentation;
* consolidate software requirements;
* prepare architecture handoff;
* prepare implementation planning;
* export engineering documentation.

This skill normally executes after Product Backlog preparation.

---

# 5. Inputs

Typical inputs include:

* Product Vision
* Business Goals
* Stakeholder Analysis
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* User Stories
* Acceptance Criteria
* Product Backlog

If mandatory engineering artifacts are missing, the skill should identify the gaps before generating the PRD.

---

# 6. Outputs

Typical deliverables include:

* Product Requirements Document (PRD)
* PRD Validation Report
* Traceability Summary
* Engineering Completeness Report
* Missing Information Report
* PRD Export Package

---

# 7. Required Knowledge

This skill should consume the following DESys knowledge.

### Required

```yaml
knowledge:
  required:
    - dep.requirements.process
    - det.prd.template
    - des.requirements.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - det.user-story.template
    - det.acceptance-criteria.template
    - dea.business-context
```

---

# 8. Execution Workflow

The PRD Generation Skill follows this workflow.

1. Validate engineering artifacts.
2. Load required documentation.
3. Verify traceability.
4. Assemble the PRD structure.
5. Populate document sections.
6. Validate completeness.
7. Produce the final Product Requirements Document.
8. Generate engineering validation report.

---

# 9. Engineering Guidelines

The generated PRD should:

* preserve business intent;
* avoid duplicated information;
* maintain complete traceability;
* reference existing engineering artifacts;
* remain implementation independent;
* follow DESys documentation standards.

The PRD should summarize engineering knowledge rather than redefine it.

---

# 10. PRD Structure

The generated Product Requirements Document should include:

* Product Vision
* Business Goals
* Stakeholder Summary
* Product Scope
* Functional Requirements
* Non-Functional Requirements
* Business Rules
* User Stories
* Acceptance Criteria
* Product Backlog Summary
* Assumptions
* Constraints
* Risks
* Traceability Summary

Projects may extend this structure according to organizational standards.

---

# 11. Validation

Before completion the skill verifies:

* all mandatory sections exist;
* engineering artifacts are internally consistent;
* duplicate requirements are absent;
* traceability is complete;
* missing dependencies are identified;
* documentation follows DESys standards.

---

# 12. Dependencies

### Parent Skill

* DSK-1010 Requirements Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The PRD Generation Skill commonly collaborates with:

* Architecture Engineering
* Documentation Engineering
* Testing Engineering
* Project Planning
* Engineering Review

The generated PRD becomes the primary engineering reference for downstream activities.

---

# 14. Expected Outcomes

After execution, the Product Requirements Document should provide:

* a complete engineering specification;
* standardized documentation;
* consolidated business knowledge;
* implementation-ready requirements;
* complete traceability across engineering artifacts;
* a reliable foundation for architecture, development and testing.

The PRD Generation Skill consolidates the outputs of Requirements Engineering into a single authoritative engineering document, ensuring consistency, traceability and alignment throughout the DESys software engineering lifecycle.
