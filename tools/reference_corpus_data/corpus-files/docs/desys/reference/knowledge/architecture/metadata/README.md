# Metadata

This directory contains the draft DESys metadata contract and its
machine-readable validation artifact:

- [DEKG-0040 - Metadata Schema](../dekg/specification/DEKG-0040-metadata-schema.md)
- [DESys metadata JSON Schema](desys-metadata.schema.json)

DEKG-0040 defines scope, authority, fields, identity rules, local loading, and
release provenance. The JSON Schema defines the metadata mapping accepted by
schema version `1.0.0`.

When these files are installed through a future opt-in reference corpus, they
remain reference material unless a consumer adopts them through local
governance. The approved distribution design requires the schema to be packaged
at:

```text
docs/desys/reference/knowledge/architecture/metadata/desys-metadata.schema.json
```

The schema `$id` is
`urn:uuid:22eb6a5c-efb9-5581-9ee5-e52435153086`. Load the schema from the local
file and associate that exact URN with the resource; do not treat the URN as a
network location.

Run metadata validation from the repository or an installed environment:

```bash
desys-metadata-validate
```

The repository's locked development environment can invoke the same command with:

```bash
uv run desys-metadata-validate
```
