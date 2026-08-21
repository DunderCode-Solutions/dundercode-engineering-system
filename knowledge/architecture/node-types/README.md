# Node Types

The Node Types Domain defines the categories of engineering assets represented within the DunderCode Engineering Knowledge Graph (DEKG).

Every engineering asset belongs to a well-defined node type that describes its architectural role within the engineering platform.

Rather than classifying engineering knowledge according to physical location, Node Types classify engineering assets according to their semantic purpose.

This classification enables consistent organization, navigation, validation, and AI-assisted reasoning throughout DESys.

---

# Purpose

The purpose of the Node Types Domain is to establish a shared classification model for engineering assets.

Each node type represents a distinct engineering concept that can participate in the knowledge graph.

A consistent classification model enables engineering assets to be interpreted predictably regardless of their implementation or location.

---

# What is a Node Type?

A Node Type defines the semantic category of an engineering asset.

Rather than describing a specific document, a node type identifies the engineering role performed by that asset.

Examples include:

- Layer
- Domain
- Specification
- Standard
- Blueprint
- Guide
- Template
- Decision
- Review
- Project
- Tool

Every engineering asset belongs to exactly one primary node type.

This classification enables semantic reasoning across the engineering platform.

---

# Engineering Node Model

Engineering assets are organized through semantic categories.

```text
Engineering Asset
        │
        ▼
Node Type
        │
        ▼
Metadata
        │
        ▼
Relationships
        │
        ▼
Knowledge Graph
```

This model separates asset identity from asset classification and semantic connectivity.

---

# Classification Principles

The node classification model follows several architectural principles.

## Single Primary Classification

Every engineering asset belongs to one primary node type.

## Semantic Meaning

Node types represent engineering purpose rather than storage location.

## Extensibility

New node types may be introduced without affecting existing classifications.

## Consistency

Equivalent engineering assets always share the same node type.

## Discoverability

Classification enables efficient navigation and semantic querying.

## AI Interpretability

Node types provide explicit semantic meaning for automation tools and AI agents.

---

# Relationship with Metadata

Node Types and Metadata complement one another.

Metadata describes an engineering asset.

Node Types classify an engineering asset.

```text
Engineering Asset
        │
        ├── Metadata
        │
        └── Node Type
                 │
                 ▼
Semantic Relationships
                 │
                 ▼
DEKG
```

Together they provide the structural information required by the knowledge graph.

---

# Navigation

Continue according to your objective.

| If you want to... | Read |
|-------------------|------|
| Learn the metadata model | Metadata |
| Understand semantic relationships | Relationships |
| Explore the knowledge graph | DEKG |
| Navigate the platform | Knowledge Map |
| Understand the platform architecture | DESys Architecture |

---

# Final Thought

Meaningful knowledge begins with meaningful classification.

The Node Types Domain exists to establish a consistent semantic taxonomy for engineering assets, enabling scalable organization, reliable navigation, and intelligent reasoning throughout the DunderCode Engineering System.

> **Well-defined classifications transform engineering assets into structured knowledge.**