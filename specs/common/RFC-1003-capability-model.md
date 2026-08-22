# RFC-1003: Common Capability Model

RFC: RFC-1003
Title: Common Capability Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0012 Runtime Capability Registry
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
  - RFC-0012 Runtime Capability Registry
  - RFC-0010 Runtime Manifest Specification
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the capability model defined in this document.

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
2. [Goals](#2-goals)
3. [Capability Model](#3-capability-model)
4. [Capability Registry](#4-capability-registry)
5. [Capability Entitlements](#5-capability-entitlements)
6. [Capability Query Interface](#6-capability-query-interface)
7. [Performance Budgets](#7-performance-budgets)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [References](#9-references)

---


## 2 Goals

- **Universal Discovery**: All subsystems discover capabilities through a single interface.
- **Entitlement Verification**: Subsystems verify permissions before using capabilities.
- **Fallback Handling**: Missing capabilities trigger configured fallbacks.

---



## 4 Capability Registry

Capabilities are registered in the Capability Registry (RFC-0012). The registry is populated at boot from:
1. Runtime manifest declarations (RFC-0010).
2. Hardware probes (GPU detection, memory check).
3. Software probes (OCR engine availability, AI model cache).

---



## 6 Capability Query Interface

`
interface CapabilityQuery {
  // Check if a capability is available.
  CapabilityStatus getCapability(string capabilityId);

  // List all available capabilities.
  CapabilityList listCapabilities();

  // Verify entitlement for a capability.
  bool checkEntitlement(string capabilityId, string callerId);

  // Subscribe to capability changes.
  Subscription subscribeToChanges(CapabilityEventHandler handler);
}
`

---



## 8 Acceptance Criteria

### AC-1008
- **Requirement**: All capabilities MUST be queryable through the CapabilityQuery interface.
- **Verification**: Query all registered capabilities.
- **Expected Result**: All return valid CapabilityStatus.

### AC-1009
- **Requirement**: Entitlement checks MUST enforce declared permissions.
- **Verification**: Attempt to use a capability without entitlement.
- **Expected Result**: PermissionDenied exception.

---


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

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

---

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Draft | 2026-07-01 | Spec Committee | Initial publication |
| 0.2.0 | Draft | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






