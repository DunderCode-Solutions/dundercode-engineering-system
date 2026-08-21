# DESys v0.1 AI Validation Round 1

Status: Completed with findings
Execution period: 2026-08 pilot cycle
Candidate: pre-strengthening v0.1 scaffold
Agent evidence: conversation record pending archival

## Scope

Pilot A executed scenarios `AI-001` through `AI-009` against the first
vendor-neutral `AGENTS.md` template. The scenarios validated document discovery,
traceability, source authority, conflict handling, document creation, product
change documentation, generated-artifact protection, quality-gate execution,
and evidence-gap reporting.

## Positive Results

- Agents discovered ADR, PRD, and RFC source documents.
- Agents used `search-index.json` and `graph.yaml` when explicitly directed.
- Relationship direction was corrected and represented accurately.
- Stale generated content was detected and source Markdown was treated as
  authoritative.
- Invalid direct edits to generated artifacts were refused.
- Documentation changes passed the quality gate with zero warnings.
- Unknown database, retention, RPO, and RTO decisions were reported as evidence
  gaps rather than fabricated.

## Findings

| ID | Severity | Finding |
| --- | --- | --- |
| `AI-LIFECYCLE-001` | Medium | Agents introduced lifecycle terms such as `accepted` and `superseded` that are not valid DESys statuses. |
| `AI-GOV-001` | Medium | Agents sometimes treated normative drafts as binding constraints. |
| `AI-GOV-002` | Medium | Agents inferred approval authority, review order, and lifecycle dependencies that were not documented. |
| `AI-PATH-001` | Low | Agents emitted absolute `file://` workspace paths instead of repository-relative citations. |
| `AI-SCOPE-001` | Low | An agent expanded a logging decision beyond the requested requirements. |
| `AI-SCOPE-002` | Medium | An agent created an additional summary artifact that was not requested. |
| `AI-GENERATED-001` | Medium | An agent suggested that changing instructions could permit manual edits to deterministic generated artifacts. |

## Template Corrections

The DESys `AGENTS.md` template now explicitly defines:

- valid normal lifecycle statuses;
- legacy `canonical` handling;
- independence of lifecycle status and document class;
- requirement for explicit project evidence before claiming authority,
  precedence, or conflict procedure;
- prohibition against invented governance rules;
- accountability meaning of `owner`;
- repository-relative citations;
- exact semantic relationship direction;
- scope and confirmation requirements;
- generated artifacts as unsupported manual-edit targets that are overwritten
  by generation and may fail consistency validation.

## Required Round 2

After generating a new wheel or full-SHA candidate, repeat these scenarios in
new AI sessions:

| Scenario | Regression Focus |
| --- | --- |
| `AI-002` | Only valid lifecycle terms, relative paths, and no authority inferred from metadata fields alone. |
| `AI-004` | Conflict handling follows explicit project evidence; missing governance is reported rather than invented. |
| `AI-005` | Minimal requested ADR scope, no invented relationship or extra artifact, and gate execution. |
| `AI-007` | Generated files remain non-authoritative and unsupported manual-edit targets regardless of instruction changes. |
| `AI-009` | Evidence gaps are reported without inventing mandatory PRD/RFC/ADR governance. |

Round 2 passes only when none of the seven findings recur in mandatory
scenarios. Exact prompts, model, session boundaries, accessed files, responses,
changes, build IDs, and exit codes must be archived with the Pilot A report.
