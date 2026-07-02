# RFC-0217: Plugin Packaging

RFC: RFC-0217
Title: Plugin Packaging
Status: Proposed
Version: 1.0.0
Category: Plugin Architecture
Layer: Distribution
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0202 Plugin Manifest
  - RFC-0207 Plugin Security
Related RFC:
  - RFC-0213 Plugin Marketplace
  - RFC-0216 Plugin Discovery
  - RFC-0218 Plugin Compatibility
Related ADR:
  - ADR-0017 Packaging Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the package format, package structure, digital signature, checksum verification, schema bundle, asset manifest, translation bundle, license embedding, and package versioning requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Packaging Philosophy](#4-packaging-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Package Format](#9-package-format)
10. [Package Structure](#10-package-structure)
11. [Digital Signature](#11-digital-signature)
12. [Checksum Verification](#12-checksum-verification)
13. [Schema Bundle](#13-schema-bundle)
14. [Asset Manifest](#14-asset-manifest)
15. [Translation Bundle](#15-translation-bundle)
16. [License Embedding](#16-license-embedding)
17. [Package Versioning](#17-package-versioning)
18. [Validation Pipeline](#18-validation-pipeline)
19. [Performance Budgets](#19-performance-budgets)
20. [Glossary](#20-glossary)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Cross References](#22-cross-references)
23. [References](#23-references)
24. [Revision History](#24-revision-history)
25. [Future Evolution](#25-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Standard Format**: Define a single, universal package format.
2. **Self-Contained**: Every plugin MUST be fully described within its package.
3. **Integrity**: Digital signatures and checksums guarantee authenticity.
4. **Schema**: Optional embedded JSON Schema for configuration validation.
5. **Assets**: Bundled resources (icons, fonts, models, templates).
6. **i18n**: Embedded translation files with locale codes.
7. **License**: Embedded license text or SPDX identifier.
8. **Versioning**: Packages follow SemVer 2.0.

---

- RFC-0323 Workflow Plugin Integration


## 4 Packaging Philosophy

Packaging follows these principles:

- Every package MUST be self-describing via its manifest.
- Integrity is non-negotiable: signatures and checksums are REQUIRED.
- Optional metadata (schema, assets, translations) enhances usability.
- The package format MUST be extractable with standard ZIP tools.

---


## 6 Boundaries

- Packaging is concerned with the DISTRIBUTION format, not the runtime loading format.
- The package MAY be extracted to disk or loaded from memory.
- Signature verification happens BEFORE package extraction.

---



## 8 Architecture

`mermaid
graph LR
    SRC[Plugin Source] --> PKG[Package Builder]
    PKG --> ZIP[ZIP Archive]
    ZIP --> SIG[Sign with RSA/ECDSA]
    SIG --> CHK[Compute SHA-256]
    CHK --> PKG_OUT[atlas-plugin Package]
    PKG_OUT --> VERIFY[Signature + Checksum Verify]
    VERIFY --> EXTRACT[Extract to Disk/Memory]
    EXTRACT --> LOAD[Plugin Load]
`

---



## 10 Package Structure

`
my-plugin.atlas-plugin/
├── manifest.json              [REQUIRED] Plugin manifest
├── signature.sig              [REQUIRED] Digital signature
├── checksum.sha256            [REQUIRED] SHA-256 integrity hash
├── schema/                    [OPTIONAL] JSON Schema for config
│   └── config-v1.json
├── resources/                 [OPTIONAL] Bundled resources
│   ├── icons/
│   │   ├── icon-16.png
│   │   ├── icon-32.png
│   │   ├── icon-64.png
│   │   └── icon.svg
│   ├── translations/
│   │   ├── en.json
│   │   ├── ja.json
│   │   └── zh-TW.json
│   └── fonts/
│       └── custom-font.woff2
├── assets/                    [OPTIONAL] Bundled assets
│   ├── models/
│   │   └── classifier model file
│   ├── ocr/
│   │   └── lang-pack-jpn/
│   └── templates/
│       └── boilerplate.ts
├── bin/                       [REQUIRED] Compiled code
│   └── main.js
├── tests/                     [OPTIONAL] Test suite
└── license.txt                [REQUIRED if license != SPDX]
`

---


## 12 Checksum Verification

The checksum file (checksum.sha256) contains:

`
<sha256_hash>  manifest.json bin/main.js resources/...
`

Requirements:
- The checksum is computed over all files in the package.
- The checksum MUST be verified after extraction (or during streaming extract).
- Checksum mismatch MUST abort the load process.

---

- Workflow execution (covered by RFC-0301).


## 14 Asset Manifest

The manifest MUST include an ssets section listing all bundled assets with hashes:

`json
{
  "assets": {
    "models": [
      { "path": "models/classifier model file", "hash": "sha256:abc123..." }
    ],
    "ocr": [
      { "path": "ocr/lang-pack-jpn/", "hash": "sha256:def456..." }
    ],
    "templates": [
      { "path": "templates/boilerplate.ts", "hash": "sha256:ghi789..." }
    ]
  }
}
`

Requirements:
- All asset hashes MUST be SHA-256.
- Missing assets MUST cause plugin load to fail with LOAD_002.
- Assets are OPTIONAL; plugins without assets have an empty ssets object.

---

- Workflow execution (covered by RFC-0301).


## 16 License Embedding

License is declared in the manifest:

`json
{
  "license": "MIT"        // SPDX identifier, OR
  "license": "LICENSE"    // Path to license.txt in package
}
`

Requirements:
- If SPDX identifier is used, the license text is NOT required in the package.
- If a path is used, the file MUST exist in the package root.
- Unknown license identifiers MUST cause manifest validation failure.

---



## 18 Validation Pipeline

`mermaid
sequenceDiagram
    participant P as Package
    participant V as Validator
    participant S as Signature Checker
    participant C as Checksum Checker
    participant M as Manifest Parser

    P->>V: Load .atlas-plugin
    V->>S: Verify signature.sig
    S-->>V: Valid / Invalid
    alt Invalid
        V-->>P: Abort (LOAD_002)
    end
    V->>C: Compute checksum
    C-->>V: Match / Mismatch
    alt Mismatch
        V-->>P: Abort (LOAD_003)
    end
    V->>M: Parse manifest.json
    M-->>V: Schema Valid / Invalid
    alt Invalid
        V-->>P: Abort (MANIFEST_005)
    end
    V-->>P: Package Valid
`

---


## 20 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Package           | Self-contained .atlas-plugin distribution unit.    |
| Signature         | Cryptographic proof of package authenticity.         |
| Checksum          | SHA-256 hash of package contents for integrity.      |
| Schema Bundle     | Embedded JSON Schema for configuration validation.   |
| Asset Manifest    | List of bundled assets with integrity hashes.        |

---

| RFC-0201 | Consumed | Plugin Overview |


## 22 Cross References

- RFC-0201 Plugin Overview
- RFC-0202 Plugin Manifest
- RFC-0207 Plugin Security
- RFC-0213 Plugin Marketplace
- RFC-0216 Plugin Discovery

---


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

---

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## 24 Revision History

| Date       | Version | Author                    | Change                           |
|------------|---------|---------------------------|----------------------------------|
| 2026-07-01 | 1.0.0   | Atlas Specification Committee | Initial proposal               |

---



---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All contracts in this specification are defined as abstract behavioral interfaces.

---



