# DESys v0.1 Pilot A Environment And Packaging Evidence

Status: Pass
Final collection date: 2026-08-19

## Environment

| Field | Recorded Value |
| --- | --- |
| Pilot | Pilot A - New Project |
| Project | `pilot-a-test` |
| Baseline commit | `18de9e7cd54975ef707d9a6db63c23701dca6ce8` |
| Final commit | `ac51c943ba9e0be1b5221acc4345d231b73e7143` |
| Operating system | Pop!_OS 24.04 LTS |
| Kernel | Linux 7.0.11-76070011-generic |
| Architecture | x86_64, 64-bit |
| Consumer Python | CPython 3.14.2 in `.venv` |
| DESys Python | CPython 3.12.3 in an isolated uv archive environment |
| `uv` | 0.12.3 |
| Git | 2.43.0 |
| CI | GitHub Actions |
| Existing documentation before DESys | None |
| Existing agent instructions before DESys | None |
| Existing workflow before DESys | None |

## Accepted Package

| Field | Value |
| --- | --- |
| DESys candidate | `d959114699b19a0cb1aa9b4523bceeac6e8fcf0f` |
| Package version | `0.1.0a1` |
| `Requires-Python` | `>=3.12,<3.13` |
| Runtime dependency | `PyYAML==6.0.3` |
| Source type | Committed repository-relative wheel |
| Wheel SHA-256 | `1244266ad11bc3eb8b1853aa844201fbb330b83b12662bcd00202bed26b35810` |
| CLI output | `desys-project-init 0.1.0a1` |

`tools/desys-source.txt` contains exactly:

```text
tools/vendor/d959114699b19a0cb1aa9b4523bceeac6e8fcf0f/dundercode_engineering_system-0.1.0a1-py3-none-any.whl
```

The final repository contains only this wheel. Earlier candidate wheels were
removed before squash merge.

## Consumer Integrity

| File Or Manifest | SHA-256 After Final Local Gate |
| --- | --- |
| `pyproject.toml` | `ad421f1a50cd57b8e438efba9bb05b35841605a389aa1f0f0e9c8dd187aa0e10` |
| `uv.lock` | `3f108935f82395f7ed1cb46ec6e4602817e09c6c5395237449c2b70ed032ff30` |
| `.venv/pyvenv.cfg` | `607f49cb93048092b1e1088e768844977252cf487870d8d0e964ce2ccd8d1129` |
| Installed-package manifest | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Pilot A's virtual environment contains its Python interpreter and no installed
package. DESys did not install into it or change project dependency files.
Pilot B separately proved preservation of a populated 64-package environment.

## Local Verification

Final-candidate CLI and interpreter evidence:

```text
desys-project-init 0.1.0a1
DESys Python 3.12.3
Consumer Python 3.14.2
```

The final gate passed repeatedly from the repository root and an unrelated
working directory:

```text
3 documents
0 warnings
5 artifacts
sha256:d00ef1aca0f0406d8e5c1e4238817af208d6aa784eb5fb1bb96834df646d622a
exit 0
```

The five artifact checksums were stable:

| Artifact | SHA-256 |
| --- | --- |
| `aliases.yaml` | `2942fd5bee5b03cd93719fc11438671c4cc184a256073ac2e8b6e25f591e3cfd` |
| `graph.yaml` | `f6e147939957f8da29714c5eadca2f4acadd7f96054c5e41c42338467eca0dec` |
| `index.yaml` | `12819debf4304e61d1cf926d0eb6e76f5ff2cbb0aad2d1cebde8c0a267f01958` |
| `navigation.yaml` | `f24184a32f07115b4cdfbb26c14fb35683017d0b487139f79be7a22fd09acdd0` |
| `search-index.json` | `76f8dda42116fdc11947b7cfd7da431d9dd618a616f7018e8af8e01bcbe24c8f` |

## Cache And Clean Checkout

Local cold and warm measurements passed without output changes. GitHub Actions
run `32036295650` created cache `6713876916`; run `32036377737` reused it.
Clean local and GitHub-hosted checkouts required no untracked dependency.

## Remote Verification

Final pull request:
`https://github.com/joiltonrsilva/pilot-a-test/pull/4`

Final post-merge run:
`https://github.com/joiltonrsilva/pilot-a-test/actions/runs/32272787769`

The final run passed commit `ac51c943ba9e0be1b5221acc4345d231b73e7143`.
Workflow permissions are limited to `contents: read`, checkout credentials are
not persisted, and push handling is independent from consumer branch naming.

## Test Status

| Test | Result |
| --- | --- |
| `ENV-001` | Pass |
| `PKG-001` | Pass |
| `PKG-002` | Pass |
| `PKG-003` | Pass |
| `PKG-004` | Pass |
| `PKG-005` | Pass with complementary populated-environment proof in Pilot B |
| `PKG-006` | Pass |

No environment or packaging blocker remains.
