---
metadata_schema: 1.0.0
document_id: DSK-1122
canonical_id: dsk.engineering.architecture.architecture-review
title: Architecture Review
node_type: skill
document_class: operational
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
---

# DSK-1122 | Architecture Review

# 1. Purpose

This skill defines how AI agents perform structured Architecture Reviews within the DunderCode Engineering System (DESys).

Architecture Review evaluates whether the proposed software architecture satisfies business objectives, architectural drivers, quality attributes, engineering standards and governance requirements before implementation.

It provides an objective assessment of architectural quality and identifies risks, weaknesses and improvement opportunities.

---

# 2. Scope

This skill supports:

* Architecture Assessment
* Design Validation
* Quality Attribute Review
* Risk Identification
* Architectural Compliance
* Review Reporting
* Review Recommendations
* Review Governance

---

# 3. Skill Objectives

The Architecture Review Skill aims to:

* validate architectural quality;
* identify technical risks;
* verify alignment with business objectives;
* evaluate architectural consistency;
* improve long-term maintainability;
* support engineering governance.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* review an architecture;
* validate architectural decisions;
* perform design assessment;
* evaluate architecture quality;
* conduct architecture governance.

This skill normally executes after Architecture Decision Records.

---

# 5. Inputs

Typical inputs include:

* Architecture Vision
* Architecture Drivers
* Architecture Constraints
* Domain Model
* Context Model
* Bounded Contexts
* Container Architecture
* Component Architecture
* Integration Architecture
* Data Architecture
* Infrastructure Architecture
* Architecture Decision Records

---

# 6. Outputs

Typical deliverables include:

* Architecture Review Report
* Findings
* Risks
* Recommendations
* Improvement Opportunities
* Review Decision

---

# 7. Required Knowledge

### Required

```yaml id="8mxq5a"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="o5fh8l"
knowledge:
  optional:
    - dea.architecture-evaluation
    - dea.quality-attributes
    - dea.software-governance
```

---

# 8. Execution Workflow

1. Review architectural artifacts.
2. Verify architectural consistency.
3. Evaluate quality attributes.
4. Assess risks.
5. Verify governance compliance.
6. Produce findings.
7. Recommend improvements.
8. Publish the Architecture Review.

---

# 9. Engineering Guidelines

Architecture Review should evaluate:

* architectural completeness;
* business alignment;
* technical consistency;
* quality attributes;
* operational readiness;
* governance compliance.

Reviews should remain objective, evidence-based and independent of implementation preferences.

---

# 10. Review Categories

Typical review areas include:

* Business Alignment
* Functional Coverage
* Non-Functional Requirements
* Scalability
* Performance
* Security
* Reliability
* Availability
* Maintainability
* Modularity
* Integration
* Data Management
* Infrastructure
* Observability
* Governance
* Documentation

Projects may extend these categories according to organizational standards.

---

# 11. Review Structure

Each Architecture Review should include:

* Review Identifier
* Scope
* Reviewed Artifacts
* Findings
* Risks
* Recommendations
* Review Decision
* Reviewer
* Review Date
* Related ADRs
* Traceability Reference

---

# 12. Review Decisions

Typical review outcomes include:

* Approved
* Approved with Recommendations
* Changes Required
* Rejected

All review decisions should include supporting rationale.

---

# 13. Validation

Before completion the skill verifies:

* all architectural artifacts were reviewed;
* findings are documented;
* recommendations are actionable;
* review decision is justified;
* engineering traceability is preserved.

---

# 14. Dependencies

### Parent Skill

* DSK-1100 Architecture Engineering

### Foundation Skills

* DSK-0020 Agent Navigation
* DSK-0030 Context Loading
* DSK-0040 Knowledge Resolution
* DSK-0050 Prompt Construction
* DSK-0060 Response Validation

---

# 15. Collaboration

The Architecture Review Skill commonly collaborates with:

* Architecture Decision Records
* Architecture Traceability
* Security Architecture
* Infrastructure Architecture
* Engineering Governance

Architecture Review provides the formal validation stage of the architectural lifecycle before implementation begins.

---

# 16. Expected Outcomes

After execution, the Architecture Review should provide:

* validated architectural quality;
* documented findings;
* identified technical risks;
* prioritized recommendations;
* governance compliance assessment;
* a justified architectural decision.

The Architecture Review Skill establishes the formal engineering validation process for DESys architectures, ensuring that architectural decisions are technically sound, aligned with business objectives and ready to support successful software implementation.
