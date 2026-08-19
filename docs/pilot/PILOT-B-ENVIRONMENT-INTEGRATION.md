# DESys v0.1 Pilot B Environment And Integration Evidence

Status: Local validation passed; candidate rebuild and remote CI pending
Collection date: 2026-08-19

## Environment

| Field | Recorded Value |
| --- | --- |
| Pilot identifier | Pilot B - Existing Project |
| Project | `car-wash` |
| Project type | Existing Python workspace with Django backend and Flet frontend |
| Operating system | Pop!_OS 24.04 LTS |
| Kernel | Linux 7.0.11-76070011-generic |
| CPU architecture | x86_64, 64-bit |
| Pilot branch | `develop` |
| Pilot baseline commit | `76370ff50fda111e4137f0a8ad6a6e01a527622e` |
| Consumer Python | CPython 3.13.1 in `.venv` |
| Consumer lock | 69 resolved packages in `uv.lock` |
| Consumer environment | 64 installed packages after baseline `uv sync --locked --all-packages` |
| DESys Python | CPython 3.12.3 in an isolated uv archive environment |
| `uv` | 0.12.3 |
| Git | 2.43.0 |
| Existing `.gitignore` | Yes, seven project-owned lines |
| Existing `AGENTS.md` | Yes, 310 project-owned lines |
| Existing project CI | No |
| DESys candidate commit | `30445a280e1210a158d93bf33e322258dbdf7167` |
| DESys package version | `0.1.0a1` |
| Wheel SHA-256 | `dd4bcf65f3e2994bb846586aa5da026f02d8905a6bfc4ffd76514bb05c9eb971` |

The initially created `.venv` contained only its interpreter. It was populated
from the preexisting locked workspace before DESys execution so preservation
could be measured against a real consumer environment.

## Consumer Baseline

| File Or Manifest | SHA-256 Before DESys | SHA-256 After Local Gates |
| --- | --- | --- |
| `pyproject.toml` | `b3545d83cdf6a026412ba9a07ea00837362d784544e6eb44e2c4ffaf8634c6ab` | Same |
| `uv.lock` | `00c62d0605b68fc6c8a9cb7cb4bd23b9d0709a1286d69940240cba1f25f5bb4f` | Same |
| `.python-version` | `02e735b3dfe1c32833eb550b7ff8ffa17f5f2bc3fa1e7bae61a8f5a3883ce398` | Same |
| `.venv/pyvenv.cfg` | `72b056c6abc6b45e1704c67249b0b4b23fcdfe1f723bccba4ee16b75e5551e16` | Same |
| `.venv/bin/python` | `ec7b1b2dee7cbff2a22f3ea2a1efb1ce7535f26db78aff2aa45d29feab8c9646` | Same |
| Installed-package manifest | `b0bbb28d4d43b55d9578659513c0b231eea90d0644aca3a7656e6b76ff7bc30e` | Same |
| `backend/pyproject.toml` | `feb13f1687ae8b49b64efabba75d547862db43f0eaebb7f21be4de639bd8076a` | Same |
| `frontend/pyproject.toml` | `2d9088ca1c1137618ee6779522fbfc8da51ca77b4dc74c4857703cea1ddc76e1` | Same |

`uv lock --check` passed before and after DESys execution. The consumer stayed
on Python 3.13.1 while the DESys command proved its effective interpreter was
Python 3.12.3 under the uv cache.

## Existing Project Test Baseline

After the consumer environment was populated, the existing backend test suite
reported 2 passing tests and 53 setup errors. Every setup error was caused by
the preexisting PostgreSQL service at `localhost:5432` being unavailable. This
is an application-infrastructure baseline condition, not a DESys regression.

## Initializer Results

The dry-run proposed 18 path changes and wrote no files. All consumer hashes
and Git diff state remained unchanged after the dry-run.

The apply operation:

- appended only the managed generated-artifact block to `.gitignore`;
- appended only the managed documentation-instruction block to `AGENTS.md`;
- preserved all original bytes before both appended blocks;
- created the documentation directories, workflow, quality script, source
  authority file, and indexer configuration;
- did not change runtime code, project metadata, lock state, or `.venv`.

A second initializer execution reported every path as `UNCHANGED` and zero
changed paths.

## Local Gate Results

The gate passed from the repository root and from an unrelated working
directory:

```text
0 documents
0 warnings
5 validated artifacts
sha256:32604f9d8cdae5ba4d3bb8264adb95d21dd1c7f95fbeba0e8bce8cc8fa24ad58
exit 0
```

`docs/generated/` is ignored. Artifact checksums were stable across both runs.

## Test Status

| Test ID | Result | Evidence And Remaining Work |
| --- | --- | --- |
| `PKG-003` | Pass | Wheel, CLI, and generated guide report package `0.1.0a1`. |
| `PKG-004` | Pass | `tools/desys-source.txt` records the checksum-verified relative wheel. |
| `PKG-005` | Pass | Populated Python 3.13 environment, project files, and lockfile remained byte-identical while DESys used isolated Python 3.12. |
| `INIT-001` | Pass | Dry-run completed without writes. |
| `INIT-002` | Pass | Apply created the expected scaffold. |
| `INIT-003` | Pass | Second run reported zero changes. |
| `INIT-004` | Pass | Existing `.gitignore` content was preserved outside one managed block. |
| `INIT-005` | Pass | Existing `AGENTS.md` content was preserved outside one managed block. |
| `INIT-010` | Pass | Quality script passed when invoked from outside the repository. |
| Pilot B remote CI | Pending | Scaffold and wheel must be committed and pushed before GitHub Actions execution. |

## Remaining Work

1. Rebuild the candidate with the branch-independent push trigger discovered by
   Pilot B.
2. Replace the Pilot B wheel and regenerate the managed workflow.
3. Commit and push the Pilot B scaffold and candidate wheel.
4. Capture the remote GitHub Actions result.
5. Record a team review of the generated structure and instructions.
