---
metadata_schema: 1.0.0
document_id: DSK-5014
canonical_id: dsk.security.cryptography
title: Cryptography
node_type: skill
document_class: operational
version: 2.0.0
status: canonical
legacy_status: true
language: en
owner: DunderCode Engineering
domain: Security Engineering
discipline: Engineering Cryptographic Protection
---

# DSK-5014 | Cryptography

# 1. Purpose

This skill defines the **Engineering Cryptographic Protection (ECP)** discipline adopted by the DunderCode Engineering System (DESys).

Within DESys, cryptography is not merely the selection of cryptographic algorithms.

It is the engineering discipline responsible for protecting engineering assets through governed cryptographic policies, managed key lifecycles and verifiable security mechanisms that preserve confidentiality, integrity, authenticity and long-term engineering trust.

Cryptography protects engineering assets.

---

# 2. Scope

Engineering Cryptographic Protection governs:

* Cryptographic Policies
* Cryptographic Mechanisms
* Key Management
* Cryptographic Lifecycle
* Cryptographic Registry
* Cryptographic Traceability
* Cryptographic Governance

---

# 3. Engineering Position

Cryptography protects engineering assets throughout their lifecycle.

```text id="cryptography-position"
Engineering Asset
        ↓
Protection Requirement
        ↓
Cryptographic Policy
        ↓
Cryptographic Protection
        ↓
Protected Asset
```

Cryptographic protection SHALL remain governed and measurable.

---

# 4. Engineering Objectives

Engineering Cryptographic Protection aims to:

* preserve confidentiality;
* preserve integrity;
* establish authenticity;
* support non-repudiation;
* strengthen cryptographic agility;
* enable AI-assisted cryptographic governance.

---

# 5. Engineering Cryptographic Model (ECM)

DESys adopts the **Engineering Cryptographic Model (ECM)**.

Every cryptographic implementation SHALL define:

* Protected Asset
* Security Objective
* Cryptographic Primitive
* Key Material
* Cryptographic Policy
* Lifecycle
* Evidence
* Traceability

The ECM defines the canonical cryptographic model adopted by DESys.

---

# 5.1 Engineering Key Model (EKM)

DESys adopts the **Engineering Key Model (EKM)** as a specialization of the Engineering Cryptographic Model.

Every cryptographic key SHALL possess:

* Identity
* Owner
* Purpose
* Algorithm
* Strength
* Rotation Policy
* Expiration
* Provenance
* Traceability

Keys SHALL remain governed engineering artifacts.

---

# 6. Cryptographic Security Objectives

Engineering cryptography SHALL support:

* Confidentiality
* Integrity
* Authenticity
* Non-Repudiation
* Forward Secrecy
* Cryptographic Agility

Security objectives SHALL drive cryptographic design decisions.

---

# 7. Cryptographic Building Blocks

DESys recognizes the following engineering building blocks:

* Symmetric Encryption
* Asymmetric Encryption
* Hash Functions
* Message Authentication Codes (MAC)
* Digital Signatures
* Key Derivation Functions (KDF)
* Key Exchange
* Cryptographically Secure Random Number Generation (CSPRNG)

These building blocks SHALL be selected according to engineering policies rather than implementation convenience.

---

# 8. Cryptographic Lifecycle

Every cryptographic asset progresses through a controlled lifecycle.

```text id="cryptography-lifecycle"
Defined
        ↓
Protected
        ↓
Verified
        ↓
Rotated
        ↓
Revoked
        ↓
Destroyed
```

Cryptographic material SHALL remain actively managed.

---

# 9. Cryptographic Registry (CR)

Every cryptographic implementation SHALL be registered.

Example:

```yaml id="cryptographic-registry"
asset:

  Customer Database

algorithm:

  AES-256-GCM

key:

  db-master-key

rotation:

  Quarterly

status:

  Active
```

The Cryptographic Registry preserves engineering cryptographic metadata.

---

# 10. Cryptographic Knowledge Graph (CKG)

DESys represents cryptographic relationships through the Cryptographic Knowledge Graph.

Example:

```text id="cryptography-graph"
Engineering Asset
        │ protected by
        ▼
Cryptographic Protection
        │ uses
        ▼
Key
        │ applies
        ▼
Algorithm
        │ validated through
        ▼
Evidence
```

The Cryptographic Knowledge Graph enables:

* semantic navigation;
* cryptographic reasoning;
* key dependency analysis;
* impact analysis;
* AI-assisted cryptographic governance.

---

# 11. Cryptographic Metrics

Typical engineering indicators include:

```yaml id="cryptography-metrics"
protected_assets:

  100

expired_keys:

  0

rotation_compliance:

  100

cryptographic_agility:

  100
```

Cryptographic quality SHALL remain measurable.

---

# 12. AI Cryptography Analysis

AI MAY automatically evaluate:

* deprecated algorithms;
* expired keys;
* pending key rotation;
* unprotected assets;
* policy violations;
* cryptographic agility requirements.

Recommendations SHALL remain deterministic and evidence-based.

---

# 13. Engineering Rules

Engineering Cryptography MUST:

* protect identified assets;
* use approved cryptographic primitives;
* separate cryptographic policies from implementation;
* protect key material;
* support key rotation;
* maintain complete traceability.

Engineering Cryptography MUST NOT:

* invent proprietary algorithms;
* store keys in source code;
* reuse keys outside their intended purpose;
* depend on deprecated algorithms;
* prevent cryptographic evolution.

---

# 14. Inputs

Typical inputs include:

* Engineering Assets
* Security Policies
* Protection Requirements
* Cryptographic Policies
* Compliance Requirements
* Risk Assessments

---

# 15. Outputs

Typical deliverables include:

* Cryptographic Registry
* Cryptographic Knowledge Graph
* Protected Engineering Assets
* Key Lifecycle Records
* Cryptographic Metrics
* Engineering Documentation

---

# 16. Execution Workflow

1. Identify engineering asset.
2. Define security objectives.
3. Select cryptographic policy.
4. Select cryptographic building blocks.
5. Generate or provision key material.
6. Apply cryptographic protection.
7. Register cryptographic metadata.
8. Update the Cryptographic Knowledge Graph.
9. Monitor key lifecycle and cryptographic compliance.

---

# 17. Validation

Before completion the skill verifies:

* protected assets are identified;
* cryptographic objectives are satisfied;
* approved algorithms are used;
* key lifecycle is governed;
* cryptographic evidence is preserved;
* Cryptographic Registry and Cryptographic Knowledge Graph remain synchronized.

---

# 18. Dependencies

## Parent Skill

* DSK-5000 Security Engineering Overview

## Foundation Skills

* DSK-5010 Security Principles
* DSK-5011 Threat Modeling
* DSK-5012 Authentication
* DSK-5013 Authorization

Engineering Cryptographic Protection provides the cryptographic mechanisms that support trustworthy identities, secure authorization decisions and protection of engineering assets.

---

# 19. Collaboration

The Cryptography Skill collaborates with:

* Identity Engineering
* Access Control Engineering
* Secret Management
* Infrastructure Engineering
* Security Governance
* AI Reasoning Engine

Cryptographic protection becomes the engineering foundation for protecting data, identities, communications and software artifacts throughout DESys.

---

# 20. Expected Outcomes

After execution, the Cryptography Skill should provide:

* governed cryptographic protection;
* managed cryptographic key lifecycles;
* measurable cryptographic quality;
* protected engineering assets;
* AI-assisted cryptographic governance;
* complete cryptographic traceability.

Engineering Cryptographic Protection establishes the canonical cryptography model adopted by DESys, ensuring that every engineering asset is protected through governed cryptographic policies, managed key lifecycles and traceable security mechanisms. By treating cryptography as an engineering discipline rather than a collection of algorithms, DESys enables secure evolution, cryptographic agility and long-term protection across the complete engineering lifecycle.
