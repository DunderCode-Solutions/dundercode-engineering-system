---
metadata_schema: 1.0.0
document_id: DSK-6018
canonical_id: dsk.quality.defect-engineering
title: Defect Engineering
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Quality Engineering
discipline: Defect Engineering
---

# DSK-6018 | Defect Engineering

# 1. Purpose

This skill defines the **Defect Engineering (DE)** discipline adopted by the DunderCode Engineering System (DESys).

Within DESys, defects are not merely software bugs to be tracked and resolved.

They are engineering knowledge assets that enable continuous learning, systematic improvement and prevention of future failures through structured engineering analysis.

Defect Engineering transforms failures into engineering knowledge.

---

# 2. Scope

Defect Engineering governs:

* Defect Detection
* Defect Classification
* Defect Analysis
* Root Cause Analysis
* Preventive Engineering
* Defect Metrics
* Engineering Learning
* Defect Traceability

Defect Engineering spans the complete engineering lifecycle.

---

# 3. Engineering Position

Engineering defects generate engineering knowledge.

```text id="engineering-defect-position"
Engineering Evidence
        ↓
Defect Detection
        ↓
Defect Analysis
        ↓
Root Cause
        ↓
Engineering Learning
        ↓
Engineering Improvement
```

Engineering defects SHALL continuously strengthen engineering quality.

---

# 4. Engineering Objectives

Defect Engineering aims to:

* understand engineering failures;
* identify systemic causes;
* reduce recurring defects;
* strengthen engineering quality;
* improve engineering knowledge;
* enable AI-assisted defect reasoning.

---

# 5. Engineering Defect Model (EDM)

DESys adopts the **Engineering Defect Model (EDM)**.

Every engineering defect SHALL define:

* Defect
* Detection Source
* Engineering Artifact
* Severity
* Priority
* Root Cause
* Contributing Factors
* Resolution
* Preventive Action
* Evidence
* Traceability

The EDM defines the canonical defect model adopted by DESys.

---

# 6. Engineering Defect Principles

Defect Engineering SHALL follow:

* Defect Prevention First
* Evidence-Based Analysis
* Root Cause Before Resolution
* System Thinking
* Continuous Learning
* Traceable Defects
* Reproducible Defects
* Risk-Oriented Prioritization
* Cross-Disciplinary Collaboration
* Continuous Improvement

These principles SHALL guide every defect analysis.

---

# 7. Engineering Defect Taxonomy

Engineering defects SHALL be classified according to their engineering origin.

Typical categories include:

* Requirements Defects
* Design Defects
* Architecture Defects
* Implementation Defects
* Integration Defects
* Configuration Defects
* Infrastructure Defects
* Operational Defects
* Human-Centric Defects

Every engineering defect SHALL belong to at least one category.

---

# 8. Defect Lifecycle

Every engineering defect progresses through a controlled lifecycle.

```text id="defect-lifecycle"
Detected
        ↓
Triaged
        ↓
Analyzed
        ↓
Resolved
        ↓
Verified
        ↓
Learned
        ↓
Prevented
```

Engineering defects SHALL conclude with preventive engineering actions.

---

# 9. Root Cause Analysis (RCA)

Engineering Defect Engineering adopts structured Root Cause Analysis.

```text id="root-cause-analysis"
Defect
        ↓
Immediate Cause
        ↓
Contributing Factors
        ↓
System Cause
        ↓
Preventive Action
```

Corrective actions SHALL address symptoms.

Preventive actions SHALL address causes.

---

# 10. Engineering Principles

Defect Engineering SHALL:

* preserve engineering evidence;
* prioritize prevention over correction;
* support systemic analysis;
* maintain engineering traceability;
* strengthen organizational learning.

Defect Engineering SHALL never stop at defect resolution.

---

# 11. Defect Registry (DR)

Every engineering defect SHALL be registered.

Example:

```yaml id="defect-registry"
defect:

  Checkout Timeout

category:

  Integration

severity:

  High

root_cause:

  Connection Pool Exhaustion

preventive_action:

  Pool Monitoring

status:

  Learned
```

The Defect Registry preserves engineering defect metadata.

---

# 12. Engineering Defect Knowledge Graph (EDKG)

DESys represents engineering defect relationships through the Engineering Defect Knowledge Graph.

Example:

```text id="engineering-defect-knowledge-graph"
Requirement
        │ implemented by
        ▼
Artifact
        │ affected by
        ▼
Defect
        │ explained through
        ▼
Root Cause
        │ mitigated by
        ▼
Preventive Action
        │ strengthens
        ▼
Engineering Knowledge
```

The Engineering Defect Knowledge Graph enables:

* semantic navigation;
* recurrence analysis;
* systemic reasoning;
* preventive engineering;
* AI-assisted defect evaluation.

---

# 13. Defect Quality Attributes

Engineering defects SHALL evaluate:

* Severity
* Priority
* Reproducibility
* Detectability
* Recoverability
* Business Impact
* Technical Impact
* Customer Impact
* Recurrence Risk

Engineering defect quality SHALL remain measurable.

---

# 14. Defect Metrics

Typical engineering indicators include:

```yaml id="defect-metrics"
defect_density:

  0.7

escaped_defects:

  2

root_cause_coverage:

  100

recurrence_rate:

  1

preventive_actions:

  98
```

Engineering defect management SHALL remain measurable.

---

# 15. Engineering Learning

Engineering Defect Engineering SHALL capture organizational learning.

Learning MAY include:

* recurring architectural patterns;
* process improvements;
* preventive controls;
* engineering standards;
* design improvements;
* quality recommendations.

Learning SHALL become reusable engineering knowledge.

---

# 16. AI Defect Analysis

AI MAY automatically evaluate:

* recurring defect patterns;
* architectural weaknesses;
* missing Root Cause Analyses;
* defect clusters;
* engineering hotspots;
* preventive opportunities;
* engineering quality trends.

Recommendations SHALL remain deterministic and evidence-based.

---

# 17. Engineering Rules

Defect Engineering MUST:

* classify every engineering defect;
* preserve supporting evidence;
* perform Root Cause Analysis;
* define preventive actions;
* maintain complete traceability;
* preserve organizational learning.

Defect Engineering MUST NOT:

* close defects without analysis;
* ignore recurring failures;
* lose engineering history;
* treat defects as isolated events;
* prioritize correction over prevention.

---

# 18. Inputs

Typical inputs include:

* Verification Results
* Validation Results
* Testing Evidence
* Production Incidents
* Customer Reports
* Operational Observability

---

# 19. Outputs

Typical deliverables include:

* Defect Registry
* Engineering Defect Knowledge Graph
* Root Cause Analyses
* Preventive Actions
* Defect Metrics
* Engineering Learning Reports

---

# 20. Execution Workflow

1. Detect engineering defects.
2. Classify engineering defects.
3. Assess severity and priority.
4. Perform Root Cause Analysis.
5. Define corrective actions.
6. Define preventive actions.
7. Register engineering artifacts.
8. Update the Engineering Defect Knowledge Graph.
9. Capture organizational learning.
10. Improve engineering practices.

---

# 21. Validation

Before completion the skill verifies:

* defects are classified;
* Root Cause Analysis is completed;
* preventive actions are defined;
* engineering evidence is preserved;
* defect metrics remain measurable;
* Defect Registry and Engineering Defect Knowledge Graph remain synchronized.

---

# 22. Dependencies

## Parent Skill

* DSK-6000 Quality Engineering Overview

## Foundation Skills

* DSK-6011 Verification
* DSK-6012 Validation
* DSK-6013 Testing Engineering
* DSK-6017 Quality Metrics

Defect Engineering converts engineering evidence and quality measurements into organizational learning by identifying systemic causes and preventing future failures.

---

# 23. Collaboration

The Defect Engineering Skill collaborates with:

* Software Engineering
* Security Engineering
* Infrastructure Engineering
* Quality Governance
* Reliability Engineering
* AI Reasoning Engine

Defect Engineering becomes the discipline responsible for transforming engineering failures into continuous organizational learning across the DESys ecosystem.

---

# 24. Expected Outcomes

After execution, the Defect Engineering Skill should provide:

* systematically analyzed engineering defects;
* complete Root Cause Analyses;
* measurable defect trends;
* evidence-based preventive actions;
* AI-assisted defect reasoning;
* continuously improving engineering quality.

Defect Engineering establishes the canonical defect model adopted by DESys, ensuring that every engineering defect is detected, analyzed, classified, understood and transformed into organizational knowledge. By integrating Root Cause Analysis, preventive actions, engineering evidence and continuous learning into the Engineering Defect Knowledge Graph, DESys transforms defect management from reactive issue tracking into a permanent engineering discipline that strengthens quality, resilience and engineering excellence across the complete software lifecycle.
