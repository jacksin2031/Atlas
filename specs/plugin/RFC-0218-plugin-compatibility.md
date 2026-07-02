# RFC-0218: Plugin Compatibility

RFC: RFC-0218
Title: Plugin Compatibility
Status: Proposed
Version: 1.0.0
Category: Plugin Architecture
Layer: Runtime
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0212 Plugin Versioning
  - RFC-0206 Plugin Capability
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0216 Plugin Discovery
  - RFC-0217 Plugin Packaging
Related ADR:
  - ADR-0018 Compatibility Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the compatibility dimensions, compatibility matrix, version negotiation, feature gates, breaking change policy, backward compatibility, forward compatibility, deprecation policy, compatibility check, and reject reasons requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Compatibility Philosophy](#4-compatibility-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Compatibility Dimensions](#9-compatibility-dimensions)
10. [Compatibility Matrix](#10-compatibility-matrix)
11. [Version Negotiation](#11-version-negotiation)
12. [Feature Gates](#12-feature-gates)
13. [Breaking Change Policy](#13-breaking-change-policy)
14. [Backward Compatibility](#14-backward-compatibility)
15. [Forward Compatibility](#15-forward-compatibility)
16. [Deprecation Policy](#16-deprecation-policy)
17. [Compatibility Check](#17-compatibility-check)
18. [Reject Reasons](#18-reject-reasons)
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

1. **Multi-Dimensional Compatibility**: Define compatibility across runtime, workflow, schema, API, capability, and extension points.
2. **Version Negotiation**: Handshake protocol during plugin load.
3. **Feature Gates**: Opt-in unstable features with explicit declaration.
4. **Breaking Change Policy**: Clear rules for when major version bumps are required.
5. **Deprecation Timeline**: Minimum deprecation notice period.
6. **Automated Checks**: Runtime MUST verify compatibility before loading.

---

- RFC-0323 Workflow Plugin Integration


## 4 Compatibility Philosophy

Compatibility follows these principles:

- Major version changes MAY introduce breaking changes.
- Minor version changes MUST be backward compatible.
- Patch version changes MUST NOT change behavior.
- Feature gates allow opt-in unstable features without breaking stable APIs.
- Deprecation requires a minimum notice period before removal.

---


## 6 Boundaries

- Compatibility checking happens BEFORE plugin loading.
- Runtime compatibility is checked against the runtime version.
- Plugin-to-plugin compatibility is checked through the service registry.
- Workflow schema compatibility is checked against the workflow engine version.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin
        PM[Plugin Manifest]
        FG[Feature Gates]
    end
    subgraph Runtime
        RV[Runtime Version]
        WF[Workflow Schema]
        SC[Schema Version]
        API[API Version]
        CP[Capability Registry]
        EP[Extension Point Registry]
    end
    PM --> CC[Compatibility Checker]
    FG --> CC
    RV --> CC
    WF --> CC
    SC --> CC
    API --> CC
    CP --> CC
    EP --> CC
    CC -->|Pass| LOAD[Load Plugin]
    CC -->|Fail| REJ[Reject with Error]
`

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Compatibility Matrix

The compatibility matrix declares the supported ranges:

`json
{
  "compatibility": {
    "runtime": { "min": "2.0.0", "max": "3.0.0" },
    "workflow": { "min": "1.0.0", "max": "2.0.0" },
    "schema": { "min": "1.0.0", "max": "2.0.0" },
    "api": { "min": "1.5.0", "max": "2.0.0" },
    "capabilities": ["read:workspace", "write:workspace", "ai:prompt"]
  }
}
`

Requirements:
- untime.min: Minimum runtime version required.
- untime.max: Maximum runtime version (exclusive upper bound).
- workflow.min/max: Workflow schema version range.
- schema.min/max: Data format schema version range.
- pi.min/max: Plugin API version range.
- capabilities: List of required capabilities.

---

- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 12 Feature Gates

Feature gates allow opt-in of unstable features:

`json
{
  "feature_gates": [
    { "name": "ipc-streaming", "required": false, "min_runtime": "2.1.0" },
    { "name": "ai-model-v3", "required": true, "min_runtime": "2.3.0" }
  ]
}
`

Rules:
- equired: false → Plugin works without the feature (graceful degradation).
- equired: true → Plugin fails to load if the feature gate is disabled.
- min_runtime → Minimum runtime version that supports this feature gate.

---



## 14 Backward Compatibility

- Minor and patch versions MUST be backward compatible.
- A plugin built against version N.x MUST work on runtime N.y where y >= x.
- The runtime MUST NOT remove or change existing public APIs in minor/patch releases.
- Deprecated APIs MUST continue to function for a minimum of 2 minor versions.

---


## 16 Deprecation Policy

1. A feature is marked deprecated in the manifest or changelog.
2. The feature MUST continue to function for a minimum of 2 minor versions.
3. During deprecation, the runtime logs a warning when the deprecated feature is used.
4. After 2 minor versions, the feature MAY be removed in the next major version.
5. Removal MUST be documented in the changelog with a migration guide.

---

- Workflow execution (covered by RFC-0301).


## 18 Reject Reasons

| Reject Reason          | Code      | Description                                      |
|------------------------|-----------|--------------------------------------------------|
| runtime-mismatch       | COMPAT_001| Runtime version outside declared range           |
| api-incompatible       | COMPAT_002| Plugin API version mismatch                      |
| capability-missing     | COMPAT_003| Required capability not available                |
| feature-gate-conflict  | COMPAT_004| Required feature gate is disabled                |
| dependency-conflict    | COMPAT_005| Plugin dependency version conflict               |

---


## 20 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Compatibility     | Ability of plugin and runtime to work together.      |
| Feature Gate      | Opt-in unstable feature flag.                        |
| Breaking Change   | Change that requires a major version bump.           |
| Backward Compat   | New version works with old consumers.                |
| Forward Compat    | Old version works with new producers (best effort).  |

---

| RFC-0201 | Consumed | Plugin Overview |


## 22 Cross References

- RFC-0201 Plugin Overview
- RFC-0206 Plugin Capability
- RFC-0212 Plugin Versioning
- RFC-0215 Plugin Service Model
- RFC-0224 Plugin Testing

---

- RFC-0323 Workflow Plugin Integration


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




