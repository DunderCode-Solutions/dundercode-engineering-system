# DESys Development Checkpoint

Last updated: 2026-08-21

## Current State

The canonical metadata contract, repository validator, deterministic indexer,
Python package, documentation quality gate, and consumer project initializer
are operational.

The development environment and CI use Python 3.12 and `uv`. The complete
quality gate is available through:

```bash
bash scripts/quality.sh
```

The latest verified result is:

- 278 canonical documents validated;
- 0 metadata errors and 127 governed legacy warnings;
- 40 native pytest tests passing;
- 5 deterministic index artifacts generated and cross-validated;
- Python wheel built and smoke-tested in an isolated environment;
- build ID `sha256:c0df150d39a2c9f12f74fe5a92267d54364ebe2be5bf8b1b01507e8875f104c6`.

The current release candidate uses PEP 440 package version `0.1.0a1` and public
release label `v0.1.0-alpha.1`.

## Completed Milestone

The `desys-project-init` command initializes DESys adoption in an existing
consumer Git repository.

The implemented scope covers:

- project documentation directories;
- `tools/desys_indexer.yaml`;
- local documentation quality commands;
- GitHub Actions quality workflow;
- generated-artifact ignore rules;
- DESys package source and version guidance for `uv`;
- isolated DESys Python 3.12 tooling independent from the consumer runtime;
- vendor-neutral `AGENTS.md` documentation instructions;
- non-destructive conflict preflight;
- deterministic and idempotent generation;
- dry-run support;
- built-wheel consumer smoke testing.

## Next Milestone

Pilot A and Pilot B are complete. The next milestone is to merge the release
candidate, create the immutable `v0.1.0-alpha.1` tag, verify public installation
from its resolved full SHA, and publish the GitHub release.

The required evidence, scenarios, and go/no-go criteria are defined in
[`DESYS-V0.1-PILOT-VALIDATION-PLAN.md`](DESYS-V0.1-PILOT-VALIDATION-PLAN.md).
The first AI validation findings and mandatory regression scenarios are in
[`pilot/AI-VALIDATION-ROUND-1.md`](pilot/AI-VALIDATION-ROUND-1.md).
Completed Round 2 regression results are in
[`pilot/AI-VALIDATION-ROUND-2.md`](pilot/AI-VALIDATION-ROUND-2.md).
Pilot defects and their candidate impact are tracked in
[`pilot/PILOT-DEFECTS.md`](pilot/PILOT-DEFECTS.md).
Pilot A environment and packaging evidence is in
[`pilot/PILOT-A-ENVIRONMENT-PACKAGING.md`](pilot/PILOT-A-ENVIRONMENT-PACKAGING.md).
Pilot B environment and integration evidence is in
[`pilot/PILOT-B-ENVIRONMENT-INTEGRATION.md`](pilot/PILOT-B-ENVIRONMENT-INTEGRATION.md).
The final Pilot A report is in [`pilot/PILOT-REPORT.md`](pilot/PILOT-REPORT.md),
and the final AI scenario archive is in
[`pilot/AI-VALIDATION-FINAL.md`](pilot/AI-VALIDATION-FINAL.md).

## Resume Point

Resume by completing the release-preparation checklist in
[`DESYS-V0.1-PILOT-VALIDATION-PLAN.md`](DESYS-V0.1-PILOT-VALIDATION-PLAN.md).
