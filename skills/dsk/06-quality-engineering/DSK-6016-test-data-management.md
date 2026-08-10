---
metadata_schema: 1.0.0
document_id: DSK-6016
canonical_id: dsk.quality.test-data-management
title: Test Data Management
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Quality Engineering
discipline: Engineering Test Data Management
---

# DSK-6016 | Test Data Management

# 1. Purpose

This skill defines the **Engineering Test Data Management (ETDM)** discipline adopted by the DunderCode Engineering System (DESys).

Within DESys, test data is not merely a collection of sample records.

It is an engineering asset responsible for enabling reliable, repeatable, secure and traceable production of engineering evidence throughout the Quality Engineering lifecycle.

Engineering Test Data Management governs the complete lifecycle of engineering test data.

---

# 2. Scope

Engineering Test Data Management governs:

* Test Data Strategy
* Test Data Generation
* Test Data Classification
* Test Data Provisioning
* Test Data Versioning
* Test Data Protection
* Test Data Governance
* Test Data Lifecycle

Engineering Test Data Management supports every Engineering Testing activity.

---

# 3. Engineering Position

Engineering Test Data enables trustworthy engineering evidence.

```text id="engineering-test-data-position"
Engineering Requirements
        ↓
Data Strategy
        ↓
Test Data Lifecycle
        ↓
Provisioning
        ↓
Testing
        ↓
Engineering Evidence
        ↓
Engineering Knowledge
```

Engineering evidence SHALL depend on trustworthy engineering data.

---

# 4. Engineering Objectives

Engineering Test Data Management aims to:

* ensure reliable engineering datasets;
* improve testing reproducibility;
* strengthen data governance;
* protect sensitive information;
* support continuous engineering quality;
* enable AI-assisted data reasoning.

---

# 5. Engineering Test Data Management Model (ETDMM)

DESys adopts the **Engineering Test Data Management Model (ETDMM)**.

Every engineering dataset SHALL define:

* Data Objectives
* Data Sources
* Data Classification
* Data Generation Strategy
* Data Provisioning Strategy
* Data Versioning
* Data Refresh Strategy
* Data Protection
* Data Traceability
* Data Retirement Strategy

The ETDMM defines the canonical test data management model adopted by DESys.

---

# 6. Engineering Test Data Principles

Engineering Test Data Management SHALL follow:

* Data by Design
* Deterministic Data
* Reproducible Data
* Minimal Necessary Data
* Privacy by Design
* Synthetic First
* Traceable Data
* Versioned Data
* Isolated Data
* Continuous Data Governance

These principles SHALL guide every engineering data decision.

---

# 7. Test Data Lifecycle

Every engineering dataset progresses through a controlled lifecycle.

```text id="test-data-lifecycle"
Designed
        ↓
Generated
        ↓
Provisioned
        ↓
Consumed
        ↓
Observed
        ↓
Refreshed
        ↓
Retired
```

Engineering datasets SHALL continuously evolve.

---

# 8. Data Sources

Engineering Test Data MAY originate from multiple controlled sources.

Typical sources include:

* Synthetic Data
* Masked Production Data
* Seed Data
* Generated Data
* Mock Data
* Reference Data
* Scenario Data
* Contract Data

Synthetic or protected datasets SHALL be preferred whenever feasible.

---

# 9. Data Classification

Every engineering dataset SHALL be classified.

Typical classifications include:

* Public
* Internal
* Confidential
* Restricted
* Sensitive

Classification SHALL determine handling, access and protection requirements.

---

# 10. Data Provisioning Strategy

Engineering Test Data MAY be provisioned through multiple strategies.

Typical strategies include:

* On Demand
* Per Test
* Per Suite
* Per Environment
* Per Pipeline
* Ephemeral
* Shared
* Immutable

Provisioning SHALL remain deterministic and repeatable.

---

# 11. Engineering Test Data Factory (ETDF)

DESys adopts the concept of the **Engineering Test Data Factory (ETDF)**.

The ETDF MAY provide:

* dataset generation;
* data masking;
* dataset versioning;
* provisioning;
* validation;
* lifecycle management;
* dataset recycling.

The ETDF centralizes engineering test data governance.

---

# 12. Test Data Registry (TDR)

Every engineering dataset SHALL be registered.

Example:

```yaml id="test-data-registry"
dataset:

  Customer Checkout

classification:

  Confidential

source:

  Synthetic

version:

  3.2

status:

  Active
```

The Test Data Registry preserves engineering dataset metadata.

---

# 13. Engineering Test Data Knowledge Graph (ETDKG)

DESys represents engineering data relationships through the Engineering Test Data Knowledge Graph.

Example:

```text id="engineering-test-data-knowledge-graph"
Requirement
        │ defines
        ▼
Scenario
        │ requires
        ▼
Dataset
        │ supports
        ▼
Execution
        │ produces
        ▼
Evidence
        │ strengthens
        ▼
Engineering Quality
```

The Engineering Test Data Knowledge Graph enables:

* semantic navigation;
* dataset reasoning;
* scenario analysis;
* impact assessment;
* AI-assisted dataset evaluation.

---

# 14. Data Quality Attributes

Engineering Test Data SHALL evaluate:

* Completeness
* Accuracy
* Consistency
* Freshness
* Realism
* Privacy
* Reusability
* Traceability
* Availability

Dataset quality SHALL remain measurable.

---

# 15. Data Versioning

Every engineering dataset SHALL define:

* Dataset Version
* Schema Version
* Generator Version
* Refresh Date
* Source
* Owner

Engineering datasets SHALL evolve under controlled versioning.

---

# 16. Data Metrics

Typical engineering indicators include:

```yaml id="test-data-metrics"
synthetic_data:

  92

sensitive_data:

  0

refresh_time:

  5m

provision_time:

  20s

dataset_reuse:

  84
```

Engineering data quality SHALL remain measurable.

---

# 17. AI Data Analysis

AI MAY automatically evaluate:

* obsolete datasets;
* inconsistent datasets;
* duplicated datasets;
* unmasked sensitive information;
* missing scenario coverage;
* unused datasets;
* insufficient data diversity;
* data refresh effectiveness.

Recommendations SHALL remain deterministic and evidence-based.

---

# 18. Engineering Rules

Engineering Test Data Management MUST:

* define explicit dataset ownership;
* classify every engineering dataset;
* preserve dataset versioning;
* protect sensitive information;
* maintain complete traceability;
* support reproducible engineering evidence.

Engineering Test Data Management MUST NOT:

* expose production data without protection;
* lose dataset history;
* compromise privacy;
* depend on undocumented manual data changes;
* weaken engineering reproducibility.

---

# 19. Inputs

Typical inputs include:

* Engineering Requirements
* Testing Strategy
* Test Architecture
* Automation Pipelines
* Security Policies
* Privacy Requirements

---

# 20. Outputs

Typical deliverables include:

* Test Data Registry
* Engineering Test Data Knowledge Graph
* Engineering Datasets
* Provisioning Strategies
* Dataset Documentation
* Data Quality Metrics

---

# 21. Execution Workflow

1. Define engineering data objectives.
2. Identify appropriate data sources.
3. Classify engineering datasets.
4. Generate or provision datasets.
5. Protect sensitive information.
6. Register engineering datasets.
7. Update the Engineering Test Data Knowledge Graph.
8. Measure dataset quality.
9. Refresh engineering datasets.
10. Retire obsolete datasets.

---

# 22. Validation

Before completion the skill verifies:

* dataset ownership is defined;
* classification is explicit;
* provisioning strategy is documented;
* sensitive information is protected;
* dataset quality is measurable;
* Test Data Registry and Engineering Test Data Knowledge Graph remain synchronized.

---

# 23. Dependencies

## Parent Skill

* DSK-6000 Quality Engineering Overview

## Foundation Skills

* DSK-6013 Testing Engineering
* DSK-6014 Test Architecture
* DSK-6015 Test Automation

Engineering Test Data Management provides the trusted datasets required by Testing Engineering, Test Architecture and Test Automation to continuously produce reliable engineering evidence.

---

# 24. Collaboration

The Test Data Management Skill collaborates with:

* Software Engineering
* Security Engineering
* Infrastructure Engineering
* Privacy Engineering
* Quality Governance
* AI Reasoning Engine

Engineering Test Data Management becomes the discipline responsible for governing engineering datasets across the complete DESys ecosystem.

---

# 25. Expected Outcomes

After execution, the Test Data Management Skill should provide:

* trustworthy engineering datasets;
* secure and reproducible test data;
* measurable dataset quality;
* complete dataset traceability;
* AI-assisted dataset reasoning;
* continuously governed engineering data.

Engineering Test Data Management establishes the canonical test data model adopted by DESys, ensuring that every engineering dataset is generated, classified, protected, versioned and governed throughout its complete lifecycle. By integrating dataset strategies, provisioning, quality attributes and engineering evidence into the Engineering Test Data Knowledge Graph, DESys transforms test data from disposable test fixtures into strategic engineering assets that sustain verification, validation, testing and continuous engineering excellence.
