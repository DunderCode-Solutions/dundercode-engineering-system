---
metadata_schema: 1.0.0
document_id: DSK-2014
canonical_id: dsk.domain.business-capabilities
title: Business Capabilities
node_type: skill
document_class: reference
version: 1.0.0
status: review
language: en
owner: DunderCode Engineering
relationships:
- type: depends_on
  target: dsk.domain.domain-boundaries
- type: derives_from
  target: adr.corpus.layout-and-authority
---

# DSK-2014 | Business Capabilities

## Governance Notice

This document preserves the original skill specification as reference material. It is not an Active Skill, executable instruction, compliance control or authorization to act. Terms such as "activate", "execute", "collect", "validate", "publish", "required" and "should" describe the source workflow model only; they do not grant authority or require an AI agent or person to perform an action.

Use this reference deny-by-default. It grants no authority to use tools, access networks, request or use credentials, read or write storage, change production, collect information, publish content, approve decisions, deploy changes or perform remediation. A user request alone does not establish permission. Authorized humans remain accountable for scope, access, decisions, approval and any resulting artifact.

Only authorized inputs may be used. Consumer policies, law, contracts, data classifications, access controls and retention requirements remain authoritative. Minimize confidential and personal information, distinguish facts from assumptions and stop for explicit human authorization when purpose, scope, data access, audience or ownership is unclear. No completeness, correctness, compliance, consensus, publication or outcome claim is created by this reference.

# 1. Purpose

This skill defines how AI agents identify, document and organize Business Capabilities within the DunderCode Engineering System (DESys).

Business Capabilities describe what an organization is able to do to achieve its business objectives, independently of organizational structure, processes, technologies or implementation.

They provide a stable business-oriented decomposition that supports strategic planning, software architecture and product evolution.

---

# 2. Scope

This skill supports:

* Business Capability Identification
* Capability Mapping
* Capability Relationships
* Capability Prioritization
* Strategic Business Modeling
* Capability Documentation
* Capability Governance

---

# 3. Skill Objectives

The Business Capabilities Skill aims to:

* identify organizational capabilities;
* organize business knowledge;
* establish stable business structures;
* support software architecture;
* improve strategic alignment;
* preserve engineering consistency.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify business capabilities;
* organize enterprise functions;
* model organizational competencies;
* prepare strategic architecture;
* structure business domains.

This skill normally executes after Domain Boundaries.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Domain Discovery
* Ubiquitous Language
* Domain Boundaries
* Business Goals
* Organizational Knowledge
* Stakeholder Knowledge

Capability definitions should be independent of implementation technologies and organizational charts.

---

# 6. Outputs

Typical deliverables include:

* Business Capability Map
* Capability Catalog
* Capability Hierarchy
* Capability Relationships
* Strategic Capability Overview

---

# 7. Required Knowledge

### Required

```yaml id="2p5r8a"
knowledge:
  required:
    - dep.domain.business-architecture
    - des.domain.documentation
```

### Optional

```yaml id="f9wv0u"
knowledge:
  optional:
    - dea.capability-mapping
    - dea.enterprise-architecture
```

---

# 8. Execution Workflow

1. Review domain knowledge.
2. Identify organizational capabilities.
3. Group related capabilities.
4. Define capability boundaries.
5. Document relationships.
6. Prioritize capabilities.
7. Validate with stakeholders.
8. Publish the Business Capability Map.

---

# 9. Engineering Guidelines

Business Capabilities should:

* represent enduring organizational abilities;
* remain independent of processes;
* remain independent of organizational departments;
* avoid technology-specific terminology;
* support strategic business planning;
* preserve engineering traceability.

Capabilities describe **what** the business can do, not **how** it is executed.

---

# 10. Capability Structure

Each Business Capability should include:

* Identifier
* Name
* Description
* Business Purpose
* Business Value
* Parent Capability (optional)
* Related Domains
* Related Business Goals
* Priority
* Maturity
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* capabilities are business-oriented;
* implementation details are excluded;
* capability hierarchy is consistent;
* relationships are documented;
* engineering traceability is preserved.

---

# 12. Dependencies

### Parent Skill

* DSK-2000 Domain Skills

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 13. Collaboration

The Business Capabilities Skill commonly collaborates with:

* Business Processes
* Domain Events
* Architecture Engineering
* Product Engineering
* Strategic Planning

Business Capabilities provide a stable business decomposition that guides software architecture and organizational evolution.

---

# 14. Expected Outcomes

After execution, the Business Capabilities should provide:

* a structured capability map;
* stable business decomposition;
* explicit strategic alignment;
* improved domain organization;
* stronger architecture foundations;
* complete engineering traceability.

The Business Capabilities Skill establishes the strategic functional structure of the DESys engineering lifecycle, ensuring that software solutions remain aligned with the enduring abilities of the organization rather than transient organizational structures or implementation details.
