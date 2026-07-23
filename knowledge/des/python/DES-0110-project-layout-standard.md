
# DES-0110 — Project Layout Standard

# Metadata

**Canonical ID:** des.python.layout

**Document Class:** Normative

**Version:** 1.0.0 (Draft)

**Status:** Draft

**Canonical Language:** English

**Owner:** DunderCode Engineering

**Applies To:** All Python projects developed under DESys

---

# 1. Purpose

The Project Layout Standard defines the canonical directory structure for Python projects developed under the DunderCode Engineering System (DESys).

Its purpose is to establish a consistent, predictable, and maintainable project organization that improves readability, scalability, onboarding, automation, and long-term maintenance.

This standard ensures that every DESys-compliant Python project follows the same organizational principles regardless of project size or business domain.

---

# 2. Scope

This standard applies to every Python software project developed under DESys.

It defines the required organization of source code, documentation, tests, configuration files, automation assets, and supporting resources.

Implementation details are intentionally excluded from this standard and are defined by other engineering standards.

---

# 3. Audience

This standard is intended for:

- Software Engineers
- Solution Architects
- Technical Leaders
- Engineering Managers
- Project Maintainers
- AI-assisted engineering systems

Anyone responsible for creating or maintaining Python project structures SHALL follow this standard.

---

# 4. Relationship with DES-0001

This standard specializes the engineering principles established by DES-0001 — Python Engineering Foundation Standard.

While DES-0001 defines the engineering baseline, DES-0110 specifies how Python projects SHALL be organized to satisfy those principles.

Project layout is considered a fundamental engineering concern because it directly impacts maintainability, discoverability, automation, and collaboration.
---

# 5. Engineering Principles

Project organization SHALL follow these principles.

## Consistency

Projects MUST follow a common directory structure.

## Separation of Concerns

Each directory MUST have a single well-defined responsibility.

## Discoverability

Developers SHOULD locate project resources quickly without prior project knowledge.

## Scalability

The project layout MUST support long-term growth without requiring structural redesign.

## Predictability

Projects SHOULD be organized consistently across the entire DESys ecosystem.

## Automation

The directory structure SHOULD facilitate automation by engineering tools.

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

# 6. Standard

Every DESys-compliant Python project SHALL adopt the canonical project layout defined by this standard.

The project structure MUST separate source code, documentation, testing, configuration, automation, deployment assets, and engineering knowledge into clearly defined locations.

The canonical layout is intended to maximize readability, maintainability, and engineering consistency across all projects.

---

# 7. Mandatory Requirements

Every Python project developed under DESys MUST:

- Separate source code from project documentation.
- Isolate automated tests from production code.
- Maintain engineering documentation under a dedicated knowledge directory.
- Store configuration independently from application logic.
- Organize deployment assets separately from source code.
- Keep engineering automation isolated from business logic.
- Avoid ambiguous directory names.
- Preserve a stable project structure throughout the project lifecycle.

---

# 8. Recommended Structure

The following represents the canonical DESys project layout.

```text
project/

├── apps/
├── config/
├── knowledge/
├── tests/
├── scripts/
├── deployment/
├── docs/
├── pyproject.toml
├── README.md
└── LICENSE
```

Additional directories MAY be introduced when justified by project requirements.

However, they SHOULD preserve the organizational principles established by this standard.

Projects SHOULD avoid introducing directories that duplicate existing responsibilities.

---

# 9. Compliance

A Python project complies with this standard when its directory organization follows the mandatory requirements defined herein.

Compliance SHALL be verified as part of engineering reviews and assessment reports (DAR).

Non-compliant structures SHOULD be corrected before major development activities continue.

---

# 10. References

- DEC-0001 — DunderCode Engineering Canon
- DEM-0001 — DunderCode Engineering Method
- DCSG-0001 — DunderCode Canon Style Guide
- DES-0001 — Python Engineering Foundation Standard

---

# 11. Changelog

## Version 1.0.0 (Draft)

### Added

- Initial Project Layout Standard.
- Defined the canonical DESys directory organization.
- Established mandatory project organization requirements.
- Introduced the canonical project layout for Python software.
---

> **Think First. Build Better.**
