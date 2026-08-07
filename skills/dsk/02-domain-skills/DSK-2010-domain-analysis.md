# DSK-2010 | Domain Analysis

## Metadata

Document Number: DSK-2010

Canonical ID: dsk.domain.domain-analysis

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents perform Domain Analysis within the DunderCode Engineering System (DESys).

Domain Analysis identifies, organizes and documents the business knowledge required to understand a problem domain before requirements, architecture or implementation activities begin.

It establishes the conceptual foundation upon which all subsequent engineering decisions are built.

---

# 2. Scope

This skill supports:

* Business Domain Understanding
* Problem Space Analysis
* Domain Knowledge Acquisition
* Business Concept Identification
* Stakeholder Perspective Analysis
* Domain Documentation
* Business Context Analysis

---

# 3. Skill Objectives

The Domain Analysis Skill aims to:

* understand the business domain;
* identify core business concepts;
* recognize business problems;
* organize domain knowledge;
* support engineering decisions;
* establish a reliable business foundation.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* analyze a business domain;
* understand a business problem;
* study an organization;
* document domain knowledge;
* prepare software engineering activities.

This skill normally executes immediately after the Domain Skills Overview.

---

# 5. Inputs

Typical inputs include:

* Business Vision
* Business Goals
* Stakeholder Interviews
* Existing Documentation
* Regulations
* Operational Procedures
* Existing Systems
* Market Knowledge

Incomplete or conflicting information should trigger clarification before analysis continues.

---

# 6. Outputs

Typical deliverables include:

* Domain Analysis Report
* Business Concept Catalog
* Domain Overview
* Business Context Description
* Domain Knowledge Base

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
    - dea.business-analysis
    - dea.business-architecture
    - dea.event-storming
```

---

# 8. Execution Workflow

1. Collect available business information.
2. Identify stakeholders.
3. Understand business objectives.
4. Identify business concepts.
5. Recognize business processes.
6. Detect constraints.
7. Organize domain knowledge.
8. Produce the Domain Analysis.

---

# 9. Engineering Guidelines

Domain Analysis should:

* prioritize business understanding;
* remain technology independent;
* distinguish business facts from assumptions;
* document uncertainties explicitly;
* preserve engineering traceability.

The objective is understanding the domain rather than proposing technical solutions.

---

# 10. Analysis Topics

Typical analysis areas include:

* Business Purpose
* Business Objectives
* Stakeholders
* Business Concepts
* Business Processes
* Organizational Structure
* Operational Constraints
* Regulations
* Business Risks
* Success Factors

Projects may extend these topics according to their domain.

---

# 11. Analysis Structure

Each analysis should include:

* Domain Name
* Business Purpose
* Scope
* Stakeholders
* Core Concepts
* Business Challenges
* Constraints
* Opportunities
* Assumptions
* Traceability Reference

---

# 12. Validation

Before completion the skill verifies:

* business objectives are understood;
* stakeholders are identified;
* core concepts are documented;
* assumptions are explicit;
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

The Domain Analysis Skill commonly collaborates with:

* Ubiquitous Language
* Domain Discovery
* Business Capabilities
* Business Processes
* Requirements Engineering

Domain Analysis provides the business understanding required for all subsequent engineering activities.

---

# 15. Expected Outcomes

After execution, the Domain Analysis should provide:

* comprehensive understanding of the business domain;
* documented business concepts;
* identified stakeholders;
* organized domain knowledge;
* explicit assumptions and constraints;
* a reliable foundation for software engineering.

The Domain Analysis Skill establishes the business understanding that supports the entire DESys engineering lifecycle, ensuring that architecture, design and implementation remain aligned with real business needs rather than technical assumptions.
