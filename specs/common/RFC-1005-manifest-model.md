# RFC-1005: Common Manifest Model

RFC: RFC-1005
Title: Common Manifest Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0010 Runtime Manifest Specification
Supersedes: None
Superseded By: None
Category: Common
Layer: Cross-Cutting
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
  - ADR-0014
Related RFCs:
  - RFC-0010 Runtime Manifest Specification
Target Release: 1.0.0
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas package (Runtime, Plugin, Workflow, Vision, AI, Marketplace) MUST conform to the manifest model defined in this document.

---

## Authority

This RFC is the authoritative specification for the common event model. All subsystems MUST reference this document when defining domain-specific events.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Event | A discrete occurrence within the system that may trigger state changes or notifications. | Glossary |
| Event Bus | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| Dead Letter Queue (DLQ) | A dedicated message queue containing events that could not be delivered to their target subscribers. | Glossary |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | Glossary |

---



## Layer Boundaries

### Responsibilities

This specification IS responsible for:

- Defining the architectural contract for this domain.
- Specifying behavioral requirements that all implementations MUST satisfy.
- Establishing extension points and their contracts.

### Non-Responsibilities

This specification IS NOT responsible for:

- Implementation details (see related RFCs for implementation guidance).
- Runtime platform specifics.
- User-facing UI behavior.

### Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview — foundational runtime architecture |

### Consumers

- See related RFCs for consumer listings.

### Providers

- This specification provides domain-specific contracts and behavioral models.

### Forbidden Dependencies

- This specification MUST NOT depend on any specific programming language.
- This specification MUST NOT depend on any specific storage backend.
- This specification MUST NOT depend on any specific operating system.
## Table of Contents
1. [Introduction](#1-introduction)
2. [Manifest Model](#2-manifest-model)
3. [Manifest Schema](#3-manifest-schema)
4. [Package Types](#4-package-types)
5. [Version Negotiation](#5-version-negotiation)
6. [Performance Budgets](#6-performance-budgets)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [References](#8-references)

---


## 2 Manifest Model

Every manifest has:
- manifest_version: Schema version (always 1.0).
- package_type: One of untime, plugin, workflow, ision, i, marketplace.
- 
ame: Package name.
- ersion: Package version (SemVer).
- uthor: Package author.
- description: Package description.
- capabilities: Declared capabilities.
- permissions: Required permissions.
- dependencies: Other packages this depends on.
- esource_limits: CPU, memory, disk limits.

---


## 4 Package Types

| Type | Description | Example |
|---|---|---|
| untime | Core Runtime package | Atlas Runtime v1.0 |
| plugin | Third-party plugin | MyAutomationPlugin v2.1 |
| workflow | Workflow definition | DailyBackupWorkflow v1.0 |
| ision | Vision configuration | ScreenCaptureConfig v1.0 |
| i | AI model package | OCRModel v3.2 |
| marketplace | Marketplace listing | PluginCatalog v1.0 |

---


## 6 Performance Budgets

| Metric | Budget |
|---|---|
| Manifest parse | 50 ms |
| Schema validation | 100 ms |
| Version check | 10 ms |

---



## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 8 References
1. **RFC-0010**: Runtime Manifest Specification
2. **ADR-0012**: Contract-First Specification
3. **ADR-0014**: Configuration Schema Validation
4. **glossary.md**: Unified glossary

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

All models in this specification are defined as abstract behavioral interfaces.

---
---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Draft | 2026-07-01 | Spec Committee | Initial publication |
| 0.2.0 | Draft | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |





