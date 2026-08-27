---
metadata_schema: 1.0.0
document_id: DEC-0001
canonical_id: dec.foundation.engineering-manifesto
title: The DunderCode Engineering Manifesto
node_type: canon
document_class: normative
version: 1.1.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- DESys governance and engineering assets
relationships:
- type: related
  target: dem.foundation.engineering-method
- type: related
  target: dcsg.canon.style-guide
---

# DEC-0001 - The DunderCode Engineering Manifesto

## 1. Status and Authority

This document is a draft statement of DunderCode's engineering philosophy. It
does not create binding requirements until approved through DESys governance.

When distributed to a consumer repository, it is reference guidance. Consumer
code, runtime behavior, approved policies, and project decisions remain the
authority for claims about that project. Adoption requires an explicit consumer
decision or policy.

## 2. Purpose

The manifesto records principles intended to guide the design and evolution of
DESys. It is independent of a specific programming language, framework, vendor,
or delivery method.

The manifesto asks:

> How should DunderCode reason about engineering work and reusable knowledge?

## 3. Scope

The principles apply to DESys governance, documentation, architecture, software,
automation, artificial intelligence, research, and organizational learning.

They guide decisions but do not replace domain evidence, safety constraints,
legal obligations, or context-specific risk assessment. A tool-versus-principle
conflict must be evaluated against observed behavior and the applicable approved
decision rather than resolved by slogan or hierarchy alone.

## 4. Principles

### 4.1 Understand Before Committing

Engineering begins by identifying the problem, stakeholders, constraints,
evidence, and desired outcomes. Time spent reducing material uncertainty is
engineering work.

Urgent remediation may precede complete analysis. In that case, teams should
record assumptions, risk controls, and follow-up work proportionate to impact.

### 4.2 Preserve Intent and Evidence

Documentation records intended behavior, decisions, and rationale. Source code
records implementation. Tests and runtime observations provide evidence of
actual behavior.

No single representation is universally sufficient. Material disagreement
between them is a defect to investigate, not a reason to ignore one source.

### 4.3 Make Decisions Traceable

Significant engineering decisions should identify their context, evidence,
owner, consequences, and related assets. Traceability supports review and future
change; it does not infer approval authority.

### 4.4 Prefer Necessary Simplicity

Complexity should have a demonstrated purpose. Designs should favor the simplest
approach that satisfies current requirements, safety constraints, and credible
evolution needs.

Clarity is preferred over novelty when both meet the same outcomes.

### 4.5 Standardize Repeated Decisions

Standards reduce repeated analysis and improve consistency. They should define
scope, evidence, exceptions, and a path for revision.

Standards are not substitutes for judgment. Teams should tailor implementation
to project context while documenting material deviations from adopted policy.

### 4.6 Connect Knowledge to Implementation

Analysis without delivery produces limited value. Implementation without
understanding accumulates avoidable risk. Engineering connects explicit
knowledge to testable outcomes and operational evidence.

### 4.7 Learn From Outcomes

Documents, standards, processes, and implementations evolve as evidence changes.
Participating teams should capture reusable lessons when doing so is appropriate
and permitted. Public consumers are not required to contribute project content
back to DESys.

## 5. Evidence and Authority

DESys distinguishes forms of engineering evidence:

| Evidence | Primary purpose |
| --- | --- |
| Approved decisions and policies | Record governance and intended constraints. |
| Product and architecture documents | Record goals, design intent, and rationale. |
| Source code and configuration | Record the implemented system. |
| Tests and validation results | Demonstrate selected behavior and properties. |
| Runtime observations | Demonstrate behavior in an operating environment. |
| DESys reference guidance | Offer reusable practices and terminology. |

The applicable project defines approval authority. Metadata relationships and
generated indexes improve discovery but do not approve a document or resolve a
conflict.

## 6. Role of AI Assistance

AI systems may help retrieve, draft, compare, and validate engineering material.
They are not approval authorities. Outputs require review proportionate to risk,
and claims about a project require project evidence.

## 7. Governance

Changes to this manifesto require:

- an explicit proposal and rationale;
- review against existing DESys decisions;
- identification of affected guidance;
- recorded approval by the DESys governance owner;
- a version and changelog update.

Until that process completes, draft changes remain proposals.

## 8. Related Documents

- [DEM-0001 - The DunderCode Engineering Method](../../knowledge/dem/DEM-0001-engineering-method.md)
- [DCSG-0001 - DunderCode Canon Style Guide](../documentation/DCSG-0001-canon-style-guide.md)
- [Foundation navigation](../README.md)

## 9. Revision History

### 1.1.0 - Draft

- Scoped authority to DESys and explicit consumer adoption.
- Replaced documentation-only source-of-truth claims with an evidence model.
- Added urgent-work, tailoring, AI, governance, and contribution boundaries.

### 1.0.0 - Draft

- Initial manifesto draft.
