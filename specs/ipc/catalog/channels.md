# RFC: IPC-CAT-CH

RFC: IPC-CAT-CH
Title: IPC Channel Catalog
Status: Accepted
Version: 1.0.0
Author: Atlas Team
Reviewer: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0105 IPC Channel
  - RFC-0107 IPC Security
  - RFC-0109 IPC Lifecycle
Required By:
  - All RFCs within the IPC subsystem
  - RFC-0101 IPC Overview
  - RFC-0102 Message Model
  - RFC-0103 Transport
  - RFC-0104 Routing
Supersedes: None
Superseded By: None
Category: IPC
Layer: Communication
Normative: YES
Audience: Systems Engineers, IPC Implementers
ADR References:
  - ADR-0010
Constitution References:
  - Section 3.5 (IPC Isolation)
  - Section 4.2 (Process Boundaries)
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

This specification is Normative. Every RFC within the Atlas IPC subsystem MUST reference the fixed Channel IDs defined in this catalog. Free-text channel descriptions are prohibited in favor of these canonical identifiers. Any addition, modification, or removal of a Channel ID MUST be approved through the formal Architecture Decision Record (ADR) process and MUST NOT alter existing Channel IDs or their semantics.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and RFC-0105 (IPC Channel).

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Channel Registry](#4-channel-registry)
5. [Channel Properties](#5-channel-properties)
6. [Channel Lifecycle](#6-channel-lifecycle)
7. [Channel Isolation Model](#7-channel-isolation-model)
8. [Channel Permission Matrix](#8-channel-permission-matrix)
9. [Cross-References](#9-cross-references)
10. [Glossary](#10-glossary)
11. [Revision History](#11-revision-history)

---

## 1 Introduction

### 1.1 Purpose

The Atlas platform relies on a rich ecosystem of inter-process communication channels to coordinate operations across independent runtime processes, plugins, external systems, and internal services. Without a centralized, immutable catalog of channel identifiers, different RFCs and implementations would inevitably diverge in their naming conventions, leading to interoperability failures, ambiguous security boundaries, and unmanageable complexity.

The IPC Channel Catalog establishes a single source of truth for all standard IPC channel identities within the Atlas ecosystem. Every RFC in the IPC subsystem, every implementation artifact, and every security policy document MUST reference these fixed Channel IDs rather than free-text descriptions.

### 1.2 How to Use This Catalog

Implementers and RFC authors SHOULD follow these guidelines when working with channel identifiers:

- **Referencing Channels**: Always use the canonical Channel ID (e.g., CH-SYSTEM) rather than human-readable names when specifying channel dependencies in RFCs, configuration files, or code.
- **Adding New Channels**: Propose new channels through the ADR process. New Channel IDs MUST follow the naming convention CH-{DOMAIN}, where {DOMAIN} is an uppercase alphanumeric abbreviation derived from the channel functional domain.
- **Deprecating Channels**: Existing Channel IDs MUST NOT be deleted or repurposed. Channels that are no longer in active use MUST be marked as deprecated in the catalog and transitioned through the Draining lifecycle state before removal.
- **Cross-RFC Consistency**: All IPC-related RFCs MUST maintain alignment with this catalog. Conflicts between a channel definition in this catalog and any other RFC MUST be resolved in favor of this catalog.

---

## 2 Goals

- **Immutable Identity**: Every channel MUST have a fixed, unchanging identifier that persists across all Atlas specification versions. Channel IDs are never reused, reassigned, or retired once accepted.
- **Semantic Clarity**: Each Channel ID MUST encode sufficient information about the channel purpose, domain, and access class to enable instant recognition by implementers and auditors.
- **Access Control Foundation**: The catalog provides the authoritative mapping between channel identifiers and their permission profiles, enabling consistent enforcement of the zero-trust security model defined in RFC-0107.
- **Lifecycle Governance**: Every channel MUST follow the deterministic lifecycle defined in RFC-0109, with this catalog serving as the registration point for all channel instances.
- **Namespace Integrity**: Channel IDs MUST form a globally unique namespace within the Atlas IPC subsystem, preventing collisions across domains, releases, and implementations.

---

## 3 Non-Goals

- **Transport Implementation Details**: This catalog does not specify the physical transport mechanism (named pipes, Unix sockets, TCP) for any channel. Transport selection is governed by RFC-0103.
- **Message Schema Definitions**: Payload structures, serialization formats, and schema validation rules for individual channels are defined in RFC-0102, not herein.
- **Routing Configuration**: The specific routing rules, endpoint mappings, and discovery mechanisms for channels are governed by RFC-0104.
- **Operational Tuning**: Per-channel performance budgets, backpressure thresholds, and capacity planning parameters are outside the scope of this catalog.

---

## 4 Channel Registry

The following table defines the complete set of standard IPC channels within the Atlas platform. Each entry represents a permanent, immutable channel identity.

| Channel ID | Name | Type | Access Class | Owner | Description |
|---|---|---|---|---|---|
| CH-SYSTEM | System Control | System | L4 | Runtime | Runtime-internal control plane for lifecycle management, coordination, and supervisory operations |
| CH-PLUGIN | Plugin Bus | Plugin | L2 | Runtime | Plugin-to-Runtime and Plugin-to-Plugin communication channel for dynamic service discovery and invocation |
| CH-WORKFLOW | Workflow Engine | Workflow | L3 | Runtime | Workflow step coordination, DAG execution, and pipeline orchestration channel |
| CH-VISION | Vision Capture | Vision | L3 | Runtime | Vision frame capture, streaming, and recognition results distribution channel |
| CH-AI | AI Agent | AI | L3 | Runtime | AI agent reasoning, tool calls, and response channel for model inference coordination |
| CH-STORAGE | Storage Gateway | Storage | L2 | Runtime | Persistent storage access, data synchronization, and CRUD operations channel |
| CH-LOGGER | Diagnostic Logger | Internal | L1 | Runtime | Centralized logging, audit trail, and diagnostic event distribution channel |
| CH-EXTERNAL | External Systems | External | L1 | Runtime | Cross-workspace and external system integration channel for third-party service communication |
| CH-MARKETPLACE | Marketplace | Internal | L2 | Runtime | Plugin marketplace catalog, listing, and update notification channel |
| CH-SCHEDULER | Scheduler | Internal | L3 | Runtime | Task dispatch, priority management, and resource allocation channel |
| CH-KNOWLEDGE | Knowledge Packs | Internal | L2 | Runtime | Knowledge pack retrieval, versioning, and update distribution channel |
| CH-INTERNAL | Internal Bridge | Internal | L1 | Runtime | Intra-process communication boundary channel for same-host process interactions |

### 4.1 Channel ID Naming Convention

All Channel IDs follow the pattern CH-{DOMAIN} where:

- CH is the fixed prefix denoting an IPC channel.
- {DOMAIN} is a domain-specific uppercase identifier drawn from the set: SYSTEM, PLUGIN, WORKFLOW, VISION, AI, STORAGE, LOGGER, EXTERNAL, MARKETPLACE, SCHEDULER, KNOWLEDGE, INTERNAL.

New Channel IDs MUST extend this pattern with a domain abbreviation that is at most 15 characters long, consists exclusively of uppercase ASCII letters and digits, and begins with an alphabetic character.

### 4.2 Access Class Taxonomy

Access classes define the security sensitivity tier of each channel. The taxonomy is as follows:

| Access Class | Sensitivity Level | Description |
|---|---|---|
| L1 | Public | No authentication required; visible to all processes within the workspace |
| L2 | Internal | Requires valid process token; restricted to registered Runtime services and authorized plugins |
| L3 | Restricted | Requires elevated token with domain-specific capabilities; restricted to designated subsystems |
| L4 | Confidential | Requires admin-level token with encrypted transport; restricted to Runtime core supervisory operations |

### 4.3 Channel Type Classification

Channel types categorize the functional domain of each channel:

| Channel Type | Description |
|---|---|
| System | Runtime-internal control plane and lifecycle coordination |
| Plugin | Dynamic plugin ecosystem communication |
| Workflow | Pipeline and DAG-based orchestration |
| Vision | Computer vision frame and result streaming |
| AI | Artificial intelligence agent coordination |
| Storage | Persistent data access and synchronization |
| Internal | Runtime-internal utility and diagnostic channels |
| External | Cross-boundary and third-party integration channels |

---

## 5 Channel Properties

Every channel defined in this catalog possesses the following immutable properties. Implementations MUST enforce these property constraints.

### 5.1 Property Schema

| Property | Type | Constraint | Description |
|---|---|---|---|
| channel_id | String | Fixed per registry entry | Canonical identifier from the Channel Registry |
| 
ame | String | Human-readable, 1-64 characters | Descriptive channel name |
| 	ype | Enum | From Channel Type Classification | Functional domain category |
| ccess_class | Enum | L1 through L4 | Security sensitivity tier |
| owner | String | Fixed per registry entry | Authoritative owning process |
| description | String | 1-512 characters | Functional description of the channel |
| max_bandwidth | Integer | Measured in bytes per second | Upper bound on sustained throughput |
| min_priority | Integer | 1-10, where 10 is highest | Minimum scheduling priority for channel messages |

### 5.2 Default Property Values

When a channel-specific property value is not explicitly configured, implementations MUST apply the following defaults:

| Channel ID | Max Bandwidth | Min Priority |
|---|---|---|
| CH-SYSTEM | 1,048,576 bytes/s (1 MiB/s) | 10 |
| CH-PLUGIN | 524,288 bytes/s (512 KiB/s) | 6 |
| CH-WORKFLOW | 2,097,152 bytes/s (2 MiB/s) | 8 |
| CH-VISION | 10,485,760 bytes/s (10 MiB/s) | 7 |
| CH-AI | 5,242,880 bytes/s (5 MiB/s) | 7 |
| CH-STORAGE | 2,097,152 bytes/s (2 MiB/s) | 5 |
| CH-LOGGER | 1,048,576 bytes/s (1 MiB/s) | 3 |
| CH-EXTERNAL | 524,288 bytes/s (512 KiB/s) | 4 |
| CH-MARKETPLACE | 262,144 bytes/s (256 KiB/s) | 2 |
| CH-SCHEDULER | 1,048,576 bytes/s (1 MiB/s) | 9 |
| CH-KNOWLEDGE | 2,097,152 bytes/s (2 MiB/s) | 5 |
| CH-INTERNAL | 524,288 bytes/s (512 KiB/s) | 4 |

### 5.3 Property Immutability

Once a Channel ID is accepted into this catalog, its channel_id, 	ype, ccess_class, and owner properties are IMMUTABLE. The 
ame and description fields MAY be updated through the ADR process, provided the update preserves the semantic meaning of the channel. All other properties are configurable at runtime within the bounds defined in this section.

---

## 6 Channel Lifecycle

Every channel MUST follow the deterministic lifecycle state machine defined below. Transitions between states are governed by strict rules to ensure predictable behavior and prevent resource leaks.

### 6.1 Lifecycle States

| State | Description |
|---|---|
| Created | The channel has been registered in this catalog and its metadata has been initialized, but no message exchange has commenced |
| Active | The channel is fully operational and accepting messages from authorized senders |
| Paused | The channel is temporarily suspended; no new messages are accepted, but existing connections remain intact |
| Draining | The channel is in the process of being decommissioned; new messages are rejected with ChannelDraining error, but in-flight messages are permitted to complete |
| Closed | The channel has been fully terminated; all connections are severed, resources are released, and the channel ID is reserved (never reused) |

### 6.2 State Transition Rules

| From State | To State | Condition |
|---|---|---|
| Created | Active | Owner signals readiness and all permission checks pass |
| Active | Paused | Owner initiates pause, or an administrative policy requires suspension |
| Paused | Active | Owner signals resumption and all permission checks pass |
| Paused | Draining | Owner initiates decommissioning from paused state |
| Active | Draining | Owner initiates decommissioning from active state |
| Draining | Closed | All in-flight messages have been delivered and the drain timeout has elapsed |
| Created | Closed | Initialization fails validation before activation |

### 6.3 Mandatory Constraints

- A channel MUST NOT transition directly from Created to Draining or Closed. It MUST pass through Active at least once.
- A channel in Draining state MUST NOT revert to Active or Paused. The transition to Draining is irreversible.
- The maximum drain timeout from Draining to Closed is 30 seconds. Implementations MAY configure a shorter timeout but MUST NOT exceed this upper bound.
- A channel in Closed state MUST retain its Channel ID in the catalog permanently. The ID MUST NOT be reassigned to any new channel.

---

## 7 Channel Isolation Model

The Atlas IPC channel architecture enforces three orthogonal isolation dimensions. Every channel MUST satisfy all three isolation requirements simultaneously.

### 7.1 Namespace Isolation

Each channel operates within a distinct logical namespace identified by its Channel ID. The namespace hierarchy is flat; there are no parent-child relationships between channels. Cross-namespace communication MUST occur through explicit message forwarding mediated by the channel owner.

| Isolation Property | Constraint |
|---|---|
| Namespace uniqueness | Every Channel ID MUST be globally unique within the IPC subsystem |
| Namespace visibility | Processes MUST NOT discover Channel IDs outside their granted permission set |
| Namespace collision prevention | Duplicate Channel ID registration attempts MUST be rejected with ChannelAlreadyExists error |

### 7.2 Permission Isolation

Permission isolation ensures that only authorized processes can interact with a given channel. The permission model is enforced at the channel boundary, before any message reaches the transport layer.

| Permission Dimension | Enforcement Point |
|---|---|
| Read access | Verified at message reception; unauthorized readers receive PermissionDenied |
| Write access | Verified at message transmission; unauthorized writers receive PermissionDenied |
| Admin access | Required for lifecycle transitions (pause, drain, close); unauthorized operators receive AdminRequired |
| Token scope | Each process token MUST explicitly enumerate the Channel IDs it is authorized to access |

### 7.3 Resource Isolation

Resource isolation prevents any single channel from consuming disproportionate system resources. Each channel operates within independently enforced resource quotas.

| Resource Dimension | Quota Scope | Enforcement Mechanism |
|---|---|---|
| Bandwidth | Per-channel maximum throughput | Token bucket rate limiter |
| Message queue depth | Per-channel pending message count | Backpressure signal to sender |
| Connection count | Per-channel simultaneous connections | Connection pool allocator |
| Memory footprint | Per-channel serialization buffer | Heap reservation limit |

### 7.4 Isolation Boundary Rules

- A process MUST NOT access a channel for which it holds no permission token, regardless of its privilege level.
- Resource quotas MUST be evaluated independently per channel; exhaustion of one channel quota MUST NOT affect other channels.
- Isolation boundaries MUST be verifiable through automated compliance testing as defined in RFC-0107.

---

## 8 Channel Permission Matrix

The following matrix defines which process types are authorized to read from and write to each channel. The matrix is normative; any deviation MUST be approved through the ADR process.

### 8.1 Legend

| Symbol | Meaning |
|---|---|
| RW | Read and Write access granted |
| R | Read-only access granted |
| W | Write-only access granted |
| - | No access granted |
| Admin | Administrative access required for lifecycle operations |

### 8.2 Permission Matrix

| Process Type | CH-SYSTEM | CH-PLUGIN | CH-WORKFLOW | CH-VISION | CH-AI | CH-STORAGE | CH-LOGGER | CH-EXTERNAL | CH-MARKETPLACE | CH-SCHEDULER | CH-KNOWLEDGE | CH-INTERNAL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Runtime Core | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW | Admin/RW |
| Plugin Host | - | RW | R | R | R | R | R | - | R | R | R | R |
| Vision Engine | - | - | - | RW | R | - | R | - | - | - | - | - |
| AI Host | - | - | - | R | RW | - | R | - | - | - | R | - |
| Workflow Engine | - | - | RW | R | R | R | R | - | - | R | - | - |
| Storage Service | - | - | R | - | - | RW | R | R | - | - | R | R |
| Logger Service | - | R | R | R | R | R | RW | R | R | R | R | R |
| Scheduler Service | - | - | RW | - | - | - | R | - | - | RW | - | - |
| External Adapter | - | - | - | - | - | R | - | RW | - | - | - | R |
| Marketplace Client | - | R | - | - | - | - | R | - | RW | - | R | - |
| Knowledge Client | - | R | - | - | - | - | R | - | - | - | RW | R |
| Bridge Service | - | R | R | R | R | R | R | R | R | R | R | RW |
| Diagnostic Tool | - | R | R | R | R | R | RW | R | R | R | R | R |

### 8.3 Permission Inheritance Rules

- **Runtime Core** retains Admin-level access to all channels by virtue of its supervisory role.
- **Plugin Host** inherits read access to all channels except those explicitly marked as Runtime-internal (CH-SYSTEM, CH-EXTERNAL).
- **Service-specific processes** (Vision Engine, AI Host, etc.) receive write access only to their primary channel and read access to all supporting channels.
- **Utility processes** (Logger Service, Diagnostic Tool) receive read access to all channels and write access to CH-LOGGER exclusively.

### 8.4 Permission Enforcement

- Permission checks MUST occur at the channel boundary, before any message is enqueued or dequeued.
- A process attempting to access a channel without the required permission MUST receive an immediate PermissionDenied response.
- Permission violations MUST be logged to CH-LOGGER with the process identity, target channel ID, attempted operation, and timestamp.

---

## 9 Cross-References

This catalog is a foundational artifact within the IPC subsystem and MUST be referenced alongside the following specifications:

| Reference | Title | Relationship |
|---|---|---|
| RFC-0101 | IPC Overview | Defines the overall IPC architecture; this catalog provides the channel identity layer for RFC-0101 conceptual model |
| RFC-0105 | IPC Channel | Defines the channel abstraction, lifecycle, and state machine; this catalog enumerates the concrete channel instances |
| RFC-0107 | IPC Security | Defines the security model and permission enforcement; this catalog provides the channel identity basis for RFC-0107 access control rules |
| RFC-0109 | IPC Lifecycle | Defines the channel lifecycle protocol; this catalog lifecycle rules in Section 6 are consistent with RFC-0109 state machine |
| RFC-0104 | IPC Routing | Defines message routing mechanics; channel IDs from this catalog are the primary routing keys for RFC-0104 |
| RFC-0102 | Message Model | Defines message schemas; each channel in this catalog carries messages conforming to RFC-0102 schemas |
| RFC-0103 | IPC Transport | Defines transport mechanisms; channels in this catalog are transport-agnostic and MAY use any RFC-0103-compliant transport |

---

## 10 Glossary

| Term | Definition |
|---|---|
| **Channel ID** | A fixed, immutable identifier (e.g., CH-SYSTEM) that uniquely identifies an IPC channel within the Atlas ecosystem |
| **Access Class** | A four-tier security sensitivity classification (L1 through L4) that determines the authentication and authorization requirements for channel access |
| **Channel Type** | A categorical classification of a channel functional domain (e.g., System, Plugin, Workflow, Vision, AI, Storage, Internal, External) |
| **Owner** | The authoritative process responsible for a channel lifecycle decisions, permission grants, and resource allocation |
| **Lifecycle State** | One of the five deterministic states (Created, Active, Paused, Draining, Closed) that a channel traverses during its existence |
| **Drain Timeout** | The maximum duration (30 seconds) that a channel may remain in the Draining state before transitioning to Closed |
| **Isolation Dimension** | One of three orthogonal isolation mechanisms (namespace, permission, resource) that enforce channel boundaries |
| **Permission Matrix** | A normative table defining which process types may read, write, or administer each channel |
| **Zero-Trust IPC** | The security principle that every IPC message crossing a process boundary MUST be authenticated, authorized, and validated before processing |
| **ADR** | Architecture Decision Record; the formal governance mechanism for approving changes to this catalog |

---

## 11 Revision History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 1.0.0 | 2026-06-30 | Atlas Team | Initial release. Defined 12 standard IPC channels, access class taxonomy, channel type classification, lifecycle state machine, isolation model, permission matrix, and glossary. |

---

## Compatibility

- Compatible with Spec Version 1.x.
- All Channel IDs in this catalog are forward-compatible with Spec 2.x and beyond. No Channel ID MAY be removed or repurposed in any future specification version.
