# Metadata

The Metadata Domain defines the common metadata model shared by every engineering asset within the DunderCode Engineering System (DESys).

It establishes the structural information that enables engineering assets to be uniquely identified, versioned, classified, traced, reviewed, and semantically connected across the platform.

Rather than describing engineering content, metadata describes the engineering assets themselves.

This shared model provides the foundation for consistency, discoverability, governance, and semantic interoperability.

---

# Purpose

The purpose of the Metadata Domain is to establish a unified metadata model for the engineering platform.

Every engineering asset published within DESys follows the same metadata structure, enabling predictable organization, navigation, traceability, lifecycle management, and AI-assisted discovery.

A standardized metadata model ensures that engineering knowledge remains consistent as the platform evolves.

---

# Engineering Metadata Model

Metadata represents structured information about an engineering asset.

Rather than describing technical implementation, metadata defines the identity and lifecycle of engineering knowledge.

Typical metadata includes information such as:

- Identification
- Classification
- Versioning
- Review status
- Ownership
- Scope
- Traceability

Every engineering asset is expected to expose a consistent metadata structure.

---

# Metadata Principles

The metadata model follows a common set of principles.

## Consistency

Equivalent engineering assets should expose equivalent metadata.

## Traceability

Metadata should enable relationships between engineering assets to be explicitly established.

## Reusability

The same metadata model should be reusable across all engineering domains.

## Version Awareness

Metadata should capture the evolution of engineering assets over time.

## Machine Readability

Metadata should support reliable interpretation by automation tools and AI agents.

## Extensibility

The metadata model should evolve without breaking existing engineering assets.

---

# Metadata Fields

The complete metadata contract is defined by DEKG-0040 and serialized as YAML front matter.

Typical metadata categories include:

| Category | Purpose |
|----------|---------|
| Identification | Uniquely identifies engineering assets. |
| Classification | Categorizes engineering knowledge. |
| Lifecycle | Tracks publication and review status. |
| Governance | Records ownership and responsibility. |
| Traceability | Connects related engineering assets. |

The normative machine-readable schema is available at `knowledge/architecture/metadata/desys-metadata.schema.json`.

Every non-empty, identifier-bearing DESys document must conform to that schema. README files remain navigation surfaces outside the DEKG, and empty placeholders are not indexed as nodes.

Validate the repository with:

```bash
python3 tools/validate_metadata.py
```

---

# Relationship with the DEKG

Metadata provides the descriptive layer that enriches the DunderCode Engineering Knowledge Graph (DEKG).

```text
Engineering Asset
        │
        ▼
Metadata
        │
        ▼
Semantic Relationships
        │
        ▼
DEKG
```

While the DEKG defines how engineering assets are connected, metadata defines the descriptive information that enables those connections to be understood, validated, and queried.

Together they establish the semantic foundation of the engineering platform.

---

# Navigation

Continue according to your objective.

| If you want to... | Read |
|-------------------|------|
| Understand the semantic graph | DEKG |
| Apply the metadata contract | DEKG-0040 Metadata Schema |
| Learn node classifications | Node Types |
| Explore semantic connections | Relationships |
| Navigate the platform | Knowledge Map |
| Understand the platform architecture | DESys Architecture |

---

# Final Thought

Engineering knowledge becomes significantly more valuable when every asset is consistently described.

The Metadata Domain exists to establish a shared descriptive model that enables engineering assets to remain identifiable, traceable, interoperable, and semantically connected throughout the evolution of the DunderCode Engineering System.

> **Consistent metadata transforms engineering assets into connected engineering knowledge.**
