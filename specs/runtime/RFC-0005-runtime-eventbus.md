# RFC-0005: Runtime Event Bus

RFC: RFC-0005
Title: Runtime Event Bus
Status: Frozen
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-27
Last Updated: 2026-06-30
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
Required By:
  - RFC-0004 Runtime Scheduler
  - RFC-0006 Runtime State Management
  - RFC-0007 Runtime IPC Architecture
  - RFC-0008 Runtime Plugin Host
  - RFC-0009 Runtime Resource Management
  - RFC-0010 Runtime Manifest Specification
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.2 (Event Bus Interface)
Related RFCs:
  - RFC-0001 Runtime Overview
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the event structures, channel configurations, queue prioritization systems, and delivery guarantees defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

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
4. [Event Philosophy](#4-event-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Event Bus Architecture](#8-event-bus-architecture)
9. [Standard Event Schema](#9-standard-event-schema)
10. [Queue Management and Priorities](#10-queue-management-and-priorities)
11. [Delivery Guarantees and Ordering](#11-delivery-guarantees-and-ordering)
12. [Event Propagation Diagram](#12-event-propagation-diagram)
13. [Request-Response Pattern](#13-request-response-pattern)
14. [Backpressure and Flow Control](#14-backpressure-and-flow-control)
15. [Dead Letter Queue Routing](#15-dead-letter-queue-routing)
16. [Security and Access Control](#16-security-and-access-control)
17. [Performance Budgets](#17-performance-budgets)
18. [Exposed Event Bus APIs](#18-exposed-event-bus-apis)
19. [Normative Contracts](#19-normative-contracts)
20. [Compliance Checklist](#20-compliance-checklist)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [References](#22-references)
23. [Changelog](#23-changelog)
24. [Compatibility](#24-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Loose Coupling**: Services MUST communicate via asynchronous events instead of direct invocations.
- **Payload Validation**: The Event Bus MUST validate all published events against their registered schemas before propagation.
- **Priority-Based Dispatching**: Critical events (such as panic signals or user interrupts) MUST override lower-priority background tasks.
- **Traceability**: Every event MUST carry Correlation IDs and Trace IDs to enable end-to-end trace auditing.
- **Flow Control**: The system MUST deploy backpressure mechanisms to prevent slow subscribers from blocking the bus.

---



## 4 Event Philosophy

1. **Events are Immutable**: Once published, event payloads MUST NOT be mutated by subscribers.
2. **Wildcard Routing**: Subscriptions support namespace pattern matching (e.g., workflow.*).
3. **Defense-in-Depth**: Unauthorized components MUST NOT intercept or publish restricted system events.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Event Bus may communicate with**:
  - Service Registry (refer to RFC-0003)
  - Scheduler (refer to RFC-0004)
  - Config Manager
- **Event Bus MUST NOT communicate with**:
  - Local database caches directly
  - UI client libraries

---



## 8 Event Bus Architecture

The Event Bus consists of three core components: the Channel Router, the Priority Queue Manager, and the Subscriber Registry.

`mermaid
graph TD
    Pub[Publishers] --> Router[Channel Router]
    Router --> PQ1[Priority Queue 1: Critical]
    Router --> PQ2[Priority Queue 2: High]
    Router --> PQ3[Priority Queue 3: Normal]
    Router --> PQ4[Priority Queue 4: Background]
    PQ1 --> Dispatcher[Event Dispatcher]
    PQ2 --> Dispatcher
    PQ3 --> Dispatcher
    PQ4 --> Dispatcher
    Dispatcher --> Sub[Subscriber Registry]
    Sub --> S1[Service A Handler]
    Sub --> S2[Service B Handler]
    Sub --> S3[Service N Handler]
    Router --> DLQ[Dead Letter Queue]
`

### 8.1 Channel Router

The Channel Router matches published events to subscribed channels using pattern matching. Wildcard patterns are supported using standard glob syntax:
- * matches a single path segment.
- ** matches zero or more path segments.

### 8.2 Priority Queue Manager

Events are enqueued into priority queues based on their priority level. The Priority Queue Manager ensures that higher-priority events are dispatched before lower-priority events.

### 8.3 Subscriber Registry

The Subscriber Registry maintains the mapping from channels to subscribers. It supports:
- **Direct subscriptions**: Exact channel name match.
- **Pattern subscriptions**: Glob pattern match.
- **Topic subscriptions**: Namespace-level match.

---




## 11 Delivery Guarantees and Ordering

### 11.1 Delivery Guarantees

The Event Bus provides the following delivery guarantees:

| Guarantee Level | Description | Use Case |
|---|---|---|
| At-Most-Once | Event is delivered zero or one time | Metrics, telemetry |
| At-Least-Once | Event is delivered one or more times | State changes, workflow updates |
| Exactly-Once | Event is delivered exactly one time | Transaction commits |

### 11.2 Ordering Guarantees

Events published to the same channel by the same source are delivered in publication order. Events from different sources on the same channel are ordered by timestamp, with ties broken by trace ID.

---

    end
`

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 14 Backpressure and Flow Control

### 14.1 Backpressure Mechanisms

When subscribers are slow to process events, the Event Bus applies backpressure:

1. **Queue Watermark**: When the subscriber queue reaches 80% capacity, a BackpressureWarning event is published.
2. **Queue Saturation**: When the queue reaches 100% capacity, new events are routed to the Dead Letter Queue.
3. **Subscriber Suspension**: If a subscriber consistently fails to keep up, the Event Bus may temporarily suspend event delivery to that subscriber.

### 14.2 Flow Control Signals

Subscribers MAY send flow control signals to the Event Bus:
- **Ack**: Event processed successfully.
- **Nack**: Event processing failed; request retry.
- **Throttle**: Subscriber is overloaded; reduce event rate.

---

This specification IS NOT responsible for:
- Implementation details (see related RFCs).
- Cross-cutting concerns handled by other subsystems.


## 16 Security and Access Control

### 16.1 Publication Permissions

Only authorized publishers MAY publish to restricted channels. The Event Bus validates the publisher token against the channel permissions before accepting the event.

### 16.2 Subscription Permissions

Only authorized subscribers MAY subscribe to restricted channels. The Event Bus validates the subscriber token against the channel permissions before registering the subscription.

### 16.3 Event Encryption

Events containing sensitive data MAY be encrypted at rest in the DLQ. Encryption keys are managed by the Security Manager.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 18 Exposed Event Bus APIs

`
interface EventBus {
  // Publish an event to the specified channel.
  void publish(Channel channel, Event event);

  // Subscribe to a channel pattern. Returns SubscriptionHandle.
  SubscriptionHandle subscribe(string pattern, EventHandler handler);

  // Unsubscribe from a channel.
  void unsubscribe(SubscriptionHandle handle);

  // Get statistics about the event bus.
  EventBusStats getStats();
}

interface EventHandler {
  void onEvent(Event event);
}
`

---


## 20 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| EB-01 | Events conform to standard schema | Schema validation test |
| EB-02 | Priority ordering is enforced | Priority ordering test |
| EB-03 | DLQ receives undeliverable events | DLQ routing test |
| EB-04 | Backpressure is applied at watermark | Queue saturation test |
| EB-05 | Wildcard routing works correctly | Pattern matching test |
| EB-06 | Request-response correlation works | Correlation ID test |

---

- **Expected Result**: Backpressure warning event is published.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 23 Changelog
- 1.0.0: Initial release. Defined Event Bus channels and schemas.
- 1.1.0: Expanded all placeholder sections with full architecture, delivery guarantees, and compliance checklist.

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






