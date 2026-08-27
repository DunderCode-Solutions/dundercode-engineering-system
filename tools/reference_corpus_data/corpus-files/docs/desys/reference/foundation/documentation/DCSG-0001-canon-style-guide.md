---
metadata_schema: 1.0.0
document_id: DCSG-0001
canonical_id: dcsg.canon.style-guide
title: DunderCode Canon Style Guide
node_type: style-guide
document_class: normative
version: 1.2.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- Documentation produced and governed within DESys
relationships:
- type: related
  target: dec.foundation.engineering-manifesto
- type: related
  target: dem.foundation.engineering-method
- type: depends_on
  target: dekg.specification.metadata-schema
---

# DCSG-0001 - DunderCode Canon Style Guide

## 1. Status and Authority

This document is a draft of the DESys editorial standard. Its requirements become
binding within DESys only after lifecycle approval.

When vendored into a consumer repository, this guide is reference material.
Consumer projects adopt it through their own governance. It does not override
consumer code, runtime evidence, approved decisions, legal obligations, or local
documentation policy.

## 2. Purpose

This guide defines proposed rules for creating, reviewing, publishing, and
maintaining DESys documentation. The rules support clear human communication,
stable machine-readable identity, traceability, and deterministic indexing.

Documentation records intent and knowledge. It remains synchronized with source
code, tests, runtime observations, and approved decisions rather than replacing
those forms of evidence.

## 3. Scope

This guide applies to identifier-bearing DESys documents and DESys navigation
surfaces, including:

- canons, methods, standards, assessments, decisions, proposals, and guides;
- product requirements and architecture records;
- templates and skills represented as documentation;
- repository and collection README files;
- generated documentation instructions and indexes.

It does not define software architecture, programming practices, product
requirements, or approval roles. Those responsibilities belong to the applicable
project and domain governance.

## 4. Editorial Principles

DESys documentation follows these principles:

- **Clarity:** state scope, terms, assumptions, and conclusions explicitly.
- **Precision:** distinguish requirements, recommendations, examples, and facts.
- **Traceability:** identify authoritative sources and semantic relationships.
- **Consistency:** use stable terminology, identity, and structure.
- **Maintainability:** avoid duplicated authority and version-sensitive claims
  without references.
- **Evidence:** qualify claims according to the evidence available.
- **Proportionality:** apply structure and detail appropriate to document risk and
  purpose.
- **Accessibility:** use navigable headings, descriptive links, and readable
  tables and diagrams.

Marketing language, slogans, unsupported guarantees, and exaggerated claims
SHOULD NOT appear in governed technical content.

## 5. Lifecycle

Canonical lifecycle values are:

```text
draft -> review -> approved -> published -> deprecated
```

A metadata value records state; it does not prove that an authorized transition
occurred. Lifecycle changes MUST have governance evidence outside the metadata
field, such as an approved review or pull request.

Draft documents MUST NOT describe themselves as approved, official, or binding.
Deprecated documents MUST identify their replacement when one exists.

## 6. Canonical Language

The canonical source language for metadata schema v1 is English.

Translations are derived documents and MUST NOT replace or silently modify the
canonical source. A translation SHOULD identify its canonical source and the
revision from which it was derived.

## 7. Normative Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in normative DESys documents are to be interpreted as described in
[BCP 14](https://www.rfc-editor.org/info/bcp14) when, and only when, they appear
in all capitals, as specified by
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

| Keywords | Meaning |
| --- | --- |
| `MUST`, `REQUIRED`, `SHALL` | Absolute requirement. |
| `MUST NOT`, `SHALL NOT` | Absolute prohibition. |
| `SHOULD`, `RECOMMENDED` | Recommended unless a justified exception exists. |
| `SHOULD NOT`, `NOT RECOMMENDED` | Discouraged unless a justified exception exists. |
| `MAY`, `OPTIONAL` | Permitted but not required. |

Lowercase forms have their ordinary English meaning. Authors MUST use uppercase
keywords only for deliberate requirements and MUST define the scope to which
each requirement applies.

Informative documents and navigation files MAY use ordinary language. They MUST
NOT use requirement-like wording to imply authority they do not possess.

## 8. Document Structure

An indexable document MUST:

- begin with canonical YAML front matter on line 1;
- contain one level-one heading identifying the document;
- use level-two and deeper headings without skipping levels unnecessarily;
- state purpose and scope;
- distinguish normative requirements from informative explanation;
- identify material assumptions, limitations, and references;
- preserve a stable document ID and canonical ID.

Additional sections SHOULD be selected according to document type. A short
decision record does not need the same structure as a complete standard.

README files are navigation surfaces. They SHOULD describe collection scope,
authority, lifecycle state, and provide working relative Markdown links.

## 9. Metadata

Every non-empty, identifier-bearing DESys Markdown document MUST satisfy
[DEKG-0040](../../knowledge/architecture/dekg/specification/DEKG-0040-metadata-schema.md)
and the normative
[DESys metadata JSON Schema](../../knowledge/architecture/metadata/desys-metadata.schema.json).

README files do not require canonical metadata. Empty files are not governed
documents, do not reserve identifiers, and MUST NOT enter a public corpus bundle.

Unknown metadata fields MUST NOT be introduced without a metadata-schema change
and migration path.

## 10. Links and Relationships

Human navigation SHOULD use descriptive Markdown links rather than plain document
names. Internal links MUST be relative and MUST remain valid in the source and
documented vendored layout.

External claims SHOULD link to an authoritative, versioned source when
practical. Authors MUST record attribution and license notices when required by
the referenced material.

Semantic dependencies SHOULD also be represented through canonical metadata
relationships. A hyperlink supports navigation; a metadata relationship supports
graph semantics. Neither mechanism implies approval authority.

## 11. Voice and Terminology

Documents SHOULD use active voice, direct sentences, and consistent terms.
Authors SHOULD:

1. explain the context and reason;
2. state the requirement or guidance;
3. describe application and evidence;
4. identify exceptions or limitations.

Terms with multiple common meanings MUST be defined in context. Product names,
standards, protocols, and external methods SHOULD identify their owner and
version policy where relevant.

## 12. Examples and Technical Material

Examples SHOULD be included when they materially improve understanding. They
MUST be identified as examples and MUST NOT be presented as universally safe or
production-ready without stated assumptions.

Code and command examples MUST:

- avoid real credentials, private paths, and confidential identifiers;
- identify destructive or privileged effects;
- use placeholders that cannot be mistaken for live values;
- state relevant platform or version assumptions;
- include preflight, recovery, or human-confirmation guidance when risk warrants.

Diagrams SHOULD communicate one defined view and include accessible text where
the visual alone is insufficient. Tables SHOULD be used for structured
comparison, not as a substitute for necessary explanation.

## 13. AI-Assisted Documentation

AI systems MAY assist with retrieval, drafting, comparison, and validation. They
are not engineering or approval authorities.

AI-assisted content MUST be reviewed according to its risk. Claims about a
consumer project MUST cite consumer evidence. Missing evidence, unresolved
conflicts, and uncertain authority MUST be reported rather than invented.

Skills distributed as documents are read-only references unless a separate,
explicitly authorized execution mechanism defines otherwise. Vendoring a skill
document MUST NOT activate or execute it.

## 14. Quality Review

Before lifecycle approval, reviewers MUST verify, as applicable:

- purpose, audience, scope, and authority are explicit;
- metadata and identity validate;
- requirements use BCP 14 consistently;
- links and relationships resolve;
- factual and external claims have suitable sources;
- examples disclose material assumptions and risks;
- no credential, personal, confidential, or private-path data is present;
- duplicate or conflicting authority is resolved;
- generated artifacts are updated from source rather than edited directly;
- known limitations and residual risks are recorded.

Passing automated validation is necessary but does not replace editorial,
security, legal, or domain review.

## 15. Governance

Material changes to this guide require an RFC or equivalent recorded proposal,
review by the documentation owner, impact analysis for validators and templates,
and an explicit lifecycle decision.

Changes to metadata fields, enums, or validation behavior additionally require a
new metadata schema version and migration path.

## 16. References

- [BCP 14 - Requirement Levels](https://www.rfc-editor.org/info/bcp14)
- [RFC 2119 - Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174)
- [DEC-0001 - The DunderCode Engineering Manifesto](../canon/DEC-0001-engineering-manifesto.md)
- [DEM-0001 - The DunderCode Engineering Method](../../knowledge/dem/DEM-0001-engineering-method.md)
- [DEKG-0040 - Metadata Schema](../../knowledge/architecture/dekg/specification/DEKG-0040-metadata-schema.md)

## 17. Revision History

### 1.2.0 - Draft

- Added explicit draft, consumer-adoption, and evidence authority boundaries.
- Adopted complete BCP 14 terminology through RFC 2119 and RFC 8174.
- Added portable linking, attribution, safety, AI, and quality-review rules.
- Aligned metadata guidance with DEKG-0040 and its JSON Schema.

### 1.1.0 - Draft

- Introduced normative-language and metadata guidance.

### 1.0.0 - Draft

- Initial style-guide draft.
