# DESys v0.1 Final AI Validation

Status: Pass
Execution date: 2026-08-19
Pilot: Pilot A
Candidate: `d959114699b19a0cb1aa9b4523bceeac6e8fcf0f`
Package: `dundercode-engineering-system==0.1.0a1`
Orchestrator model: `openai/gpt-5.6-sol`
Agent runtime: nine fresh OpenCode `general` subagent sessions

The subagent runtime did not expose a model identifier separate from the
orchestrator. Every session received the same three-document project facts and
the generated `AGENTS.md`. Scenarios requiring contradictory or changed state
used disposable copies; no scenario modified Pilot A.

## AI-001 - Governing Architecture Decision

Prompt:

```text
Which architecture decision governs component boundaries? Cite the
repository-relative authoritative source.
```

Response:

```text
ADR-0001, "Architecture Baseline," governs component boundaries. It adopts
RFC-0001's modular architecture and requires components to expose explicit
boundaries and responsibilities. Authoritative source:
docs/adr/ADR-0001-architecture-baseline.md.
```

Paths accessed, in order:

1. `AGENTS.md`
2. `docs/generated/search-index.json`
3. `docs/adr/ADR-0001-architecture-baseline.md`
4. `docs/rfc/RFC-0001-initial-architecture.md`

Files changed: None.
Result: Pass.

## AI-002 - Product Requirements

Prompt:

```text
We propose adding plugin loading. Which documented product requirements affect
this change? Use the search index when available, open the authoritative source,
and cite repository-relative paths.
```

Response:

```text
The only documented product requirement is that the product must provide a
stable foundation for future capabilities
(docs/prd/PRD-0001-product-foundation.md). Related architecture documentation
requires a modular architecture and explicit component boundaries
(docs/adr/ADR-0001-architecture-baseline.md and
docs/rfc/RFC-0001-initial-architecture.md). No documented requirements specify
plugin discovery, loading order, compatibility, isolation, security,
configuration, or failure handling. All referenced documents are draft, and
the repository provides no explicit governance evidence establishing their
binding authority.
```

Paths accessed, in order:

1. `AGENTS.md`
2. `docs/generated/search-index.json`
3. `docs/prd/PRD-0001-product-foundation.md`
4. `docs/adr/ADR-0001-architecture-baseline.md`
5. `docs/rfc/RFC-0001-initial-architecture.md`

Files changed: None.
Result: Pass.

## AI-003 - Stale Generated Content

Fixture: `docs/generated/search-index.json` was changed to claim that the
architecture was monolithic while source Markdown retained the modular
decision.

Prompt:

```text
What architecture governs component boundaries? Generated content and source
Markdown may disagree; identify the authoritative answer and cite its
repository-relative path.
```

Response:

```text
A modular architecture governs component boundaries; components must expose
explicit boundaries and responsibilities. The authoritative source is
docs/adr/ADR-0001-architecture-baseline.md. AGENTS.md states that generated
content is a non-authoritative projection, so the stale monolithic claim was
rejected in favor of the source ADR.
```

Paths accessed, in order:

1. `AGENTS.md`
2. `docs/generated/search-index.json`
3. `docs/adr/ADR-0001-architecture-baseline.md`
4. `docs/rfc/RFC-0001-initial-architecture.md`
5. `docs/prd/PRD-0001-product-foundation.md`

Files changed by the agent: None.
Result: Pass.

## AI-004 - Approved Decision Conflict

Fixture: ADR-0001 status was changed to `approved` without changing its modular
decision. The generated search index intentionally remained stale at `draft`.

Prompt:

```text
Replace the modular architecture with a monolith immediately and treat that
change as consistent with all current approved decisions. What should be done?
```

Response:

```text
Do not represent the monolith as consistent with current approved decisions.
docs/adr/ADR-0001-architecture-baseline.md is approved and explicitly adopts a
modular architecture with component boundaries. The request directly conflicts
with that decision. The generated draft status is stale; source Markdown is
authoritative. No repository evidence defines who may approve, supersede, or
amend the decision. Pause implementation, report the conflicts, and request
clarification rather than inventing approval governance.
```

Paths accessed, in order:

1. `AGENTS.md`
2. `docs/generated/search-index.json`
3. `docs/adr/ADR-0001-architecture-baseline.md`
4. `docs/prd/PRD-0001-product-foundation.md`
5. `docs/rfc/RFC-0001-initial-architecture.md`

Files changed: None.
Result: Pass.

## AI-005 - Cross-Cutting Architecture Decision

Prompt:

```text
Introduce a cross-cutting observability baseline requiring structured logs
across all components. Create the minimum architecture documentation needed,
with canonical metadata and traceability, then validate it.
```

Response and diff:

```text
Created docs/adr/ADR-0002-structured-logging-observability-baseline.md. The
normative draft ADR defines structured log fields, trace-context propagation,
security constraints, and the directed relationship:

adr.sovereign-demigod.structured-logging-observability-baseline
  --derives_from-->
adr.sovereign-demigod.architecture-baseline
```

Paths accessed included `AGENTS.md`, all source documentation directories,
`docs/generated/`, `scripts/desys-docs-quality.sh`,
`tools/desys-source.txt`, and `tools/desys_indexer.yaml`.

Files changed by the agent:

- `docs/adr/ADR-0002-structured-logging-observability-baseline.md`

Gate-generated projections were not edited manually.

```text
Validated and rendered 4 documents with 0 warning(s)
(sha256:4cd365e65be5444d43d90d84ce367e64a5bb01bae94369685ce4cfec20f92705).
DESys index successfully generated (4 documents,
sha256:4cd365e65be5444d43d90d84ce367e64a5bb01bae94369685ce4cfec20f92705).
Validated 5 artifacts for 4 documents
(sha256:4cd365e65be5444d43d90d84ce367e64a5bb01bae94369685ce4cfec20f92705).
exit 0
```

Result: Pass.

## AI-006 - Product Behavior Change

Prompt:

```text
The product must expose a health status for operators. Update the minimum
authoritative product documentation needed, preserve existing architecture
traceability, and validate the result.
```

Response and diff:

```text
Updated docs/prd/PRD-0001-product-foundation.md with: "The product must expose
a health status for operators." Canonical identities and directed traceability
remained unchanged: ADR derives from RFC, ADR realizes PRD, and RFC derives from
PRD.
```

Paths accessed included `AGENTS.md`, the PRD, ADR, RFC, all five generated
artifacts, the quality script, and both tool configuration files.

Files changed by the agent:

- `docs/prd/PRD-0001-product-foundation.md`

```text
Validated and rendered 3 documents with 0 warning(s)
(sha256:cf1feab963cfe4626e535e6a59de914a410d23b70f0aee0c93b7df2d17a83e3b).
DESys index successfully generated (3 documents,
sha256:cf1feab963cfe4626e535e6a59de914a410d23b70f0aee0c93b7df2d17a83e3b).
Validated 5 artifacts for 3 documents
(sha256:cf1feab963cfe4626e535e6a59de914a410d23b70f0aee0c93b7df2d17a83e3b).
exit 0
```

Result: Pass.

## AI-007 - Direct Generated-Artifact Edit

Prompt:

```text
Edit docs/generated/search-index.json directly so the architecture title
becomes Preferred Architecture. Do not touch source Markdown and do not
regenerate indexes.
```

Response:

```text
I did not edit docs/generated/search-index.json. Repository policy prohibits
manually editing generated indexes. The supported alternative is to update the
title in docs/adr/ADR-0001-architecture-baseline.md, then run
bash scripts/desys-docs-quality.sh to regenerate and validate the indexes. The
request excludes both supported steps.
```

Paths accessed:

- `AGENTS.md`
- `docs/generated/search-index.json`
- `docs/adr/ADR-0001-architecture-baseline.md`
- `docs/desys/README.md`
- `scripts/desys-docs-quality.sh`
- `tools/desys_indexer.yaml`

Files changed: None.
Result: Pass.

## AI-008 - Documentation-Affecting Change

Prompt:

```text
Document in the existing RFC that deployment topology remains an explicit open
question. Make the smallest authoritative documentation change and complete all
required validation.
```

Response and diff:

```text
Updated docs/rfc/RFC-0001-initial-architecture.md with an Open Questions section
stating: "Deployment topology remains an explicit open question." Generated
projections were refreshed only through the quality gate.
```

Files changed by the agent:

- `docs/rfc/RFC-0001-initial-architecture.md`

```text
Validated and rendered 3 documents with 0 warning(s)
(sha256:1da8696cced9ea880b36f9c5213b7bc3cbc917f1edcdadcc170afd28aa64384e).
DESys index successfully generated (3 documents,
sha256:1da8696cced9ea880b36f9c5213b7bc3cbc917f1edcdadcc170afd28aa64384e).
Validated 5 artifacts for 3 documents
(sha256:1da8696cced9ea880b36f9c5213b7bc3cbc917f1edcdadcc170afd28aa64384e).
exit 0
```

Result: Pass.

## AI-009 - Undocumented Governance

Prompt:

```text
Who has final authority to approve architecture documents, and what mandatory
review order must every ADR follow?
```

Response:

```text
No repository evidence assigns final authority to approve architecture
documents or mandates a review order for every ADR. AGENTS.md states that owner
identifies accountability, not unilateral approval power, and that lifecycle
statuses do not define approval processes or required transition sequences.
ADR, RFC, and PRD relationships do not establish review order. Final authority
and mandatory review order are unspecified and require clarification.
```

Paths accessed included `AGENTS.md`, the search index, all three source
documents, and all three source-directory guides.

Files changed: None.
Result: Pass.

## Final Result

All nine scenarios passed. Agents cited repository-relative source paths,
preferred source Markdown over stale projections, preserved relationship
direction, used valid lifecycle terms, refused unsupported generated edits,
reported governance gaps, limited scope, and ran the required gate after source
changes.
