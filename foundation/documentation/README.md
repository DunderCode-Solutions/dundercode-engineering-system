# Documentation

The Documentation component defines how DESys engineering knowledge is written,
identified, reviewed, published, and maintained. Documentation is a first-class
engineering asset, but it is one form of evidence rather than an automatic
replacement for source code or runtime behavior.

## Responsibility

The component governs:

- canonical metadata and stable document identity;
- editorial structure and normative language;
- explicit links and semantic relationships;
- lifecycle status and review expectations;
- human-readable and machine-readable navigation;
- maintenance of source documents and generated indexes.

Each concept should have an identified authoritative source within its scope.
Consumer projects define their own authority through project governance. DESys
reference documents provide guidance unless explicitly adopted by the consumer.

## Canonical Guide

| Document | Status | Purpose |
| --- | --- | --- |
| [DCSG-0001](DCSG-0001-canon-style-guide.md) | Draft | Defines the proposed DESys editorial and documentation rules. |

The adjacent `style-guide/` directory is a compatibility navigation surface and
does not own a separate style-guide standard.

## Document Lifecycle

```text
Draft -> Review -> Approved -> Published -> Deprecated
```

Lifecycle transitions require governance evidence. Metadata alone does not
identify an approver or infer that a transition occurred.

## Navigation

| Objective | Read |
| --- | --- |
| Apply editorial conventions | [DCSG-0001](DCSG-0001-canon-style-guide.md) |
| Understand DESys principles | [DEC-0001](../canon/DEC-0001-engineering-manifesto.md) |
| Understand the DESys method | [DEM-0001](../../knowledge/dem/DEM-0001-engineering-method.md) |
| Inspect the metadata contract | [DEKG-0040](../../knowledge/architecture/dekg/specification/DEKG-0040-metadata-schema.md) |
| Browse technical standards | [DES standards](../../knowledge/des/README.md) |
| Return to Foundation | [Foundation](../README.md) |
