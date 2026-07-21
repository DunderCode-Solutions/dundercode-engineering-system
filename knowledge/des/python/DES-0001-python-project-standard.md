# DES-0001 — Python Project Standard

**Document ID:** DES-0001

**Title:** Python Project Standard

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Owner:** DunderCode Engineering

**Canonical Language:** English

**Category:** Engineering Standard

**Depends On:** DEC-0001, DEM-0001

---

# 1. Purpose

This standard defines the official engineering requirements for Python projects developed within the DunderCode Engineering System (DESys).

Its purpose is to establish a consistent, maintainable, and production-ready foundation for all Python applications, ensuring that projects share the same engineering practices, quality standards, and development workflow.

---

# 2. Scope

This standard applies to all Python projects maintained by DunderCode, including:

* Libraries
* APIs
* Web applications
* Desktop applications
* CLI tools
* Automation scripts
* AI applications
* Internal tools

Project-specific exceptions shall be documented through an Architecture Decision Record (ADR).

---

# 3. Guiding Principles

Every Python project shall:

* Follow the DunderCode Engineering Canon (DEC).
* Follow the DunderCode Engineering Method (DEM).
* Prefer clarity over cleverness.
* Be reproducible.
* Be testable.
* Be maintainable.
* Be fully documented.

Technology choices exist to support engineering principles.

---

# 4. Supported Python Version

The reference Python version is:

* **Python 3.13 or newer**

Projects should adopt the latest stable Python release whenever practical.

---

# 5. Dependency Management

The official dependency manager is:

* **uv**

Requirements:

* Dependencies shall be declared in `pyproject.toml`.
* Lock files shall be committed to version control.
* Reproducible environments are mandatory.

---

# 6. Project Metadata

Every project shall include:

* `pyproject.toml`
* `README.md`
* `LICENSE`
* `.gitignore`
* `.editorconfig`
* `.gitattributes`

Optional files may be added according to project needs.

---

# 7. Project Structure

Projects shall follow the official DunderCode project layout.

Reference implementations are maintained through DunderCode Solution Blueprints (DSB).

---

# 8. Code Quality

Static analysis is mandatory.

Official tools:

* Ruff
* BasedPyright

Linting and type checking must pass before merging changes.

---

# 9. Testing

Every project shall include automated tests.

Reference framework:

* pytest

Requirements:

* Unit tests
* Integration tests (when applicable)
* Regression tests (when applicable)

Testing is considered part of implementation.

---

# 10. Documentation

Documentation is mandatory.

Every project shall include:

* README
* Architecture documentation (when applicable)
* Public API documentation (when applicable)
* Engineering decisions documented through ADRs

Documentation remains the authoritative source of truth.

---

# 11. Version Control

Git is the official version control system.

Branching shall follow the DunderCode Git workflow.

Commits shall follow the DunderCode commit convention.

The reference commit formatter is:

* Task Commit

---

# 12. Continuous Integration

Every repository shall include an automated CI pipeline.

Minimum checks:

* Formatting
* Linting
* Type checking
* Tests
* Documentation validation

No change shall be merged while mandatory checks are failing.

---

# 13. Security

Projects shall:

* Keep dependencies up to date.
* Minimize unnecessary dependencies.
* Protect secrets from source control.
* Validate external inputs.
* Automate dependency auditing whenever practical.

Security is part of engineering quality.

---

# 14. Reference Toolchain

The standard reference toolchain includes:

| Purpose                | Tool                         |
| ---------------------- | ---------------------------- |
| Package Management     | uv                           |
| Formatting & Linting   | Ruff                         |
| Type Checking          | BasedPyright                 |
| Testing                | pytest                       |
| Documentation          | MkDocs + Material for MkDocs |
| Commit Standardization | Task Commit                  |
| Continuous Integration | GitHub Actions               |

Equivalent tools may only be adopted through an approved ADR.

---

# 15. Compliance

A Python project is considered compliant with DES-0001 when it:

* Adheres to the Engineering Canon.
* Follows the Engineering Method.
* Implements this standard.
* Documents justified deviations through ADRs.

Compliance is evaluated by engineering practices rather than by tooling alone.

---

# 16. Evolution

This standard evolves through practical experience.

Improvements shall originate from real projects and be proposed through the DunderCode engineering process before becoming part of the standard.

---

# 17. Closing Statement

The Python Project Standard establishes a shared engineering foundation for every Python project developed within DunderCode.

By reducing unnecessary variation, teams can focus on solving business problems while maintaining consistent engineering quality.

---

> **Think First. Build Better.**
