# DSK-2016 | Domain Events

## Metadata

Document Number: DSK-2016

Canonical ID: dsk.domain.domain-events

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents identify, model and document Domain Events within the DunderCode Engineering System (DESys).

Domain Events represent significant business facts that have already occurred and are meaningful to the business domain.

They capture business state changes independently of technical implementation and provide the behavioral foundation for modern software architectures.

---

# 2. Scope

This skill supports:

* Domain Event Identification
* Business State Changes
* Event Modeling
* Event Documentation
* Event Relationships
* Business Event Catalog
* Event Governance

---

# 3. Skill Objectives

The Domain Events Skill aims to:

* identify meaningful business events;
* capture business state transitions;
* document domain behavior;
* support event-driven thinking;
* improve business modeling;
* preserve engineering consistency.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* identify domain events;
* model business behavior;
* document business facts;
* analyze process outcomes;
* prepare event-driven architectures.

This skill normally executes after Business Processes.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Business Capabilities
* Business Processes
* Business Rules
* Ubiquitous Language
* Stakeholder Knowledge

Only events that represent completed business facts should be modeled as Domain Events.

---

# 6. Outputs

Typical deliverables include:

* Domain Event Catalog
* Event Definitions
* Event Relationships
* Event Flow Documentation
* Business Event Timeline

---

# 7. Required Knowledge

### Required

```yaml id="r5m2nt"
knowledge:
  required:
    - dep.domain.ddd
    - des.domain.documentation
```

### Optional

```yaml id="qjv1ik"
knowledge:
  optional:
    - dea.event-storming
    - dea.event-driven-architecture
```

---

# 8. Execution Workflow

1. Review Business Processes.
2. Identify completed business facts.
3. Define Domain Events.
4. Document event meaning.
5. Identify event producers.
6. Identify affected business concepts.
7. Validate with stakeholders.
8. Publish the Domain Event Catalog.

---

# 9. Engineering Guidelines

Domain Events should:

* describe completed business facts;
* use past-tense names;
* remain technology independent;
* avoid implementation details;
* represent meaningful business changes;
* preserve engineering traceability.

Domain Events describe **what happened**, not **what should happen**.

---

# 10. Event Structure

Each Domain Event should include:

* Identifier
* Event Name
* Business Meaning
* Trigger
* Related Business Process
* Related Business Capability
* Producing Domain
* Affected Concepts
* Business Consequences
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* events describe completed business facts;
* event names use past tense;
* business meaning is explicit;
* implementation details are excluded;
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

The Domain Events Skill commonly collaborates with:

* Business Processes
* Domain Services
* Integration Architecture
* Event-Driven Architecture
* Requirements Engineering

Domain Events provide the behavioral model that later supports architectural integration patterns while remaining grounded in business semantics.

---

# 14. Expected Outcomes

After execution, the Domain Events should provide:

* a catalog of meaningful business events;
* explicit business state transitions;
* consistent event terminology;
* improved behavioral understanding;
* stronger foundations for event-driven solutions;
* complete engineering traceability.

The Domain Events Skill establishes the behavioral perspective of the DESys engineering lifecycle, ensuring that business facts are modeled consistently, independently of implementation technology, and remain reusable across requirements, architecture and software design.
