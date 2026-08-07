# DSK-2011 | Ubiquitous Language

## Metadata

Document Number: DSK-2011

Canonical ID: dsk.domain.ubiquitous-language

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This skill defines how AI agents establish, maintain and evolve a Ubiquitous Language within the DunderCode Engineering System (DESys).

Ubiquitous Language provides a shared business vocabulary used consistently by domain experts, stakeholders, analysts, architects, developers and AI agents.

It ensures that every business concept is represented by a single, well-defined and consistently applied term throughout the software engineering lifecycle.

---

# 2. Scope

This skill supports:

* Business Terminology
* Shared Vocabulary
* Domain Glossary
* Concept Definitions
* Synonym Management
* Naming Consistency
* Business Communication
* Domain Documentation

---

# 3. Skill Objectives

The Ubiquitous Language Skill aims to:

* establish a shared vocabulary;
* eliminate ambiguous terminology;
* improve communication;
* preserve business knowledge;
* support consistent modeling;
* increase engineering quality.

---

# 4. Activation Criteria

Activate this skill when the user requests:

* define business terminology;
* create a domain glossary;
* normalize business concepts;
* establish naming conventions;
* document business language.

This skill normally executes after Domain Analysis.

---

# 5. Inputs

Typical inputs include:

* Domain Analysis
* Stakeholder Interviews
* Business Documentation
* Existing Systems
* Business Rules
* Product Vision
* Business Goals

Conflicting terminology should be identified and resolved before publication.

---

# 6. Outputs

Typical deliverables include:

* Ubiquitous Language
* Business Glossary
* Canonical Terms
* Synonym Catalog
* Naming Conventions
* Domain Vocabulary

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
    - dea.business-architecture
    - dea.domain-storytelling
```

---

# 8. Execution Workflow

1. Collect business terminology.
2. Identify duplicated concepts.
3. Resolve terminology conflicts.
4. Define canonical terms.
5. Register accepted synonyms.
6. Document definitions.
7. Validate with stakeholders.
8. Publish the Ubiquitous Language.

---

# 9. Engineering Guidelines

Every business concept should:

* have one canonical name;
* possess an explicit definition;
* avoid ambiguity;
* remain technology independent;
* be consistently used across all engineering artifacts.

Names should reflect business meaning rather than implementation details.

---

# 10. Term Structure

Each domain term should include:

* Identifier
* Canonical Name
* Definition
* Synonyms
* Context
* Related Concepts
* Usage Examples
* Forbidden Terms
* Traceability Reference

---

# 11. Validation

Before completion the skill verifies:

* every important concept has a definition;
* duplicated meanings are eliminated;
* conflicting terminology is resolved;
* canonical names are consistently applied;
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

The Ubiquitous Language Skill commonly collaborates with:

* Domain Analysis
* Business Capabilities
* Business Processes
* Domain Events
* Requirements Engineering
* Architecture Engineering

The resulting vocabulary should become the official language for all DESys engineering artifacts.

---

# 14. Expected Outcomes

After execution, the Ubiquitous Language should provide:

* a shared business vocabulary;
* unambiguous terminology;
* consistent engineering communication;
* improved domain understanding;
* stronger alignment between business and engineering;
* a stable linguistic foundation for software development.

The Ubiquitous Language Skill establishes the official business vocabulary of the DESys engineering lifecycle, ensuring that every stakeholder and AI agent communicates using consistent, precise and business-oriented terminology across all phases of software engineering.
