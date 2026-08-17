# DESys v0.1 Pilot A Environment And Packaging Evidence

Status: Partial, version identity approved
Collection date: 2026-08-12

## Environment

| Field | Recorded Value |
| --- | --- |
| Pilot identifier | Pilot A - New Project |
| Project | `sovereign-demigod` |
| Project type | Python project without an application framework |
| Project lifecycle stage | New project |
| Operating system | Pop!_OS 24.04 LTS |
| Kernel | Linux 7.0.11-76070011-generic |
| CPU architecture | x86_64, 64-bit |
| Consumer Python declaration | `requires-python = ">=3.12"` |
| Consumer Python environment | No `.venv`, `.python-version`, or `uv.lock` present |
| Additional installed Python | CPython 3.14.2 free-threaded |
| DESys tool Python | CPython 3.12.3 in an isolated uv archive environment |
| `uv` | 0.12.3 |
| Git | 2.43.0 |
| Pilot branch | `develop` |
| Pilot baseline commit | `18de9e7cd54975ef707d9a6db63c23701dca6ce8` |
| Committed pilot candidate | `3388a1d3ec20e5a381016ba373b500a036f0611b` |
| CI platform | GitHub Actions; remote pull-request run passed |
| AI agent | Claude Opus; exact model revision not archived |
| Existing documentation before DESys | None |
| Existing `AGENTS.md` before DESys | No |
| Existing `.gitignore` before DESys | No |
| DESys candidate commit | `411cc16c1ac77cca26d95fd49272146a295c4b68` |
| DESys source | Repository-relative wheel |
| Wheel SHA-256 | `724138ecd901b9f7f731c5ed6d4c76a5804d176440e40ddd7cb10fc8fa6d93a2` |

Version identity was subsequently retested with candidate
`74ee350c3513a4eb992339d1b646ba9dfdf5bca1` and wheel SHA-256
`dd4bcf65f3e2994bb846586aa5da026f02d8905a6bfc4ffd76514bb05c9eb971`.

## Package Inspection

The candidate wheel reports:

```text
Name: dundercode-engineering-system
Version: 0.1.0
Requires-Python: <3.13,>=3.12
Requires-Dist: PyYAML==6.0.3
```

The wheel contains all five expected console entry points:

- `desys-build-index`;
- `desys-check-indexes`;
- `desys-metadata-migrate`;
- `desys-metadata-validate`;
- `desys-project-init`.

The wheel contains 19 files and no undeclared runtime dependency was observed.

## Integrity Snapshots

The following values were identical before and after cold and warm isolated
execution:

| File | SHA-256 |
| --- | --- |
| `pyproject.toml` | `63f9443d080c08631dc68e96dd631344af9aec29c21f7e13323ea0a75735f744` |
| `tools/desys-source.txt` | `3059ec907363e8a697a882cd1243f55f7570ae678feed7173d44076f7b15338d` |
| Candidate wheel | `724138ecd901b9f7f731c5ed6d4c76a5804d176440e40ddd7cb10fc8fa6d93a2` |

DESys created no `.venv`, `.python-version`, or `uv.lock` in the consumer
repository.

## Cold And Warm Measurements

Measurements used dedicated empty uv cache directories under `/tmp`.

| Operation | Cold | Warm | Result |
| --- | --- | --- | --- |
| `desys-project-init --version` | 1.27 s | 0.12 s | `desys-project-init 0.1.0`, exit 0 |
| Complete documentation quality gate | 1.29 s | 0.40 s | 3 documents, 0 warnings, 5 artifacts, exit 0 |

Both gate executions produced:

```text
sha256:d00ef1aca0f0406d8e5c1e4238817af208d6aa784eb5fb1bb96834df646d622a
```

The effective DESys interpreter was CPython 3.12.3 under the uv cache, not a
consumer virtual environment.

## Test Status

| Test ID | Result | Evidence And Remaining Work |
| --- | --- | --- |
| `ENV-001` | Partial | Core environment and successful remote CI platform execution recorded. Exact Claude model revision remains missing. |
| `PKG-001` | Pass | Scaffold and wheel are committed in Pilot A. A local clean clone with an empty uv cache reproduced the gate from commit `3388a1d3ec20e5a381016ba373b500a036f0611b`. |
| `PKG-002` | Pass | Dedicated empty cache resolved and executed the wheel independently from the DESys development environment. |
| `PKG-003` | Pass | Candidate wheel, CLI, and generated integration guide report package `0.1.0a1`; public README reports `v0.1.0-alpha.1`. |
| `PKG-004` | Pass | `tools/desys-source.txt` contains exactly the validated repository-relative wheel source. |
| `PKG-005` | Partial | `pyproject.toml` remained unchanged and no environment or lockfile was created. Pilot A has no preexisting `.venv` or `uv.lock`; preservation of populated consumer files remains for Pilot B. |
| `PKG-006` | Pass | Cold and warm runs succeeded; warm cache materially reduced execution time without changing output. |

## Generated Artifact Checksums

| Artifact | SHA-256 |
| --- | --- |
| `aliases.yaml` | `2942fd5bee5b03cd93719fc11438671c4cc184a256073ac2e8b6e25f591e3cfd` |
| `graph.yaml` | `f6e147939957f8da29714c5eadca2f4acadd7f96054c5e41c42338467eca0dec` |
| `index.yaml` | `12819debf4304e61d1cf926d0eb6e76f5ff2cbb0aad2d1cebde8c0a267f01958` |
| `navigation.yaml` | `f24184a32f07115b4cdfbb26c14fb35683017d0b487139f79be7a22fd09acdd0` |
| `search-index.json` | `76f8dda42116fdc11947b7cfd7da431d9dd618a616f7018e8af8e01bcbe24c8f` |

`docs/generated/` is correctly ignored. The candidate wheel and source file are
tracked in the pilot commit.

## Clean Clone Verification

A `git clone --no-local` clone of Pilot A was created outside the source
workspace. Before execution it contained no `docs/generated/`, `.venv`,
`uv.lock`, or `.python-version`.

With a dedicated empty uv cache, the complete gate finished in 1.66 seconds and
reported:

```text
3 documents
0 warnings
5 validated artifacts
sha256:d00ef1aca0f0406d8e5c1e4238817af208d6aa784eb5fb1bb96834df646d622a
exit 0
```

The worktree remained clean because generated output is ignored. Wheel,
consumer project, source-file, and artifact checksums matched the original
pilot execution.

## Remote CI Verification

GitHub Actions ran the `DESys Documentation Quality` workflow for Pilot A pull
request 1 at commit `3388a1d3ec20e5a381016ba373b500a036f0611b`.

| Field | Result |
| --- | --- |
| Pull request | Success; `develop`; commit `3388a1d3ec20e5a381016ba373b500a036f0611b`; 12 seconds; run `32033553632` |
| Push after merge | Success; `master`; commit `f2d160c2e5b60297dce04b253ad6be0875cb6ff9`; 14 seconds; run `32035734317` |
| Manual dispatch | Success; `master`; commit `f2d160c2e5b60297dce04b253ad6be0875cb6ff9`; 12 seconds; run `32035779701` |
| Repeated dispatch | Success; `master`; commit `f2d160c2e5b60297dce04b253ad6be0875cb6ff9`; 11 seconds; run `32036033693` |

This proves the valid-document path, clean remote checkout, push trigger,
manual trigger, and three consecutive successful runs of the final merge
revision.

The remaining CI scenarios were executed independently:

| Test | Evidence | Result |
| --- | --- | --- |
| `CI-002` | PR 2 changed ADR status to an unsupported value; run `32036573425` failed the `Documentation` job as expected. | Pass |
| `CI-003` | PR 3 changed the source to mutable range `dundercode-engineering-system>=0.1.0a1`; run `32036679891` failed before DESys execution as expected. | Pass |
| `CI-005` | All caches were removed before cold run `32036295650`. It passed in 16 seconds and created cache `6713876916`; warm run `32036377737` passed in 12 seconds and updated the same cache's last-access time. | Pass |
| `CI-009` | Concurrent dispatch `32036766700` was cancelled in favor of `32036767097`, which completed successfully. | Pass |

Both negative PRs were closed without merge. `master` remained on merge commit
`f2d160c2e5b60297dce04b253ad6be0875cb6ff9` throughout the cache and
concurrency tests.

## Release Blockers

1. Record the exact AI model revision if available.
2. Complete runtime and lockfile preservation evidence in Pilot B.
