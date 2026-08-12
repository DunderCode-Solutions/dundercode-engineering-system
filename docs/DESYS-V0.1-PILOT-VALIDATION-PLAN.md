# DESys v0.1 Pilot Validation Plan

Status: Draft
Plan version: 1.1
Last updated: 2026-08-10

## 1. Purpose

This plan defines the evidence required to decide whether DESys v0.1 is ready
for public release. It validates the system in real consumer repositories,
outside the DESys development workspace, with realistic documentation, CI, and
AI-assisted engineering workflows.

The plan produces an auditable go/no-go decision. Passing automated tests in
the DESys repository is an entry condition, not sufficient release evidence.

## 2. Release Scope

DESys v0.1 provides documentation-as-code capabilities:

- canonical metadata for project engineering documents;
- ADR, PRD, and RFC project collections;
- deterministic indexing and generated knowledge artifacts;
- local and CI documentation quality gates;
- `desys-project-init` consumer scaffolding;
- vendor-neutral `AGENTS.md` documentation instructions;
- isolated Python 3.12 tooling managed by `uvx`, independent from the consumer
  runtime and dependency environment.

The following capabilities are outside the v0.1 release scope:

- automatic DESys skill installation or activation;
- agent-specific plugins or configuration;
- retrieval-augmented generation services;
- vector databases or hosted search;
- automatic migration of arbitrary existing documentation;
- automatic updates of a scaffold created by an older DESys version;
- support for canonical document languages other than English.

## 3. Validation Objectives

The pilot must establish that:

1. A consumer can install DESys from an immutable source.
2. The initializer is safe, deterministic, understandable, and idempotent.
3. Existing consumer content is not lost or silently replaced.
4. Real ADR, PRD, and RFC documents can be validated and indexed.
5. Generated artifacts are deterministic and internally consistent.
6. AI agents can discover and respect project documentation through
   `AGENTS.md` and the generated indexes.
7. The generated GitHub Actions workflow works from a clean checkout.
8. Adoption instructions are sufficient without direct maintainer support.
9. Known platform and product constraints are explicit before release.

## 4. Required Pilot Portfolio

At least two consumer repositories must complete this plan.

| Pilot | Required Profile |
| --- | --- |
| Pilot A | New or nearly empty Git repository with no engineering documentation. |
| Pilot B | Existing project with source code, `.gitignore`, CI, and an existing `AGENTS.md` if available. |

At least one pilot must be executed by a person who did not implement
`desys-project-init`. This validates the documentation rather than maintainer
familiarity.

## 5. Supported Environment Under Test

Record the following for every pilot before execution.

| Field | Recorded Value |
| --- | --- |
| Pilot identifier | |
| Project type | |
| Project lifecycle stage | |
| Primary language and framework | |
| Operating system | |
| CPU architecture | |
| Python version | |
| DESys tool Python version | |
| `uv` version | |
| Git version | |
| CI platform | |
| AI agent or assistant | |
| Existing documentation structure | |
| Existing `AGENTS.md` | Yes / No |
| Existing `.gitignore` | Yes / No |
| Existing GitHub Actions workflows | Yes / No |
| DESys source version or full commit SHA | |

The DESys tool baseline is Python 3.12 and `uv` 0.12.3. The consumer project may
use another Python version or another implementation language. The pilot must
prove that DESys does not modify or constrain that consumer runtime.

## 6. Evidence Handling

Evidence must not contain secrets, credentials, proprietary source code,
personal information, or confidential business data. Sanitize logs and sample
documents before attaching them to the pilot report.

Required evidence types are:

- command and version output;
- initializer dry-run and apply logs;
- sanitized Git diffs;
- quality-gate logs;
- CI run links or exported logs;
- generated artifact summaries and build IDs;
- AI scenario prompts and sanitized responses;
- elapsed-time observations;
- defect records and user feedback.

## 7. Entry Criteria

Pilot execution may begin only when:

- the DESys quality gate passes on the candidate revision;
- all automated tests pass;
- metadata validation reports zero errors;
- the candidate revision is pushed and immutable for the pilot duration;
- package metadata and installation instructions identify the same version;
- the pilot repository has a recoverable baseline commit;
- the tester understands which project information must be sanitized.

## 8. Reference Commands

Replace the placeholders with an approved HTTPS repository and full Git commit
SHA. Exact published versions and committed repository-relative wheels are also
supported immutable sources.

```bash
DESYS_SOURCE="dundercode-engineering-system @ git+https://<REPOSITORY_URL>@<FULL_COMMIT_SHA>"

uvx --isolated --no-config --python 3.12 --from "$DESYS_SOURCE" \
  desys-project-init --root . --desys-source "$DESYS_SOURCE" --dry-run
uvx --isolated --no-config --python 3.12 --from "$DESYS_SOURCE" \
  desys-project-init --root . --desys-source "$DESYS_SOURCE"
bash scripts/desys-docs-quality.sh
```

Capture the command, exit code, standard output, standard error, and elapsed
time for every test that executes a command.

## 9. Environment And Packaging Tests

| ID | Test | Expected Result | Required Evidence |
| --- | --- | --- | --- |
| ENV-001 | Record all environment fields from section 5. | No required field is blank. | Completed environment table. |
| PKG-001 | Install from a full commit SHA or exact published package version. | Installation succeeds without an unpinned branch or tag source. | Command, source revision, and output. |
| PKG-002 | Repeat installation in a clean environment without the DESys development virtual environment. | The command resolves and runs independently. | Clean-environment log. |
| PKG-003 | Run `desys-project-init --version`. | Output matches package metadata and release documentation. | Version output. |
| PKG-004 | Inspect `tools/desys-source.txt`. | It contains exactly the immutable source used to invoke the initializer. | Source file and candidate revision. |
| PKG-005 | Run the gate in a project with its own runtime and lockfile. | DESys uses isolated Python 3.12 and does not modify `.venv`, `pyproject.toml`, or the consumer lockfile. | Before/after checksums and command output. |
| PKG-006 | Run the gate twice with the same source. | The first run resolves the tool; the second reuses the uv cache without changing behavior. | Cold and warm logs. |

## 10. Initializer Safety And Behavior Tests

| ID | Test | Expected Result | Required Evidence |
| --- | --- | --- | --- |
| INIT-001 | Run dry-run in Pilot A. | Exit code 0, complete plan shown, no filesystem change. | Log and before/after `git status`. |
| INIT-002 | Apply the clean plan in Pilot A. | Expected scaffold is created and reported. | Apply log and sanitized diff. |
| INIT-003 | Run the initializer again without changes. | Exit code 0 and every managed path is `UNCHANGED`. | Second-run log. |
| INIT-004 | Run dry-run in Pilot B with an existing `.gitignore`. | DESys proposes only the managed ignore block and preserves existing bytes. | Before/after file and log. |
| INIT-005 | Apply in Pilot B with an existing `AGENTS.md`. | Existing instructions remain unchanged outside one DESys marker block. | Before/after file and diff. |
| INIT-006 | Create a divergent managed file and run the initializer. | Exit code 1, conflict reported, and no unrelated path is written. | Conflict log and before/after status. |
| INIT-007 | Create an incomplete DESys marker block. | Exit code 1 and a malformed-marker conflict is reported. | Conflict log. |
| INIT-008 | Run against a directory that is not a Git worktree root. | Exit code 1 with an actionable root error. | Command and error output. |
| INIT-009 | Replace a managed path with a symlink in a disposable fixture. | Exit code 1 and no scaffold write occurs. | Fixture description and log. |
| INIT-010 | Invoke the generated quality script from another working directory. | The script resolves and operates on its own repository. | Command and output. |
| INIT-011 | Compare clean scaffolds generated in equivalent repositories. | Generated file bytes are identical. | Checksums or recursive diff. |
| INIT-012 | Review all generated paths with the consumer team. | No generated file has an unexplained purpose. | Review notes. |

## 11. Scaffold Content Review

Confirm that the applied scaffold contains:

| Path | Validation |
| --- | --- |
| `AGENTS.md` | Contains exactly one complete DESys instruction block. |
| `.gitignore` | Ignores `/docs/generated/` exactly once. |
| `docs/adr/README.md` | Explains ADR filename and metadata expectations. |
| `docs/prd/README.md` | Explains PRD filename and metadata expectations. |
| `docs/rfc/README.md` | Explains RFC filename and metadata expectations. |
| `docs/desys/README.md` | Explains isolated tooling, immutable source, quality gate, generated output, and agent usage. |
| `tools/desys-source.txt` | Contains exactly one supported immutable DESys source. |
| `tools/desys_indexer.yaml` | Selects project sources and all five artifacts. |
| `scripts/desys-docs-quality.sh` | Uses isolated Python 3.12 to perform dry-run, generation, and artifact validation. |
| `.github/workflows/desys-docs-quality.yml` | Installs only uv and runs the isolated local gate. |

## 12. Real Documentation Tests

The pilot must create meaningful, sanitized project documents rather than
placeholder-only examples.

| ID | Test | Expected Result | Required Evidence |
| --- | --- | --- | --- |
| DOC-001 | Create one ADR with canonical metadata. | Metadata and filename validate. | Document path and validation output. |
| DOC-002 | Create one PRD with canonical metadata. | Metadata and filename validate. | Document path and validation output. |
| DOC-003 | Create one RFC with canonical metadata. | Metadata and filename validate. | Document path and validation output. |
| DOC-004 | Add at least one valid semantic relationship between pilot documents. | Relationship target resolves in `graph.yaml`. | Source metadata and graph edge. |
| DOC-005 | Run the documentation quality gate. | Exit code 0, zero errors, and zero warnings for new project documents. | Complete quality log. |
| DOC-006 | Introduce an invalid required field in a disposable change. | Gate fails with the document path and actionable message. | Failure log. |
| DOC-007 | Introduce a duplicate document or canonical ID. | Gate fails and identifies the duplicate identity. | Failure log. |
| DOC-008 | Introduce an unresolved relationship. | Gate fails and identifies the unresolved target. | Failure log. |
| DOC-009 | Restore valid content and rerun the gate. | Gate returns to exit code 0. | Recovery log. |
| DOC-010 | Run generation twice without source changes. | Both runs produce the same build ID and file checksums. | Build IDs and checksums. |
| DOC-011 | Review generated search content. | Titles, paths, summaries, metadata, and content match source documents. | Sanitized artifact excerpts. |
| DOC-012 | Confirm generated-output ownership. | No source document or manually maintained file exists under `docs/generated/`. | Directory listing. |

## 13. Generated Artifact Tests

| Artifact | Required Validation |
| --- | --- |
| `index.yaml` | Contains every pilot document once, sorted by canonical ID. |
| `graph.yaml` | Contains every node and all deliberate relationships. |
| `navigation.yaml` | Groups all documents under their project paths. |
| `aliases.yaml` | Contains only deliberate aliases with valid targets. |
| `search-index.json` | Contains searchable source content and correct source paths. |

All five artifacts must share the same schema version and build ID. The
artifact checker rejects missing, additional, or internally inconsistent files.
Manual edits are unsupported and overwritten by normal generation; provenance
of a pre-generation artifact is not independently detected.

## 14. AI Agent Validation Scenarios

Use the same sanitized project facts for every tested agent so results can be
compared. Record the exact prompt, relevant repository state, response, files
read, files changed, and final quality-gate result.

| ID | Scenario | Expected Agent Behavior | Required Evidence |
| --- | --- | --- | --- |
| AI-001 | Ask which architecture decision governs a pilot component. | Reads `AGENTS.md`, discovers the ADR, and cites its source path. | Prompt, response, and accessed paths. |
| AI-002 | Ask for requirements affecting a proposed change. | Uses the search index when available and opens the authoritative PRD. | Prompt, response, and accessed paths. |
| AI-003 | Make generated index content intentionally stale in a disposable fixture. | Treats source Markdown as authoritative rather than stale generated content. | Fixture and response. |
| AI-004 | Request a change that contradicts an approved ADR. | Reports the conflict and does not silently bypass the decision. | Prompt and response. |
| AI-005 | Request a new cross-cutting architecture decision. | Creates or proposes an ADR with canonical metadata. | Resulting diff. |
| AI-006 | Request a product behavior change. | Updates or proposes the relevant PRD and preserves traceability. | Resulting diff. |
| AI-007 | Request direct editing of `docs/generated/`. | Refuses direct edits and points to source documents and regeneration. | Prompt and response. |
| AI-008 | Complete a documentation-affecting change. | Runs the quality gate and reports its result. | Agent log and gate output. |
| AI-009 | Ask a question not answered by project documentation. | States the evidence gap rather than inventing a project decision. | Prompt and response. |

An AI scenario fails if the agent fabricates a decision, cites the wrong source,
edits generated artifacts directly, ignores an approved contradiction, or
claims validation without running the required command.

The generated `AGENTS.md` instructions also require valid lifecycle terms,
repository-relative citations, exact relationship direction, independent
interpretation of lifecycle and document class, explicit governance evidence
gaps, and confirmation before expanding the requested scope. Results from a
previous instruction template must be repeated after that template changes.

## 15. Continuous Integration Tests

| ID | Test | Expected Result | Required Evidence |
| --- | --- | --- | --- |
| CI-001 | Open a pull request with valid project documents. | Documentation job passes. | CI link or exported log. |
| CI-002 | Open or simulate a pull request with invalid metadata. | Documentation job fails at validation. | CI failure log. |
| CI-003 | Make `tools/desys-source.txt` missing, malformed, mutable, or unresolvable. | CI fails before executing DESys tooling. | CI failure log. |
| CI-004 | Run CI from a clean checkout. | No untracked local dependency is required. | CI checkout and install log. |
| CI-005 | Run once with a cold cache and once with a warm cache. | Both runs pass; cache changes performance only. | Durations and logs. |
| CI-006 | Run the same revision three consecutive times. | All runs pass with the same build ID. | Three run links and build IDs. |
| CI-007 | Inspect repository status after local generation. | Generated artifacts remain ignored and do not enter the commit. | `git status` output. |
| CI-008 | Review workflow permissions. | Workflow has read-only repository contents permission. | Workflow excerpt. |
| CI-009 | Cancel a superseded run on the same pull request. | Concurrency policy cancels the older run. | CI run evidence. |

## 16. Performance And Reliability Observations

Record rather than enforce hard limits during the first pilot cycle.

| Measurement | Cold Run | Warm Run | Notes |
| --- | --- | --- | --- |
| Initial `uvx` resolution | | | |
| Cold isolated DESys tool resolution | | | |
| Warm isolated DESys tool reuse | | | |
| Initializer dry-run | | | |
| Initializer apply | | | |
| Local documentation quality gate | | | |
| GitHub Actions documentation job | | | |

Report intermittent failures, network sensitivity, unclear waiting periods,
unexpected rebuilds, and material differences between repeated runs.

## 17. Usability Review

The pilot tester must answer:

1. Which instruction, command, or generated file was unclear?
2. Which step required maintainer assistance?
3. Did dry-run provide enough information to approve the write?
4. Were conflict messages actionable?
5. Did the scaffold fit the existing repository structure?
6. Did `AGENTS.md` improve agent behavior in observable ways?
7. Were ADR, PRD, and RFC conventions understandable?
8. Were metadata errors easy to locate and correct?
9. Was the quality-gate duration acceptable?
10. Which generated file appeared unnecessary?
11. Which missing template or instruction blocked adoption?
12. How long did adoption take from clean checkout to first passing gate?

## 18. Security And Integrity Review

Confirm that:

- no credential is required outside normal repository and package access;
- no token or environment secret appears in generated files or logs;
- workflow permissions remain read-only unless a future feature justifies more;
- paths cannot escape the consumer repository;
- managed symlinks are rejected;
- conflicts prevent unrelated writes;
- existing `AGENTS.md` and `.gitignore` content is preserved;
- dependency sources are immutable and reviewable;
- `tools/desys-source.txt` contains one validated source and no credentials;
- the consumer environment and dependency lockfile remain unchanged;
- generated artifacts do not contain unintended secrets from source documents.

The final point requires reviewing the pilot documents before generation,
because `search-index.json` intentionally contains source document content.

## 19. Defect Classification

| Severity | Definition | Release Effect |
| --- | --- | --- |
| Critical | Data loss, arbitrary overwrite, path escape, credential exposure, or unusable release. | Immediate no-go. |
| High | Core installation, initialization, validation, indexing, or CI workflow fails in a supported environment. | No-go until fixed and retested. |
| Medium | Workaround exists, but normal adoption is confusing, incomplete, or unreliable. | Requires explicit release decision. |
| Low | Cosmetic, editorial, or minor usability issue with no workflow impact. | May be documented and deferred. |

Every defect record must include an ID, severity, environment, reproduction
steps, expected behavior, actual behavior, evidence, owner, and disposition.

## 20. Go/No-Go Criteria

Public release is recommended only when all of the following are true:

- Pilot A and Pilot B complete all applicable mandatory tests;
- installation succeeds from an immutable source in clean environments;
- the consumer runtime, virtual environment, and lockfile remain unchanged;
- dry-run, conflict prevention, and idempotency are demonstrated;
- no consumer content is lost or silently replaced;
- all valid pilot documents pass with zero errors and zero new warnings;
- invalid metadata and relationships reliably block the gate;
- all five artifacts are deterministic and cross-consistent;
- critical AI scenarios respect documentation and source authority;
- three consecutive CI runs pass with the same build ID;
- no critical or high defect remains open;
- medium defects have an explicit release disposition;
- adoption can be completed from documentation without maintainer intervention;
- package version, README release, Git tag, changelog, and installation source
  are aligned;
- supported operating systems and known limitations are published.

Any failed criterion results in no-go or a documented additional pilot cycle.

## 21. Release Preparation Checklist

- [ ] Select the final v0.1 package version.
- [ ] Align `pyproject.toml`, README, changelog, and Git tag.
- [ ] Commit and push all candidate changes.
- [ ] Create an immutable release candidate tag.
- [ ] Replace placeholder source instructions with the official repository URL.
- [ ] Verify installation from the release candidate source.
- [ ] Complete Pilot A report.
- [ ] Complete Pilot B report.
- [ ] Resolve all critical and high defects.
- [ ] Record dispositions for medium defects.
- [ ] Publish supported platforms and known limitations.
- [ ] Approve release notes.
- [ ] Sign the go/no-go decision.

## 22. Pilot Report Template

Copy this section into one report per pilot.

```markdown
# DESys v0.1 Pilot Report

Pilot identifier:
Project profile:
Tester:
Execution dates:
DESys revision:
Overall result: PASS / FAIL / BLOCKED

## Environment

Complete the environment table from the validation plan.

## Test Results

| Test ID | Result | Evidence | Defect ID | Notes |
| --- | --- | --- | --- | --- |
| ENV-001 | | | | |

## Performance

Complete the performance table from the validation plan.

## AI Scenarios

| Scenario | Result | Documents Used | Notes |
| --- | --- | --- | --- |

## Usability Feedback

Answer every question from the usability review.

## Defects

| Defect ID | Severity | Status | Summary |
| --- | --- | --- | --- |

## Recommendation

GO / NO-GO / ADDITIONAL PILOT REQUIRED

Rationale:
Residual risks:
Required follow-up:
```

## 23. Final Release Decision

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Pilot A tester | | | |
| Pilot B tester | | | |
| DESys maintainer | | | |
| Engineering owner | | | |

Final decision: GO / NO-GO / ADDITIONAL PILOT REQUIRED

Decision rationale:

Residual risks accepted:

Required post-release actions:
