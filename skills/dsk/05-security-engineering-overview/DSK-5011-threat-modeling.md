---
metadata_schema: 1.0.0
document_id: DSK-5011
canonical_id: dsk.security.threat-modeling
title: Threat Modeling
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Security Engineering
discipline: Engineering Threat Modeling
---

# DSK-5011 | Threat Modeling

# 1. Purpose

This skill defines the **Engineering Threat Modeling (ETM)** discipline adopted by the DunderCode Engineering System (DESys).

Within DESys, threat modeling is not a checklist-based activity.

It is the engineering discipline responsible for identifying, modeling, evaluating and governing threats as engineering knowledge connected to business assets, domain concepts, architecture, software components and security controls.

Every threat becomes an Engineering Threat Artifact.

---

# 2. Scope

Engineering Threat Modeling governs:

* Asset Identification
* Attack Surface Modeling
* Threat Identification
* Risk Evaluation
* Security Controls
* Threat Registry
* Threat Traceability

---

# 3. Engineering Position

Threat Modeling connects engineering assets with security controls.

```text id="threat-modeling-position"
Business Asset
        ↓
Domain Asset
        ↓
Architecture
        ↓
Threat
        ↓
Risk
        ↓
Control
        ↓
Evidence
```

Threats SHALL remain connected to engineering knowledge.

---

# 4. Engineering Objectives

Engineering Threat Modeling aims to:

* identify engineering threats;
* evaluate engineering risks;
* define effective security controls;
* preserve engineering traceability;
* strengthen engineering security;
* support AI-assisted threat reasoning.

---

# 5. Engineering Threat Model (ETM)

DESys adopts the **Engineering Threat Model (ETM)**.

Every threat SHALL possess:

* Identity
* Asset
* Threat
* Risk
* Likelihood
* Impact
* Controls
* Evidence
* Traceability

The ETM defines the canonical threat model adopted by DESys.

---

# 6. Threat Lifecycle

Every threat progresses through a controlled lifecycle.

```text id="threat-lifecycle"
Identified
        ↓
Modeled
        ↓
Evaluated
        ↓
Mitigated
        ↓
Verified
        ↓
Monitored
```

Threats SHALL remain continuously managed.

---

# 7. Engineering Principles

Threat Modeling SHALL:

* begin with engineering assets;
* preserve engineering context;
* remain evidence-based;
* support continuous reassessment;
* strengthen engineering governance.

Threats SHALL never exist independently of engineering assets.

---

# 8. Threat Registry (TR)

Every threat SHALL be registered.

Example:

```yaml id="threat-registry"
threat:

  SQL Injection

asset:

  Customer API

risk:

  High

control:

  Parameterized Queries

status:

  Mitigated
```

The Threat Registry preserves engineering threat metadata.

---

# 9. Threat Knowledge Graph (TKG)

DESys represents threats through the Threat Knowledge Graph.

Example:

```text id="threat-graph"
Engineering Assets
        │ expose
        ▼
Attack Surface
        │ enables
        ▼
Threats
        │ generate
        ▼
Risks
        │ mitigated by
        ▼
Controls
        │ validated through
        ▼
Evidence
```

The Threat Knowledge Graph enables:

* semantic navigation;
* threat reasoning;
* attack surface analysis;
* control verification;
* AI-assisted security analysis.

---

# 10. Threat Metrics

Typical engineering indicators include:

```yaml id="threat-metrics"
modeled_assets:

  100

mitigated_threats:

  98

high_risk:

  0

traceability:

  100
```

Threat quality SHALL remain measurable.

---

# 11. AI Threat Analysis

AI MAY automatically evaluate:

* uncovered assets;
* missing controls;
* residual risks;
* attack surface evolution;
* architectural impact;
* threat traceability.

Recommendations SHALL remain deterministic and evidence-based.

---

# 12. Engineering Rules

Threat Modeling MUST:

* associate every threat with an asset;
* evaluate engineering risks;
* define explicit controls;
* preserve engineering evidence;
* maintain complete traceability.

Threat Modeling MUST NOT:

* create orphan threats;
* evaluate risks without engineering context;
* define undocumented controls;
* lose engineering provenance.

---

# 13. Inputs

Typical inputs include:

* Business Assets
* Domain Models
* Architecture Specifications
* Software Components
* Engineering Decisions
* Security Policies

---

# 14. Outputs

Typical deliverables include:

* Threat Registry
* Threat Knowledge Graph
* Risk Analysis
* Security Controls
* Threat Metrics
* Engineering Documentation

---

# 15. Execution Workflow

1. Identify engineering assets.
2. Identify attack surfaces.
3. Model engineering threats.
4. Evaluate risks.
5. Define security controls.
6. Produce engineering evidence.
7. Register threats.
8. Update the Threat Knowledge Graph.
9. Monitor residual risks.

---

# 16. Validation

Before completion the skill verifies:

* every asset has been evaluated;
* every threat has associated controls;
* risks are explicitly classified;
* evidence supports mitigation;
* Threat Registry and Threat Knowledge Graph remain synchronized.

---

# 17. Dependencies

## Parent Skill

* DSK-5000 Security Engineering Overview

## Foundation Skills

* DSK-5010 Security Principles

Engineering Threat Modeling applies the Engineering Security Principles to identify and govern risks throughout the engineering lifecycle.

---

# 18. Collaboration

The Threat Modeling Skill collaborates with:

* Business Engineering
* Domain Engineering
* Architecture Engineering
* Software Engineering
* Infrastructure Engineering
* Security Governance
* AI Reasoning Engine

Threat Modeling becomes the engineering mechanism responsible for transforming assets into governed security knowledge.

---

# 19. Expected Outcomes

After execution, the Threat Modeling Skill should provide:

* complete engineering threat models;
* measurable engineering risks;
* explicit security controls;
* complete threat traceability;
* AI-assisted threat reasoning;
* continuously governed engineering security.

Engineering Threat Modeling establishes the canonical threat modeling discipline adopted by DESys, ensuring that every engineering asset is systematically associated with threats, risks, controls and evidence, preserving security knowledge, engineering traceability and continuous risk governance throughout the complete software lifecycle.
