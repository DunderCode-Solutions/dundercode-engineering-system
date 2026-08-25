# DESys Development Checkpoint

Last updated: 2026-08-25

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

- 280 documents validated;
- 0 metadata errors and 127 governed legacy warnings;
- 118 native pytest tests passing;
- 5 deterministic index artifacts generated and cross-validated;
- source distribution and derived wheel built and smoke-tested in an isolated
  environment;
- approved 41-entry reference bundle checksum
  `sha256:cdaa64e389b897fdc673da24d552468f2edd0ddf569f8b3b9dc0f00c092997df`.

The current candidate uses PEP 440 package version `0.2.0a1` and intended public
release label `v0.2.0-alpha.1`. It is not yet tagged or published.

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
- opt-in governed reference-corpus installation;
- manifest-backed ownership and same-snapshot reconciliation;
- consumer-authority preservation and fail-closed conflict handling.

## Next Milestone

The current milestone is to validate the `v0.2.0-alpha.1` candidate on Linux,
macOS, and Windows, complete consumer corpus pilots, approve release evidence,
and only then create and verify the immutable public tag.

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

Resume by running the new platform compatibility workflow and recording the
`v0.2.0-alpha.1` consumer-pilot and release-approval evidence.
