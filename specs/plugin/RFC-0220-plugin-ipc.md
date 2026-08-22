# RFC-0220: Plugin IPC

RFC: RFC-0220
Title: Plugin IPC
Status: Proposed
Version: 1.0.0
Category: Plugin Architecture
Layer: Communication
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0209 Plugin API
  - RFC-0210 Plugin Events
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0219 Plugin Permission Model
  - RFC-0221 Plugin Resources
Related ADR:
  - ADR-0020 IPC Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the IPC channel architecture, direct import prohibition, IPC types (request/reply, publish/subscribe, stream, RPC), message format, service discovery via IPC, rate limiting, timeout policy, error propagation, security, connection lifecycle, circuit breaker, and message queue requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [IPC Philosophy](#4-ipc-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [IPC Channel Architecture](#9-ipc-channel-architecture)
10. [Direct Import Prohibition](#10-direct-import-prohibition)
11. [IPC Types](#11-ipc-types)
12. [Message Format](#12-message-format)
13. [Service Discovery via IPC](#13-service-discovery-via-ipc)
14. [Rate Limiting](#14-rate-limiting)
15. [Timeout Policy](#15-timeout-policy)
16. [Error Propagation](#16-error-propagation)
17. [Security](#17-security)
18. [Connection Lifecycle](#18-connection-lifecycle)
19. [Circuit Breaker](#19-circuit-breaker)
20. [Message Queue](#20-message-queue)
21. [Performance Budgets](#21-performance-budgets)
22. [Glossary](#22-glossary)
23. [Acceptance Criteria](#23-acceptance-criteria)
24. [Cross References](#24-cross-references)
25. [References](#25-references)
26. [Revision History](#26-revision-history)
27. [Future Evolution](#27-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Centralized Routing**: All plugin-to-plugin communication goes through the runtime IPC router.
2. **Direct Import Prohibition**: Plugins MUST NOT directly import or call other plugins.
3. **Multiple IPC Types**: Support request/reply, pub/sub, stream, and RPC patterns.
4. **Message Format**: Standardized JSON-RPC 2.0 message format.
5. **Rate Limiting**: Prevent IPC flood attacks.
6. **Timeout Policy**: Configurable per-call timeouts.
7. **Error Propagation**: IPC errors mapped to plugin error codes.
8. **Security**: Authenticated channels with optional encrypted payloads.
9. **Circuit Breaker**: Auto-fail on repeated IPC failures.
10. **Message Queue**: Buffered delivery for offline plugins.

---

- RFC-0323 Workflow Plugin Integration


## 4 IPC Philosophy

IPC follows these principles:

- The runtime is the sole communication mediator between plugins.
- Direct plugin-to-plugin imports are FORBIDDEN.
- All communication is asynchronous at the protocol level.
- Failures are handled gracefully through circuit breakers and retries.
- Security is enforced at the channel level.

---


## 6 Boundaries

- IPC is confined to the runtime instance. Cross-runtime communication uses the network layer.
- IPC channels are authenticated; unauthenticated channels are rejected.
- Message payloads are validated against declared schemas.
- The IPC layer does NOT modify message content (passthrough).

---

| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
graph TB
    subgraph Plugin A
        PA[Plugin A]
    end
    subgraph Plugin B
        PB[Plugin B]
    end
    subgraph Plugin C
        PC[Plugin C]
    end
    subgraph Runtime IPC
        IR[IPC Router]
        EB[Event Bus]
        MQ[Message Queue]
        CB[Circuit Breaker]
        RL[Rate Limiter]
    end
    PA -->|request/reply| IR
    PB -->|request/reply| IR
    PC -->|subscribe| EB
    PA -->|publish| EB
    IR --> RL
    RL --> CB
    CB --> MQ
    IR --> PB
`

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Direct Import Prohibition

The following patterns are FORBIDDEN in plugin code:

`	ypescript
// FORBIDDEN: Direct plugin import
import { PluginBService } from '../plugins/plugin-b';

// FORBIDDEN: Direct function call to another plugin
PluginB.someMethod();

// FORBIDDEN: Direct class instantiation from another plugin
const svc = new PluginB.SomeClass();
`

The following patterns are REQUIRED:

`	ypescript
// REQUIRED: Via runtime IPC
const result = await runtime.ipc.invoke('plugin-b', 'someMethod', params);

// REQUIRED: Via service registry
const svc = await runtime.services.resolve('plugin-b-service');

// REQUIRED: Via event subscription
runtime.events.subscribe('plugin-b.event', handler);
`

---

`

### 11.3 Stream

Bidirectional continuous data transfer:

`	ypescript
const stream = await runtime.ipc.openStream({
  target: 'plugin-b',
  type: 'data-transfer'
});
stream.send(chunk);
stream.on('data', (chunk) => { /* ... */ });
stream.close();
`

### 11.4 RPC

Typed remote procedure call with interface contracts:

`	ypescript
interface IRemoteService {
  compute(a: number, b: number): Promise<number>;
  getStatus(): Promise<Status>;
}

const proxy = runtime.ipc.createProxy<IRemoteService>('plugin-b', 'remote-service');
const result = await proxy.compute(1, 2);
`

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 14 Rate Limiting

Rate limits are enforced per-caller:

| Level        | Default Limit          | Max Limit             |
|--------------|------------------------|-----------------------|
| low          | 100 requests/sec       | 1000 requests/sec     |
| normal       | 500 requests/sec       | 5000 requests/sec     |
| elevated     | 2000 requests/sec      | 20000 requests/sec    |
| privileged   | Unlimited              | Configurable          |

Violations:
- Exceeding the limit queues the message (up to 1000 messages).
- Queue overflow rejects with IPC_003 (Rate Limited).

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 16 Error Propagation

IPC errors are mapped to plugin error codes:

| IPC Error          | Plugin Error Code | Description                     |
|--------------------|-------------------|---------------------------------|
| ChannelNotFound    | IPC_001           | IPC channel does not exist      |
| MessageTimeout     | IPC_005           | Request exceeded timeout        |
| RateLimited        | IPC_004           | IPC rate limit exceeded         |
| CircuitBreakerOpen | IPC_006           | Target service circuit breaker open |
| SerializationError | IPC_005           | Message serialization failed    |

---


## 18 Connection Lifecycle

`mermaid
stateDiagram-v2
    [*] --> Connecting
    Connecting --> Connected: handshake succeeds
    Connecting --> Error: handshake fails
    Connected --> Exchange: send/receive messages
    Exchange --> Connected: message acknowledged
    Exchange --> Draining: close requested
    Draining --> Disconnected: all messages flushed
    Error --> [*]
    Disconnected --> [*]
`

---

- Workflow execution (covered by RFC-0301).


## 20 Message Queue

For offline or slow plugins:

- Messages are buffered when the target plugin is unavailable.
- Maximum queue size: 10,000 messages per channel.
- Queue eviction: FIFO when full (oldest dropped with warning).
- Queue persistence: configurable (disk-backed for critical messages).
- Delivery guarantee: at-least-once for guaranteed messages.

---



## 22 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| IPC Router        | Central message routing component in the runtime.    |
| Circuit Breaker   | Pattern preventing cascading failures.               |
| Rate Limiter      | Component enforcing per-caller request limits.       |
| Message Queue     | Buffer for messages when target is unavailable.      |

---

| RFC-0201 | Consumed | Plugin Overview |


## 24 Cross References

- RFC-0201 Plugin Overview
- RFC-0209 Plugin API
- RFC-0210 Plugin Events
- RFC-0215 Plugin Service Model
- RFC-0219 Plugin Permission Model

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

## 26 Revision History

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



