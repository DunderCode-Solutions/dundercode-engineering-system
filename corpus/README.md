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

## Classifications

| Classification | Indexable | Meaning |
| --- | --- | --- |
| `document` | Yes | Non-empty, identifier-bearing document with canonical metadata. |
| `navigation` | No | Collection README used for human navigation. |
| `placeholder` | No | Empty identifier-bearing file reserved for future work. |
| `legal` | No | License or attribution notice required beside an installed corpus. |
| `schema` | No | Machine-readable contract required by distributed documents. |
| `supplemental` | No | Other Markdown content outside the managed identifier contract. |

## Commands

Update the inventory after source changes:

```bash
uv run desys-corpus-inventory
```

Verify that the tracked inventory is complete and current:

```bash
uv run desys-corpus-inventory --check
```

Manual review changes only `distribution` and, for excluded entries,
`exclusion_reason`. The review owner, source paths, targets, metadata fields,
checksums, and review fingerprints are generated and validated. A fingerprint
binds an approval to the content and its target, collection, classification,
indexability, and configured owner.

Non-Markdown files MUST be declared in `assets.yaml`. Paths must identify regular
files inside the repository; symlinks, traversal, duplicate entries, and implicit
directory inclusion are rejected.
