# DESys v0.2.0-alpha.1 Candidate Release Notes

DESys `v0.2.0-alpha.1` introduces an opt-in, governed reference corpus while
preserving consumer documentation as the authoritative project evidence. This
candidate is not yet published or tagged.

## Reference Corpus

- `desys-project-init --with-reference-corpus` installs 41 approved resources
  under `docs/desys/`.
- The bundle contains 24 indexable reference documents, navigation assets, the
  metadata schema, the MIT License, and third-party notices.
- A checksum-validated consumer manifest records package, bundle, source,
  target, classification, distribution, and installed-content provenance.
- Existing consumer ADRs, PRDs, RFCs, code, policies, and operational evidence
  retain authority and are never silently overwritten.

## Safety And Upgrade Policy

- Initial installation and same-snapshot reconciliation are supported.
- Manifests from other bundle checksums fail closed before ownership is trusted.
- Modified, deleted, unmanaged, linked, executable, or otherwise unsafe managed
  paths block all planned writes with actionable diagnostics.
- Cross-snapshot reconciliation is deferred until trusted predecessor
  descriptors are available.

## Validation

- 118 automated tests pass on the local Linux release gate.
- The governed inventory contains 349 entries, including 41 approved bundle
  resources.
- 280 repository documents validate with zero errors and the governed baseline
  of 127 warnings.
- The source distribution, derived wheel, exact package-resource coverage,
  isolated installation, opt-in initialization, idempotent rerun, and a
  24-document consumer indexing pilot pass.
- Native macOS and Windows candidate gates are defined but must pass remotely
  before release approval.

## Distribution

The candidate will be distributed from the public
[DunderCode-Solutions/dundercode-engineering-system](https://github.com/DunderCode-Solutions/dundercode-engineering-system)
repository after release approval. It is not published to PyPI. No installation
should claim `v0.2.0-alpha.1` until the immutable tag exists.

## Compatibility And Limitations

DESys tooling requires CPython 3.12. Consumer projects are not required to use
Python 3.12. Canonical documentation is English only in metadata schema v1. See
[`SUPPORTED-PLATFORMS.md`](SUPPORTED-PLATFORMS.md) for the complete support and
limitations statement.

## Upgrade Policy

This remains an alpha release. Review release changes, run
`desys-project-init --dry-run --with-reference-corpus`, and resolve every
conflict before applying the candidate. Do not manually transfer a corpus
manifest between package snapshots.
