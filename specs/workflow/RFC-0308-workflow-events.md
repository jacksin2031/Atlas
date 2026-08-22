RFC: RFC-0308
Title: Workflow Events
Status: Proposed
Version: 1.1.0
Auth
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Event | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Type | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Category | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Payload | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Schema | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Routing | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Delivery | The guarantee that an emitted event reaches its intended consumers. | RFC-1001 |
| Event Ordering | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Deduplication | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Replay | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
or: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0005 Runtime Event Bus
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0307 Workflow Context
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1004 Common Contract Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012 (Contract-First Specification-Driven Development)
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0307 Workflow Context
  - RFC-0309 Workflow Actions
  - RFC-0312 Workflow Scheduler
  - RFC-0313 Workflow Parallelism
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Related ADR: ADR-0012
Related JSON Schema: contracts/json/workflow.schema.json
Related Catalog: specs/workflow/catalog/workflow-events.md

---

## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Events specification defines the event model for Atlas workflows. Events are the primary mechanism through which workflow state changes, errors, completions, and other significant occurrences are communicated to observers and other subsystems.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0308 workflow events.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined authoritatively in the [Atlas Master Glossary](../glossary.md) and MUST be interpreted consistently across all implementations:

| Term | Definition | Source |
|---|---|---|
| **Workflow** | A directed acyclic graph (DAG) defining a series of automation steps, inputs, outputs, and dependencies. | Glossary |
| **Workflow Instance** | A single execution of a workflow definition with concrete parameter bindings and runtime state. | RFC-0301 |
| **Event** | A discrete notification of a significant occurrence in the workflow execution lifecycle. | RFC-0301 |
| **Event Bus** | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| **Node** | An atomic unit of work within a workflow DAG, representing a single action or group of actions. | RFC-0301 |
| **Correlation ID** | A unique identifier linking related events across the workflow lifecycle. | RFC-0301 |
| **Trace ID** | A unique identifier for distributed tracing of a workflow execution. | RFC-0301 |
| **Dead Letter Queue (DLQ)** | A dedicated message queue containing events that could not be delivered to their target subscribers. | Glossary |
| **Subscriber** | A component that registers interest in specific event types or categories. | RFC-0301 |
| **Publisher** | A component that creates and emits events to the event bus. | RFC-0301 |
| **Checkpoint** | A saved snapshot of workflow state at a specific point, enabling recovery and resumption. | RFC-0315 |
| **Scheduler** | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | Glossary |

### 1.1 Normative Language

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2 Layer Boundaries

### 2.1 Responsibilities

The Workflow Events layer is responsible for:

- Defining the event model for workflow-specific occurrences.
- Specifying event categories, types, structures, and payloads.
- Defining event routing rules and subscription mechanisms.
- Establishing event ordering guarantees and durability requirements.
- Defining event sampling policies for high-volume scenarios.

### 2.2 Non-Responsibilities

The Workflow Events layer MUST NOT:

- Define the runtime event bus implementation (deferred to RFC-0005).
- Define event storage engines (deferred to RFC-0324).
- Define event visualization or dashboarding (deferred to RFC-0321).
- Implement event processing logic beyond routing and filtering.
- Manage event schema evolution (deferred to RFC-0318).

### 2.3 Dependencies

| Dependency | Direction | Rationale |
|---|---|---|
| RFC-0301 Workflow Overview | Consumes | Provides the overarching graph model |
| RFC-0304 Workflow Runtime | Consumes | Runtime provides the event emission infrastructure |
| RFC-0305 Workflow Lifecycle | Consumes | Lifecycle defines event emission triggers |
| RFC-0306 Workflow State | Consumes | State model provides event state tracking |
| RFC-0307 Workflow Context | Consumes | Context provides event correlation |
| RFC-0005 Runtime Event Bus | Consumes | Event bus provides routing infrastructure |
| RFC-1001 Common Event Model | Consumes | Common model provides base event structure |

### 2.4 Consumers

- RFC-0304 Workflow Runtime (event emission during execution)
- RFC-0305 Workflow Lifecycle (lifecycle transition events)
- RFC-0314 Workflow Error Handling (error events)
- RFC-0315 Workflow Recovery (recovery events)
- RFC-0316 Workflow Debugging (debug events)
- RFC-0321 Workflow Observability (metric events)

### 2.5 Providers

- RFC-0301 Workflow Overview (graph model)
- RFC-0005 Runtime Event Bus (routing infrastructure)
- RFC-1001 Common Event Model (base event structure)

### 2.6 Forbidden Dependencies

The Workflow Events layer MUST NOT depend on:

- Any runtime implementation technology (a systems programming language, Node.js, a desktop application framework, a desktop application framework).
- Any specific event bus implementation (Kafka, RabbitMQ, NATS, an in-memory data store Streams).
- Any operating system primitives (threads, processes, signals).
- Any GPU or hardware acceleration model.
- Any browser or presentation-layer technology.

---

## 3 Event Model Overview

Workflow events extend the common event model (RFC-1001) with workflow-specific event types, categories, and routing rules.

---

## 4 Event Categories

| Category | Description | Examples |
|---|---|---|
| Execution | Node execution state changes | NodeStarted, NodeCompleted, NodeFailed |
| Scheduling | Scheduling decisions and queue changes | NodeQueued, NodeDispatched, PriorityChanged |
| Error | Error conditions and handling | NodeFailed, RetryExhausted, CompensationFailed |
| Recovery | Recovery operations | CheckpointCreated, RecoveryStarted, RecoveryCompleted |
| Debug | Debugging instrumentation | DebugBreakpoint, DebugStep, DebugInspect |
| Observability | Performance and metric data | MetricEmitted, ResourceUtilized, TimingRecorded |
| Security | Security-related events | PermissionDenied, SandboxViolation, AuditLogged |
| Version | Version-related events | VersionChecked, CompatibilityChecked, MigrationApplied |
| Compliance | Compliance-related events | ComplianceChecked, ComplianceViolation, AuditTrailGenerated |

---

## 5 Event Structure

### 5.1 Event Fields

| Field | Type | Required | Description |
|---|---|---|---|
| event_id | String | YES | Unique event identifier |
| event_type | String | YES | Event type identifier |
| category | String | YES | Event category |
| timestamp | Timestamp | YES | Event emission time |
| workflow_id | String | YES | Associated workflow instance |
| node_id | String | NO | Associated node (if applicable) |
| correlation_id | String | YES | Correlation with parent event |
| trace_id | String | YES | Trace for distributed debugging |
| payload | Object | YES | Event-specific data |
| severity | String | YES | Event severity (info, warning, error, critical) |
| source | String | YES | Event source (node, scheduler, engine) |

### 5.2 Event Payloads

Event payloads are category-specific:

| Category | Payload Fields |
|---|---|
| Execution | node_id, previous_state, current_state, duration |
| Scheduling | node_id, policy, queue_position |
| Error | node_id, error_code, error_message, stack_trace |
| Recovery | recovery_type, checkpoint_id, duration |

---

## 6 Event Routing

### 6.1 Routing Rules

Events are routed through the runtime event bus (RFC-0005) according to these rules:

1. Events are published to the event bus upon emission.
2. Subscribers receive events based on event type and category filters.
3. Events are queued for offline subscribers.
4. Undeliverable events are sent to the dead letter queue.

### 6.2 Event Subscriptions

Subscriptions are defined by:

| Subscription Attribute | Description |
|---|---|
| Event Types | Filter by event type |
| Categories | Filter by event category |
| Workflow Instances | Filter by workflow ID |
| Nodes | Filter by node ID |
| Severity | Filter by severity level |

### 6.3 Subscription Priority

- Subscriptions MAY be assigned a priority level.
- Higher priority subscriptions MUST be delivered first.
- Priority levels are integers from 0 (lowest) to 100 (highest).

---

## 7 Event Lifecycle

### 7.1 Event Phases

| Phase | Description |
|---|---|
| Creation | Event is created by the emitting component |
| Publishing | Event is published to the event bus |
| Routing | Event is routed to subscribers |
| Delivery | Event is delivered to subscribers |
| Acknowledgment | Subscriber acknowledges receipt |
| Completion | Event processing is complete |

### 7.2 Event Durability

- Events MUST be persisted before publishing.
- Events MUST survive system failures.
- Events MUST be replayable from the event log.

---

## 8 Event Ordering

### 8.1 Ordering Guarantees

| Guarantee | Description | Scope |
|---|---|---|
| Causal | Causally related events maintain order | Workflow instance |
| Total | All events are totally ordered | Workflow instance |
| Partial | Only causally related events are ordered | System-wide |

### 8.2 Ordering Enforcement

- Events within a single workflow instance are totally ordered.
- Events across workflow instances are partially ordered.
- Event timestamps are used for ordering when sequence numbers collide.

---

## 9 Event Sampling

### 9.1 Sampling Rules

To manage event volume:

- High-frequency events MAY be sampled.
- Critical events (errors, security) MUST NOT be sampled.
- Sampling rates are configurable per event category.

---

## 10 Security

### 10.1 Event Security Controls

- Event payloads containing sensitive data MUST be encrypted.
- Event publishing MUST require authorization from the publisher identity.
- Event subscriptions MUST be validated against the subscriber's permission grants.
- Security events (PermissionDenied, SandboxViolation) MUST NOT be subject to sampling.
- Event audit logs MUST be immutable and tamper-evident.

### 10.2 Event Privacy

- Event payloads MUST NOT contain plaintext credentials, tokens, or secrets.
- Personal data in event payloads MUST be anonymized or pseudonymized per the platform privacy policy.
- Event retention periods MUST comply with the platform data retention policy.

---

## 11 Performance

### 11.1 Event Performance Requirements

- Event emission MUST complete within 1ms for in-memory event buses.
- Event routing to subscribers MUST complete within 5ms per subscriber.
- Event persistence MUST complete within 10ms for durable events.
- Dead letter queue delivery MUST complete within 100ms.

### 11.2 Resource Constraints

- The event bus MUST support at least 100,000 events per second.
- Event memory buffering MUST NOT exceed 10MB per workflow instance.
- Event replay from the log MUST complete within 30s for standard-definition workflows.

---

## 12 Compatibility

### 12.1 Event Format Compatibility

- Event schemas MUST be versioned and MUST include a compatibility header.
- Older event formats MUST be readable by newer implementations.
- New event fields MUST be optional and MUST have default values.
- Removed event fields MUST be migrated before the removal version is deployed.

### 12.2 Cross-Version Operations

- Event categories defined in older versions MUST remain valid in newer versions.
- Event type identifiers MUST be globally unique and MUST NOT be reused.

---

## 13 Compliance

### 13.1 Regulatory Compliance

- Event audit trails MUST satisfy SOX Section 404 requirements for operational process logging.
- Event retention MUST comply with the platform data retention policy.
- Security and compliance events MUST be retained for a minimum of 7 years.

### 13.2 Internal Policy Compliance

- All event emissions MUST be consistent with the Atlas Constitution Section 1 (Workflow Philosophy).
- Event privacy MUST comply with the platform data privacy policy.
- Event sampling policies MUST be reviewed annually for compliance adequacy.

---

## 14 Future Evolution

### 14.1 Planned Extensions

- Event-driven workflow orchestration (events triggering workflow creation) is planned for future versions.
- Cross-runtime event federation (multi-runtime event sharing) is under consideration.
- Machine learning-based event anomaly detection is exploratory.

### 14.2 Stability Guarantee

The event categories and structure defined in this RFC are stable and MUST NOT change without a formal RFC revision cycle.

---

## 15 Runtime Independence

This specification makes NO assumptions about:

- **Implementation language**: No a systems programming language, Node.js, Python, Go, or any other language is required.
- **Runtime environment**: No a desktop application framework, a desktop application framework, browser, or desktop framework dependency.
- **Event bus technology**: No Kafka, RabbitMQ, NATS, an in-memory data store Streams, or any specific message broker is mandated.
- **Operating system**: No thread model, process model, signal handling, or OS-specific primitive is assumed.
- **Hardware**: No GPU, VRAM, CPU affinity, or hardware acceleration is required.
- **Network topology**: No specific network protocol or topology is assumed.

The event model is purely logical and protocol-based. Any implementation MAY use any technology stack to realize this specification.

---

## 16 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST support nine event categories as defined in Section 4. | Category enumeration test |
| AC-02 | The implementation MUST define twelve event fields as defined in Section 5.1. | Field enumeration test |
| AC-03 | The implementation MUST enforce four routing rules as defined in Section 6.1. | Routing test |
| AC-04 | The implementation MUST define six event lifecycle phases as defined in Section 7.1. | Phase enumeration test |
| AC-05 | The implementation MUST support three ordering guarantees as defined in Section 8.1. | Ordering test |

---

## 17 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (graph model, event definitions) |
| RFC-0304 | Workflow Runtime (event emission infrastructure) |
| RFC-0305 | Workflow Lifecycle (lifecycle transition events) |
| RFC-0306 | Workflow State (event state tracking) |
| RFC-0307 | Workflow Context (event correlation) |
| RFC-0309 | Workflow Actions (action-related events) |
| RFC-0312 | Workflow Scheduler (scheduling events) |
| RFC-0313 | Workflow Parallelism (concurrent event ordering) |
| RFC-0314 | Workflow Error Handling (error events) |
| RFC-0315 | Workflow Recovery (recovery events) |
| RFC-0316 | Workflow Debugging (debug events) |
| RFC-0318 | Workflow Versioning (event schema evolution) |
| RFC-0319 | Workflow Security (security event controls) |
| RFC-0320 | Workflow Performance (performance metrics) |
| RFC-0321 | Workflow Observability (metric events) |
| RFC-0324 | Workflow Storage (event persistence) |
| RFC-0329 | Workflow Compatibility (event format compatibility) |
| RFC-0330 | Workflow Compliance (compliance events) |
| RFC-0005 | Runtime Event Bus (routing infrastructure) |
| RFC-1001 | Common Event Model (base event structure) |
| RFC-1002 | Common State Model (base state types) |
| ADR-0012 | Contract-First Specification-Driven Development |
| JSON Schema | contracts/json/workflow.schema.json |
| Catalog | specs/workflow/catalog/workflow-events.md |
| Glossary | specs/glossary.md (Atlas Master Glossary) |


---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |
