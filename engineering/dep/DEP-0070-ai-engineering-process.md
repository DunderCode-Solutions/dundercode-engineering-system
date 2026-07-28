# DEP-0070 — AI Engineering Process

# Metadata

**Canonical ID:** dep.ai.engineering.process

**Document Class:** Engineering Process Standard

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

**Applies To:** All AI-enabled software systems developed within DESys

---

# 1. Purpose

The AI Engineering Process defines the standardized engineering workflow for designing, developing, validating, deploying, operating, and governing Artificial Intelligence systems within the DunderCode Engineering System (DESys).

Its purpose is to ensure that AI systems are engineered using the same level of discipline, traceability, quality, governance, and continuous improvement expected from traditional software engineering.

---

# 2. Scope

This process applies to:

* Large Language Model (LLM) applications
* Retrieval-Augmented Generation (RAG)
* AI Assistants
* AI Agents
* Prompt-based systems
* Knowledge-driven AI
* Machine Learning integrations
* Hybrid software systems containing AI components

---

# 3. Audience

This document is intended for:

* AI Engineers
* Software Engineers
* AI Architects
* Solution Architects
* Technical Leaders
* Engineering Managers
* MLOps Engineers
* Platform Engineers
* AI Governance Teams

---

# 4. AI Engineering Workflow

Every AI-enabled solution SHALL follow the workflow below.

```text
Business Need
        │
        ▼
AI Feasibility Analysis
        │
        ▼
Knowledge Engineering
        │
        ▼
Prompt & Solution Design
        │
        ▼
AI Implementation
        │
        ▼
AI Evaluation
        │
        ▼
Human Oversight Review
        │
        ▼
Deployment
        │
        ▼
AI Operations
        │
        ▼
Continuous Improvement
```

Each phase SHALL produce engineering artifacts that support traceability and governance.

---

# 5. Process Activities

## 5.1 AI Feasibility Analysis

Determine whether AI is the appropriate solution.

Typical activities include:

* Problem definition
* Business value assessment
* Risk analysis
* AI suitability analysis
* Cost estimation

Output:

* AI feasibility assessment

---

## 5.2 Knowledge Engineering

Prepare the knowledge foundation used by the AI system.

Typical activities include:

* Knowledge source identification
* Knowledge organization
* Retrieval strategy definition
* Knowledge quality validation
* Knowledge versioning

Output:

* Knowledge Base

Reference:

* DES-0920 Knowledge Engineering

---

## 5.3 Prompt & Solution Design

Design AI interaction behavior.

Typical activities include:

* Prompt engineering
* Context strategy
* Guardrails
* Output constraints
* Tool orchestration
* Conversation design

Output:

* Prompt specification

Reference:

* DES-0910 Prompt Engineering

---

## 5.4 AI Implementation

Develop the AI-enabled solution.

Typical activities include:

* Model integration
* API integration
* Retrieval implementation
* Agent implementation
* Tool integration
* Logging implementation

Output:

* AI implementation

---

## 5.5 AI Evaluation

Evaluate AI quality before production.

Typical activities include:

* Accuracy evaluation
* Hallucination detection
* Consistency validation
* Prompt evaluation
* Retrieval evaluation
* Performance validation

Output:

* AI Evaluation Report

Reference:

* DES-0940 AI Evaluation

---

## 5.6 Human Oversight Review

Human reviewers validate AI behavior.

Typical activities include:

* Human review
* Risk validation
* Exception analysis
* Decision approval

Output:

* Human Approval

Reference:

* DES-0960 Human Oversight

---

## 5.7 Deployment

Deploy the validated AI solution.

Reference:

* DEP-0060 Deployment Process

---

## 5.8 AI Operations

Operate and monitor AI systems.

Typical activities include:

* Model monitoring
* Prompt monitoring
* Cost monitoring
* Latency monitoring
* Knowledge updates
* Incident management

Output:

* Operational AI Metrics

Reference:

* DES-0970 AI Operations

---

## 5.9 Continuous Improvement

Continuously improve the AI system.

Typical activities include:

* Prompt refinement
* Knowledge updates
* Model replacement
* Evaluation improvements
* User feedback analysis
* Governance review

Output:

* Improved AI System

---

# 6. Engineering Principles

Every AI engineering activity SHALL follow these principles.

## Human-Centered

AI shall augment human capabilities.

---

## Knowledge Driven

AI shall rely on governed knowledge whenever practical.

---

## Explainability

AI behavior should be understandable and reviewable.

---

## Safety

AI shall incorporate engineering safety controls.

---

## Governance

AI decisions shall remain governed throughout their lifecycle.

---

## Continuous Evaluation

AI quality shall be continuously measured.

---

## Human Oversight

Critical decisions SHALL support human supervision.

---

## Traceability

AI outputs shall remain traceable to prompts, knowledge, models, and engineering decisions.

---

# 7. Engineering Deliverables

| Activity               | Deliverable               |
| ---------------------- | ------------------------- |
| AI Feasibility         | AI Feasibility Assessment |
| Knowledge Engineering  | Knowledge Base            |
| Prompt Design          | Prompt Specification      |
| AI Implementation      | AI Solution               |
| AI Evaluation          | AI Evaluation Report      |
| Human Oversight        | Human Approval            |
| Deployment             | Operational AI System     |
| AI Operations          | Operational Metrics       |
| Continuous Improvement | Updated AI System         |

---

# 8. Compliance

An AI system complies with this process when it:

* Demonstrates business justification.
* Uses governed knowledge.
* Documents prompt behavior.
* Successfully completes AI evaluation.
* Supports human oversight.
* Preserves engineering traceability.
* Complies with DES AI Engineering Standards.

---

# 9. Relationship with Other DEP Documents

| Document | Relationship                         |
| -------- | ------------------------------------ |
| DEP-0010 | Defines the engineering lifecycle    |
| DEP-0020 | Provides AI requirements             |
| DEP-0030 | Defines AI architecture              |
| DEP-0040 | Implements AI components             |
| DEP-0050 | Validates AI behavior                |
| DEP-0060 | Deploys AI systems                   |
| DEP-0070 | Defines the AI engineering lifecycle |
| DEP-0080 | Governs AI engineering execution     |

The AI Engineering Process extends the standard software engineering lifecycle with AI-specific engineering activities while maintaining consistency with the overall DESys engineering model.

---

# 10. References

* DES-0900 — AI Engineering Principles
* DES-0910 — Prompt Engineering
* DES-0920 — Knowledge Engineering
* DES-0930 — Model Lifecycle Management
* DES-0940 — AI Evaluation
* DES-0950 — AI Safety
* DES-0960 — Human Oversight
* DES-0970 — AI Operations
* DES-0980 — AI Governance
* DEA — DunderCode Engineering Architecture
* DET — DunderCode Engineering Templates

---

# 11. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial AI Engineering Process.
* Defined the standardized AI engineering lifecycle.
* Established AI engineering activities, principles, deliverables, compliance requirements, and governance checkpoints.
* Integrated the complete DES AI Standards (DES-0900 through DES-0980) into a unified engineering execution process.
