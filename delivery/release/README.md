# Release Management

The Release Management Domain defines the processes and practices used to prepare, version, approve, and publish software releases throughout the DunderCode Engineering System (DESys).

A release represents an officially packaged and approved version of a software product that is ready to be distributed or deployed.

Rather than focusing on software deployment, this domain governs the lifecycle of software versions.

---

# Purpose

The purpose of the Release Management Domain is to establish a consistent and traceable process for creating and publishing software releases.

By standardizing versioning, release preparation, approval, and publication, DESys ensures that every software release is reliable, reproducible, and aligned with engineering standards.

Release Management promotes predictable software evolution while reducing operational risk.

---

# Release Principles

Release Management within DESys follows a common set of engineering principles.

## Version Consistency

Every release must follow an officially adopted versioning strategy.

## Traceability

Every release must be traceable to source code, engineering changes, and supporting documentation.

## Repeatability

Release creation should be reproducible through automated processes.

## Approval

Official releases should follow a defined approval workflow before publication.

## Documentation

Every release should include appropriate documentation, including release notes and change history.

## Recoverability

Release strategies should consider rollback and recovery mechanisms whenever applicable.

---

# Release Lifecycle

Software releases progress through a structured lifecycle.

```text
Engineering Changes
        │
        ▼
Continuous Integration
        │
        ▼
Version Assignment
        │
        ▼
Release Candidate
        │
        ▼
Validation
        │
        ▼
Approval
        │
        ▼
Official Release
        │
        ▼
Deployment
```

This lifecycle ensures that software versions are formally managed before reaching production.

---

# Relationship with the Delivery Layer

Release Management connects continuous integration with software deployment.

```text
CI/CD
        │
        ▼
Release
        │
        ▼
Deployment
        │
        ▼
Operations
```

Release Management governs software versions, while Deployment governs software installation.

---

# Navigation

Continue according to your objective.

| If you want to... | Read |
|-------------------|------|
| Automate software delivery | CI/CD |
| Deploy software | Deployment |
| Operate production environments | Operations |
| Implement observability | Observability |
| Manage production support | Support |

---

# Final Thought

Reliable software delivery depends on disciplined release management.

The Release Management Domain exists to ensure that software versions are prepared, documented, approved, and published through consistent engineering practices before they are deployed to production.

> **Every successful deployment begins with a well-managed release.**