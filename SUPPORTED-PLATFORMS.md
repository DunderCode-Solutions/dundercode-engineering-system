# Supported Platforms And Known Limitations

This document applies to DESys `v0.1.0-alpha.2`.

## Supported Tool Host

The alpha is validated on:

- Linux x86_64;
- Pop!_OS 24.04 LTS and GitHub Actions `ubuntu-latest`;
- CPython 3.12 for DESys tooling;
- `uv` 0.12.3;
- Git 2.43.0;
- GitHub-hosted repositories and GitHub Actions.

DESys consumer tooling runs through `uvx --isolated --no-config --python 3.12`.
The consumer project may use another Python version or another implementation
language. Pilot B preserved a Python 3.13 virtual environment, project metadata,
and lockfile while DESys used isolated Python 3.12.

## Not Yet Validated

The alpha has not been validated on:

- Windows;
- macOS;
- Linux ARM64;
- non-GitHub CI platforms;
- Python tool hosts other than CPython 3.12.

These environments are not claimed as supported by this release.

## Known Product Limitations

- Metadata schema v1 supports canonical source prose in English only and
  requires `language: en`.
- The alpha distributes tooling from the public GitHub repository; no PyPI
  package is published for this release.
- Consumer source configuration accepts only an exact package version, a full
  SHA HTTPS Git source, or a repository-relative wheel.
- Skills are documentation assets in v0.1; automatic skill installation or
  activation is outside this release.
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
