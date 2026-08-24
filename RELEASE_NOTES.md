# DESys v0.1.0-alpha.2 Release Notes

DESys `v0.1.0-alpha.2` is a corrective release of the first validated foundation
of the DunderCode Engineering System documentation platform.

## Correction

- Restores the complete MIT License text and the copyright notice for
  DunderCode Solutions.
- Adds a release gate that rejects an empty `LICENSE` file.
- Supersedes `v0.1.0-alpha.1`, whose source and package artifacts contained an
  empty license file despite declaring the MIT License.

There are no runtime, metadata-schema, indexer, or consumer-scaffold behavior
changes in this release.

## Validation

- 40 automated tests pass, and the license-presence gate passes.
- 278 documents validate with zero errors.
- Five generated artifacts are cross-consistent and deterministic.
- Pilot A passed new-project, documentation, negative, recovery, AI, cache, and
  CI concurrency scenarios.
- Pilot B preserved a populated Python 3.13 environment and lockfile, passed 55
  application tests, and passed CI on a nonstandard default branch.
- All critical, high, medium, and low pilot defects are fixed and retested.

## Distribution

This corrective alpha is distributed from the public
[DunderCode-Solutions/dundercode-engineering-system](https://github.com/DunderCode-Solutions/dundercode-engineering-system)
repository. It is not published to PyPI. Resolve the release tag to its full
commit SHA and follow the initialization commands in the repository README.

## Compatibility And Limitations

DESys tooling requires CPython 3.12 and is validated on Linux x86_64. Consumer
projects are not required to use Python 3.12. Canonical documentation is English
only in metadata schema v1. See
[`SUPPORTED-PLATFORMS.md`](SUPPORTED-PLATFORMS.md) for the complete support and
limitations statement.

## Upgrade Policy

This remains an alpha release. Managed scaffold files are protected by conflict
preflight rather than silently overwritten. Review release changes, run
`desys-project-init --dry-run`, and resolve any managed-file differences before
applying a future candidate.
