# DSK-1121 | Architecture Decision Records (ADR)

## Metadata

Document Number: DSK-1121

Canonical ID: dsk.engineering.architecture.architecture-decision-records

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents create, maintain and review Architecture Decision Records (ADR) within the DunderCode Engineering System (DESys).

Architecture Decision Records document significant architectural decisions together with their context, motivations, evaluated alternatives and expected consequences.

They provide long-term architectural knowledge and preserve engineering rationale throughout the software lifecycle.

---

# 2. Scope

This skill supports:

* Architecture Decision Documentation
* Decision History
* Alternative Evaluation
* Decision Review
* Architectural Governance
* Decision Traceability
* Decision Lifecycle Management

---

# 3. Skill Objectives

The Architecture Decision Records Skill aims to:

* preserve architectural knowledge;
* document engineering rationale;
* improve long-term maintainability;
* support architectural evolution;
* facilitate onboarding;
* establish architectural governance.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* document architecture decisions;
* create ADRs;
* justify architectural choices;
* register technical decisions;
* review architectural history.

This skill normally executes after Infrastructure Architecture.

---

# 5. Inputs

Typical inputs include:

* Architecture Vision
* Architecture Drivers
* Architecture Constraints
* Container Architecture
* Component Architecture
* Integration Architecture
* Data Architecture
* Infrastructure Architecture

Architectural decisions lacking sufficient context should trigger clarification before documentation.

---

# 6. Outputs

Typical deliverables include:

* Architecture Decision Records
* Decision Catalog
* Decision History
* Decision Review Report
* Architectural Rationale

---

# 7. Required Knowledge

### Required

```yaml id="9kzqtp"
knowledge:
  required:
    - dep.architecture.process
    - des.architecture.documentation
```

### Optional

```yaml id="zjlwmx"
knowledge:
  optional:
    - dea.architecture-governance
    - dea.decision-management
```

---

# 8. Execution Workflow

1. Review architectural context.
2. Identify significant decisions.
3. Document the decision.
4. Describe the motivation.
5. Evaluate alternatives.
6. Record consequences.
7. Validate engineering consistency.
8. Publish the ADR.

---

# 9. Engineering Guidelines

Each ADR should:

* document one primary decision;
* describe the architectural context;
* explain the motivation;
* evaluate relevant alternatives;
* describe expected consequences;
* preserve engineering traceability.

Architecture decisions should remain understandable even years after their creation.

---

# 10. ADR Structure

Each Architecture Decision Record should include:

* ADR Identifier
* Title
* Status
* Decision Date
* Context
* Decision
* Motivation
* Alternatives Considered
* Consequences
* Risks
* Related Requirements
* Related Architecture Artifacts
* Traceability Reference

---

# 11. ADR Lifecycle

Typical ADR states include:

* Proposed
* Accepted
* Superseded
* Deprecated
* Rejected

The complete decision history should be preserved.

---

# 12. Validation

Before completion the skill verifies:

* architectural context is documented;
* decision rationale is explicit;
* alternatives were evaluated;
* consequences are described;
* related architectural artifacts are referenced;
* engineering traceability is preserved.

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

The Architecture Decision Records Skill commonly collaborates with:

* Architecture Review
* Architecture Traceability
* Infrastructure Architecture
* Integration Architecture
* Data Architecture

Architecture Decision Records preserve the engineering rationale supporting the entire software architecture.

---

# 15. Expected Outcomes

After execution, the ADR repository should provide:

* documented architectural knowledge;
* explicit engineering rationale;
* preserved decision history;
* improved architectural governance;
* simplified future maintenance;
* complete architectural accountability.

The Architecture Decision Records Skill establishes the institutional memory of the software architecture, ensuring that architectural knowledge, rationale and evolution remain permanently documented throughout the DESys engineering lifecycle.
