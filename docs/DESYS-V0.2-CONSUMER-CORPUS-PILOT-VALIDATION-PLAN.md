# DESys v0.2 Consumer Corpus Pilot Validation Plan

Status: PRE-TAG GO; public-tag validation pending

Plan date: 2026-08-26

## 1. Purpose

This plan defines the two consumer pilots required by RFC-0001 before
`v0.2.0-alpha.1` may be published. Repository tests and package smoke tests are
entry conditions; they do not replace consumer evidence.

No tag or release may be created from this plan alone. The pre-tag decision may
authorize creation of the immutable candidate tag, after which anonymous
installation from that tag must pass before the final release decision.

## 2. Candidate Baseline

| Field | Required Value |
| --- | --- |
| Package version | `0.2.0a1` |
| Intended release tag | `v0.2.0-alpha.1` |
| Tooling commit | `e7db715635e8611f08144ef27c7f803daa468a49` |
| Corpus source commit | `1ba18c126dc9adf035f64c0ca6eda75186e73b60` |
| Corpus version | `0.1.0` |
| Inventory schema | `1.2.0` |
| Bundle schema | `1.1.0` |
| Consumer manifest schema | `1.1.0` |
| Approved resources | 41 |
| Indexable reference documents | 24 |
| Bundle checksum | `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a` |
| Linux quality run | [32967325745](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325745) |
| Platform compatibility run | [32967325802](https://github.com/DunderCode-Solutions/dundercode-engineering-system/actions/runs/32967325802) |

## 3. Pilot Profiles

| Pilot | Profile | Primary Proof |
| --- | --- | --- |
| Pilot A | New Git repository with no existing DESys scaffold | First opt-in install from an isolated immutable wheel without a DESys checkout |
| Pilot B | Populated repository with local documents, runtime metadata, lockfile, environment marker, agent instructions, ignore rules, and CI | Safe opt-in adoption while preserving consumer-owned evidence and runtime state |

Both pilots use CPython 3.12 for DESys. The consumer project may declare another
runtime because DESys runs through an isolated environment.

## 4. Mandatory Scenarios

| Test ID | Scenario | Expected Result |
| --- | --- | --- |
| `CORPUS-001` | Run opt-in dry-run before installation | Exact plan is reported and no path is written |
| `CORPUS-002` | Apply the opt-in installation | Exactly 41 approved resources, legal notices, and one manifest are installed |
| `CORPUS-003` | Inspect manifest provenance | Package version/source, release tag, source commit, corpus version, bundle checksum, and entry checksums match the candidate |
| `CORPUS-004` | Rerun the same snapshot | Zero creates, updates, deletes, or conflicts; bytes and mtimes remain unchanged |
| `INDEX-001` | Index local and corpus documents together | Every configured local and reference document appears exactly once |
| `INDEX-002` | Repeat index generation | All five generated artifacts are byte-identical |
| `COMPAT-001` | Omit the opt-in flag on a corpus-free project | v0.1-compatible scaffold remains corpus-free |
| `COMPAT-002` | Omit the flag after corpus installation | Installed corpus remains enabled and unchanged |
| `AUTH-001` | Review generated authority guidance | Consumer code and documents remain authoritative; corpus is reference-only |
| `SAFE-001` | Modify or delete a managed corpus file while another write is planned | Complete plan conflicts and performs no writes |
| `SAFE-002` | Add an unmanaged path inside the reference namespace | Complete plan conflicts and performs no writes |
| `SAFE-003` | Present another bundle checksum or valid-but-wrong release provenance | Manifest is rejected before ownership is trusted and no writes occur |
| `IDENT-001` | Add a local identifier collision | Validation fails and reports both repository-relative source paths |
| `STATE-001` | Compare consumer-owned files before and after adoption | Runtime code, project metadata, lockfile, environment, local documents, and existing CI remain byte-identical |
| `CI-001` | Run generated documentation quality command | Metadata, index generation, and artifact validation pass outside the DESys checkout |
| `TAG-001` | Install anonymously from the immutable public tag | Installation, opt-in initialization, rerun, and quality command pass with credentials disabled |

## 5. Required Evidence

Each pilot report records:

- full candidate commit, wheel filename, wheel SHA-256, and package source;
- operating system, architecture, Python, `uv`, and Git versions;
- dry-run, apply, rerun, quality, and negative-case commands with exit status;
- manifest schemas, release tag, source commit, bundle checksum, and entry counts;
- before/after SHA-256 values for consumer-owned files;
- generated document counts and deterministic artifact checksums;
- CI run URLs, defects, residual risks, tester, date, and recommendation.

Secrets, credential-bearing URLs, local home paths, and environment contents must
not be copied into evidence.

## 6. Go/No-Go Criteria

Pre-tag creation is recommended only when:

- both pilot reports pass every applicable mandatory scenario except `TAG-001`;
- final Linux, macOS, and Windows gates pass on the same candidate commit;
- the final security, licensing, and editorial review is PASS;
- no critical or high defect remains open;
- medium defects have explicit dispositions;
- release notes, supported platforms, schemas, checksum, and authority guidance
  match the tested candidate.

Final release is recommended only when `TAG-001` also passes against the exact
tag under anonymous conditions and the signed decision below is complete.

## 7. RFC-0001 Traceability

| Acceptance Criterion | Evidence | Status |
| --- | --- | --- |
| Exact approved package inventory | Inventory, bundle checks, wheel inspection | Ready |
| License and attribution checksums | Final distribution review and manifest | Ready |
| Install and dry-run without source checkout | Pilot A and Pilot B | PASS |
| Same-version rerun produces zero changes | Pilot A and Pilot B | PASS |
| Other bundle checksum fails closed | Automated tests and Pilot B | PASS |
| Modified or deleted corpus blocks writes | Automated tests and Pilot B | PASS |
| Project-owned files remain byte-identical | Pilot B | PASS |
| Local and corpus sources indexed exactly | Pilot A and Pilot B | PASS |
| Generated artifacts deterministic | Both pilots | PASS |
| Anonymous public-tag installation | `TAG-001` | Blocked until authorized tag exists |
| Linux, macOS, and Windows gates | Final GitHub Actions runs | PASS |
| Both consumer pilots pass | [Pilot A](pilot/PILOT-A-V0.2-CONSUMER-CORPUS-EVIDENCE.md) and [Pilot B](pilot/PILOT-B-V0.2-CONSUMER-CORPUS-EVIDENCE.md) | PASS |
| Limitations and authority model published | Release notes and supported platforms | Ready |

## 8. Decision Record

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Pilot A tester | OpenCode automated execution | PASS | 2026-08-26 |
| Pilot B tester | OpenCode automated execution | PASS | 2026-08-26 |
| DESys maintainer | Joilton | PRE-TAG GO | 2026-08-26 |
| Engineering owner | Pending | FINAL GO / NO-GO | Pending |

Final decision: PRE-TAG GO; `TAG-001` AND FINAL APPROVAL PENDING

Pre-tag approval was granted for the exact immutable candidate after all
automated gates and consumer pilots passed without a blocking defect.

Required post-tag action: Execute `TAG-001` anonymously on the claimed supported
hosts before publishing the release.
