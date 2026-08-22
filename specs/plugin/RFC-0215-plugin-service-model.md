# RFC-0215: Plugin Service Model

RFC: RFC-0215
Title: Plugin Service Model
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
  - RFC-0203 Plugin Lifecycle
  - RFC-0205 Plugin Registry
Related RFC:
  - RFC-0216 Plugin Discovery
  - RFC-0220 Plugin IPC
  - RFC-0221 Plugin Resources
Related ADR:
  - ADR-0015 Service Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the service registration, service lifetime, service scope, singleton, transient, shared, lazy, service registry, dependency injection, service lifecycle, inter-service communication, and error handling requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Service Philosophy](#4-service-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Service Registration](#9-service-registration)
10. [Service Lifetime](#10-service-lifetime)
11. [Service Scope](#11-service-scope)
12. [Service Registry](#12-service-registry)
13. [Service Resolution](#13-service-resolution)
14. [Dependency Injection](#14-dependency-injection)
15. [Service Lifecycle](#15-service-lifecycle)
16. [Inter-Service Communication](#16-inter-service-communication)
17. [Error Handling](#17-error-handling)
18. [Performance Budgets](#18-performance-budgets)
19. [Glossary](#19-glossary)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [Cross References](#21-cross-references)
22. [References](#22-references)
23. [Revision History](#23-revision-history)
24. [Future Evolution](#24-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Service Registration**: Enable plugins to register services with the runtime.
2. **Service Lifetime**: Define clear lifetime semantics for registered services.
3. **Service Scope**: Restrict service visibility to appropriate boundaries.
4. **Service Registry**: Maintain a runtime-managed lookup table for all services.
5. **Service Resolution**: Provide name-based, interface-based, and capability-based resolution.
6. **Dependency Injection**: Offer optional DI container for service consumption.
7. **Service Lifecycle**: Manage service init, ready, running, draining, and disposal.
8. **Inter-Service Communication**: Support synchronous calls and async events.
9. **Error Handling**: Define clear error semantics for service-not-found, service-already-registered, and service-unavailable.

---


## 4 Service Philosophy

The service model follows these principles:

- Services are registered with the runtime, not with individual plugins.
- Service lifetime is managed by the runtime, not by the plugin.
- Service scope enforces visibility boundaries.
- Dependency injection is opt-in; direct resolution is always available.
- Services MUST be stateless where possible; stateful services MUST declare their scope.

---


## 6 Boundaries

- Plugins register services through the runtime API; they do not manage service instances directly.
- The runtime service registry is the sole source of truth for service discovery.
- Cross-runtime service communication is handled by the IPC layer (RFC-0220), not the service model.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin A
        PA_Svc[Service Impl A]
    end
    subgraph Plugin B
        PB_Svc[Service Impl B]
    end
    subgraph Runtime
        SR[Service Registry]
        DI[DI Container]
        LC[Lifecycle Manager]
    end
    PA_Svc -->|register| SR
    PB_Svc -->|register| SR
    SR -->|resolve| PB_Svc
    SR -->|resolve| DI
    DI -->|inject| PB_Svc
    LC -->|monitor| SR
`

---


---

### 10.5 Lazy

- Instance created on first resolution call.
- Factory function deferred until needed.
- Suitable for: heavy model loading, expensive resource initialization.

---

- Establishing the boundaries between plugin layers.


## 12 Service Registry

The runtime maintains a service registry with the following operations:

`	ypescript
interface ServiceRegistry {
  register(def: ServiceDef): ServiceRegistration;
  resolve(name: string, scope?: string): ServiceInstance;
  unregister(name: string): boolean;
  list(filter?: RegistryFilter): ServiceDef[];
  exists(name: string, scope?: string): boolean;
}
`

Requirements:
- The registry MUST be thread-safe for concurrent register/resolve operations.
- The registry MUST support filtering by interface, capability, and scope.
- The registry MUST maintain a reverse index from interface name to service list.

---

- Establishing the boundaries between plugin layers.


## 14 Dependency Injection

The DI container is OPTIONAL. When present, it provides:

`	ypescript
interface DIContainer {
  register<T>(token: string, factory: () => T): void;
  resolve<T>(token: string): T;
  resolveAll<T>(token: string): T[];
  dispose(): void;
}
`

Requirements:
- DI registration MUST map to registered services by name.
- DI resolution MUST respect service lifetime semantics.
- DI containers MUST be scoped to the requesting plugin.

---


## 16 Inter-Service Communication

Services communicate through:

1. **Direct method calls**: Synchronous calls on the service instance.
2. **Async events**: Publish/subscribe through the runtime event bus (RFC-0210).
3. **Callback registration**: Services register callbacks for notifications.

Requirements:
- Direct calls MUST respect service scope boundaries.
- Async events MUST be delivered through the IPC layer for cross-plugin communication.
- Callbacks MUST be unregistered on service disposal.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 18 Performance Budgets

- Service registration: < 10ms per service.
- Service resolution: < 1ms for cached (singleton/shared).
- Service resolution: < 10ms for transient/lazy (first call).
- Service registry query: < 5ms for filtered list.
- Total services per runtime: MAX 1000.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Acceptance Criteria

1. GIVEN a plugin registers a singleton service, WHEN resolved twice, THEN both calls return the same instance.
2. GIVEN a plugin registers a transient service, WHEN resolved twice, THEN each call returns a new instance.
3. GIVEN a plugin registers a scoped service, WHEN resolved from plugins in different workspaces, THEN each workspace gets a separate instance.
4. GIVEN a service is registered with scope plugin-local, WHEN another plugin attempts resolution, THEN resolution fails with scope-violation.
5. GIVEN a service factory throws during init, THEN the service registration fails and the registry returns SVC_NOT_FOUND.
6. GIVEN a service is in Draining state, WHEN resolution is requested, THEN the runtime returns SVC_UNAVAILABLE.
7. GIVEN two plugins register services with the same name in global-runtime scope, THEN the second registration fails with SVC_ALREADY_REG.

---



## 22 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- [Dependency Injection](https://martinfowler.com/articles/injection.html) — Martin Fowler.
- [Service Locator Pattern](https://martinfowler.com/articles/injection.html) — Martin Fowler.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 24 Future Evolution

1. Support for service versioning (multiple versions of the same service).
2. Support for service health checks and auto-restart.
3. Support for distributed service registry across runtime instances.
4. Support for service metrics and observability integration.

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

All plugin contracts are defined as abstract behavioral interfaces.

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
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |