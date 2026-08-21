---
metadata_schema: 1.0.0
document_id: DSK-6017
canonical_id: dsk.quality.quality-metrics
title: Quality Metrics
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Quality Engineering
discipline: Engineering Quality Metrics
---

# DSK-6017 | Quality Metrics

# 1. Purpose

This skill defines the **Engineering Quality Metrics (EQM)** discipline adopted by the DunderCode Engineering System (DESys).

Within DESys, quality metrics are not isolated indicators or dashboard numbers.

They are the engineering discipline responsible for transforming engineering evidence into measurable knowledge that supports engineering decisions, governance and continuous improvement.

Engineering Quality Metrics enable engineering intelligence.

---

# 2. Scope

Engineering Quality Metrics governs:

* Engineering Measurements
* Engineering Indicators
* Quality Dashboards
* Trend Analysis
* Engineering Intelligence
* Decision Support
* Continuous Measurement
* Metrics Governance

Engineering Quality Metrics spans the complete engineering lifecycle.

---

# 3. Engineering Position

Engineering metrics transform evidence into engineering decisions.

```text id="engineering-quality-metrics-position"
Engineering Evidence
        ↓
Measurements
        ↓
Engineering Metrics
        ↓
Quality Intelligence
        ↓
Engineering Decisions
        ↓
Continuous Improvement
```

Engineering measurements SHALL continuously support engineering excellence.

---

# 4. Engineering Objectives

Engineering Quality Metrics aims to:

* measure engineering quality;
* transform evidence into knowledge;
* support engineering decisions;
* identify engineering trends;
* strengthen engineering governance;
* enable AI-assisted engineering intelligence.

---

# 5. Engineering Quality Metrics Model (EQMM)

DESys adopts the **Engineering Quality Metrics Model (EQMM)**.

Every engineering metric SHALL define:

* Metric
* Engineering Objective
* Measurement Method
* Data Source
* Calculation Rule
* Threshold
* Trend
* Owner
* Evidence
* Traceability

The EQMM defines the canonical quality metrics model adopted by DESys.

---

# 6. Engineering Measurement Principles

Engineering Quality Metrics SHALL follow:

* Evidence-Based Metrics
* Actionable Metrics
* Context-Aware Metrics
* Objective Metrics
* Reproducible Metrics
* Traceable Metrics
* Continuous Measurement
* Engineering-Oriented Metrics
* Decision-Driven Metrics
* Improvement-Oriented Metrics

These principles SHALL guide every engineering measurement.

---

# 7. Engineering Metric Categories

Engineering Quality Metrics organizes indicators into engineering categories.

## Quality

* Defect Density
* Escaped Defects
* Defect Leakage

## Verification

* Verification Coverage
* Review Coverage

## Validation

* Validation Coverage
* Validation Confidence

## Testing

* Scenario Coverage
* Risk Coverage
* Automation Coverage

## Reliability

* Availability
* Mean Time Between Failures (MTBF)
* Mean Time to Recovery (MTTR)

## Delivery

* Deployment Frequency
* Lead Time for Changes
* Change Failure Rate
* Failed Deployment Recovery Time
* Deployment Rework Rate

## Architecture

* Maintainability
* Complexity
* Technical Debt

## Security

* Vulnerability Density
* Compliance Coverage
* Trust Score

Each category SHALL measure a distinct engineering capability.

---

# 8. Metrics Lifecycle

Every engineering metric progresses through a controlled lifecycle.

```text id="metrics-lifecycle"
Defined
        ↓
Collected
        ↓
Validated
        ↓
Measured
        ↓
Analyzed
        ↓
Reported
        ↓
Improved
```

Engineering metrics SHALL continuously evolve.

---

# 9. Engineering Principles

Engineering Quality Metrics SHALL:

* support engineering decisions;
* remain evidence-based;
* preserve engineering traceability;
* enable continuous improvement;
* remain technology-independent.

Engineering metrics SHALL never become vanity indicators.

---

# 10. Metrics Registry (MR)

Every engineering metric SHALL be registered.

Example:

```yaml id="metrics-registry"
metric:

  Validation Confidence

category:

  Validation

target:

  >=95

owner:

  Quality Engineering

status:

  Active
```

The Metrics Registry preserves engineering measurement metadata.

---

# 11. Engineering Quality Metrics Knowledge Graph (EQMKG)

DESys represents engineering measurements through the Engineering Quality Metrics Knowledge Graph.

Example:

```text id="engineering-quality-metrics-knowledge-graph"
Engineering Goal
        │ evaluated by
        ▼
Evidence
        │ quantified through
        ▼
Metric
        │ analyzed as
        ▼
Trend
        │ supports
        ▼
Decision
        │ drives
        ▼
Improvement
```

The Engineering Quality Metrics Knowledge Graph enables:

* semantic navigation;
* engineering reasoning;
* trend analysis;
* impact assessment;
* AI-assisted engineering intelligence.

---

# 12. Engineering Dashboards

Engineering Quality Metrics MAY provide specialized dashboards.

Typical dashboards include:

## Executive Dashboard

* Overall Engineering Quality
* Reliability
* Delivery Health

## Engineering Dashboard

* Verification Coverage
* Validation Confidence
* Test Coverage
* Defect Trends
* Architecture Quality

## Operations Dashboard

* Availability
* Incident Recovery
* Operational Validation

Dashboards SHALL support their intended audience.

---

# 13. Metric Quality Attributes

Every engineering metric SHALL evaluate:

* Accuracy
* Completeness
* Timeliness
* Consistency
* Explainability
* Reproducibility
* Traceability

Metric quality SHALL remain measurable.

---

# 14. Engineering Metrics Intelligence

Engineering metrics SHALL support:

* trend identification;
* anomaly detection;
* quality forecasting;
* engineering benchmarking;
* decision prioritization;
* continuous improvement.

Engineering intelligence SHALL remain evidence-driven.

---

# 15. Metrics Indicators

Typical engineering indicators include:

```yaml id="quality-metrics"
verification_coverage:

  100

validation_confidence:

  96

automation_coverage:

  94

delivery_health:

  High

engineering_quality:

  Excellent
```

Engineering quality SHALL remain measurable.

---

# 16. AI Metrics Analysis

AI MAY automatically evaluate:

* engineering trends;
* quality regressions;
* metric correlations;
* engineering bottlenecks;
* conflicting indicators;
* improvement opportunities;
* engineering forecasts.

Recommendations SHALL remain deterministic and evidence-based.

---

# 17. Engineering Rules

Engineering Quality Metrics MUST:

* define explicit engineering objectives;
* preserve reproducible calculations;
* identify reliable data sources;
* maintain complete traceability;
* support engineering decisions.

Engineering Quality Metrics MUST NOT:

* measure individual engineer productivity;
* encourage vanity metrics;
* ignore engineering context;
* produce unsupported conclusions;
* disconnect metrics from engineering evidence.

---

# 18. Inputs

Typical inputs include:

* Engineering Evidence
* Verification Results
* Validation Results
* Testing Results
* Automation Reports
* Engineering Observability
* Delivery Metrics

---

# 19. Outputs

Typical deliverables include:

* Metrics Registry
* Engineering Quality Metrics Knowledge Graph
* Engineering Dashboards
* Trend Reports
* Engineering Intelligence
* Decision Support Reports

---

# 20. Execution Workflow

1. Define engineering objectives.
2. Select engineering metrics.
3. Collect engineering evidence.
4. Validate measurement quality.
5. Calculate engineering indicators.
6. Register engineering metrics.
7. Update the Engineering Quality Metrics Knowledge Graph.
8. Analyze engineering trends.
9. Produce engineering intelligence.
10. Recommend continuous improvements.

---

# 21. Validation

Before completion the skill verifies:

* metrics possess explicit objectives;
* measurement methods are reproducible;
* engineering evidence supports calculations;
* indicators remain measurable;
* engineering traceability is complete;
* Metrics Registry and Engineering Quality Metrics Knowledge Graph remain synchronized.

---

# 22. Dependencies

## Parent Skill

* DSK-6000 Quality Engineering Overview

## Foundation Skills

* DSK-6011 Verification
* DSK-6012 Validation
* DSK-6013 Testing Engineering
* DSK-6014 Test Architecture
* DSK-6015 Test Automation
* DSK-6016 Test Data Management

Engineering Quality Metrics consolidates engineering evidence produced across the Quality Engineering lifecycle into measurable indicators that support engineering governance and continuous improvement.

---

# 23. Collaboration

The Quality Metrics Skill collaborates with:

* Software Engineering
* Security Engineering
* Infrastructure Engineering
* DevOps Engineering
* Quality Governance
* AI Reasoning Engine

Engineering Quality Metrics becomes the discipline responsible for measuring engineering excellence across the DESys ecosystem.

---

# 24. Expected Outcomes

After execution, the Quality Metrics Skill should provide:

* measurable engineering quality;
* evidence-based engineering intelligence;
* trustworthy engineering dashboards;
* complete metrics traceability;
* AI-assisted engineering analysis;
* continuously improving engineering excellence.

Engineering Quality Metrics establishes the canonical measurement model adopted by DESys, ensuring that every engineering decision is supported by objective evidence, reproducible calculations and meaningful indicators. By integrating engineering evidence, metrics, trends and continuous improvement into the Engineering Quality Metrics Knowledge Graph, DESys transforms quality measurement from isolated reporting into a permanent engineering discipline that drives governance, learning and engineering excellence throughout the software lifecycle.
