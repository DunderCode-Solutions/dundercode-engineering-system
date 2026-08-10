---
metadata_schema: 1.0.0
document_id: DET-0040
canonical_id: det.api.templates
title: API Templates
node_type: template
document_class: normative
version: 1.0.0
status: draft
language: en
owner: DunderCode Engineering
applies_to:
- All API documentation developed within DESys
---

# DET-0040 — API Templates

# 1. Purpose

The API Templates Standard defines the engineering principles and reusable templates used to document Application Programming Interfaces (APIs) and integration contracts within the DunderCode Engineering System (DESys).

Its purpose is to establish a standardized approach for documenting service interfaces, communication contracts, integration models, and API specifications while preserving consistency, interoperability, traceability, and engineering quality.

API templates ensure that service contracts are clear, versioned, and implementation-independent.

---

# 2. Scope

This standard applies to every API-related artifact produced within DET.

It covers reusable templates for:

* REST API Specifications
* GraphQL Specifications
* AsyncAPI Specifications
* OpenAPI Specifications
* Event Contracts
* Webhook Specifications
* Integration Contracts
* Service Interface Specifications
* API Version Documentation
* Error Contract Specifications

Implementation code is intentionally outside the scope of this document.

---

# 3. Audience

This document is intended for:

* Software Architects
* Solution Architects
* API Designers
* Backend Engineers
* Integration Engineers
* Platform Engineers
* QA Engineers
* Technical Writers
* AI-assisted engineering systems

---

# 4. Relationship with DESys

API Templates document the communication contracts defined by the engineering architecture.

```text id="f6m8pa"
Requirements
        ↓
Architecture
        ↓
API Templates
        ↓
Implementation
        ↓
Consumers
```

API documentation serves as the authoritative contract between service providers and consumers.

---

# 5. Engineering Principles

Every API Template SHALL follow the principles below.

## Contract First

API documentation SHALL define the service contract before implementation whenever practical.

---

## Clarity

API contracts SHALL be clear, precise, and unambiguous.

---

## Consistency

Equivalent services SHOULD follow equivalent API documentation patterns.

---

## Technology Independence

API templates SHOULD describe service behavior independently of implementation technologies.

---

## Versionability

API contracts SHALL support controlled version evolution.

---

## Traceability

API documentation SHALL remain traceable to requirements, architecture, and implementation.

---

## Interoperability

Templates SHALL facilitate interoperability between systems.

---

## Maintainability

API documentation SHOULD remain easy to update as interfaces evolve.

---

## Security

API templates SHALL document authentication, authorization, and security requirements whenever applicable.

---

## Governance

API documentation SHALL support engineering governance and lifecycle management.

---

# 6. Standard Template Structure

API templates SHOULD include, when applicable:

* Metadata
* Purpose
* Scope
* Service Description
* Endpoint or Operation
* Request Definition
* Response Definition
* Data Models
* Authentication
* Authorization
* Error Responses
* Version Information
* Rate Limits
* Integration Notes
* Dependencies
* References
* Changelog

Additional sections MAY be introduced according to integration complexity.

---

# 7. Mandatory Requirements

Every API template MUST:

* Clearly identify the service.
* Describe supported operations.
* Define request and response contracts.
* Document error behavior.
* Include version information.
* Preserve engineering traceability.
* Follow DET documentation standards.

---

# 8. API Documentation Lifecycle

API documentation SHALL evolve alongside the service lifecycle.

```text id="j5r9qw"
API Design
        ↓
Contract Definition
        ↓
Technical Review
        ↓
Publication
        ↓
Implementation
        ↓
Consumer Adoption
        ↓
Contract Evolution
```

API documentation SHALL remain synchronized with production interfaces.

---

# 9. Compliance

An API Template complies with this standard when it:

* Documents the service contract completely.
* Supports interoperability.
* Preserves engineering traceability.
* Aligns with DES API standards.
* Supports controlled API evolution.

---

# 10. Relationship with Other DET Documents

API Templates connect architectural communication models with software implementation.

| Document | Relationship                   |
| -------- | ------------------------------ |
| DET-0000 | Engineering Templates Overview |
| DET-0010 | Project Templates              |
| DET-0020 | Requirements Templates         |
| DET-0030 | Architecture Templates         |
| DET-0040 | API Templates                  |
| DET-0050 | Testing Templates              |
| DET-0060 | Operational Templates          |
| DET-0070 | AI Templates                   |
| DET-0080 | Template Governance            |

API Templates provide the standardized documentation used to specify service contracts and integrations.

---

# 11. Recommended Template Catalog

The following templates are recommended within this family.

| Template                        | Purpose                           |
| ------------------------------- | --------------------------------- |
| OpenAPI Specification           | REST API contract                 |
| GraphQL Specification           | GraphQL schema documentation      |
| AsyncAPI Specification          | Event-driven API contract         |
| Event Contract                  | Event payload definition          |
| Webhook Specification           | Callback interface documentation  |
| Service Interface Specification | Internal service contract         |
| Integration Contract            | System-to-system integration      |
| API Version Specification       | Version management documentation  |
| Error Contract                  | Standardized error responses      |
| Authentication Specification    | Security and authentication model |

Organizations MAY extend this catalog while preserving DET principles.

---

# 12. References

* DEC-0001 — DunderCode Engineering Canon
* DEM-0001 — DunderCode Engineering Method
* DCSG-0001 — DunderCode Canon Style Guide
* DES — DunderCode Engineering Standards
* DEA — DunderCode Engineering Architecture
* DET-0000 — Engineering Templates Overview
* DET-0030 — Architecture Templates

---

# 13. Changelog

## Version 1.0.0 (Draft)

### Added

* Initial API Templates Standard.
* Defined engineering principles for API documentation.
* Established the standard structure for API templates.
* Introduced the API Documentation Lifecycle.
* Included the recommended catalog of reusable API documentation templates.
* Positioned API Templates as the standardized contract layer between architecture and software integration.
