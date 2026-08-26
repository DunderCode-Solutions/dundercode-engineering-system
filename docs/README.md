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
- 123 native pytest tests passing;
- 5 deterministic index artifacts generated and cross-validated;
- source distribution and derived wheel built and smoke-tested in an isolated
  environment;
- native GitHub Actions gates passed on `ubuntu-latest`, `macos-latest`, and
  `windows-latest`, including installed-package smoke tests on macOS and Windows;
- both v0.2 consumer corpus pilots passed every required pre-tag scenario on
  immutable candidate `e7db715635e8611f08144ef27c7f803daa468a49`;
- approved 41-entry reference bundle checksum
  `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a`.

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

Cross-platform candidate validation is complete on Linux, GitHub-hosted macOS,
and GitHub-hosted Windows. The current milestone is to complete consumer corpus
pilots, approve release evidence, and only then create and verify the immutable
public tag.

The current corpus-pilot evidence, scenarios, and staged go/no-go criteria are
defined in
[`DESYS-V0.2-CONSUMER-CORPUS-PILOT-VALIDATION-PLAN.md`](DESYS-V0.2-CONSUMER-CORPUS-PILOT-VALIDATION-PLAN.md).
The executed evidence is recorded in
[`pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md`](pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md)
and
[`pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md`](pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md).

The v0.1 adoption evidence remains available as historical compatibility proof.
Its validation plan is
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

Resume by recording the remaining `v0.2.0-alpha.1` consumer-pilot and
release-approval evidence. The completed host-validation evidence is recorded in
[`SUPPORTED-PLATFORMS.md`](../SUPPORTED-PLATFORMS.md) and
[`RELEASE_NOTES.md`](../RELEASE_NOTES.md).
