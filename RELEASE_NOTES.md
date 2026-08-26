# DESys v0.2.0-alpha.1 Tagged Candidate Release Notes

DESys `v0.2.0-alpha.1` introduces an opt-in, governed reference corpus while
preserving consumer documentation as the authoritative project evidence. The
immutable tag exists; a GitHub Release and PyPI package are not published.

## Reference Corpus

- `desys-project-init --with-reference-corpus` installs 41 approved resources
  under `docs/desys/`.
- The bundle contains 24 indexable reference documents, navigation assets, the
  metadata schema, the MIT License, and third-party notices.
- A checksum-validated consumer manifest records package, bundle, source,
  immutable release tag, corpus source commit, target, classification,
  distribution, and installed-content provenance.
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

- 123 automated tests pass on the local Linux release gate.
- The governed inventory contains 349 entries, including 41 approved bundle
  resources.
- 280 repository documents validate with zero errors and the governed baseline
  of 127 warnings.
- The source distribution, derived wheel, exact package-resource coverage,
  isolated installation, opt-in initialization, idempotent rerun, and a
  24-document installed-wheel consumer smoke test pass.
- Immutable pilot candidate
  [`e7db715`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/commit/e7db715635e8611f08144ef27c7f803daa468a49)
  passes the Linux
  [`Quality` run](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325745)
  and the native macOS and Windows
  [`Platform Compatibility` run](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325802),
  including installed-package smoke tests on both compatibility hosts.
- The two required consumer corpus pilots are governed by the
  [v0.2 pilot validation plan](docs/DESYS-V0.2-CONSUMER-CORPUS-PILOT-VALIDATION-PLAN.md).
  [Pilot A](docs/pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md) and
  [Pilot B](docs/pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md) pass every
  required pre-tag scenario.
- Anonymous installation and initialization from public tag
  [`v0.2.0-alpha.1`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1)
  passes [`TAG-001`](docs/pilot/TAG-001-V0.2-ANONYMOUS-PUBLIC-TAG-EVIDENCE.md),
  including tag-triggered Linux, macOS, and Windows gates.

## Distribution

The immutable candidate tag is available from the public
[DunderCode-Solutions/dundercode-engineering-system](https://github.com/DunderCode-Solutions/dundercode-engineering-system)
repository and resolves to commit `d736b028b285a3c4f4d22b685ddd5a0903c9822d`.
Final GitHub Release approval is pending. It is not published to PyPI.

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
