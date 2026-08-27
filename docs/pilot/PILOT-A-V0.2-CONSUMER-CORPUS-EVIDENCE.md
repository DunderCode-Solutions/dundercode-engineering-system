# DESys v0.2 Pilot A Consumer Corpus Evidence

Status: PASS for the pre-tag scenario set

Collection date: 2026-08-26

Tester: OpenCode automated execution

`TAG-001` was not executed and is not claimed.

## Environment

| Field | Recorded Value |
| --- | --- |
| Profile | New Git repository with no existing DESys scaffold |
| Operating system | Pop!_OS 24.04 LTS |
| Kernel | Linux 7.0.11-76070011-generic |
| Architecture | x86_64, 64-bit |
| DESys Python | CPython 3.12.3 in an isolated `uvx` environment |
| `uv` | 0.12.5 |
| Git | 2.43.0 |
| Hosted consumer CI | Not used; generated command executed locally outside both checkouts |

## Candidate

| Field | Value |
| --- | --- |
| Tooling commit | `e7db715635e8611f08144ef27c7f803daa468a49` |
| Package version | `0.2.0a1` |
| Wheel | `dundercode_engineering_system-0.2.0a1-py3-none-any.whl` |
| Wheel SHA-256 | `ac19bf025534fd780b5c461e1cc4c1ab162e1cb95450a92fa14bdbc0613c50da` |
| Package source | Repository-relative wheel under `tools/vendor/e7db715635e8611f08144ef27c7f803daa468a49/` |
| Release tag in manifest | `v0.2.0-alpha.1` |
| Corpus source commit | `1ba18c126dc9adf035f64c0ca6eda75186e73b60` |
| Corpus version | `0.1.0` |
| Inventory schema | `1.2.0` |
| Bundle schema | `1.1.0` |
| Consumer manifest schema | `1.1.0` |
| Bundle checksum | `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a` |
| Consumer manifest SHA-256 | `31b21ba70da3e6ac85b99947e04a83bf9dc965b1603ac984d545e82ddd85d168` |

The detached candidate clone had no Git object alternates. The source
distribution and wheel were built in an isolated temporary directory, and the
consumer contained no DESys source checkout. The wheel contains exactly one
descriptor and all 41 declared resources, with no missing, stale, unexpected,
or duplicate resource paths.

## Installation

The opt-in dry-run exited zero and reported that no files were written. The only
consumer file present before initialization, the vendored wheel, retained both
its checksum and nanosecond mtime.

The apply operation exited zero and installed exactly 41 approved resources:
39 reference targets, `LICENSE`, and `THIRD_PARTY_NOTICES.md`, plus one consumer
ownership manifest. Every source and target was unique. Bundle, original,
installed, and physical file checksums matched for all entries.

The same-snapshot rerun reported every operation as `UNCHANGED` and zero changed
paths. Across 53 initialized files:

| Measurement | Before | After |
| --- | --- | --- |
| Aggregate byte digest | `a260da9424704d9a59331285bb968bf42718c498d2c783e3931252906a5f7ce6` | Same |
| Aggregate mtime digest | `fea11be12105f274148e38fd2fe868ad9b643d0b86c3d0edcf087601767f22bf` | Same |

Omitting `--with-reference-corpus` after installation also reported zero
changes and retained the enabled corpus. A separate corpus-free repository was
initialized without the flag; it contained no corpus manifest, reference
namespace, or reference index source, and its generated quality command passed.

## Indexing

Two valid local documents were added. The generated quality command indexed
exactly 26 unique paths: two local documents and all 24 indexable corpus
documents. Every path appeared once, and both complete runs reported zero
warnings and the same build identifier:

`sha256:65bfd2fffa7fc0ab33a09a6a47f35f56a2c6040d7687b97c0f0346cbfe36b498`

| Artifact | SHA-256 |
| --- | --- |
| `aliases.yaml` | `bbcadbbe31a186b956924375cef5aecc31eaa6aa5e3ce8afe2ddfaf787a3685f` |
| `graph.yaml` | `08d12ca213aec025a6a70e60e15310879f12979a7e5ee916b6c8923ccb230ffe` |
| `index.yaml` | `a9eafdf2336577fdeac33f3160881c65b19ea9035225bfc75c3bcd5e28dced58` |
| `navigation.yaml` | `ca59fdef8ff3835084a39ac31544c0243ec9c44838fcd71ba711f54ff9f4c26c` |
| `search-index.json` | `76f405f605e5fa42fdcfb53e16d3e5a41505971e59bd05b11a9db4837952ca03` |

The quality script was invoked from an unrelated working directory outside the
DESys and consumer checkouts. It resolved the consumer root and exited zero
with 26 documents, zero warnings, and five validated artifacts.

## Authority

Generated instructions state that corpus material is reference-only, does not
override consumer code, policies, ADRs, PRDs, RFCs, or operational evidence,
and that contradictions follow consumer evidence. Generated indexes establish
neither ownership nor authority.

## Scenario Status

| Scenario | Result |
| --- | --- |
| `CORPUS-001` | PASS |
| `CORPUS-002` | PASS |
| `CORPUS-003` | PASS |
| `CORPUS-004` | PASS |
| `INDEX-001` | PASS |
| `INDEX-002` | PASS |
| `COMPAT-001` | PASS |
| `COMPAT-002` | PASS |
| `AUTH-001` | PASS |
| `CI-001` | PASS |
| `TAG-001` | NOT RUN |

No candidate defect was observed. Hosted consumer CI, non-Linux consumer hosts,
negative ownership cases assigned to Pilot B, and anonymous installation from a
public tag remain outside this report.
