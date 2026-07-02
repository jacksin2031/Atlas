# RFC-IPC-CAP: IPC Capability Registry

RFC: IPC-CAP
Title: IPC Capability Registry
Status: Accepted
Version: 1.0.0
Category: IPC
Layer: Extension
Normative: YES
Authors: Atlas Team
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0101 IPC Overview
  - RFC-0107 IPC Security
  - RFC-0108 IPC Reliability
  - RFC-0110 IPC Observability
  - RFC-0112 IPC Extension
Required By:
  - RFC-0108 IPC Reliability
  - RFC-0110 IPC Observability
  - RFC-0112 IPC Extension
Supersedes: None
Superseded By: None
Constitution References:
  - Section 3.5 IPC Isolation
Audience: Plugin Developers, Platform Architects, Systems Engineers
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

This specification is Normative. Every Atlas Runtime implementation MUST expose the Capability Registry and MUST allow plugins to query it at startup. Every plugin MUST perform capability negotiation against this registry before activating any extended behavior. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, RFC-0101, and RFC-0112.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Capability Registry](#2-capability-registry)
3. [Capability Query Protocol](#3-capability-query-protocol)
4. [Capability Negotiation](#4-capability-negotiation)
5. [Capability Dependency Graph](#5-capability-dependency-graph)
6. [Capability Lifecycle](#6-capability-lifecycle)
7. [Cross-References](#7-cross-references)
8. [Glossary](#8-glossary)
9. [Revision History](#9-revision-history)

---

## 1 Introduction

### 1.1 Purpose

The IPC Capability Registry is the authoritative catalogue of all features that the Atlas Runtime IPC subsystem exposes to plugins and extension processes. Rather than requiring plugins to probe the runtime imperatively or to encode capability assumptions in manifest files, the Registry provides a single, deterministic query interface that every plugin consumes during its initialization phase.

Every Atlas plugin MUST query the Capability Registry at startup to determine which IPC capabilities are available before activating any behavior that depends on those capabilities. This ensures that plugins gracefully degrade when optional capabilities are unavailable and that they never invoke behaviors the runtime does not support.

### 1.2 Design Principles

The Capability Registry adheres to the following principles:

1. **Deterministic Discovery**: A plugin query MUST return a reproducible result for a given runtime version. The registry content is immutable within a single runtime version.
2. **Implementation Independence**: This specification defines only the capability identifiers, their semantics, the query protocol, and the negotiation rules. It does not prescribe any particular transport, serialization format, or programming language for the implementation.
3. **Forward Compatibility**: New capabilities MAY be added in future runtime versions without breaking existing plugins. Plugins MUST treat unlisted capabilities as absent.
4. **Backward Compatibility**: Existing capabilities MUST NOT be removed or have their semantics weakened within a single major version. Deprecated capabilities enter a grace period before removal.

### 1.3 Scope

This document defines:

- The complete set of Capability IDs and their semantic definitions.
- The protocol by which plugins query the registry at startup.
- The version negotiation rules per capability.
- The dependency relationships between capabilities.
- The lifecycle states that each capability transitions through.
- Cross-references to related RFCs in the IPC specification suite.

### 1.4 Relationship to Other Specifications

The Capability Registry integrates with the IPC specification suite as follows:

- **RFC-0101 (IPC Overview)** provides the architectural context within which capabilities operate.
- **RFC-0107 (IPC Security)** defines the security primitives that security-related capabilities build upon.
- **RFC-0108 (IPC Reliability)** defines reliability primitives that reliability-related capabilities consume.
- **RFC-0110 (IPC Observability)** defines observability primitives that observability-related capabilities expose.
- **RFC-0112 (IPC Extension)** defines the extension point architecture that capabilities augment.

---

## 2 Capability Registry

The Capability Registry enumerates every IPC capability exposed by the Atlas Runtime. Each capability carries a unique Capability ID, a human-readable name, a category classification, a list of components that require it, and a semantic description.

### 2.1 Registry Table

| Capability ID | Name | Category | Required By | Description |
|---|---|---|---|---|
| CAP-IPC-STREAM | Stream Transport | Transport | Runtime | Bidirectional and unidirectional streaming support for continuous message flows |
| CAP-IPC-BATCH | Batch Processing | Transport | Runtime | Message batching and bulk operations for throughput optimization |
| CAP-IPC-BROADCAST | Broadcast Routing | Routing | Runtime | Multicast and broadcast message delivery to multiple subscribers |
| CAP-IPC-ENCRYPTION | End-to-End Encryption | Security | Runtime | Message-level encryption in transit using negotiated cipher suites |
| CAP-IPC-COMPRESS | Payload Compression | Serialization | Runtime | LZ4 and Zstandard compression support for payload reduction |
| CAP-IPC-DEDUP | Message Deduplication | Reliability | Runtime | Automatic duplicate message detection and removal via correlation tracking |
| CAP-IPC-ORDERING | Ordered Delivery | Transport | Runtime | Guaranteed per-channel message ordering using monotonic sequence enforcement |
| CAP-IPC-GUARANTEED | Guaranteed Delivery | Reliability | Runtime | At-least-once and exactly-once delivery semantics with acknowledgment tracking |
| CAP-IPC-CIRCUIT-BREAKER | Circuit Breaker | Reliability | Runtime | Automatic fault isolation, failure counting, and recovery circuit transitions |
| CAP-IPC-TRACE | Distributed Tracing | Observability | Runtime | End-to-end message trace propagation with correlation and span identifiers |
| CAP-IPC-METRICS | Telemetry Metrics | Observability | Runtime | Real-time performance metric collection including latency, throughput, and error rates |
| CAP-IPC-AUDIT | Audit Trail | Security | Runtime | Immutable audit logging of all IPC events with tamper-evident sequencing |
| CAP-IPC-SCHEMA-EVOLUTION | Schema Evolution | Serialization | Runtime | Forward and backward schema compatibility with versioned schema registration |
| CAP-IPC-SEQUENCING | Sequence Numbering | Message | Runtime | Monotonic sequence generation, gap detection, and reordering correction |
| CAP-IPC-TTL | Message TTL | Message | Runtime | Per-message time-to-live enforcement with configurable expiration policies |
| CAP-IPC-PRIORITY | Priority Scheduling | Routing | Runtime | Priority-based message routing and queue scheduling with fairness guarantees |
| CAP-IPC-REPLAY | Replay Protection | Security | Runtime | Anti-replay token and nonce management with bounded replay window enforcement |
| CAP-IPC-FRAGMENT | Message Fragmentation | Serialization | Runtime | Large payload fragmentation and reassembly with configurable maximum fragment size |
| CAP-IPC-HEARTBEAT | Connection Health | Transport | Runtime | Heartbeat-based liveness monitoring with configurable interval and timeout |
| CAP-IPC-RECONNECT | Automatic Reconnect | Transport | Runtime | Exponential backoff reconnect with jitter for transient connection failures |

### 2.2 Category Definitions

Capabilities are classified into six categories. Every capability belongs to exactly one category.

| Category | Description | Capability Count |
|---|---|---|
| Transport | Capabilities governing message flow mechanics, connection management, and throughput optimization | 6 |
| Security | Capabilities governing confidentiality, integrity, authenticity, and non-repudiation | 3 |
| Reliability | Capabilities governing delivery guarantees, fault tolerance, and recovery | 3 |
| Serialization | Capabilities governing payload encoding, schema management, and size optimization | 3 |
| Observability | Capabilities governing visibility, diagnostics, and operational telemetry | 2 |
| Routing | Capabilities governing message distribution, multiplexing, and scheduling | 2 |
| Message | Capabilities governing message-level metadata, sequencing, and lifecycle | 2 |

### 2.3 Capability Semantics

Each capability ID encodes a well-defined behavioral contract. The semantics are normative and implementation-independent.

#### 2.3.1 CAP-IPC-STREAM

Provides bidirectional streaming where both endpoints MAY send messages independently without request-response pairing. Provides unidirectional streaming where a single endpoint pushes messages to subscribers. The runtime MUST support concurrent streams per connection up to the configured concurrency limit.

#### 2.3.2 CAP-IPC-BATCH

Allows aggregating multiple discrete messages into a single batch envelope for reduced per-message overhead. The runtime MUST enforce a maximum batch size and MUST NOT permit a single batch to exceed the configured transport limit. Individual messages within a batch retain their own correlation and trace identifiers.

#### 2.3.3 CAP-IPC-BROADCAST

Delivers a single message to multiple subscribers on a shared channel without requiring the sender to address each recipient individually. The runtime MUST ensure that broadcast delivery respects subscriber permissions and channel access controls. Duplicate delivery to the same subscriber MUST be prevented.

#### 2.3.4 CAP-IPC-ENCRYPTION

Applies message-level encryption to payload content in transit between communicating processes. The runtime MUST negotiate cipher suite parameters during channel establishment and MUST rotate encryption keys at the configured rotation interval. Plaintext payload content MUST NOT be accessible to any intermediate process.

#### 2.3.5 CAP-IPC-COMPRESS

Applies lossless compression to IPC payload content to reduce bandwidth consumption. The runtime MUST support LZ4 and Zstandard compression algorithms and MUST negotiate the compression algorithm and level during channel establishment. Compressed payloads MUST be decompressed before schema validation.

#### 2.3.6 CAP-IPC-DEDUP

Detects and removes duplicate messages within a configurable deduplication window. The runtime MUST compute a deduplication key from message metadata and MUST track seen keys within the window. Messages exceeding the window age MUST be eligible for garbage collection of their deduplication state.

#### 2.3.7 CAP-IPC-ORDERING

Guarantees that messages arriving on a channel are delivered to the consumer in the same order they were sent by the producer. The runtime MUST enforce monotonic sequence numbers per channel and MUST buffer out-of-order messages until the gap is filled or the reorder timeout expires.

#### 2.3.8 CAP-IPC-GUARANTEED

Ensures that every message is delivered at least once (at-least-once) or exactly once (exactly-once) to its intended recipient. The runtime MUST track delivery acknowledgments and MUST implement retransmission for unacknowledged messages. Exactly-once semantics require coordination with CAP-IPC-DEDUP.

#### 2.3.9 CAP-IPC-CIRCUIT-BREAKER

Monitors failure rates on connections and channels, transitioning between closed, open, and half-open states based on configurable thresholds. The runtime MUST stop routing new messages to a connection in the open state and MUST periodically probe for recovery in the half-open state.

#### 2.3.10 CAP-IPC-TRACE

Propagates correlation identifiers and span identifiers across all IPC hops to enable end-to-end request tracing. The runtime MUST inject trace context into message headers and MUST preserve trace context across all intermediate processes. Trace data MUST be compatible with the observability subsystem defined in RFC-0110.

#### 2.3.11 CAP-IPC-METRICS

Collects and exposes real-time performance metrics including message latency, throughput, error rates, queue depths, and connection counts. The runtime MUST expose metrics through a standardized interface and MUST support both pull-based and push-based metric export.

#### 2.3.12 CAP-IPC-AUDIT

Records an immutable log of all IPC events including connection establishments, message deliveries, permission violations, and configuration changes. The runtime MUST append audit entries in chronological order and MUST prevent modification or deletion of existing entries. Audit entries MUST include timestamps, source identifiers, and event classifications.

#### 2.3.13 CAP-IPC-SCHEMA-EVOLUTION

Manages schema version compatibility allowing producers and consumers to evolve their message formats independently. The runtime MUST support forward compatibility (new schemas accepted by old consumers) and backward compatibility (old schemas accepted by new consumers) within the configured compatibility window.

#### 2.3.14 CAP-IPC-SEQUENCING

Generates and enforces monotonic sequence numbers for messages on each channel. The runtime MUST detect sequence gaps and MUST report gap events through the observability subsystem. Sequence number overflow MUST wrap to the minimum value without losing monotonicity within a single channel lifetime.

#### 2.3.15 CAP-IPC-TTL

Enforces a time-to-live duration on individual messages. The runtime MUST discard messages whose TTL has expired before delivery and MUST propagate TTL information through intermediate hops. TTL MUST be evaluated at each hop, and the remaining TTL MUST be decremented accordingly.

#### 2.3.16 CAP-IPC-PRIORITY

Assigns priority levels to messages and routes them through priority-ordered queues. The runtime MUST guarantee that higher-priority messages are delivered before lower-priority messages within the same channel. The runtime MUST prevent priority starvation of lower-priority messages through configurable aging mechanisms.

#### 2.3.17 CAP-IPC-REPLAY

Manages anti-replay tokens and nonces to prevent malicious reuse of captured messages. The runtime MUST issue unique nonces per message and MUST reject messages presenting expired or reused nonces. The replay protection window MUST be configurable and MUST be enforced at the receiving endpoint.

#### 2.3.18 CAP-IPC-FRAGMENT

Splits oversized messages into fragments for transport and reassembles them at the receiving endpoint. The runtime MUST ensure that all fragments of a message arrive at the same endpoint and MUST discard partial fragment sets that exceed the reassembly timeout. Fragment order MUST be preserved during reassembly.

#### 2.3.19 CAP-IPC-HEARTBEAT

Periodically sends health check signals between connected endpoints to detect connection liveness. The runtime MUST configure heartbeat intervals and MUST declare a connection unhealthy when heartbeats are missed for the configured timeout period. Heartbeat messages MUST NOT interfere with application message ordering.

#### 2.3.20 CAP-IPC-RECONNECT

Automatically attempts to restore connections that have been lost due to transient failures. The runtime MUST implement exponential backoff with jitter for reconnection attempts and MUST respect maximum retry limits. Reconnection MUST preserve channel state and MUST re-establish authentication credentials.

---

## 3 Capability Query Protocol

### 3.1 Overview

Plugins query the Capability Registry during their initialization phase, before registering any handlers or opening any channels. The query protocol is defined abstractly; implementations MAY use any transport mechanism that satisfies the protocol semantics.

### 3.2 Query Phases

The capability query process consists of three phases executed in order:

**Phase 1 — Registry Discovery**: The plugin discovers the registry endpoint. The runtime MUST advertise the registry location through the standard service discovery mechanism defined in RFC-0112.

**Phase 2 — Capability Enumeration**: The plugin requests the full capability list. The runtime MUST respond with every capability ID currently registered, along with its version and status.

**Phase 3 — Capability Details**: The plugin MAY request detailed metadata for specific capabilities. The runtime MUST respond with the capability description, supported versions, and dependency information.

### 3.3 Query Contract

The query protocol obeys the following constraints:

| Constraint | Requirement |
|---|---|
| Query Timing | MUST occur before any IPC channel operations |
| Query Frequency | MAY be cached by the plugin for the duration of its lifetime |
| Response Completeness | MUST include all registered capabilities |
| Response Latency | MUST complete within 100 ms under normal conditions |
| Error Handling | MUST return RegistryUnavailable if the runtime is not ready |
| Idempotency | Multiple queries MUST return identical results within a runtime version |

### 3.4 Abstract Query Interface

The following abstract interface describes the query protocol. Implementations are NOT required to match this interface syntactically; they MUST satisfy the behavioral constraints.

```
interface CapabilityRegistry {
  // Returns the full capability list with IDs, versions, and statuses.
  CapabilityList queryAll();

  // Returns metadata for a specific capability by ID.
  CapabilityDetail queryById(CapabilityId id);

  // Returns capabilities belonging to a specific category.
  CapabilityList queryByCategory(Category category);

  // Returns capabilities that a specific component requires.
  CapabilityList queryByComponent(ComponentId component);
}

struct CapabilityList {
  CapabilityEntry[] entries;
  string runtimeVersion;
  timestamp queryTimestamp;
}

struct CapabilityEntry {
  CapabilityId id;
  string name;
  Category category;
  string status;       // "available", "deprecated", or "removed"
  VersionRange versions;
}

struct CapabilityDetail {
  CapabilityId id;
  string name;
  Category category;
  string description;
  VersionRange versions;
  string[] dependencies;
  string[] dependedBy;
  map<string, string> metadata;
}
```

### 3.5 Query Caching

Plugins MUST cache the registry response for the duration of their initialization phase. Caching across the full plugin lifetime is OPTIONAL but RECOMMENDED. The runtime MUST signal registry changes through the standard notification mechanism defined in RFC-0112. A plugin receiving a registry change notification MUST invalidate its cached copy and perform a fresh query.

---

## 4 Capability Negotiation

### 4.1 Overview

After discovering available capabilities, a plugin negotiates the specific version of each capability it intends to use. Version negotiation ensures that both the plugin and the runtime agree on the behavioral contract before any capability-dependent operations commence.

### 4.2 Negotiation Protocol

The negotiation protocol proceeds as follows:

1. The plugin requests a specific version for each capability it intends to use.
2. The runtime evaluates the requested version against its supported version range.
3. The runtime responds with either acceptance (the requested version is supported) or a counter-proposal (the closest compatible version the runtime supports).
4. The plugin accepts the runtime's response or aborts initialization if no compatible version exists.

### 4.3 Version Compatibility Rules

| Rule | Constraint |
|---|---|
| Major Version Mismatch | Communication MUST NOT proceed across different major versions |
| Minor Version Increase | A plugin using minor version N MUST be compatible with runtime minor version N+1 (backward compatible) |
| Minor Version Decrease | A runtime using minor version N MUST accept plugins with minor version N-1 (forward compatible) |
| Patch Version | Patch versions are implementation details and MUST NOT affect compatibility |
| Deprecated Versions | Plugins MUST NOT negotiate deprecated capability versions after the deprecation grace period expires |

### 4.4 Negotiation Failure

If negotiation fails for any capability, the plugin MUST:

1. Abort initialization for that capability.
2. Continue initialization for capabilities that negotiated successfully.
3. Report the negotiation failure through the standard error reporting mechanism defined in RFC-0111.
4. Operate in degraded mode if the failed capability is optional.

### 4.5 Capability Version Table

| Capability ID | Current Version | Supported Range | Deprecation Policy |
|---|---|---|---|
| CAP-IPC-STREAM | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-BATCH | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-BROADCAST | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-ENCRYPTION | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-COMPRESS | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-DEDUP | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-ORDERING | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-GUARANTEED | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-CIRCUIT-BREAKER | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-TRACE | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-METRICS | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-AUDIT | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-SCHEMA-EVOLUTION | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-SEQUENCING | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-TTL | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-PRIORITY | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-REPLAY | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-FRAGMENT | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-HEARTBEAT | 1.0 | 1.0.x | No deprecation planned |
| CAP-IPC-RECONNECT | 1.0 | 1.0.x | No deprecation planned |

---

## 5 Capability Dependency Graph

### 5.1 Dependency Overview

Certain capabilities depend on others for correct operation. The dependency graph defines mandatory and optional relationships. A capability MUST NOT be activated unless all its mandatory dependencies are also activated.

### 5.2 Dependency Matrix

| Capability ID | Mandatory Dependencies | Optional Dependencies |
|---|---|---|
| CAP-IPC-STREAM | None | CAP-IPC-HEARTBEAT, CAP-IPC-RECONNECT |
| CAP-IPC-BATCH | CAP-IPC-STREAM | CAP-IPC-COMPRESS |
| CAP-IPC-BROADCAST | CAP-IPC-STREAM | CAP-IPC-PRIORITY |
| CAP-IPC-ENCRYPTION | None | CAP-IPC-AUDIT |
| CAP-IPC-COMPRESS | None | None |
| CAP-IPC-DEDUP | CAP-IPC-SEQUENCING | CAP-IPC-GUARANTEED |
| CAP-IPC-ORDERING | CAP-IPC-SEQUENCING | None |
| CAP-IPC-GUARANTEED | CAP-IPC-ORDERING, CAP-IPC-DEDUP | CAP-IPC-RECONNECT |
| CAP-IPC-CIRCUIT-BREAKER | None | CAP-IPC-METRICS, CAP-IPC-HEARTBEAT |
| CAP-IPC-TRACE | None | CAP-IPC-METRICS, CAP-IPC-AUDIT |
| CAP-IPC-METRICS | None | CAP-IPC-TRACE |
| CAP-IPC-AUDIT | None | None |
| CAP-IPC-SCHEMA-EVOLUTION | None | CAP-IPC-COMPRESS |
| CAP-IPC-SEQUENCING | None | None |
| CAP-IPC-TTL | None | CAP-IPC-SEQUENCING |
| CAP-IPC-PRIORITY | CAP-IPC-SEQUENCING | CAP-IPC-BROADCAST |
| CAP-IPC-REPLAY | CAP-IPC-ENCRYPTION, CAP-IPC-SEQUENCING | None |
| CAP-IPC-FRAGMENT | CAP-IPC-STREAM | CAP-IPC-COMPRESS |
| CAP-IPC-HEARTBEAT | None | CAP-IPC-RECONNECT |
| CAP-IPC-RECONNECT | CAP-IPC-HEARTBEAT | None |

### 5.3 Dependency Resolution

When a plugin activates a capability, the runtime MUST automatically activate all mandatory transitive dependencies. Optional dependencies MUST NOT be activated implicitly. If a mandatory dependency is unavailable, the dependent capability MUST be marked as inactive and the plugin MUST be notified through the standard error reporting mechanism.

### 5.4 Circular Dependency Prevention

The capability dependency graph MUST be a directed acyclic graph (DAG). The runtime MUST reject any configuration that would introduce a circular dependency. Circular dependency detection MUST occur at capability registration time.

---

## 6 Capability Lifecycle

### 6.1 Lifecycle States

Every capability transitions through four lifecycle states:

```
                    ┌───────────┐
                    │ Available │
                    └─────┬─────┘
                          │ Runtime ships with capability
                          ▼
                    ┌───────────┐
              ┌────│   Active  │────┐
              │    └───────────┘    │
              │                     │
              ▼                     ▼
        ┌─────────────┐     ┌─────────────┐
        │  Deprecated │     │  Removed    │
        └──────┬──────┘     └─────────────┘
               │
               │ Grace period expires
               ▼
        ┌─────────────┐
        │   Removed   │
        └─────────────┘
```

### 6.2 State Definitions

| State | Description | Plugin Behavior |
|---|---|---|
| Available | Capability is fully implemented and functional | MAY query and negotiate normally |
| Active | Capability is in use by one or more plugins | MUST continue to function; MUST NOT be removed |
| Deprecated | Capability is scheduled for removal; replacement available | SHOULD migrate to replacement; MUST continue to function during grace period |
| Removed | Capability has been removed from the runtime | MUST NOT be queried; MUST NOT be negotiated |

### 6.3 Transition Rules

| Transition | Condition | Notification |
|---|---|---|
| Available → Active | First plugin negotiates the capability | None required |
| Active → Deprecated | Architecture Board approves deprecation | Published in changelog; registry status updated |
| Deprecated → Removed | Grace period expires (minimum 2 major versions) | Published in changelog; registry status updated |
| Available → Removed | Capability has a critical security flaw | Emergency advisory through RFC-0111 error channel |

### 6.4 Deprecation Grace Period

A deprecated capability MUST remain functional for a minimum of two major runtime versions before transitioning to Removed. During the deprecation period:

1. Plugins using the deprecated capability MUST continue to function.
2. The runtime MUST log warnings when deprecated capabilities are exercised.
3. Documentation MUST direct plugins toward the recommended replacement capability.
4. New plugins MUST NOT depend on deprecated capabilities.

---

## 7 Cross-References

### 7.1 Related Specifications

| Specification | Relationship |
|---|---|
| RFC-0101 IPC Overview | Defines the overarching IPC architecture within which capabilities operate |
| RFC-0102 IPC Message Model | Defines message structures consumed by capability-dependent operations |
| RFC-0103 IPC Transport | Defines transport-layer protocols that transport capabilities build upon |
| RFC-0104 IPC Routing | Defines routing protocols that routing capabilities extend |
| RFC-0105 IPC Channel | Defines channel abstractions that capabilities operate on |
| RFC-0106 IPC Serialization | Defines serialization contracts that serialization capabilities augment |
| RFC-0107 IPC Security | Defines security primitives that security capabilities implement |
| RFC-0108 IPC Reliability | Defines reliability primitives that reliability capabilities implement |
| RFC-0109 IPC Lifecycle | Defines lifecycle protocols that lifecycle-related capabilities follow |
| RFC-0110 IPC Observability | Defines observability primitives that observability capabilities expose |
| RFC-0111 IPC Error Model | Defines error semantics used by capability negotiation failures |
| RFC-0112 IPC Extension | Defines the extension framework that capability discovery serves |
| RFC-0007 Runtime IPC | Defines the Runtime-level IPC dispatcher that hosts the Capability Registry |

### 7.2 Integration Points

The Capability Registry integrates with the following Atlas subsystems:

- **Service Registry**: The registry endpoint is advertised through the service discovery mechanism.
- **Plugin Host**: The plugin host enforces capability query timing constraints during plugin initialization.
- **Security Manager**: Security capabilities coordinate with the Security Manager for key management and credential rotation.
- **Audit Subsystem**: Audit capabilities write to the centralized audit log managed by the Runtime.
- **Observability Pipeline**: Observability capabilities feed metrics and traces into the standard observability pipeline.

---

## 8 Glossary

Terms used in this specification have the following meanings. Additional terms are defined in the [Atlas Master Glossary](../glossary.md).

| Term | Definition |
|---|---|
| Capability | A discrete feature declaration exposed by the Runtime IPC subsystem that plugins MAY query and negotiate |
| Capability ID | A unique, immutable identifier for a capability, formatted as CAP-IPC-{NAME} |
| Capability Registry | The authoritative catalogue of all IPC capabilities exposed by the Runtime |
| Category | A classification grouping capabilities by functional domain (Transport, Security, Reliability, Serialization, Observability, Routing, Message) |
| Negotiation | The process by which a plugin and runtime agree on a specific capability version for use |
| Dependency | A relationship where one capability requires another capability to be active for correct operation |
| Mandatory Dependency | A dependency that MUST be satisfied; the dependent capability MUST NOT activate without it |
| Optional Dependency | A dependency that MAY be satisfied; the dependent capability MAY activate without it |
| Grace Period | The minimum duration (two major versions) that a deprecated capability MUST remain functional |
| Version Range | The set of minor and patch versions supported for a capability, expressed as a bounded interval |
| Transitive Dependency | A dependency that is not direct but is required through a chain of mandatory dependencies |
| DAG | Directed Acyclic Graph; the mathematical structure that the capability dependency graph MUST conform to |

---

## 9 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0.0 | 2026-06-30 | Atlas Team | Initial release. Defined 20 capability IDs, registry table, query protocol, negotiation rules, dependency graph, lifecycle states, and cross-references. |

---

*This document is part of the Atlas Specification hierarchy. For the complete RFC index, see [RFC_INDEX.md](../RFC_INDEX.md).*