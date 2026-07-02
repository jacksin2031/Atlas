# RFC-0003: Runtime Service Model

RFC: RFC-0003
Title: Runtime Service Model
Status: Frozen
Authors: Atlas Team
Created: 2026-06-27
Last Updated: 2026-06-30
Requires:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Target Release: 1.0.0

---

## Normative Status

## Authority

This RFC is the authoritative specification for the domain defined in this document.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Runtime | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | Glossary |
| Service | A modular system component registered with the Service Registry. | Glossary |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | Glossary |

---
This specification is Normative. Every Atlas Runtime implementation MUST conform to the service lifecycle contracts, service registry rules, lookup patterns, and dependency injection behaviors defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

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
4. [Service Philosophy](#4-service-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Service Registry Architecture](#8-service-registry-architecture)
9. [Service Lifecycle Contracts](#9-service-lifecycle-contracts)
10. [Service State Machine](#10-service-state-machine)
11. [Service Dependency and Injection](#11-service-dependency-and-injection)
12. [Legal Service Transitions](#12-legal-service-transitions)
13. [Service Registration Sequence](#13-service-registration-sequence)
14. [Service Discovery and Lookup](#14-service-discovery-and-lookup)
15. [Service Hook System](#15-service-hook-system)
16. [Health and Metrics Contract](#16-health-and-metrics-contract)
17. [Concurrency and Reentrancy Rules](#17-concurrency-and-reentrancy-rules)
18. [Security and Isolation](#18-security-and-isolation)
19. [Performance Budgets](#19-performance-budgets)
20. [Exposed Service Registry APIs](#20-exposed-service-registry-apis)
21. [Standard Service Event Schema](#21-standard-service-event-schema)
22. [Normative Contracts](#22-normative-contracts)
23. [Compliance Checklist](#23-compliance-checklist)
24. [Acceptance Criteria](#24-acceptance-criteria)
25. [References](#25-references)
26. [Changelog](#26-changelog)
27. [Compatibility](#27-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Strict Decoupling**: Services MUST NOT import other service implementations directly.
- **Topological Bootstrapping**: The Service Registry MUST resolve service dependencies at startup and boot modules in topological order.
- **Interface Stability**: Service contracts MUST remain stable across minor releases.
- **Swappable Implementations**: Service adapters MUST be replaceable without modifying the registry or other services.

---



## 4 Service Philosophy

1. **Contract-First Interfaces**: Services declare standard contracts. Implementations are treated as swap-in adapters.
2. **Dependency Injection Over Service Locator**: Services declare their dependencies explicitly in their registration metadata. The Service Registry resolves and injects these dependencies.
3. **Minimal Public Surface**: Each service exposes only the interfaces required by its declared consumers. Internal implementation details are private.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Service Model may communicate with**:
  - Event Bus (refer to RFC-0005)
  - Config Manager
  - State Manager (refer to RFC-0006)
- **Service Model MUST NOT communicate with**:
  - External file drivers directly
  - UI controllers

---



## 8 Service ID Registry

To prevent name collisions, the Service Registry enforces unique Service Identifiers:
- SRV-LOGGER: System log exporter service.
- SRV-STORAGE: Workspace file storage driver.
- SRV-PLUGIN: Extension sandboxing and loading manager.
- SRV-VISION: Video frame capture pipeline.
- SRV-WORKFLOW: Directed acyclic graph executor service.
- SRV-SCHEDULER: Task priority dispatcher coordinator.
- SRV-AI: Inference prompt routing manager.
- SRV-METRICS: System diagnostic time-series collector.


---

    Reg --> DG[Dependency Graph]
    Reg --> RDM[Reverse Dependency Map]
    SM --> SE1[Service Entry 1]
    SM --> SE2[Service Entry 2]
    SM --> SE3[Service Entry N]
    DG --> TS[Topological Sort]
    TS --> ORD[Initialization Order]
`

---


### 10.1 Lifecycle Phases

| Phase | Method Invoked | Timing |
|---|---|---|
| Discovery | getDependencies() | During boot, before initialization |
| Initialization | initialize() | During boot, in topological order |
| Active | healthCheck() | Periodic, at health_check_interval_ms |
| Degraded | healthCheck() returns false | After first failed health check |
| Disabled | deinitialize() | After max retry count exceeded |
| Shutdown | deinitialize() | During shutdown sequence |

---

---

- Implementation details (see related RFCs).
- Cross-cutting concerns handled by other subsystems.


## 13 Legal Service Transitions

| From State | To State | Trigger |
|---|---|---|
| Inactive | Initializing | register() |
| Initializing | Active | initialize() succeeds |
| Initializing | Degraded | initialize() fails after retries |
| Active | Degraded | healthCheck() fails |
| Degraded | Active | healthCheck() succeeds |
| Degraded | Disabled | Max retries exceeded |
| Active | Disabled | Explicit deinitialize |
| Disabled | [*] | Terminal state |

---

    else Graph has Cycle
        Reg-->>Host: CircularDependencyException
    end
`

---

- Defining the architecture and requirements for this subsystem.


## 16 Service Hook System

### 16.1 Hook Types

- **PreInitialize**: Invoked before initialize() is called.
- **PostInitialize**: Invoked after initialize() succeeds.
- **PreDeinitialize**: Invoked before deinitialize() is called.
- **PostDeinitialize**: Invoked after deinitialize() completes.
- **OnHealthCheckFailure**: Invoked when a health check fails.

### 16.2 Hook Execution

Hooks execute sequentially in registration order. A hook that fails with a Fatal failure policy prevents the lifecycle transition. A hook that fails with a Warning policy logs the error and continues.

---



## 18 Concurrency and Reentrancy Rules

### 18.1 Single-Threaded Service Execution

Each service initialize(), healthCheck(), and deinitialize() methods MUST be thread-safe. The Service Registry guarantees that these methods are never invoked concurrently on the same service instance.

### 18.2 Reentrancy

Services MUST be reentrant with respect to their public interfaces. A service MAY be called recursively through the Event Bus (refer to RFC-0005) or IPC (refer to RFC-0007). Services that are not reentrant MUST declare this in their contract.

### 18.3 Deadlock Prevention

Services MUST NOT acquire locks in an order that could cause deadlock. The Service Registry enforces a global lock ordering based on service dependency order.

---

- Cross-cutting concerns handled by other subsystems.


## 20 Performance Budgets

| Metric | Target Budget Limit | Measurement Context |
|---|---|---|
| Dependency Resolution | 100 ms | During boot, resolving full dependency graph |
| Service Lookup | 0.05 ms | Retrieving service reference from registry |
| Health Check Invocation | 10 ms | Single healthCheck() call |
| Hook Execution | 500 ms per hook | Lifecycle hook callback |
| Registration | 50 ms | Full registration including validation |

---


## 22 Standard Service Event Schema

`json
{
  "": "https://atlas.dev/schemas/service-event.schema.json",
  "type": "object",
  "required": ["eventId", "serviceName", "eventType", "timestamp"],
  "properties": {
    "eventId": { "type": "string", "format": "uuid" },
    "serviceName": { "type": "string" },
    "eventType": { "type": "string", "enum": ["registered", "initialized", "degraded", "disabled", "unregistered"] },
    "timestamp": { "type": "integer" },
    "previousState": { "type": "string" },
    "newState": { "type": "string" },
    "error": { "type": "object", "nullable": true }
  }
}
`

---

- Downstream subsystem RFCs reference this specification.


## 24 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| SVC-01 | All services implement ServiceContract | Interface compliance test |
| SVC-02 | No circular dependencies | Graph cycle detection test |
| SVC-03 | Topological initialization order | Initialization trace test |
| SVC-04 | Health checks execute at correct interval | Timing verification test |
| SVC-05 | Lookup completes within 0.05 ms | Performance benchmark |
| SVC-06 | Hooks execute in registration order | Hook execution trace test |

---

- **Expected Result**: healthCheck() is called exactly once every 5000 ms (plus or minus 100 ms tolerance).

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 27 Changelog
- 1.0.0: Initial release. Defined service IDs and registrations.
- 1.1.0: Expanded all placeholder sections with full architecture, state machine, dependency injection, and compliance checklist.

---


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
| 1.0.0 | Frozen | 2026-06-30 | Runtime Architecture Board | Initial publication |
| 1.1.0 | Frozen | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






