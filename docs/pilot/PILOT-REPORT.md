# DESys v0.1 Pilot A Partial Report

Pilot identifier: Pilot A - New Project  
Project profile: New Python project  
Execution status: PARTIAL  
Release decision: BLOCKED  
Assessment date: 2026-08-10

## 1. Assessment Summary

The collected evidence demonstrates that an earlier DESys scaffold could be
initialized in a new repository, installed from a local path, synchronized by
`uv`, and used to generate and validate all five artifacts for an empty corpus.

The evidence does not yet validate the current v0.1 release candidate. The
recorded initializer created 17 paths and did not create `AGENTS.md` or
`tools/desys-source.txt`; the current candidate creates 19 paths and includes
vendor-neutral agent instructions plus isolated tool-source configuration. The
pilot must therefore be repeated from a clean baseline using one immutable
candidate revision.

The original pilot also exposed undesirable runtime coupling: DESys was added
to a CPython 3.14.2 free-threaded consumer environment even though the DESys
package targets Python 3.12. The corrected candidate runs DESys through an
isolated `uvx --python 3.12` environment and must be retested while leaving the
consumer's Python 3.14 environment unchanged.

## 2. Evidence Inventory

| Evidence | Observation | Assessment |
| --- | --- | --- |
| `01-git-flow-init` | Git Flow was initialized, but the log contains an absolute local path. | Context only; sanitize before publication. |
| `02-uv-init` | Project `sovereign-demigod` was initialized. | Partial environment evidence. |
| `03-new-project-with-dry-run` | Dry-run reported 17 `CREATE` operations and no writes. | Provisional pass for an older candidate. |
| `04-new-project-without-dry-run` | Initializer applied 17 changes successfully. | Provisional pass for an older candidate. |
| `05-structure` | Documentation, workflow, script, and indexer paths exist. | Missing current `AGENTS.md` and `tools/desys-source.txt`. |
| `06-uv-add-group-desys` | Local editable source installed DESys 0.1.0 and PyYAML 6.0.3. | Historical evidence for the rejected coupled architecture. |
| `07-uv-sync-locked-group-desys` | Locked group synchronization completed. | Historical evidence; current design does not synchronize consumer dependencies. |
| `08-desys-docs-quality` | Five artifacts validated for zero documents. | Pass for empty-corpus smoke test only. |
| `docs/generated/` | All five generated artifacts are present. | Valid zero-document artifact set. |

## 3. Blocking Findings

### PILOT-A-001 - Candidate Mismatch

Severity: High

The initializer evidence predates the `AGENTS.md` integration. It cannot be
used as release evidence for the current candidate because generated behavior
and scaffold content differ.

Required action: select one full commit SHA, recreate Pilot A from a clean
repository, and record that revision in every result.

### PILOT-A-002 - Consumer Runtime Coupling

Severity: High

The old workflow installed DESys into the consumer's CPython 3.14.2
free-threaded environment even though DESys tooling is validated on Python
3.12. A documentation tool should not constrain or mutate the application
runtime.

Correction implemented: the current scaffold records one immutable source in
`tools/desys-source.txt` and runs DESys with
`uvx --isolated --no-config --python 3.12`.

Required action: retain the consumer's Python 3.14 runtime during the repeated
pilot and prove that its `.venv`, `pyproject.toml`, and `uv.lock` remain
unchanged.

### PILOT-A-003 - Mutable Package Source

Severity: Medium

DESys was installed from a local working directory. That validates local
development but not installation from an immutable public source.

Required action: repeat with a full Git commit SHA or exact published package
version.

### PILOT-A-004 - Incomplete Evidence

Severity: Medium

Logs do not consistently include commands, exit codes, elapsed time, before and
after repository status, environment versions, or sanitized diffs.

Required action: capture every field required by the pilot validation plan.

## 4. Validation Status

| Test ID | Current Result | Evidence Gap Or Note |
| --- | --- | --- |
| ENV-001 | PARTIAL | Python recorded; OS, architecture, `uv`, Git, CI, and agent are missing. |
| PKG-001 | NOT RUN | Local mutable path is not an immutable source. |
| PKG-002 | PARTIAL | New environment used, but isolation from the DESys workspace is not established. |
| PKG-003 | NOT RUN | No `desys-project-init --version` evidence. |
| PKG-004 | NOT RUN | Current `tools/desys-source.txt` behavior was not present. |
| PKG-005 | NOT RUN | Isolated tooling and consumer-environment preservation were not tested. |
| PKG-006 | NOT RUN | Cold and warm isolated tool resolution were not compared. |
| INIT-001 | PASS, PROVISIONAL | Dry-run succeeded for the older 17-path scaffold. |
| INIT-002 | PASS, PROVISIONAL | Apply succeeded for the older 17-path scaffold. |
| INIT-003 | NOT RUN | No second initializer run showing all paths `UNCHANGED`. |
| INIT-004 | NOT APPLICABLE | Pilot A started without an existing `.gitignore`. |
| INIT-005 | NOT RUN | Current `AGENTS.md` behavior was not present. |
| INIT-006 | NOT RUN | Divergent managed-file conflict not tested. |
| INIT-007 | NOT RUN | Malformed marker conflict not tested. |
| INIT-008 | NOT RUN | Invalid Git root not tested. |
| INIT-009 | NOT RUN | Managed symlink not tested. |
| INIT-010 | NOT RUN | Quality script was not invoked from another working directory. |
| INIT-011 | NOT RUN | Equivalent scaffold determinism not compared. |
| INIT-012 | PARTIAL | Structure captured; team review notes are missing. |
| DOC-001 | NOT RUN | No real ADR. |
| DOC-002 | NOT RUN | No real PRD. |
| DOC-003 | NOT RUN | No real RFC. |
| DOC-004 | NOT RUN | No semantic relationship. |
| DOC-005 | NOT RUN | Empty-corpus success does not validate real documents. |
| DOC-006 to DOC-009 | NOT RUN | Negative and recovery scenarios missing. |
| DOC-010 | NOT RUN | Repeated build ID and checksum evidence missing. |
| DOC-011 | NOT RUN | Search content cannot be reviewed with zero documents. |
| DOC-012 | PASS, PROVISIONAL | Generated directory contains only five expected artifacts. |
| AI-001 to AI-009 | NOT RUN | No AI-agent scenarios collected. |
| CI-001 to CI-009 | NOT RUN | No GitHub Actions evidence collected. |

## 5. Positive Evidence

- The old dry-run completed without reported conflicts.
- The old scaffold applied successfully.
- Local DESys and PyYAML installation completed quickly.
- Locked synchronization completed successfully under the superseded coupled design.
- Empty-corpus rendering is supported.
- All five artifact files were generated and cross-validated.
- The zero-document build ID was
  `sha256:32604f9d8cdae5ba4d3bb8264adb95d21dd1c7f95fbeba0e8bce8cc8fa24ad58`.

## 6. Required Next Execution

1. Create a fresh Pilot A repository or restore its clean baseline.
2. Record OS, architecture, Python, `uv`, Git, CI, and agent versions.
3. Keep the consumer's Python 3.14 runtime and record checksums of its environment files.
4. Select and record one immutable DESys commit SHA as `DESYS_SOURCE`.
5. Capture `desys-project-init --version`.
6. Run dry-run and prove no filesystem change with `git status`.
7. Apply the current 19-path scaffold and capture its sanitized diff.
8. Run the initializer again and confirm every path is `UNCHANGED`.
9. Prove that `.venv`, `pyproject.toml`, and `uv.lock` remain unchanged.
10. Create one meaningful ADR, PRD, and RFC with one valid relationship.
11. Execute positive, negative, recovery, and determinism documentation tests.
12. Execute AI-agent scenarios using the generated `AGENTS.md`.
13. Execute the GitHub Actions matrix from a clean checkout.
14. Complete usability, performance, defect, and final recommendation sections.

## 7. Current Recommendation

Decision: ADDITIONAL PILOT EXECUTION REQUIRED

The existing evidence is useful as an early smoke test but is insufficient for
release approval. Do not discard the logs; retain them as historical evidence
and produce a new result set for the immutable current candidate.
