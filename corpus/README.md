# DESys Reference Corpus Inventory

`inventory.yaml` is the governed source-to-target inventory for the reference
corpus proposed by RFC-0001 and ADR-0001.

The inventory covers every Markdown file in the configured `foundation/`,
`knowledge/`, `engineering/`, `delivery/`, and `skills/` source roots, plus each
asset explicitly allowlisted in `assets.yaml`. Explicit assets include
non-Markdown contracts and required legal notices outside those roots. Coverage
does not imply approval for public distribution.

## Distribution States

| State | Meaning |
| --- | --- |
| `pending` | Editorial, security, licensing, or metadata review is incomplete. |
| `approved` | The exact checksummed content is approved for the public bundle. |
| `excluded` | The content must not enter the bundle; `exclusion_reason` is required. |

Approvals are content-bound. When a file checksum changes, the inventory builder
returns its distribution state to `pending`. Empty managed placeholders remain
`excluded` with `empty-placeholder` until substantive content is added. Empty
navigation or supplemental files remain `excluded` with `empty-file`.

## Phase Review Records

DSK remediation uses records governed by
`corpus/reviews/dsk-batch-review-1.0.0.schema.json`. Source review and final
package review are separate gates. Source review binds every selected document
to its exact checksum and review fingerprint and requires identifiable human
decisions for security, privacy, licensing, editorial, links, and identities.
Source approval alone cannot authorize distribution.

Package review binds a deterministic prospective bundle to its bundle checksum,
rendered descriptor checksum, validated closure and entry count, selected target
checksums, and packaged-copy checksums. An authorized human must separately
approve `packaged_bytes` with timestamped evidence. Only a record with both
stages `APPROVED` can authorize a later distribution-only inventory change. Any
changed source checksum or review fingerprint returns the generated inventory
entry to `pending`; a stale record cannot authorize it.

Inventory validation applies this fail-closed rule to `skills/dsk/**` approvals.
Existing approvals outside that path retain their established review governance.
The repository checker additionally validates every DSK record against the JSON
Schema and reconstructs generated candidate bindings:

```bash
uv run python tools/check_corpus_reviews.py
```

To render the selected pending DSK entries with the currently approved corpus,
choose an explicit temporary output outside the repository:

```bash
review_output="$(mktemp -d)"
uv run desys-corpus-review-candidate \
  --review-record corpus/reviews/pr6-phase-1-domain-reference-review-2026-08-30.yaml \
  --output "$review_output"
uv run desys-corpus-review-candidate \
  --review-record corpus/reviews/pr6-phase-1-domain-reference-review-2026-08-30.yaml \
  --output "$review_output" \
  --check
```

The command refuses repository-local output. It writes a candidate under
`$review_output/package/` and a deterministic binding report at
`$review_output/review-candidate.yaml`; it never writes official
`tools/reference_corpus_data/` resources or changes inventory distribution. Copy
the report's `candidate` mapping into the review record only after generation,
leave package status pending while humans inspect the descriptor, closure, and
bytes, then record the authorized packaged-byte decision. Do not track temporary
candidate output.

`CODEOWNERS` requests review for DSK sources, inventory, and review records. It
does not prove that GitHub branch protection or required-review rules are
configured. Repository administrators must enforce protected branches and the
identified reviewer requirement as an organizational release gate; this
repository does not claim that GitHub currently guarantees it.

## Release Provenance

The inventory records the intended immutable `release_tag` and the full
`source_commit` that introduced the approved corpus bytes. Both fields are
generated and validated as part of the inventory contract, copied into the
checksum-bound package descriptor, and installed in the consumer ownership
manifest. The tooling revision that builds a release is recorded separately in
release evidence.

## Classifications

| Classification | Indexable | Meaning |
| --- | --- | --- |
| `document` | Yes | Non-empty, identifier-bearing document with canonical metadata. |
| `navigation` | No | Collection README used for human navigation. |
| `placeholder` | No | Empty identifier-bearing file reserved for future work. |
| `legal` | No | License or attribution notice required beside an installed corpus. |
| `schema` | No | Machine-readable contract required by distributed documents. |
| `supplemental` | No | Other Markdown content outside the managed identifier contract. |

## Distribution Contracts

Versioned structural contracts for the generated bundle, installed consumer
manifest, and compatibility matrix are packaged under
`tools/reference_corpus_data/contracts/`. The machine-readable
`tools/reference_corpus_data/compatibility.yaml` profile binds the installed
package version to release provenance, corpus and schema versions, bundle
checksum, contract checksums, Python support, host platforms, and explicitly
supported direct predecessors. Every direct predecessor declaration binds both
the historical bundle checksum and the complete packaged descriptor checksum.
The descriptor records the exact historical entries and provenance, accepted
manifest schemas, and the single target bundle it authorizes.

JSON Schema validation establishes the portable document shape. Runtime
validation remains authoritative for semantic invariants that JSON Schema does
not express, including descriptor checksums, package-resource coverage,
cross-field provenance, portable path uniqueness, legal-resource coverage, and
installed package metadata alignment. A predecessor manifest is trusted only
after its complete provenance and ordered ownership entries match the immutable
descriptor. Planning remains blocked until the cross-snapshot planner is
implemented. Tests require supported fixtures to pass both layers and
unsupported major versions to fail before ownership is trusted.

## Commands

Update the inventory after source changes:

```bash
uv run desys-corpus-inventory
```

Verify that the tracked inventory is complete and current:

```bash
uv run desys-corpus-inventory --check
```

Inventory disposition changes only `distribution` and, for excluded entries,
`exclusion_reason`. DSK approval also requires the separately governed review
record described above. Release provenance, the review owner, source paths,
targets, metadata fields, checksums, and review fingerprints are generated and
validated. A fingerprint binds an approval to the content and its target,
collection, classification, indexability, and configured owner.

Non-Markdown files MUST be declared in `assets.yaml`. Paths must identify regular
files inside the repository; symlinks, traversal, duplicate entries, and implicit
directory inclusion are rejected.
