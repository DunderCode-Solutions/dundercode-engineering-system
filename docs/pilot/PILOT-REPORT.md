# DESys v0.1 Pilot A Final Report

Pilot identifier: Pilot A - New Project
Project: `pilot-a-test`
Assessment date: 2026-08-19
Technical status: Pass
Final decision: Pass

## 1. Executive Summary

Pilot A validates DESys adoption in a new repository. The accepted Pilot A
commit is `1c3d2f1c57e6bc4c22e841625d1b6870080d2124`, produced by squash-merging
pull request 5. It contains one immutable DESys wheel from candidate
`75e7d2fb1ec35623df04d1862060589712a440d7`.

Installation, initialization, metadata validation, indexing, deterministic
generation, agent behavior, and remote CI passed. Negative metadata, source,
relationship, conflict, malformed-marker, invalid-root, symlink, and
concurrency scenarios failed safely as expected. No critical or high defect
remains open.

The tester completed the usability review and confirmed participation only as a
tester and consumer, satisfying the independent-tester requirement. The two
review findings were corrected, rebuilt, and verified in both pilots. A fresh
language-sensitive agent session rejected Portuguese prose labeled as
`language: en` and requested clarification without changing files.

## 2. Accepted Candidate

| Field | Value |
| --- | --- |
| DESys commit | `75e7d2fb1ec35623df04d1862060589712a440d7` |
| Package version | `0.1.0a1` |
| Public release label | `v0.1.0-alpha.1` |
| Pilot commit | `1c3d2f1c57e6bc4c22e841625d1b6870080d2124` |
| Source file | `tools/desys-source.txt` |
| Source path | `tools/vendor/75e7d2fb1ec35623df04d1862060589712a440d7/dundercode_engineering_system-0.1.0a1-py3-none-any.whl` |
| Wheel SHA-256 | `671df8c27f2fc6a4e09ee21e878f9dbf933460a5c08e64c57b1405f123c0fee7` |
| Final local build ID | `sha256:d00ef1aca0f0406d8e5c1e4238817af208d6aa784eb5fb1bb96834df646d622a` |
| Final GitHub Actions run | `https://github.com/joiltonrsilva/pilot-a-test/actions/runs/32314722869` |

All superseded wheels were removed. The committed Pilot A repository contains
only the accepted wheel.

## 3. Environment

| Field | Recorded Value |
| --- | --- |
| Pilot identifier | Pilot A - New Project |
| Project type | New Python repository without an application framework |
| Project lifecycle stage | Greenfield pilot |
| Primary language and framework | Python; no application framework |
| Operating system | Pop!_OS 24.04 LTS, Linux 7.0.11-76070011-generic |
| CPU architecture | x86_64, 64-bit |
| Consumer Python | CPython 3.14.2 in a project `.venv` |
| DESys tool Python | CPython 3.12.3 in an isolated uv archive environment |
| `uv` | 0.12.3 |
| Git | 2.43.0 |
| CI platform | GitHub Actions, `ubuntu-latest` |
| AI agent or assistant | OpenCode orchestrator `openai/gpt-5.6-sol`; fresh `general` subagent sessions |
| Existing documentation structure | None at baseline |
| Existing `AGENTS.md` | No |
| Existing `.gitignore` | No |
| Existing GitHub Actions workflows | No |
| DESys source | Candidate `75e7d2fb1ec35623df04d1862060589712a440d7` relative wheel |

The subagent runtime did not expose a model identifier separate from the
orchestrator. This is recorded as a tooling limitation rather than omitted
environment data.

## 4. Test Results

### Environment And Packaging

| Test | Result | Evidence |
| --- | --- | --- |
| `ENV-001` | Pass | All section 5 environment fields are populated above. |
| `PKG-001` | Pass | Committed repository-relative wheel is checksum-fixed and reproducible from a clean clone. |
| `PKG-002` | Pass | Empty-cache local and GitHub-hosted environments resolved the wheel without the DESys development environment. |
| `PKG-003` | Pass | Wheel metadata, CLI, generated guide, package metadata, and release label align to `0.1.0a1` / `v0.1.0-alpha.1`. |
| `PKG-004` | Pass | `tools/desys-source.txt` contains exactly the invoked accepted wheel path. |
| `PKG-005` | Pass | Pilot A did not modify project metadata, lock state, or Python 3.14.2 environment; Pilot B separately proved preservation of a populated environment. |
| `PKG-006` | Pass | Cold and warm local and remote runs passed with identical output and build ID. |

### Initializer

| Test | Result | Evidence |
| --- | --- | --- |
| `INIT-001` | Pass | Final-candidate dry-run exited 0 in 0.13 seconds and wrote no files. |
| `INIT-002` | Pass | Apply exited 0 in 0.07 seconds and created the expected current scaffold. |
| `INIT-003` | Pass | Second normal invocation reported every managed path `UNCHANGED` and zero changes. |
| `INIT-004` | Pass | Pilot B preserved existing `.gitignore` bytes outside one managed block. |
| `INIT-005` | Pass | Pilot B preserved existing `AGENTS.md` bytes outside one managed block. |
| `INIT-006` | Pass | Divergent managed workflow produced exit 1; all unrelated checksums remained unchanged. |
| `INIT-007` | Pass | Missing `AGENTS.md` end marker produced an actionable malformed-marker conflict and exit 1. |
| `INIT-008` | Pass | Non-Git root produced `Repository root must contain a non-symlinked .git entry`, exit 1, and no writes. |
| `INIT-009` | Pass | Managed `AGENTS.md` symlink produced exit 1; target content and repository remained unchanged. |
| `INIT-010` | Pass | Absolute quality-script invocation from `/tmp/opencode` passed in 0.33 seconds. |
| `INIT-011` | Pass | Two equivalent fresh repositories produced recursively identical scaffolds and matching per-file checksums. |
| `INIT-012` | Pass | Independent tester completed the path and usability review; findings are recorded below. |

### Real Documentation

| Test | Result | Evidence |
| --- | --- | --- |
| `DOC-001` | Pass | `docs/adr/ADR-0001-architecture-baseline.md` has canonical metadata and valid naming. |
| `DOC-002` | Pass | `docs/prd/PRD-0001-product-foundation.md` has canonical metadata and valid naming. |
| `DOC-003` | Pass | `docs/rfc/RFC-0001-initial-architecture.md` has canonical metadata and valid naming. |
| `DOC-004` | Pass | Three deliberate directed relationships resolve in `graph.yaml`. |
| `DOC-005` | Pass | Three-document gate exits 0 with zero errors and zero warnings. |
| `DOC-006` | Pass | Unsupported ADR status identifies the source path and blocks indexing with exit 1. |
| `DOC-007` | Pass | Duplicate `ADR-0001` identifies both the filename mismatch and duplicate source path, exit 1. |
| `DOC-008` | Pass | Missing PRD relationship target identifies source path and unresolved target, exit 1. |
| `DOC-009` | Pass | Byte-exact source restoration returns the gate to exit 0 and the original build ID. |
| `DOC-010` | Pass | Repeated generations preserve build ID `d00ef1...` and all five artifact checksums. |
| `DOC-011` | Pass | Search titles, paths, summaries, metadata, and content match all three authoritative sources. |
| `DOC-012` | Pass | `docs/generated/` contains exactly five ignored generated artifacts and no maintained source. |

### AI Agent

| Test | Result | Evidence |
| --- | --- | --- |
| `AI-001` to `AI-009` | Pass | Nine fresh sessions and a final language-sensitive regression are recorded in `AI-VALIDATION-FINAL.md`. |

The final AI round preferred source Markdown over stale generated data,
reported approved-decision conflicts, created valid canonical ADR/PRD changes,
preserved traceability, refused direct generated edits, ran required gates, and
reported undocumented governance without invention.

### Continuous Integration

| Test | Result | Evidence |
| --- | --- | --- |
| `CI-001` | Pass | Valid PR checks passed, including final PR 4 run `32272669898`. |
| `CI-002` | Pass | PR 2 run `32036573425` rejected invalid ADR metadata. |
| `CI-003` | Pass | PR 3 run `32036679891` rejected a mutable source before DESys execution. |
| `CI-004` | Pass | GitHub-hosted clean checkouts used only committed source and wheel inputs. |
| `CI-005` | Pass | Cold cache run `32036295650` created cache `6713876916`; warm run `32036377737` reused it. |
| `CI-006` | Pass | Three consecutive same-revision runs passed with build ID `d00ef1...`. |
| `CI-007` | Pass | Generated output remains ignored and absent from commits. |
| `CI-008` | Pass | Workflow grants only `contents: read`; action credentials are not persisted. |
| `CI-009` | Pass | Same-PR run `32272326171` was cancelled by run `32272413359`, which passed. |

The final usability-fix squash merge triggered successful `master` run
`32314722869` at commit `1c3d2f1c57e6bc4c22e841625d1b6870080d2124`.

## 5. Performance

| Measurement | Cold | Warm | Notes |
| --- | --- | --- | --- |
| Isolated CLI resolution | 1.27 s | 0.12 s | Earlier candidate; behavior unchanged in final alpha. |
| Initializer dry-run | 0.13 s | 0.08 s | Final candidate fixture. |
| Initializer apply | 0.07 s | Not applicable | Final candidate fixture. |
| Local documentation gate | 0.49 s | 0.34 s | Three documents, identical output. |
| External-cwd gate | Not applicable | 0.33 s | Same build ID. |
| GitHub Actions job | 16 s | 12 s | Cold/warm final-revision observations. |

No intermittent failure, network-sensitive package source, unexpected rebuild,
or output difference was observed.

## 6. Security And Integrity

- No credential beyond normal private-repository access was required.
- No token, environment secret, or absolute local path is committed in generated artifacts.
- Workflow repository permission is read-only and checkout credentials are not persisted.
- Repository-root checks and path containment prevent writes outside the consumer repository.
- Managed symlinks are rejected before writes.
- Conflicts are atomic and prevent unrelated writes.
- Existing `AGENTS.md` and `.gitignore` preservation passed in Pilot B.
- The dependency source is immutable, reviewable, checksum-fixed, and credential-free.
- `tools/desys-source.txt` contains one source line.
- Consumer environments and lockfiles remained unchanged.
- Pilot source documents contain no secret; generated search content was reviewed.

## 7. Defects And Limitations

| ID | Severity | Status |
| --- | --- | --- |
| `PILOT-A-005` | High | Fixed and verified in final candidate. |
| `PILOT-B-001` | High | Fixed and verified locally and remotely. |
| `PILOT-A-006` | Low | Fixed and verified in both pilots. |
| `PILOT-A-007` | Medium | Fixed and verified by regression tests and a fresh language-sensitive agent session. |

Known limitations:

- GitHub currently warns that pinned third-party actions using Node.js 20 are
  forced onto Node.js 24. Workflows pass, but action revisions should be
  refreshed during routine maintenance.
- The validation harness exposes the orchestrator model ID but not a separate
  subagent model revision.
- Pilot documents are intentionally minimal examples, not production product
  documentation.

## 8. Usability Review

Tester role: independent tester and consumer; not an implementer of
`desys-project-init`.

| Question | Answer |
| --- | --- |
| Unclear instruction, command, or generated file | The managed `.gitignore` block was unclear. |
| Step requiring maintainer assistance | None. |
| Dry-run sufficient to approve writes | Yes. |
| Conflict messages actionable | Yes. |
| Scaffold fit repository structure | Yes. |
| `AGENTS.md` improved observable behavior | Yes. |
| ADR, PRD, and RFC conventions understandable | Yes, but an earlier agent wrote Portuguese prose while metadata declared English. |
| Metadata errors easy to locate and correct | Yes. |
| Quality-gate duration acceptable | Yes. |
| Unnecessary generated file | None. |
| Missing template or instruction blocked adoption | None. |
| Active adoption time | 10 minutes. |

The `.gitignore` clarity finding is `PILOT-A-006`. The prose-language mismatch
is `PILOT-A-007`.

## 9. Pilot Completion

No Pilot A evidence remains pending. Release-level tagging, public-source
installation, release notes, and final go/no-go approval remain separate release
preparation activities.

## 10. Recommendation

Decision: PASS

All applicable Pilot A tests pass on candidate `75e7d2f...`. Human validation,
independent-tester evidence, usability corrections, language-sensitive agent
behavior, and final remote CI are complete. Pilot A recommends proceeding to
release preparation.
