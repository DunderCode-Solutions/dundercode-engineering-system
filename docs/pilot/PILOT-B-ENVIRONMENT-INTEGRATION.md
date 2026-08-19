# DESys v0.1 Pilot B Environment And Integration Evidence

Status: Complete; local, remote, consumer, and team validation passed
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
| Pilot integration commit | `f9273a32f427b877fea11b4cfa069b0e2c4bbf04` |
| Consumer Python | CPython 3.13.1 in `.venv` |
| Consumer lock | 69 resolved packages in `uv.lock` |
| Consumer environment | 64 installed packages after baseline `uv sync --locked --all-packages` |
| Application database | PostgreSQL 16 Alpine under Docker Compose |
| DESys Python | CPython 3.12.3 in an isolated uv archive environment |
| `uv` | 0.12.3 |
| Git | 2.43.0 |
| Existing `.gitignore` | Yes, seven project-owned lines |
| Existing `AGENTS.md` | Yes, 310 project-owned lines |
| Existing project CI | No; DESys workflow added and verified |
| DESys candidate commit | `d959114699b19a0cb1aa9b4523bceeac6e8fcf0f` |
| DESys package version | `0.1.0a1` |
| Wheel SHA-256 | `1244266ad11bc3eb8b1853aa844201fbb330b83b12662bcd00202bed26b35810` |

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
the preexisting PostgreSQL service at `localhost:5432` being unavailable.

The existing `db` Compose service was then started and `pg_isready` confirmed
that it accepted connections. Repeating the same command produced:

```text
55 passed
37 warnings
20.81 seconds
```

The warnings concern the application's short test HMAC key and a deprecated
response-tuple API in `django-ninja-extra`; they are unrelated to DESys. Tests
left the Git worktree, lockfile, Python declaration, virtual environment, and
installed-package manifest unchanged.

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

The replacement candidate removed the hard-coded `main` and `master` push
filter from the generated workflow. A dry-run with that candidate reported all
managed paths `UNCHANGED`, and the local gate passed again without changing any
consumer checksum.

## Remote CI Result

Pushing the committed scaffold to the repository's default `develop` branch
automatically triggered the corrected workflow:

| Field | Result |
| --- | --- |
| Workflow | `DESys Documentation Quality` |
| Event | `push` |
| Branch | `develop` |
| Commit | `f9273a32f427b877fea11b4cfa069b0e2c4bbf04` |
| Run | `32257430389` |
| Conclusion | Success |
| Duration | 20 seconds |
| Cache | Created cache `6785411041` |

Run URL:
`https://github.com/joiltonrsilva/car-wash/actions/runs/32257430389`

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
| Consumer regression | Pass | Existing backend suite passed all 55 tests with the containerized PostgreSQL service active. |
| Pilot B remote CI | Pass | Push to nonstandard default branch `develop` automatically triggered successful run `32257430389`. |
| `INIT-012` | Pass | Project owner inspected the generated structure, managed instruction block, ignore block, and vendored source layout. |

## Team Review

The project owner reviewed the generated `docs/`, `scripts/`, and `tools/`
structure together with the appended `AGENTS.md` and `.gitignore` blocks. The
review confirmed that source documentation remains separate from ignored
generated artifacts, existing instructions remain before the managed block, and
the active wheel is isolated under its immutable candidate commit.

An empty local directory for the superseded candidate `30445a...` was found and
removed. It contained no file, was not tracked by Git, and had no effect on the
committed scaffold or tool-source authority.

No Pilot B work remains.
