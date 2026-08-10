---
metadata_schema: 1.0.0
document_id: DSK-2012
canonical_id: dsk.domain.domain-discovery
title: Domain Discovery
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-2012 | Domain Discovery

# 1. Purpose

This skill defines how AI agents perform Domain Discovery within the DunderCode Engineering System (DESys).

Domain Discovery is the process of uncovering business knowledge that is incomplete, implicit, undocumented or distributed among stakeholders.

Its objective is to transform tacit organizational knowledge into explicit engineering knowledge before software design and implementation begin.

---

# 2. Scope

This skill supports:

* Domain Knowledge Discovery
* Tacit Knowledge Identification
* Business Exploration
* Process Discovery
* Rule Discovery
* Stakeholder Knowledge Extraction
* Domain Documentation

---

# 3. Skill Objectives

The Domain Discovery Skill aims to:

* discover hidden business knowledge;
* identify undocumented business rules;
* reveal implicit processes;
* capture domain expertise;
* reduce business uncertainty;
* improve domain completeness.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* discover domain knowledge;
* explore an unfamiliar business domain;
* identify undocumented rules;
* understand operational processes;
* refine business understanding.

This skill normally executes after Domain Analysis.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Stakeholder Interviews
* Existing Documentation
* Operational Procedures
* Legacy Systems
* Business Processes
* Organizational Knowledge

Knowledge gaps identified during analysis should become the primary focus of discovery activities.

---

# 6. Outputs

Typical deliverables include:

* Domain Discovery Report
* Knowledge Gap Catalog
* Newly Identified Business Concepts
* Undocumented Business Rules
* Discovery Findings
* Domain Knowledge Repository Updates

---

# 7. Required Knowledge

### Required

```yaml
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml
knowledge:
  optional:
    - dea.event-storming
    - dea.domain-storytelling
    - dea.business-analysis
```

---

# 8. Execution Workflow

1. Review the existing Domain Analysis.
2. Identify knowledge gaps.
3. Explore business activities.
4. Capture stakeholder expertise.
5. Discover implicit business rules.
6. Validate findings with domain experts.
7. Update the domain knowledge base.
8. Publish the Domain Discovery report.

---

# 9. Engineering Guidelines

Domain Discovery should:

* prioritize business understanding;
* identify uncertainty explicitly;
* distinguish facts from assumptions;
* validate discoveries with domain experts;
* remain technology independent;
* preserve engineering traceability.

Discovery activities should focus on business behavior rather than software implementation.

---

# 10. Discovery Techniques

Typical techniques include:

* Stakeholder Interviews
* Collaborative Workshops
* Event Storming
* Domain Storytelling
* Process Observation
* Legacy System Analysis
* Documentation Review
* Incremental Discovery

Projects may combine multiple techniques according to organizational needs.

---

# 11. Discovery Structure

Each discovery activity should include:

* Identifier
* Discovery Objective
* Knowledge Gap
* Stakeholders Involved
* Findings
* New Business Concepts
* Newly Identified Rules
* Remaining Questions
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* major knowledge gaps were investigated;
* findings are validated with stakeholders;
* new concepts are documented;
* assumptions remain explicit;
* engineering traceability is preserved.

---

# 13. Dependencies

### Parent Skill

* DSK-2000 Domain Skills

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 14. Collaboration

The Domain Discovery Skill commonly collaborates with:

* Domain Analysis
* Ubiquitous Language
* Business Capabilities
* Business Processes
* Domain Events

Domain Discovery enriches the business knowledge base and continuously improves the quality and completeness of the domain model.

---

# 15. Expected Outcomes

After execution, the Domain Discovery should provide:

* reduced business uncertainty;
* documented tacit knowledge;
* newly identified business concepts;
* explicit business rules;
* improved domain completeness;
* a stronger foundation for architecture and software design.

The Domain Discovery Skill expands and refines the organizational knowledge base of the DESys engineering lifecycle, ensuring that software solutions are built upon validated business understanding rather than assumptions or incomplete documentation.
