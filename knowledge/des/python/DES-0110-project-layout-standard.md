# DES-0110 — Project Layout Standard

**Document ID:** DES-0110

**Title:** Project Layout Standard

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Owner:** DunderCode Engineering

**Canonical Language:** English

**Category:** Engineering Standard

**Depends On:** DEC-0001, DEM-0001, DES-0001

---

# 1. Purpose

This standard defines the official directory structure for Python projects developed within the DunderCode Engineering System (DESys).

Its purpose is to establish a consistent project organization that promotes clarity, maintainability, scalability, and discoverability.

A project structure is not merely a collection of directories; it is an expression of engineering intent.

---

# 2. Scope

This standard applies to all Python projects maintained by DunderCode, including libraries, APIs, desktop applications, web applications, automation tools, and internal systems.

Project-specific deviations shall be documented through an Architecture Decision Record (ADR).

---

# 3. Guiding Principles

The project layout shall:

* Reflect the domain before the technology.
* Separate responsibilities clearly.
* Minimize unnecessary nesting.
* Promote discoverability.
* Scale naturally as the project grows.
* Remain understandable by both humans and AI systems.

Directory names should communicate purpose rather than implementation details.

---

# 4. Standard Project Layout

The following structure is the reference layout for DunderCode Python projects.

```text
project/
│
├── src/
│   └── <package_name>/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── assets/
│
├── .github/
│
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── .gitattributes
└── .pre-commit-config.yaml
```

Reference Blueprints may extend this structure while preserving its overall organization.

---

# 5. Directory Responsibilities

## src/

Contains the production source code.

Business logic shall reside here.

---

## tests/

Contains automated tests.

Test code shall never be mixed with production code.

---

## docs/

Contains project documentation.

Documentation is maintained independently from implementation.

---

## scripts/

Contains development and automation scripts.

Scripts should not contain business logic.

---

## assets/

Contains static project resources such as images, icons, sample data, and diagrams.

---

## .github/

Contains repository automation, workflows, issue templates, and pull request templates.

---

# 6. Root Files

Every project shall include the following files.

| File                      | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `pyproject.toml`          | Project metadata and dependency management |
| `README.md`               | Project portal                             |
| `LICENSE`                 | Software license                           |
| `.gitignore`              | Git exclusions                             |
| `.editorconfig`           | Editor consistency                         |
| `.gitattributes`          | Repository behavior                        |
| `.pre-commit-config.yaml` | Quality automation                         |

Additional files may be introduced when justified.

---

# 7. Naming Conventions

Directory names shall:

* Use lowercase letters.
* Use descriptive names.
* Avoid abbreviations unless widely recognized.
* Reflect responsibilities instead of technologies.

Example:

Good:

* `documentation`
* `assets`
* `scripts`

Avoid:

* `misc`
* `tmp`
* `stuff`

---

# 8. Scalability

The project structure should support growth without requiring major reorganization.

New directories shall only be introduced when they represent a clear engineering responsibility.

Avoid creating structure before a demonstrated need exists.

---

# 9. Compliance

A project complies with this standard when:

* The directory structure follows the official layout.
* Responsibilities are clearly separated.
* Project conventions remain consistent.
* Exceptions are documented through ADRs.

Compliance is evaluated by architectural consistency rather than strict folder counts.

---

# 10. Evolution

The project layout is expected to evolve as engineering practices mature.

Changes to this standard shall be proposed through the DunderCode engineering process and validated through real-world projects before adoption.

---

# 11. Closing Statement

A well-organized project structure reduces cognitive load, accelerates onboarding, and improves long-term maintainability.

The project layout is therefore considered an essential engineering asset rather than a matter of personal preference.

---

> **Think First. Build Better.**
