# DESys Development Checkpoint

Last updated: 2026-08-29

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

- 281 documents validated;
- 0 metadata errors and 127 governed legacy warnings;
- full native pytest suite passing;
- 5 deterministic index artifacts generated and cross-validated;
- source distribution and derived wheel built and smoke-tested in an isolated
  environment;
- native GitHub Actions gates passed on `ubuntu-latest`, `macos-latest`, and
  `windows-latest`, including installed-package smoke tests on macOS and Windows;
- both v0.2 consumer corpus pilots passed every required pre-tag scenario on
  immutable candidate `e7db715635e8611f08144ef27c7f803daa468a49`;
- anonymous installation from public tag `v0.2.0-alpha.1` and its Linux, macOS,
  and Windows gates passed on tagged commit
  `d736b028b285a3c4f4d22b685ddd5a0903c9822d`;
- development-candidate compatibility publication controls passing locally.

The published prerelease remains PEP 440 package version `0.2.0a1` and public
release label `v0.2.0-alpha.1`. The current development target is `0.3.0a1` /
`v0.3.0-alpha.1`; it has not been published. No PyPI package is published.

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

Roadmap PRs 3 and 4 are complete.
PR5 is in progress pending committed CI and merge. Local checker success cannot
establish the completion of its own publication controls. PR6 remains blocked
until that gate closes. This does not approve any Reference Skill.
Active Skills remain not implemented.

The approved architecture decision is
[`ADR-0002`](../knowledge/adr/ADR-0002-cross-snapshot-migration-and-skill-boundaries.md).
The ordered implementation PRs, compatibility gates, and SaaS adoption protocol
are defined in
[`DESYS-SKILLS-COMPATIBILITY-DELIVERY-ROADMAP.md`](DESYS-SKILLS-COMPATIBILITY-DELIVERY-ROADMAP.md).
The v0.3 development-candidate matrix, evidence links, and operator procedures
are in [`DESYS-V0.3-COMPATIBILITY.md`](DESYS-V0.3-COMPATIBILITY.md).

The current corpus-pilot evidence, scenarios, and staged go/no-go criteria are
defined in
[`DESYS-V0.2-CONSUMER-CORPUS-PILOT-VALIDATION-PLAN.md`](DESYS-V0.2-CONSUMER-CORPUS-PILOT-VALIDATION-PLAN.md).
The executed evidence is recorded in
[`pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md`](pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md)
and
[`pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md`](pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md).
Anonymous public-tag evidence is recorded in
[`pilot/TAG-001-V0.2-ANONYMOUS-PUBLIC-TAG-EVIDENCE.md`](pilot/TAG-001-V0.2-ANONYMOUS-PUBLIC-TAG-EVIDENCE.md).

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

## Next Work

Monitor `v0.2.0-alpha.1` adoption and execute the Skills compatibility roadmap in
small, independently reviewed PRs without weakening the fail-closed ownership
model. Completed release evidence is recorded in
[`SUPPORTED-PLATFORMS.md`](../SUPPORTED-PLATFORMS.md) and
[`RELEASE_NOTES.md`](../RELEASE_NOTES.md).
