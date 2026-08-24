# DESys Reference Corpus Editorial Review

Review date: 2026-08-24

Review status: BLOCKED

Review owner: DunderCode Engineering

Review method: OpenCode-assisted complete corpus review with checksum-bound
dispositions recorded in `corpus/inventory.yaml`.

## 1. Scope

This review covers all 346 Markdown files inventoried from `delivery/`,
`engineering/`, `foundation/`, `knowledge/`, and `skills/` for the proposed DESys
v0.2 reference corpus.

The review evaluated:

- substantive completeness and public usefulness;
- canonical English, precision, and editorial consistency;
- compatibility with the authority model in ADR-0001;
- confidential data, credentials, private paths, and unsafe instructions;
- licensing and attribution;
- links and navigation after vendoring;
- metadata lifecycle and unresolved references;
- claims of execution, approval, compliance, or automatic authority;
- stale, absolute, misleading, or insufficiently qualified technical guidance.

`APPROVE` means the exact checksummed content may enter the public bundle.
`REVISE` means the file remains a candidate but must change and be reviewed
again. `EXCLUDE` means the file must not enter the first bundle in its current
role.

## 2. Disposition Summary

| Collection | Files | Approve | Revise | Exclude |
| --- | ---: | ---: | ---: | ---: |
| `delivery` | 7 | 0 | 4 | 3 |
| `engineering` | 31 | 0 | 30 | 1 |
| `foundation` | 11 | 0 | 7 | 4 |
| `knowledge` | 131 | 0 | 109 | 22 |
| `skills` | 166 | 0 | 165 | 1 |
| **Total** | **346** | **0** | **315** | **31** |

The 31 exclusions consist of 26 previously identified empty files and five new
editorial exclusions. The 315 revision candidates remain `pending` in the
inventory. No file was approved automatically.

## 3. Release Blockers

### 3.1 Missing License Text

`pyproject.toml` and `README.md` declare the MIT License, but the repository
`LICENSE` file is empty. Public redistribution must remain blocked until the
intended license text, copyright holder, year, and third-party attribution policy
are confirmed and published.

This blocker applies to the current package and every proposed corpus file.

### 3.2 Authority Ambiguity

Many normative drafts present themselves as official, mandatory, complete, or
authoritative without the consumer boundary required by ADR-0001. Examples
include:

- `foundation/canon/DEC-0001-engineering-manifesto.md:18`;
- `foundation/documentation/DCSG-0001-canon-style-guide.md:20`;
- `engineering/dep/README.md:5`;
- `engineering/det/README.md:7`;
- `knowledge/des/README.md:3`;
- `skills/dsk/01-engineering-skills/DSK-1020-prd-generation.md:218`.

Vendored guidance must be explicitly reference-only and must not override
consumer code, policies, decisions, or identified human approvers.

### 3.3 Nonfunctional Navigation

Navigation tables generally contain plain labels instead of relative Markdown
links. No usable Markdown links were found in the reviewed `delivery/`,
`engineering/`, or `knowledge/` collections. Representative locations include:

- `delivery/README.md:123`;
- `engineering/README.md:271`;
- `foundation/README.md:139`;
- `knowledge/README.md:124`.

Vendored navigation must resolve within `docs/desys/reference/` and distinguish
local project documents from DESys reference documents.

### 3.4 Incomplete Knowledge Contracts

The metadata specification identifies
`knowledge/architecture/metadata/desys-metadata.schema.json` as normative, but
the Markdown-only inventory does not include that required machine-readable
asset. Several DEKG specifications and guides are empty, including the
relationship taxonomy required by
`knowledge/architecture/relationships/README.md:91`.

The distribution design must inventory required non-Markdown assets and either
complete or exclude navigation that promises unavailable content.

### 3.5 Draft Normative Guidance

The engineering and knowledge collections contain broad normative requirements
while their metadata remains draft. Draft status alone is not a blocker, but the
text frequently describes the guidance as already official or universally
applicable. Normative keywords are also inconsistent with the style guide and do
not provide a corpus-wide BCP 14 interpretation.

Documents must either complete governance or be reframed as draft reference
guidance with measurable applicability and conformance boundaries.

### 3.6 Skill Execution and Approval Claims

The approved v0.2 architecture distributes skills only as read-only reference
material. Current skill documents describe executable behavior, deterministic
AI outcomes, autonomous remediation, production deployment, and approval
decisions. Representative locations include:

- `skills/dsk/README.md:37`;
- `skills/dsk/00-foundation/DSK-0010-skill-architecture.md:112`;
- `skills/dsk/03-design-skills/DSK-3022-design-review.md:307`;
- `skills/dsk/05-security-engineering-overview/DSK-5021-security-review.md:332`;
- `skills/dsk/09-operations-engineering/DSK-9017-operational-automation-engineering.md:21`.

All such claims require reference-only framing, explicit human authority,
deny-by-default execution boundaries, bounded credentials, preflight controls,
and clear statements that vendoring performs no action.

### 3.7 Legacy Metadata and Unresolved References

The skills collection contains 105 documents using the governed
`status: canonical` legacy exception. The review also identified widespread
canonical-shaped body references that do not resolve to current documents.

Legacy lifecycle migration and reference resolution must be completed through
governed review rather than inferred automatically.

### 3.8 Safety and Technical Precision

Several engineering, security, DevOps, and operations documents require stronger
qualification. Examples include universal rollback requirements for data
migrations, prompt-oriented requirements applied to all machine learning,
unqualified key rotation intervals, opaque trust scores, autonomous remediation,
and compliance conclusions without qualified review.

These documents must define risk-based tailoring, recovery alternatives,
privacy controls, human decision ownership, evidence requirements, and current
authoritative sources.

## 4. New Editorial Exclusions

| Source | Reason |
| --- | --- |
| `delivery/ci-cd/README.md` | No substantive child assets; generic overview does not provide a useful navigation surface. |
| `delivery/operations/README.md` | No substantive child assets; guidance lacks operational procedures and risk boundaries. |
| `delivery/support/README.md` | No substantive child assets; conflates requests, incidents, feedback, and support cases. |
| `engineering/dea/DEA-0040-architecture-templates.md` | Duplicates and conflicts with the template ownership of `DET-0030`. |
| `foundation/glossary/README.md` | Advertises an authoritative glossary whose three content files are empty. |

These exclusions are content-bound. A future replacement with a new checksum
returns to `pending` and requires a new review.

## 5. Collection Remediation

### Foundation

- resolve the conflicting three-, four-, and five-domain descriptions;
- align the Method README with DEM-0001;
- correct BCP 14 language and references in DCSG-0001;
- qualify documentation source-of-truth claims for consumer use;
- consolidate the overlapping Documentation and Style Guide navigation.

### Delivery

- retain only navigation with substantive destinations;
- link to exact deployment and observability standards;
- add privacy, service-objective, recovery, and authority qualifications;
- distinguish continuous integration, delivery, and deployment;
- replace promotional conclusions with objective scope statements.

### Engineering

- introduce risk-based lifecycle tailoring and exception paths;
- replace universal rollback with tested recovery strategies;
- add AI safety, privacy, provenance, abuse, drift, and incident controls;
- provide actual templates and examples instead of catalogs alone;
- remove the duplicate DEA architecture-template standard;
- add exact relationships, citations, and portable links.

### Knowledge

- complete or remove 22 empty files;
- include required machine-readable schemas in the distribution inventory;
- resolve the DAR terminology conflict;
- add measurable conformance criteria or reclassify abstract principles;
- complete relationship metadata and navigation links;
- normalize normative language and external references.

### Skills

- establish corpus-wide reference-only and non-activation language;
- migrate 105 legacy statuses through explicit governance;
- resolve body references and add authoritative sources;
- qualify security, privacy, compliance, automation, and production guidance;
- remove duplicated governance skills and normalize filenames;
- replace automatic approval claims with advisory outputs and human ownership.

## 6. Required Review Sequence

1. Restore and approve the repository license and attribution policy.
2. Add shared authority, lifecycle, normative-language, and navigation rules.
3. Extend the inventory to required non-Markdown corpus assets.
4. Remediate Foundation and cross-corpus terminology.
5. Remediate Engineering and Knowledge by domain.
6. Migrate and remediate Skills in bounded batches.
7. Regenerate checksums; changed content returns to `pending`.
8. Repeat editorial, security, licensing, and link review.
9. Mark only exact reviewed checksums as `approved`.

## 7. Decision

The editorial decision for the current corpus snapshot is **NO-GO** for public
bundle generation. The v0.1 tooling release remains technically separate from
this proposed corpus, but its empty `LICENSE` file requires immediate owner
resolution because the public repository currently declares MIT licensing.
