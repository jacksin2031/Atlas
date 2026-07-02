# RFC-1001: Common Event Model

RFC: RFC-1001
Title: Common Event Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0005 Runtime Event Bus
Supersedes: None
Superseded By: None
Category: Common
Layer: Cross-Cutting
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.2 (Event Bus Interface)
Related RFCs:
  - RFC-0005 Runtime Event Bus
  - RFC-0007 Runtime IPC Architecture
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the event model defined in this document. This is the single source of truth for event structure across ALL subsystems (Runtime, Workflow, Vision, AI, Plugin, Marketplace).

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
3. [Non-Goals](#3-non-goals)
4. [Event Model](#4-event-model)
5. [Event Schema](#5-event-schema)
6. [Event Categories](#6-event-categories)
7. [Event Naming Convention](#7-event-naming-convention)
8. [Event Payload Structure](#8-event-payload-structure)
9. [Event Lifecycle](#9-event-lifecycle)
10. [Cross-Subsystem Event Mapping](#10-cross-subsystem-event-mapping)
11. [Performance Budgets](#11-performance-budgets)
12. [Acceptance Criteria](#12-acceptance-criteria)
13. [References](#13-references)

---


## 2 Goals

- **Universal Consistency**: All subsystems use the same event structure.
- **Cross-Subsystem Tracing**: Events flow between subsystems with preserved correlation and trace IDs.
- **Extensibility**: New event types can be added without changing the core model.
- **Tooling Support**: Standardized events enable automated tooling (logging, monitoring, debugging).

---



## 4 Event Model

Every event in Atlas follows this model:

1. **Identity**: Every event has a unique ID, name, category, and version.
2. **Origin**: Every event identifies its source subsystem and component.
3. **Context**: Every event carries correlation and trace IDs for end-to-end tracking.
4. **Payload**: The event data is structured as a typed object.
5. **Priority**: Every event has a priority level that determines delivery order.
6. **Lifecycle**: Events move through a defined lifecycle from creation to acknowledgment.

---

- Subsystem-specific extensions (each subsystem defines its own extensions).
- Implementation details.


## 7 Event Naming Convention

Event names follow the pattern: {Subsystem}.{Action}

| Pattern | Example | Description |
|---|---|---|
| {Subsystem}.Created | Runtime.Created | Entity created |
| {Subsystem}.Starting | Workflow.Starting | Lifecycle start |
| {Subsystem}.Ready | Plugin.Ready | Ready for use |
| {Subsystem}.Running | Vision.Running | Actively executing |
| {Subsystem}.Paused | Workflow.Paused | Execution paused |
| {Subsystem}.Stopping | AI.Stopping | Lifecycle stop |
| {Subsystem}.Terminated | Runtime.Terminated | Fully stopped |
| {Subsystem}.Failed | Plugin.Failed | Error occurred |
| {Subsystem}.Recovered | Workflow.Recovered | Recovery complete |
| {Subsystem}.Updated | Capability.Updated | Configuration changed |

---

{
  "error_code": "ERR_SCH_TIMEOUT",
  "error_class": "Timeout",
  "severity": "Recoverable",
  "trace_id": "uuid",
  "context": { "task_id": "task_001", "timeout_ms": 5000 }
}
`

### 8.4 Capability Events
`json
{
  "capability": "vision.capture",
  "status": "available",
  "details": { "max_fps": 60, "codecs": ["h264", "raw"] }
}
`

---



## 10 Cross-Subsystem Event Mapping

Events flow between subsystems using the common model. The mapping is:

| Source Subsystem | Target Subsystem | Event |
|---|---|---|
| Runtime → Workflow | Runtime.Running → Workflow subscribes |
| Runtime → Plugin | Plugin.Loaded → Runtime publishes |
| Workflow → Vision | Workflow.NodeStarted → Vision captures |
| Vision → Workflow | Vision.FrameCaptured → Workflow processes |
| AI → Workflow | AI.InferenceComplete → Workflow continues |
| Plugin → Runtime | Plugin.CrashDetected → Runtime recovers |

---

| RFC-0001 | Consumed | Runtime Overview |


## 12 Acceptance Criteria

### AC-1001
- **Requirement**: Every event MUST conform to the common event schema (Section 5).
- **Verification**: Validate all events against the JSON schema.
- **Expected Result**: Zero schema violations.

### AC-1002
- **Requirement**: Event names MUST follow the naming convention (Section 7).
- **Verification**: Scan all event names across subsystems.
- **Expected Result**: All names match {Subsystem}.{Action} pattern.

### AC-1003
- **Requirement**: Every event MUST carry correlationId and traceId.
- **Verification**: Audit event payloads.
- **Expected Result**: Both fields present and valid UUIDs.

### AC-1004
- **Requirement**: Events MUST not exceed performance budgets (Section 11).
- **Verification**: Benchmark event throughput.
- **Expected Result**: All metrics within budget.

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






