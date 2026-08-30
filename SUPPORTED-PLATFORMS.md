# Supported Platforms And Known Limitations

This document records the published DESys `v0.2.0-alpha.1` platform history.
All v0.3 development-candidate identities, support claims, successful jobs,
contract versions, and procedures are canonical only in
[`docs/DESYS-V0.3-COMPATIBILITY.md`](docs/DESYS-V0.3-COMPATIBILITY.md). Keeping
those claims in one generated publication prevents this summary from drifting.

## Supported Tool Host

The published v0.2 alpha was validated on:

- Linux x86_64;
- Pop!_OS 24.04 LTS and GitHub Actions `ubuntu-latest`;
- GitHub Actions `macos-latest`;
- GitHub Actions `windows-latest` with Git Bash;
- CPython 3.12 for DESys tooling;
- `uv` 0.12.3 and 0.12.5;
- Git 2.43.0;
- GitHub-hosted repositories and GitHub Actions.

DESys consumer tooling runs through `uvx --isolated --no-config --python 3.12`.
The consumer project may use another Python version or another implementation
language. Pilot B preserved a Python 3.13 virtual environment, project metadata,
and lockfile while DESys used isolated Python 3.12.

## Not Yet Validated

The alpha has not been validated on:

- Linux ARM64;
- self-hosted Windows or macOS runners;
- Windows or macOS versions outside the GitHub-hosted `*-latest` images;
- non-GitHub CI platforms;
- Python tool hosts other than CPython 3.12.

These environments are not claimed as supported by this release.

## Validation Evidence

Candidate commit
[`e7db715`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/commit/e7db715635e8611f08144ef27c7f803daa468a49)
passed the Linux
[`Quality` run](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325745)
and the native macOS and Windows
[`Platform Compatibility` run](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325802)
on 2026-08-26. Both compatibility jobs passed the portable quality gates and
installed-package smoke test.

The same immutable candidate passed the
[new-project corpus pilot](docs/pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md)
and the
[populated-project corpus pilot](docs/pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md)
on Linux x86_64. Anonymous installation from public tag `v0.2.0-alpha.1` also
passed with credentials disabled, as recorded in
[`TAG-001`](docs/pilot/TAG-001-V0.2-ANONYMOUS-PUBLIC-TAG-EVIDENCE.md). The tag's
[Linux quality gate](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32970276050)
and
[macOS/Windows gates](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32970276004)
passed on commit `d736b028b285a3c4f4d22b685ddd5a0903c9822d`.

The historical v0.2 support claims are limited to the environments and hosted
runner labels above. They do not imply validation of every operating-system
release or hardware architecture represented by those platform families.

## Known Product Limitations

- Metadata schema v1 supports canonical source prose in English only and
  requires `language: en`.
- The alpha distributes tooling from the public GitHub repository; no PyPI
  package is published for this release.
- Consumer source configuration accepts only an exact package version, a full
  SHA HTTPS Git source, or a repository-relative wheel.
- Skills are documentation assets in v0.2; automatic skill installation or
  activation is outside this release.
- Cross-snapshot corpus reconciliation is not supported in the first v0.2 alpha.
  A manifest from another bundle checksum fails closed.
- Generated `search-index.json` intentionally includes source-document content.
  Source documents must be reviewed for credentials and confidential data.
- The DESys repository carries a governed baseline of 127 legacy warnings. New
  warnings are rejected by the quality gate.
- Generated consumer CI targets GitHub Actions. Other CI platforms require a
  manual adaptation of the local quality command.
- Pinned GitHub Actions currently emit a Node.js runtime migration warning but
  pass under GitHub's forced Node.js 24 execution.

Report release-specific problems through the official
[GitHub issue tracker](https://github.com/DunderCode-Solutions/dundercode-engineering-system/issues).
