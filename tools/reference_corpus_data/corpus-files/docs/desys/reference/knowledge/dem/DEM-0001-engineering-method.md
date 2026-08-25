---
metadata_schema: 1.0.0
document_id: DEM-0001
canonical_id: dem.foundation.engineering-method
title: The DunderCode Engineering Method
node_type: method
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
relationships:
- type: depends_on
  target: dec.foundation.engineering-manifesto
---

# DEM-0001 - The DunderCode Engineering Method

## 1. Status and Authority

This document is a draft normative method for work governed by DESys. Its
requirements are proposals until an authorized lifecycle decision approves
them. Draft metadata records that state; it does not itself provide approval.

When this document is installed through the opt-in reference corpus, it is
read-only reference guidance. It does not govern a consumer project, require
every project to use this method, or override consumer code, runtime behavior,
approved decisions, policies, contracts, or legal obligations. A consumer may
adopt or adapt the method only through its own governance.

## 2. Purpose

The method offers a shared set of engineering concerns for moving from an
uncertain need to a tested outcome and useful learning. It encourages explicit
reasoning without treating documentation volume or phase completion as goals in
themselves.

The [Engineering Manifesto](../../foundation/canon/DEC-0001-engineering-manifesto.md)
provides related principles. This method proposes one way to apply them; neither
document replaces project evidence or project-specific decisions.

## 3. Scope and Tailoring

The method is intended for DESys engineering work and for consumers that
explicitly adopt it. It may be useful for software, automation, research,
documentation, and AI-assisted work, but it is not a universal project mandate.

Teams select the depth, order, and artifacts that fit the work. Tailoring should
consider:

- impact on users, operations, security, privacy, safety, and compliance;
- uncertainty, novelty, complexity, and external dependencies;
- reversibility and the cost of failure;
- delivery urgency and the useful lifetime of the result;
- available evidence and the needs of affected stakeholders.

A small, reversible change may address all lifecycle concerns in a short issue
and review. High-impact or difficult-to-reverse work may need explicit models,
decisions, specifications, independent review, and operational evidence. A team
should record a material omission or exception when doing so helps reviewers
understand accepted risk. It need not create an artifact that adds no useful
evidence or control.

## 4. Lifecycle Model

The lifecycle consists of seven concerns:

```text
Understand <-> Model <-> Design <-> Specify <-> Implement <-> Validate <-> Learn
```

The concerns are iterative rather than mandatory sequential gates. Work may
move backward, combine concerns, run them concurrently, or revisit them as new
evidence appears. The accountable project authority decides any required gates.

## 5. Engineering Concerns

### 5.1 Understand

Establish the need, affected people, desired outcome, constraints, assumptions,
and important unknowns. Useful evidence may include a problem statement,
support or operational observations, stakeholder interviews, existing system
behavior, and initial acceptance measures.

Evidence should be current enough and representative enough for the decision.
Stakeholder statements are inputs, not automatically complete requirements.

### 5.2 Model

Represent the parts of the problem that materially affect the solution. A model
may be prose, examples, a glossary, a state description, a data model, or a
diagram. It is useful only while its abstractions and limitations are understood;
it is not presumed to reproduce reality completely.

### 5.3 Design

Compare feasible approaches and identify important interfaces, data flows,
failure modes, tradeoffs, and recovery options. Record a decision when its
impact, irreversibility, or future maintenance cost warrants a durable rationale.
Routine implementation choices do not all require architecture records.

### 5.4 Specify

State the behavior and constraints that implementers and reviewers need. The
form may be acceptance criteria, examples, an interface contract, a risk
control, or a larger specification. Detail should match the cost of ambiguity;
it need not predict every implementation detail before work begins.

### 5.5 Implement

Create the smallest maintainable change that satisfies the adopted constraints.
Applicable consumer standards and approved decisions take precedence over
vendored DESys guidance. Material behavior, assumptions, and operator-facing
effects should be documented where future users can maintain them.

### 5.6 Validate

Evaluate both the result and the assumptions behind it. Depending on risk,
evidence may include focused automated tests, static analysis, review,
experiments, security assessment, accessibility checks, observed runtime
behavior, recovery exercises, or acceptance by an authorized stakeholder.

Validation supports bounded claims. Passing tests does not prove all behavior,
and documentation agreement does not prove runtime correctness. Negative,
inconclusive, stale, or conflicting evidence should be reported rather than
silently converted into a successful result.

### 5.7 Learn

Compare outcomes with expectations and decide whether a local adjustment or a
governed DESys proposal is worthwhile. Useful inputs may include incidents,
support trends, delivery data, retrospective findings, and user research.

Feedback should be collected for a defined question and handled under applicable
privacy, consent, retention, and access rules. Small samples, self-selection,
and missing feedback limit the conclusions that can be drawn. A project is not
required to contribute information to DESys, and a lesson does not become a
standard without review and lifecycle approval.

## 6. Urgent Work

An incident, security response, or other time-critical condition may require
implementation or containment before normal analysis and documentation. The
method should not delay action needed to protect people, data, service, or legal
obligations.

The response should apply the minimum controls practical in the circumstances:

- identify an accountable decision-maker and the immediate objective;
- preserve relevant evidence without impeding containment;
- consider blast radius, access, safety, and a rollback or recovery path;
- validate the immediate effect with the strongest available signal;
- record material decisions, uncertainty, and deferred work.

After stabilization, the team should complete only the analysis, validation,
documentation, and learning justified by residual risk. Consumer incident and
emergency policies remain authoritative.

## 7. Typical Evidence and Artifacts

No artifact is mandatory merely because it appears in this table.

| Concern | Examples |
| --- | --- |
| Understand | Problem statement, observations, constraints, outcome measures |
| Model | Examples, glossary, state or data model, context diagram |
| Design | Options analysis, prototype, architecture decision, threat model |
| Specify | Acceptance criteria, interface contract, operational constraints |
| Implement | Source change, configuration, migration, supporting documentation |
| Validate | Test results, review record, runtime observation, recovery exercise |
| Learn | Outcome comparison, incident finding, retrospective, change proposal |

Evidence may serve more than one concern. Links to durable evidence are often
more useful than copied summaries that can become stale.

## 8. Outcome Assessment

The adopting project defines success criteria before making a conformance or
completion claim. Assessment should account for the intended outcome, accepted
risk, observed behavior, maintainability, and unresolved evidence. Completion
of seven labels, production of every example artifact, or incorporation of a
lesson into DESys is not by itself evidence of project success.

## 9. Distribution and Editorial Context

The [reference corpus RFC](../rfc/RFC-0001-reference-corpus-distribution.md) and
[authority ADR](../adr/ADR-0001-reference-corpus-layout-and-authority.md) define
opt-in distribution, ownership, provenance, and consumer authority. The
[Canon Style Guide](../../foundation/documentation/DCSG-0001-canon-style-guide.md)
defines the draft editorial conventions used by this document. Vendoring any of
these documents does not approve or activate the method for a consumer project.
