# RFC-0227: Plugin Service Discovery

RFC: RFC-0227
Title: Plugin Service Discovery
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
  - RFC-0215 Plugin Service Model
  - RFC-0206 Plugin Capability
Related RFC:
  - RFC-0216 Plugin Discovery
  - RFC-0220 Plugin IPC
  - RFC-0226 Plugin Dependency Resolution
Related ADR:
  - ADR-0027 Service Discovery Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the service discovery protocol, capability-based lookup, interface-based resolution, name-based resolution, service filtering, service ranking, discovery cache, dynamic discovery, and discovery event emission requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Service Discovery Philosophy](#4-service-discovery-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Discovery Protocol](#9-discovery-protocol)
10. [Capability-Based Lookup](#10-capability-based-lookup)
11. [Interface-Based Resolution](#11-interface-based-resolution)
12. [Name-Based Resolution](#12-name-based-resolution)
13. [Service Filtering](#13-service-filtering)
14. [Service Ranking](#14-service-ranking)
15. [Discovery Cache](#15-discovery-cache)
16. [Dynamic Discovery](#16-dynamic-discovery)
17. [Discovery Events](#17-discovery-events)
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

1. **Capability-Based Discovery**: Find services by their capability (Vision, OCR, AI, Storage, Logger, Workflow).
2. **Interface-Based Resolution**: Resolve services by their declared interface contract.
3. **Name-Based Resolution**: Resolve services by their registered name.
4. **Service Filtering**: Filter discovered services by scope, version, or metadata.
5. **Service Ranking**: Rank discovered services by quality, latency, or priority.
6. **Discovery Cache**: Cache discovery results for performance.
7. **Dynamic Discovery**: React to services appearing and disappearing at runtime.
8. **No Direct Imports**: Plugins discover services through the runtime, NOT by importing.

---

- RFC-0323 Workflow Plugin Integration


## 4 Service Discovery Philosophy

Service discovery follows these principles:

- Plugins discover services by WHAT they do (capability), not WHO provides them.
- The runtime is the sole source of truth for service availability.
- Discovery results are cached for performance but invalidated on changes.
- Multiple services providing the same capability are ranked by quality metrics.
- Dynamic discovery enables runtime adaptation to service availability.

---


## 6 Boundaries

- Service discovery is confined to the runtime instance.
- Discovery results include only services visible to the requesting plugin's scope.
- Discovery does NOT load or activate services; it only returns available service metadata.
- Cross-runtime service discovery is handled by the IPC layer (RFC-0220).

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin A
        PA[Plugin A]
    end
    subgraph Plugin B
        PB[Plugin B - Vision Service]
    end
    subgraph Plugin C
        PC[Plugin C - OCR Service]
    end
    subgraph Plugin D
        PD[Plugin D - AI Service]
    end
    subgraph Runtime
        SD[Service Discovery]
        SR[Service Registry]
        DC[Discovery Cache]
        DE[Discovery Events]
    end
    PB -->|registers| SR
    PC -->|registers| SR
    PD -->|registers| SR
    PA -->|discover| SD
    SD --> SR
    SD --> DC
    SD --> DE
    SR --> PB
    SR --> PC
    SR --> PD
`

---


|---------------|------------------------------------------------|
| ision      | Vision processors, image analyzers             |
| ocr         | OCR engines, text extractors                   |
| i          | AI model runners, prompt adapters              |
| storage     | Storage providers, cache managers              |
| logger      | Logging services, audit loggers                |
| workflow    | Workflow engines, pipeline orchestrators       |
| scheduler   | Timer services, job queues                     |
| 
etwork     | HTTP clients, WebSocket bridges                |

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 12 Name-Based Resolution

Direct name-based resolution for known services:

`	ypescript
// Resolve by exact name
const myLogger = discovery.resolve('core-logger');
const myStorage = discovery.resolve('workspace-storage');
`

Rules:
- Name resolution is scoped: the scope parameter limits visibility.
- If the service does not exist, returns 
ull.
- If the service exists but is outside the scope, returns 
ull.
- Name resolution is the FASTEST discovery method (direct lookup).

---


---

- Establishing the boundaries between plugin layers.


## 16 Dynamic Discovery

Plugins can subscribe to discovery events:

`	ypescript
interface DiscoveryCallback {
  (event: DiscoveryEvent): void;
}

interface DiscoveryEvent {
  type: 'service_added' | 'service_removed' | 'service_updated' | 'service_rank_changed';
  service: ServiceInfo;
  timestamp: ISO8601;
}

// Subscribe to changes
const unsubscribe = discovery.subscribe((event) => {
  if (event.type === 'service_removed') {
    console.log(Service  is no longer available);
  }
});
`

Dynamic discovery rules:
- Events are emitted synchronously when a service registers or unregisters.
- Subscribers MUST process events within 100ms.
- Unsubscribed callbacks are removed immediately.
- Maximum subscribers per discovery channel: 100.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 18 Performance Budgets

- Name-based resolution: < 0.1ms (cached), < 5ms (uncached).
- Capability-based lookup: < 1ms (cached), < 10ms (uncached).
- Interface-based resolution: < 1ms (cached), < 10ms (uncached).
- Filtered search: < 5ms.
- Ranked result: < 2ms.
- Cache hit: < 0.1ms.
- Discovery event dispatch: < 0.5ms.

---

| RFC-0201 | Consumed | Plugin Overview |


## 20 Acceptance Criteria

1. GIVEN a plugin calls indByCapability('vision'), WHEN multiple plugins provide vision services, THEN ALL vision services are returned.
2. GIVEN a plugin calls esolve('core-logger'), WHEN the service exists, THEN the service info is returned.
3. GIVEN a plugin calls esolve('nonexistent-service'), WHEN the service does not exist, THEN 
ull is returned.
4. GIVEN a service registers at runtime, WHEN a subscriber is active, THEN the service_available event is emitted within 100ms.
5. GIVEN three services provide the same capability, WHEN discovery runs, THEN services are ranked by the default ranking factors.
6. GIVEN a discovery cache has a 30-second TTL, WHEN 31 seconds elapse, THEN the cache entry is invalidated.

---



## 22 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [Service Discovery Pattern](https://microservices.io/patterns/service-discovery.html) — Microservices.io.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 24 Future Evolution

1. Support for cross-runtime service discovery (distributed service registry).
2. Support for service health scoring based on runtime metrics.
3. Support for service version negotiation during discovery.

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