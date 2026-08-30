<!-- BEGIN GENERATED COMPATIBILITY PUBLICATION -->
# DESys v0.3 Development-Candidate Compatibility

Status: DEVELOPMENT CANDIDATE, NOT A RELEASE

This publication records observed compatibility for the immutable migration implementation commit
[`33fee4aea9cac80fa57a70f1aa572839047add76`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/commit/33fee4aea9cac80fa57a70f1aa572839047add76). It is a development candidate, not a release,
and does not change the packaged compatibility profile.

## Artifact Identity

- Candidate/tooling artifact: [`33fee4aea9cac80fa57a70f1aa572839047add76`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/commit/33fee4aea9cac80fa57a70f1aa572839047add76) (`git-commit`).
- Corpus source commit: `d84693cd117e5b792fe63fcaaa1550acda427c16`. This is separately labeled corpus provenance, not the candidate artifact.
- Target package and release label: `0.3.0a1` / `v0.3.0-alpha.1`.
- Target corpus: version `0.1.0`, bundle `sha256:374a986cbcd2bcf8fb66149daa9f7ea54d80e0c7f5fcc981cea7281a9378aa5b`.
- Package Python support remains `3.12.x`; exact observed patches appear per host.

## Distribution Contracts

| Contract | Version | Packaged checksum |
| --- | --- | --- |
| Inventory schema | `1.2.0` | identity only |
| Reference bundle schema | `1.1.0` | `sha256:6cb3297d1fdd4a91fefe27af8c1233c87955e3737375769ddc1a02f892c1bab2` |
| Consumer manifest schema | `1.1.0` | `sha256:dd1cc5e5a84205f4627c3a71489568eaa1953c578db48e3f1a9f74f57aaae125` |
| Metadata schema | `1.0.0` | identity only |
| Compatibility schema | `1.1.0` | `sha256:90e80040b28469d76d7e10cbcaa69c6d12717a0bb9662c2d92243f2252fc1a48` |
| Predecessor descriptor schema | `1.0.0` | `sha256:df30cc9e2ea593767065c8bd11791244b0ca1d0ff089135d5fe20784670f8cda` |

The evidence checker cross-checks these identities and available contract checksums against
the packaged compatibility profile and predecessor descriptors. Inventory and metadata
schema checksums are not fields in the packaged compatibility profile and are not claimed here.

## Compatibility Matrix

| Migration path | Host environment | Python / uv | Capability | Manually verified recorded job |
| --- | --- | --- | --- | --- |
| [`v0.2.0-alpha.1`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1) `0.2.0a1` `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a`<br>to `v0.3.0-alpha.1` `0.3.0a1` `sha256:374a986cbcd2bcf8fb66149daa9f7ea54d80e0c7f5fcc981cea7281a9378aa5b` | Ubuntu 24.04.4 LTS<br>`ubuntu-24.04` image `20260823.283.1`<br>`x86_64` | CPython `3.12.14` / uv `0.12.3` | **transaction-support**<br>`predecessor-validation`, `deterministic-planning`, `transactional-apply`, `apply-failure-automatic-rollback`, `interrupted-transaction-recovery` | [`Python 3.12` job 99173529309](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030965/job/99173529309) recorded `success`<br>[run 33280030965](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030965) recorded `push` / `success`<br>recorded head `33fee4aea9cac80fa57a70f1aa572839047add76` |
| [`v0.2.0-alpha.1`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1) `0.2.0a1` `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a`<br>to `v0.3.0-alpha.1` `0.3.0a1` `sha256:374a986cbcd2bcf8fb66149daa9f7ea54d80e0c7f5fcc981cea7281a9378aa5b` | macOS 26.5.2 build 25F84<br>`macos-26-arm64` image `20260728.0273.1`<br>`arm64` | CPython `3.12.10` / uv `0.12.3` | **transaction-support**<br>`predecessor-validation`, `deterministic-planning`, `transactional-apply`, `apply-failure-automatic-rollback`, `interrupted-transaction-recovery` | [`Python 3.12 / macos-latest` job 99173529445](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030951/job/99173529445) recorded `success`<br>[run 33280030951](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030951) recorded `push` / `success`<br>recorded head `33fee4aea9cac80fa57a70f1aa572839047add76` |
| [`v0.2.0-alpha.1`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1) `0.2.0a1` `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a`<br>to `v0.3.0-alpha.1` `0.3.0a1` `sha256:374a986cbcd2bcf8fb66149daa9f7ea54d80e0c7f5fcc981cea7281a9378aa5b` | Windows Server 2025 10.0.26100<br>`windows-2025-vs2026` image `20260824.214.3`<br>`x86_64` | CPython `3.12.10` / uv `0.12.3` | **refusal-only**<br>`transaction-refusal`, `pending-state-guard` | [`Python 3.12 / windows-latest` job 99173529165](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030951/job/99173529165) recorded `success`<br>[run 33280030951](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/33280030951) recorded `push` / `success`<br>recorded head `33fee4aea9cac80fa57a70f1aa572839047add76` |

## Predecessor Provenance

- Published package tag: [`v0.2.0-alpha.1`](https://github.com/DunderCode-Solutions/dundercode-engineering-system/tree/v0.2.0-alpha.1).
- Peeled package release commit: `d736b028b285a3c4f4d22b685ddd5a0903c9822d`.
- Predecessor corpus source commit: `1ba18c126dc9adf035f64c0ca6eda75186e73b60`.
- Predecessor bundle: `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a`.

## Evidence Boundary

The GitHub run and job metadata recorded above was manually verified on `2026-08-29`
using method `manual-github-review` and is retained as evidence about migration implementation commit
`33fee4aea9cac80fa57a70f1aa572839047add76`. The recorded conclusions are not cryptographically authenticated by this checker.

The offline checker does not query GitHub or authenticate remote metadata; it validates only the structure and internal bindings of the manually verified values recorded here.
The linked implementation runs do not contain this PR's release-evidence schema, canonical publication renderer,
or stale-document tests. This uncommitted working tree can only exercise those controls locally. PR5 completion
may be recorded only after this diff is committed, passes CI, and merges. Final immutable tag and wheel evidence
also remain pending release gates and require an evidence-record update before release.

Every packaged direct predecessor has path evidence on both supported transaction hosts and separate
Windows refusal evidence. Windows is not a transaction-support host: apply and recovery refuse before
mutation, while pending-state guards continue to block DESys operations.

## Skill Scope

- Reference Skills: none.
- Active Skills: not implemented.

This candidate publishes corpus migration compatibility only. It does not approve, install, activate,
or execute Skills.

## Upgrade Procedure

1. Start from one exact predecessor listed in the matrix and retain its manifest unchanged.
2. Create and verify a repository backup that restores the complete worktree, Git metadata, managed corpus bytes, and manifest.
3. Use one of the exact supported host commands below. Each command verifies uv before invoking the candidate.
4. Review every `ADD`, `UPDATE`, `REMOVE`, `UNCHANGED`, or `CONFLICT`; do not apply a conflicting plan.
5. Remove `--dry-run` only after review, then run consumer quality checks and verify the target manifest.

### Upgrade dry run: Ubuntu 24.04.4 LTS

```bash
set -euo pipefail
REPOSITORY_ROOT="/absolute/path/to/consumer-repository"
UV_VERSION="0.12.3"
DESYS_PYTHON="3.12.14"
DESYS_SOURCE="dundercode-engineering-system @ git+https://github.com/DunderCode-Solutions/dundercode-engineering-system.git@33fee4aea9cac80fa57a70f1aa572839047add76"
uvx --version | grep -Eq "^uvx ${UV_VERSION}( |$)"
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \
  --with-reference-corpus --dry-run

# Run only after reviewing the conflict-free dry run and verified backup.
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \
  --with-reference-corpus
```

### Upgrade dry run: macOS 26.5.2 build 25F84

```bash
set -euo pipefail
REPOSITORY_ROOT="/absolute/path/to/consumer-repository"
UV_VERSION="0.12.3"
DESYS_PYTHON="3.12.10"
DESYS_SOURCE="dundercode-engineering-system @ git+https://github.com/DunderCode-Solutions/dundercode-engineering-system.git@33fee4aea9cac80fa57a70f1aa572839047add76"
uvx --version | grep -Eq "^uvx ${UV_VERSION}( |$)"
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \
  --with-reference-corpus --dry-run

# Run only after reviewing the conflict-free dry run and verified backup.
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --desys-source "$DESYS_SOURCE" \
  --with-reference-corpus
```

## Refusal Procedure

1. Preserve unknown, skipped, altered, or forged predecessor state and its diagnostic; never edit a manifest to bypass validation.
2. On Windows, cross-snapshot apply must refuse before mutation. This is the supported Windows result, not transaction support.
3. If pending state exists on Windows, stop DESys operations and move the unchanged worktree and state to a supported host for recovery.

## Recovery Procedure

1. Stop repository writers and preserve all transaction directories, intermediates, managed files, and the verified backup.
2. On a supported host, use the matching exact command below. Recovery uses the same SHA-pinned candidate as apply.
3. Verify exact predecessor bytes after `restored`, or exact target bytes after authenticated committed cleanup.
4. Preserve the repository for investigation if authentication or recovery fails; never manually delete pending state.

### Recovery: Ubuntu 24.04.4 LTS

```bash
set -euo pipefail
REPOSITORY_ROOT="/absolute/path/to/consumer-repository"
UV_VERSION="0.12.3"
DESYS_PYTHON="3.12.14"
DESYS_SOURCE="dundercode-engineering-system @ git+https://github.com/DunderCode-Solutions/dundercode-engineering-system.git@33fee4aea9cac80fa57a70f1aa572839047add76"
uvx --version | grep -Eq "^uvx ${UV_VERSION}( |$)"
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --recover
```

### Recovery: macOS 26.5.2 build 25F84

```bash
set -euo pipefail
REPOSITORY_ROOT="/absolute/path/to/consumer-repository"
UV_VERSION="0.12.3"
DESYS_PYTHON="3.12.10"
DESYS_SOURCE="dundercode-engineering-system @ git+https://github.com/DunderCode-Solutions/dundercode-engineering-system.git@33fee4aea9cac80fa57a70f1aa572839047add76"
uvx --version | grep -Eq "^uvx ${UV_VERSION}( |$)"
uvx --isolated --no-config --python "$DESYS_PYTHON" --from "$DESYS_SOURCE" \
  desys-project-init --root "$REPOSITORY_ROOT" --recover
```

## Rollback And Reversal

Automatic rollback occurs only when transactional apply fails before a successful commit; it restores and
verifies the exact predecessor. There is no `--rollback` operation. After successful apply, reversal requires
restoring the complete independently verified pre-upgrade repository backup and then verifying predecessor
manifest and managed checksums. Running the old package over the new manifest is unsupported.

## Release Gate

- Final immutable tag evidence: pending.
- Final wheel evidence: pending.
- Required update: Replace development-candidate evidence with evidence for the final immutable tag and wheel before release.
<!-- END GENERATED COMPATIBILITY PUBLICATION -->
