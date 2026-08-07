# DSK-2015 | Business Processes

## Metadata

Document Number: DSK-2015

Canonical ID: dsk.domain.business-processes

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, model and document Business Processes within the DunderCode Engineering System (DESys).

Business Processes describe how an organization performs its business capabilities through coordinated activities, decisions, events and responsibilities.

They provide the operational perspective of the business while remaining independent of software implementation.

---

# 2. Scope

This skill supports:

* Business Process Modeling
* Process Discovery
* Process Documentation
* Workflow Identification
* Activity Modeling
* Decision Point Identification
* Process Governance

---

# 3. Skill Objectives

The Business Processes Skill aims to:

* document business workflows;
* identify operational activities;
* describe business behavior;
* clarify business responsibilities;
* support software analysis;
* improve organizational understanding.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* model business processes;
* describe operational workflows;
* document organizational procedures;
* analyze business operations;
* understand process execution.

This skill normally executes after Business Capabilities.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Domain Boundaries
* Business Capabilities
* Business Rules
* Organizational Procedures
* Stakeholder Knowledge
* Operational Documentation

Business processes should represent operational reality rather than desired future implementations.

---

# 6. Outputs

Typical deliverables include:

* Business Process Catalog
* Process Models
* Workflow Documentation
* Activity Diagrams
* Process Descriptions

---

# 7. Required Knowledge

### Required

```yaml id="kh5n91"
knowledge:
  required:
    - dep.business.process-modeling
    - des.domain.documentation
```

### Optional

```yaml id="0yq2qe"
knowledge:
  optional:
    - dea.bpmn
    - dea.value-stream-mapping
    - dea.event-storming
```

---

# 8. Execution Workflow

1. Identify the related Business Capability.
2. Discover business activities.
3. Define process boundaries.
4. Identify inputs and outputs.
5. Document decision points.
6. Identify participating roles.
7. Validate with stakeholders.
8. Publish the Business Process documentation.

---

# 9. Engineering Guidelines

Business Processes should:

* describe business behavior;
* remain independent of software implementation;
* identify responsibilities clearly;
* document decision points;
* identify business events;
* preserve engineering traceability.

Processes describe **how** business capabilities are executed, not how software implements them.

---

# 10. Process Structure

Each Business Process should include:

* Identifier
* Name
* Business Purpose
* Related Capability
* Trigger
* Inputs
* Activities
* Decision Points
* Outputs
* Participating Roles
* Business Rules
* Related Events
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* every process supports a business capability;
* activities are ordered logically;
* decision points are documented;
* roles are identified;
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

The Business Processes Skill commonly collaborates with:

* Business Capabilities
* Domain Events
* Domain Services
* Requirements Engineering
* Architecture Engineering

Business Processes provide the operational understanding required to derive domain events, user interactions and system behaviors.

---

# 14. Expected Outcomes

After execution, the Business Processes should provide:

* documented operational workflows;
* clear business activity sequences;
* explicit decision points;
* identified business participants;
* stronger alignment between operations and engineering;
* complete engineering traceability.

The Business Processes Skill establishes the operational behavior of the DESys engineering lifecycle, ensuring that software solutions are designed to support real organizational workflows while preserving business intent and process consistency.
