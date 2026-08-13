# DESys v0.1 Pilot A Environment And Packaging Evidence

Status: Partial, release blockers identified
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
| CI platform | GitHub Actions workflow generated; remote execution not yet tested |
| AI agent | Claude Opus; exact model revision not archived |
| Existing documentation before DESys | None |
| Existing `AGENTS.md` before DESys | No |
| Existing `.gitignore` before DESys | No |
| DESys candidate commit | `411cc16c1ac77cca26d95fd49272146a295c4b68` |
| DESys source | Repository-relative wheel |
| Wheel SHA-256 | `724138ecd901b9f7f731c5ed6d4c76a5804d176440e40ddd7cb10fc8fa6d93a2` |

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
| `ENV-001` | Partial | Core environment recorded. Exact Claude model revision and successful remote CI platform evidence remain missing. |
| `PKG-001` | Partial | Wheel checksum is fixed, but the wheel and scaffold are untracked in Pilot A. A clean clone cannot reproduce the relative source until they are committed. |
| `PKG-002` | Pass | Dedicated empty cache resolved and executed the wheel independently from the DESys development environment. |
| `PKG-003` | Fail on tested candidate | CLI and wheel reported `0.1.0`, while release documentation reported `v0.1.0-alpha`. The next candidate is aligned to package `0.1.0a1` and release `v0.1.0-alpha.1`; clean-candidate verification remains required. |
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

`docs/generated/` is correctly ignored. The candidate wheel is not ignored,
but it is not yet tracked.

## Release Blockers

1. Verify package `0.1.0a1` and public label `v0.1.0-alpha.1` from the next
   clean candidate.
2. Commit the Pilot A scaffold and candidate wheel, then verify from a clean
   clone.
3. Record the exact AI model revision if available.
4. Run the generated GitHub Actions workflow.
5. Complete runtime and lockfile preservation evidence in Pilot B.
