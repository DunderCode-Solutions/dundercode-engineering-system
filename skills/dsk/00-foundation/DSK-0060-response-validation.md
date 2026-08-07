# DSK-0060 | Response Validation

## Metadata

Document Number: DSK-0060

Canonical ID: dsk.foundation.response-validation

Document Class: Engineering Skill

Version: 1.0.0

Status: Draft

Canonical Language: English

Owner: DunderCode Engineering

---

# 1. Purpose

This document defines the response validation strategy used by AI agents within the DunderCode Engineering System (DESys).

Before any engineering deliverable is presented to the user, the agent must validate that the response complies with engineering standards, project constraints and the active skill.

Response Validation represents the final engineering quality gate of the DESys AI Runtime.

---

# 2. Validation Philosophy

DESys follows one fundamental principle:

> Every engineering response must be validated before delivery.

Generating an answer is not the end of execution.

Validation is a mandatory engineering activity.

Responses that fail validation should be corrected before being presented.

---

# 3. Validation Pipeline

Every engineering response follows the same validation sequence.

```text
Engineering Reasoning

↓

Response Generation

↓

Engineering Validation

↓

Correction (if required)

↓

Approval

↓

Final Deliverable
```

Validation occurs before the response reaches the user.

---

# 4. Validation Dimensions

Every response should be evaluated across multiple dimensions.

* Engineering correctness
* Process compliance
* Architecture consistency
* Template compliance
* Completeness
* Traceability
* Clarity
* Actionability

No single dimension is sufficient by itself.

---

# 5. Engineering Validation

Engineering validation verifies that:

* engineering standards were respected;
* canonical documentation was followed;
* architectural principles remain consistent;
* project constraints were preserved.

Engineering correctness always takes precedence over stylistic quality.

---

# 6. Process Validation

The agent verifies compliance with the applicable engineering processes.

Examples include:

* requirements process;
* architecture process;
* testing process;
* deployment process;
* governance process.

Responses should never bypass mandatory engineering workflows.

---

# 7. Documentation Validation

The response should reference the correct engineering knowledge.

Validation confirms:

* required documents were consulted;
* canonical references remain valid;
* obsolete documentation was not used;
* dependencies were resolved correctly.

---

# 8. Deliverable Validation

Every deliverable should satisfy its own acceptance criteria.

Examples:

* PRD
* ADR
* RFC
* API Specification
* Test Plan
* Deployment Guide

Completion criteria should be objective and verifiable.

---

# 9. Consistency Validation

The response should remain internally consistent.

Validation includes:

* terminology consistency;
* architectural consistency;
* process consistency;
* technology consistency;
* document consistency.

Contradictory engineering recommendations should never be produced.

---

# 10. Self-Review

Before finalizing the response, the agent performs a structured self-review.

Typical review questions include:

* Was the correct skill executed?
* Was the correct documentation loaded?
* Were engineering constraints respected?
* Are required deliverables complete?
* Is the response technically consistent?
* Can another engineer reproduce the result?

---

# 11. Validation Outcomes

Validation produces one of the following outcomes.

* Approved
* Approved with Recommendations
* Requires Revision
* Rejected

Only approved responses should be delivered without modification.

---

# 12. Failure Handling

When validation fails, the agent should:

1. identify the issue;
2. determine the root cause;
3. correct the response;
4. repeat validation.

Validation should continue until the response satisfies all mandatory engineering requirements.

---

# 13. Validation Principles

Response Validation follows these principles:

* Engineering First
* Documentation First
* Deterministic Evaluation
* Explicit Quality Gates
* Human Review Friendly
* Canonical Traceability
* Continuous Improvement

---

# 14. Vendor Independence

Response Validation is independent of any AI platform.

Regardless of whether execution occurs in ChatGPT, Claude, Gemini, Cursor, Copilot or future AI systems, the same engineering quality criteria must be applied.

Validation standards belong to DESys, not to the execution engine.

---

# 15. Expected Outcomes

Applying Response Validation enables AI agents to:

* deliver technically correct engineering outputs;
* reduce engineering inconsistencies;
* minimize hallucinations;
* improve documentation traceability;
* maintain compliance with DESys standards;
* increase confidence in AI-generated engineering artifacts.

Response Validation represents the final quality gate of the DESys AI Runtime, ensuring that every engineering deliverable is complete, consistent and aligned with organizational standards before reaching the user.
