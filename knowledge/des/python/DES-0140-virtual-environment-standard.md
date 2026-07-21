# DES-0130 — Packaging Standard

**Document ID:** DES-0130

**Title:** Packaging Standard

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Owner:** DunderCode Engineering

**Canonical Language:** English

**Category:** Engineering Standard

**Depends On:** DEC-0001, DEM-0001, DES-0001, DES-0120

---

# 1. Purpose

This standard defines the official packaging practices for Python projects developed within the DunderCode Engineering System (DESys).

Its objective is to ensure that Python software is packaged, versioned, distributed, and maintained in a consistent, reliable, and reproducible manner.

Packaging is considered an engineering responsibility that extends beyond software distribution.

---

# 2. Scope

This standard applies to every Python project intended for distribution, including:

* Public libraries
* Internal libraries
* Command-line applications
* Reusable frameworks
* Automation tools
* SDKs
* Plugins

Projects that are not distributed externally should still follow this standard whenever applicable.

---

# 3. Guiding Principles

Packaging shall:

* Promote reproducibility.
* Be deterministic.
* Follow Python packaging standards.
* Minimize configuration duplication.
* Preserve project metadata.
* Support long-term maintainability.

Consistency is preferred over customization.

---

# 4. Project Metadata

Every project shall maintain its metadata in:

`pyproject.toml`

The project metadata is the authoritative source for:

* Project name
* Version
* Description
* Authors
* License
* Python requirements
* Dependencies
* Build system
* Project URLs

Metadata shall remain accurate throughout the project lifecycle.

---

# 5. Build System

Projects shall use a standards-compliant build backend.

The selected backend shall:

* Support modern Python packaging.
* Integrate with the official dependency manager.
* Produce reproducible artifacts.
* Follow PEP-compliant packaging practices.

Build system selection may evolve through approved ADRs.

---

# 6. Distribution Artifacts

Whenever applicable, projects should generate:

* Source Distribution (sdist)
* Built Distribution (wheel)

Distributed artifacts shall be reproducible and traceable to a released version.

---

# 7. Versioning

Projects shall adopt Semantic Versioning (SemVer).

Version numbers communicate compatibility and release intent.

Breaking changes shall increment the major version.

---

# 8. Release Process

Releases should:

* Be reproducible.
* Be traceable.
* Correspond to tagged versions.
* Be documented.

Release notes should accompany every public release.

---

# 9. Licensing

Every distributed project shall define an explicit software license.

The selected license shall be compatible with the project's intended distribution model.

License information shall be included in project metadata.

---

# 10. Project Identity

Every project shall provide:

* README
* LICENSE
* CHANGELOG (recommended)
* Project URLs
* Repository information

Public projects should clearly communicate their purpose, installation method, and usage.

---

# 11. Distribution Repositories

Projects may be distributed through:

* Public package repositories
* Private package repositories
* Internal artifact repositories

Distribution targets shall be documented as part of the project.

---

# 12. Compliance

A project complies with this standard when it:

* Maintains complete project metadata.
* Produces reproducible distribution artifacts.
* Uses Semantic Versioning.
* Documents releases.
* Includes licensing information.
* Follows Python packaging standards.

Compliance is evaluated through engineering practices rather than publication targets.

---

# 13. Evolution

Packaging practices evolve with the Python ecosystem.

Changes to this standard shall be validated through real projects before becoming part of DESys.

---

# 14. Closing Statement

Packaging is the process through which software becomes a reusable engineering asset.

Within DESys, packaging ensures that software can be reliably shared, versioned, maintained, and reused across projects and teams.

---

> **Think First. Build Better.**
