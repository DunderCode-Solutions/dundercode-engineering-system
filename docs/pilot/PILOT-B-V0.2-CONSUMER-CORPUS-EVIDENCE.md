# DESys v0.2 Pilot B Consumer Corpus Evidence

Status: PASS for the pre-tag scenario set

Collection date: 2026-08-26

Tester: OpenCode automated execution

`TAG-001` was not executed and is not claimed.

## Environment

| Field | Recorded Value |
| --- | --- |
| Profile | Populated Git repository with local documentation and existing runtime state |
| Operating system | Pop!_OS 24.04 LTS |
| Kernel | Linux 7.0.11-76070011-generic |
| Architecture | x86_64 |
| DESys Python | CPython 3.12.3 in an isolated `uvx` environment |
| Consumer lock Python | CPython 3.13.1 |
| `uv` | 0.12.5 |
| Git | 2.43.0 |
| Hosted consumer CI | Not used; existing workflow was preserved byte-identically |

The consumer baseline contained runtime source, `pyproject.toml`, `uv.lock`, a
Python marker, environment example, three valid local documents, custom agent
instructions, ignore rules, an existing CI workflow, and a vendored wheel.

## Candidate

| Field | Value |
| --- | --- |
| Tooling commit | `e7db715635e8611f08144ef27c7f803daa468a49` |
| Package version | `0.2.0a1` |
| Wheel | `dundercode_engineering_system-0.2.0a1-py3-none-any.whl` |
| Wheel SHA-256 | `4b4f75f3e28e6ed7a1f8f83ac1b2bfe3126126af794d1fb66d332de5b3315917` |
| Package source | Repository-relative immutable wheel under `tools/vendor/` |
| Release tag in manifest | `v0.2.0-alpha.1` |
| Corpus source commit | `1ba18c126dc9adf035f64c0ca6eda75186e73b60` |
| Corpus version | `0.1.0` |
| Inventory schema | `1.2.0` |
| Bundle schema | `1.1.0` |
| Consumer manifest schema | `1.1.0` |
| Bundle checksum | `sha256:d78bb3a685bf285f29d542d1709be9874842f759f00d9739ba073ce94633f62a` |
| Consumer manifest SHA-256 | `7adf7314a9471847bf057e83548a08b682e75a43fe963e7dd146d903803a1d0c` |

Pilot A and Pilot B independently derived wheels from the same immutable source
commit. Their archive hashes differ because the build containers were created
separately. This report is bound to the exact hash above; package-resource
coverage and every checksum-bound corpus byte matched the candidate descriptor.

## Consumer Preservation

The dry-run exited zero with an exact 77-path plan and left the Git worktree and
all baseline hashes unchanged. Apply exited zero. DESys appended only its marked
blocks to `.gitignore` and `AGENTS.md`; their original bytes remain unchanged as
prefixes.

| Consumer-Owned File | SHA-256 Before | After |
| --- | --- | --- |
| `.env.example` | `f0c24ba74ac80c0f3a2f6ddda900cc1b820648db78c3a3d73e1e78968a323b00` | Same |
| `.github/workflows/consumer-ci.yml` | `8a93767c579f45e52ef87ae8124d68caa74a9187bab637c892931b2bbc9de2e6` | Same |
| `.python-version` | `02e735b3dfe1c32833eb550b7ff8ffa17f5f2bc3fa1e7bae61a8f5a3883ce398` | Same |
| `README.md` | `b32dc54e1060c235969512694981819db5999ce251823bcc9c342b4be22fafa0` | Same |
| `docs/adr/ADR-0042-runtime-boundary.md` | `e4883eef1cfc246f7fb6b1943e6355ddb7e98fac652f4c3da7028ad6d73b3482` | Same |
| `docs/prd/PRD-0042-documentation-search.md` | `488879395fc2755355f2549368d551906e1078227d7536f72acc0aa5d5a88739` | Same |
| `docs/rfc/RFC-0042-quality-gate.md` | `0de1f3f0f1f9d5ffce9a032d442bd616eb3e94786c2b2871c86a57d0554c6902` | Same |
| `pyproject.toml` | `299a7b9e6141f1ca8d3703500424319a410ee7d2ec50a4ee86e036076b373dac` | Same |
| `src/pilot_b/__init__.py` | `8ce742f402ddd7791ac7958248cb77f4e117f2852ccf790352280126c3f72824` | Same |
| `src/pilot_b/service.py` | `9290a4d27de138e976e7a5445f1618b71142ffa6798e847177fbf2f71eb36bb6` | Same |
| `uv.lock` | `63e594c7476ab2db8c3370ee2e85c68357c9328bf72e0f90ac64e3816f291e96` | Same |
| Vendored wheel | `4b4f75f3e28e6ed7a1f8f83ac1b2bfe3126126af794d1fb66d332de5b3315917` | Same |

## Corpus And Indexing

Apply installed 41 approved resources: 39 reference targets and two legal
resources. All physical, original, and installed checksums matched. A
same-snapshot rerun reported zero creates, updates, deletes, or conflicts. The
aggregate corpus byte-and-mtime digest remained:

`64c25cea9dd190e1d9a15ce77b311fb744f2036ddf9a9a16fca78a9d981f0be3`

Omitting the opt-in flag after installation retained the enabled corpus with
zero changes. A separate corpus-free baseline initialized without the flag had
no manifest, reference namespace, or reference source.

The quality command indexed exactly 27 unique paths: three local documents and
24 indexable corpus documents. Both runs reported zero warnings and the same
build identifier:

`sha256:d9fb5574ed881209b5fc4e87026bf10d234fa4e645122da792440b7efdcdd652`

| Artifact | SHA-256 |
| --- | --- |
| `aliases.yaml` | `c63e826031ef2c788cb1be7621d6ea39c7a9290c93f99bea7a20688a501b447c` |
| `graph.yaml` | `df55a3d4157bd3b84f2a270e16b5e4b6094e4b53ec5d362ed12fbc5789d5d9e7` |
| `index.yaml` | `4afb509fb73acba5cb2647804edda6fa89021063e2ed82e27e0499bd3be40baa` |
| `navigation.yaml` | `e782c3e83890204c66df0bffd0b98f8d59d6b3b141122e184915c45cae664173` |
| `search-index.json` | `ad07a9d86945e87daf971518479225df0d14254569e233d24763df22f38c205c` |

The quality script was invoked from an unrelated working directory and exited
zero. It resolved the consumer root and used only the isolated wheel source.

## Fail-Closed Cases

For every ownership case, a generated workflow was first removed to establish
an unrelated planned `CREATE`. The initializer exited one, reported the conflict,
left the workflow absent, and preserved the complete byte-and-mtime digest.

| Case | Exact Reason | Preserved Digest |
| --- | --- | --- |
| Modified managed resource | `managed corpus file was modified locally` | `82250e734dc7e3670272145ef1af31135824db6ed20bf9b599eb6b2360941d61` |
| Deleted managed resource | `managed corpus file was deleted locally` | `90d0cfd2d4ace51f14d1a457b4edf8edb47ccb2c17a030f4837f3579a96f65f7` |
| Unmanaged reference path | `unmanaged path inside the DESys reference namespace` | `ee5111bf5d4bd73781bf872915ddc18e03b3dc7a1ea8db3368a8378c1d769a75` |
| Alternate valid bundle checksum | `unsupported prior corpus bundle` | `eee48767040cc2b1bdcd259ff54f162d12170111ec1b64a6a8978de0bf001ab8` |
| Valid but wrong source commit | `corpus manifest release provenance is inconsistent` | `165f0f81f019152a1c92a25c398740179a0d3f5143b623227cae1167c0599501` |

The identifier-collision case exited one and reported both paths:

```text
docs/rfc/RFC-0043-collision.md
docs/desys/reference/knowledge/rfc/RFC-0001-reference-corpus-distribution.md
```

Both claimed canonical identity `rfc.corpus.reference-distribution`.

## Authority

Generated instructions state that corpus documents are reference-only, do not
override consumer code, policies, ADRs, PRDs, RFCs, or operations, and that
contradictions follow consumer evidence. Generated indexes establish neither
ownership nor authority.

## Scenario Status

| Scenario | Result |
| --- | --- |
| `CORPUS-001` through `CORPUS-004` | PASS |
| `INDEX-001` and `INDEX-002` | PASS |
| `COMPAT-001` and `COMPAT-002` | PASS |
| `AUTH-001` | PASS |
| `SAFE-001` through `SAFE-003` | PASS |
| `IDENT-001` | PASS |
| `STATE-001` | PASS |
| `CI-001` | PASS |
| `TAG-001` | NOT RUN |

No candidate defect was observed. Residual risks are Linux-only consumer pilot
execution, no hosted temporary-consumer CI run, independently generated wheel
archive hashes, and pending anonymous public-tag installation.
