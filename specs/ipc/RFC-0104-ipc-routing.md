# RFC-0104: IPC Routing

RFC: RFC-0104
Title: IPC Routing
Status: Accepted
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0101 IPC Overview
  - RFC-0102 Message Model
  - RFC-0103 Transport
Required By:
  - RFC-0105 Channel
  - RFC-0108 Reliability
Supersedes: None
Superseded By: None
Category: IPC
Layer: Routing
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010
Constitution References:
  - Section 4.2 (Message Routing)
Related RFCs:
  - RFC-0101 IPC Overview
  - RFC-0102 Message Model
  - RFC-0103 Transport
  - RFC-0105 Channel
  - RFC-0108 Reliability
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x
---

## Normative Status

## Authority

This RFC is the authoritative specification for the IPC subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| IPC | Inter-Process Communication; the unified messaging fabric enabling cross-process data exchange. | Glossary |
| Channel | A bidirectional or unidirectional communication pathway between two endpoints. | Glossary |
| Transport | The underlying mechanism by which messages are delivered between processes. | Glossary |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | Glossary |

---
This specification is Normative. Every Atlas IPC implementation MUST conform to the routing protocols, rule evaluation order, scheduling disciplines, and reliability mechanisms defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and all active IPC-related ADRs.

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
4. [Routing Engine](#4-routing-engine)
5. [Routing Rules](#5-routing-rules)
6. [Static Route](#6-static-route)
7. [Dynamic Route](#7-dynamic-route)
8. [Broadcast](#8-broadcast)
9. [Directed Route](#9-directed-route)
10. [Priority Scheduling](#10-priority-scheduling)
11. [Retry Logic](#11-retry-logic)
12. [Dead Letter Queue](#12-dead-letter-queue)
13. [Routing Tables](#13-routing-tables)
14. [Discovery](#14-discovery)
15. [Registration](#15-registration)
16. [Routing Metrics](#16-routing-metrics)
17. [Glossary](#17-glossary)
18. [Acceptance Criteria](#18-acceptance-criteria)
19. [References](#19-references)
---


## 2 Goals

- **Deterministic Path Selection**: Given identical routing state and identical messages, the Routing Engine MUST always select the same delivery path.
- **Rule-Based Flexibility**: Routing decisions MUST be governed by composable, evaluable rules that support static and dynamic configurations.
- **Priority Preservation**: Message priority MUST be honored end-to-end across all routing hops, with explicit priority inheritance semantics.
- **Storm Prevention**: Broadcast and multicast routing MUST include bounded fan-out and anti-loop mechanisms to prevent network saturation.
- **Reliable Delivery Guarantee**: Failed messages MUST be retried according to configurable policies and ultimately diverted to a Dead Letter Queue for inspection.
- **Endpoint Discovery**: The Routing Engine MUST support automatic discovery and registration of available message endpoints.
- **Metric-Driven Routing**: Route selection MAY incorporate quantitative metrics such as latency, hop count, load, and reliability scores.

---

- RFC-0327 Workflow IPC (consumes IPC routing model)


## 4 Routing Engine

### 4.1 Architecture

The Routing Engine is the central decision-making component of the IPC subsystem. It receives messages from the Transport Layer, evaluates routing rules against the message metadata and current routing state, selects a delivery path, and forwards the message to the appropriate outbound channel.

```mermaid
graph TD
    A["Inbound Message from Transport"] --> B["Routing Engine"]
    B --> C["Rule Evaluator"]
    B --> D["Routing Table Lookup"]
    B --> E["Priority Scheduler"]
    C --> F["Static Router"]
    C --> G["Dynamic Router"]
    C --> H["Broadcast Router"]
    C --> I["Directed Router"]
    F --> J["Route Resolver"]
    G --> J
    H --> J
    I --> J
    J --> K["Delivery Dispatcher"]
    K --> L["Outbound Transport"]
    E --> K
    D --> C
`

### 4.2 Responsibilities

The Routing Engine MUST perform the following functions:

| Responsibility | Description |
|---|---|
| Rule Evaluation | Evaluate routing rules in defined priority order against incoming messages. |
| Route Resolution | Select the optimal delivery path from available routes based on rules and metrics. |
| Priority Scheduling | Queue and schedule messages according to their priority attributes. |
| Retry Orchestration | Manage retry policies and backoff strategies for failed deliveries. |
| Dead Letter Management | Divert unrecoverable messages to the Dead Letter Queue. |
| Discovery Coordination | Coordinate with the Discovery subsystem for endpoint registration and lookup. |
| Metrics Collection | Gather and expose routing performance metrics. |

### 4.3 Invariants

- **Single Decision Point**: Every message MUST pass through exactly one Routing Engine instance before reaching the Transport Layer.
- **Immutable Metadata**: The Routing Engine MUST NOT modify the inbound message payload. Only routing metadata MAY be appended.
- **Stateless Fallback**: If the Routing Engine loses its routing table state, it MUST fall back to directed routing only. Broadcast and dynamic routes are suspended.
---

The Routing Engine MUST enforce the following rule ordering constraints:

1. **Security Rules** (evaluated first): Rules governing access control and origin validation.
2. **Drop Rules** (evaluated second): Rules that unconditionally drop messages.
3. **Static Rules** (evaluated third): Rules referencing static route entries.
4. **Dynamic Rules** (evaluated fourth): Rules referencing dynamically discovered endpoints.
5. **Default Rule** (evaluated last): The catch-all rule, which MUST exist and MUST be configurable.

### 5.4 Rule Composition

Rules MAY be composed into rule groups. A rule group is evaluated atomically: either all rules in the group match, or none do. Rule groups enable modular routing policies that can be enabled, disabled, or replaced as a unit.

- **AND Composition**: All constituent rules MUST match for the group to match.
- **OR Composition**: At least one constituent rule MUST match for the group to match.

### 5.5 Rule Persistence

All routing rules MUST be persisted in the routing configuration store. The Routing Engine MUST reload all rules on startup from the persisted store. In-memory rules MUST NOT survive a restart.
---

### 6.4 Route Persistence

Static routes MUST be stored in a persistent configuration store. The Routing Engine MUST validate all static routes at load time and reject entries with unresolved targets or invalid patterns.

### 6.5 Route Tables

Static routes are organized into routing tables. Each table has a unique name and MAY contain overlapping patterns. When multiple tables define routes for the same pattern, the table with the highest explicit priority is consulted first.

---



### 7.1 Overview

A Dynamic Route is a route entry whose target is determined at runtime through the Discovery subsystem. Dynamic routes enable automatic adaptation to endpoint availability, health status, and load conditions.

### 7.2 Route Discovery

Dynamic routes are discovered through the following mechanisms:

| Mechanism | Description |
|---|---|
| Health-Based | Routes are created or removed based on endpoint health probes. |
| Load-Based | Routes are distributed proportionally to endpoint load metrics. |
| Capability-Based | Routes are matched to endpoints advertising compatible capabilities. |
| Lease-Based | Routes are created for the duration of an endpoint registration lease. |

### 7.3 Route Adaptation

The Routing Engine MUST support automatic route adaptation:

1. **Endpoint Addition**: When a new endpoint is discovered, the Routing Engine MUST evaluate existing dynamic rules and create corresponding route entries.
2. **Endpoint Removal**: When an endpoint becomes unavailable, the Routing Engine MUST remove or redirect routes pointing to that endpoint.
3. **Load Shift**: When endpoint load exceeds configured thresholds, the Routing Engine MUST redistribute routes to lighter endpoints.

### 7.4 Route Optimization

The Routing Engine MAY optimize dynamic routes based on collected routing metrics. Optimization decisions MUST be deterministic: given the same metric state, the optimization algorithm MUST produce identical route selections.
---


### 8.4 Broadcast Delivery Guarantees

Broadcast delivery is AT-MOST-ONCE. The Routing Engine does NOT guarantee that all matching endpoints receive every broadcast message. Endpoints that are temporarily unreachable when a broadcast is dispatched will NOT receive retroactive delivery.

---

    alt TTL > 0
        RE->>Endpoint1: Deliver broadcast (seq=N)
        RE->>Endpoint2: Deliver broadcast (seq=N)
        RE->>EndpointN: Deliver broadcast (seq=N)
    else TTL <= 0
        RE->>DL: Drop expired broadcast
    end
    Endpoint1-->>Sender: Ack received
    Endpoint2-->>Sender: Ack received
    EndpointN-->>Sender: Ack received

### 9.1 Overview

Directed routing delivers a message to a single, specific endpoint. It is the default routing mode when no broadcast, dynamic, or static pattern match applies.

### 9.2 Destination Resolution

The Routing Engine resolves directed destinations through the following lookup order:

1. **Explicit Address**: The message metadata contains a fully qualified endpoint address.
2. **Service Registry**: The Routing Engine queries the registration database for the target service name.
3. **Capability Lookup**: The Routing Engine searches for an endpoint advertising the required capability.
4. **Default Endpoint**: If no match is found, the message is routed to the configured default endpoint.

### 9.3 Route Selection

When multiple endpoints satisfy a directed routing criterion, the Routing Engine MUST select the route with the highest composite metric score. If scores are equal, the endpoint with the lowest registered ID is selected deterministically.

### 9.4 Unreachable Destinations

If the resolved destination endpoint is unreachable, the Routing Engine MUST:

1. Apply the configured retry policy (see Section 11).
2. If all retries are exhausted, divert the message to the Dead Letter Queue (see Section 12).
---


---

| attempt_count | Number of delivery attempts made. |
| last_error | Error code from the most recent failed attempt. |
| next_retry_at | Timestamp of the next scheduled retry. |
| route_history | Ordered list of routes attempted. |

### 11.4 Retry Exhaustion

When all retry attempts are exhausted, the Routing Engine MUST divert the message to the Dead Letter Queue. The diversion MUST include the full retry state for diagnostic purposes.
---

| retention_period | How long messages are retained in the DLQ | 30 days |
| max_dlq_size | Maximum number of messages in the DLQ | 1,000,000 |
| eviction_policy | How to evict old messages when the limit is reached | FIFO |
| access_control | Who may inspect or replay DLQ messages | Admin role |
| notification_enabled | Whether to notify admins of DLQ entries | True |

### 12.3 DLQ Storage

The DLQ MUST persist messages in durable storage. Each DLQ entry contains:

- The original message payload.
- The complete routing metadata.
- The full retry history.
- The error conditions encountered.
- Timestamps for receipt, each retry, and DLQ insertion.

### 12.4 DLQ Operations

Authorized operators MAY perform the following DLQ operations:

| Operation | Description |
|---|---|
| inspect | View DLQ entries and associated metadata. |
| replay | Re-submit a DLQ message into the routing pipeline. |
| dead_letter | Permanently remove a DLQ entry. |
| batch_delete | Remove multiple DLQ entries matching a filter. |

### 12.5 DLQ Retention

Messages in the DLQ MUST be automatically purged after the retention period elapses. The eviction policy determines which messages are purged first when the DLQ size limit is approached.
---

- **Checksum Validation**: The Routing Engine validates the table checksum on every load. A mismatch indicates corruption and triggers a table rebuild from the configuration store.

### 13.4 Table Partitioning

For large-scale deployments, routing tables MAY be partitioned by domain. Each partition is managed independently and contributes to the overall routing decision. Partition boundaries are defined by route pattern prefixes.

---


### 14.4 Discovery Cache

The Routing Engine maintains an in-memory cache of discovered endpoints. The cache MUST be invalidated on any of the following events:

- Endpoint registration or deregistration.
- Health probe failure.
- Capability advertisement change.
- Cache entry TTL expiration.
---

| Lease expiration | Automatic deregistration after max retries on renewal failure. |
| Health probe failure | Automatic deregistration after configured consecutive failures. |
| Administrative revocation | Forced deregistration by system operator. |

### 15.4 Lease Renewal

Active endpoints MUST renew their leases before expiry. The renewal process is identical to the initial registration but does not require capability re-advertisement unless capabilities have changed.

---

Routing metrics MUST be persisted for a minimum of 24 hours. Metrics older than the retention period MAY be aggregated into summary statistics and discarded.
---

- Establishing the boundaries between IPC layers.


## 18 Acceptance Criteria

### AC-401
- **Requirement**: The Routing Engine MUST evaluate routing rules in ascending priority order.
- **Verification**: Create two rules with priorities 1 and 10; send a message matching both.
- **Expected Result**: The rule with priority 1 is evaluated and applied first.

### AC-402
- **Requirement**: The Routing Engine MUST support at least five priority levels (Critical through Idle).
- **Verification**: Assign each of the five priority levels to separate messages and observe queue ordering.
- **Expected Result**: Messages dequeue in strict priority order: Critical first, Idle last.

### AC-403
- **Requirement**: Broadcast messages MUST include a monotonically increasing sequence number.
- **Verification**: Send 100 broadcast messages and inspect sequence numbers.
- **Expected Result**: All sequence numbers are unique and strictly increasing.

### AC-404
- **Requirement**: The Routing Engine MUST enforce a maximum broadcast fan-out of 100 endpoints by default.
- **Verification**: Configure a broadcast pattern matching 150 endpoints and send a broadcast.
- **Expected Result**: The message is delivered to at most 100 endpoints; a truncation log entry is created.

### AC-405
- **Requirement**: Messages that exhaust all retry attempts MUST be diverted to the Dead Letter Queue.
- **Verification**: Configure a route with max_attempts=3 and a target that always fails; send 5 messages.
- **Expected Result**: All 5 messages appear in the DLQ after 3 failed delivery attempts each.

### AC-406
- **Requirement**: The Routing Engine MUST implement exponential backoff with jitter for retry delays.
- **Verification**: Measure the time intervals between consecutive retry attempts.
- **Expected Result**: Intervals follow exponential growth with random jitter; no two intervals are identical.

### AC-407
- **Requirement**: Static routes MUST take precedence over dynamic routes in rule evaluation.
- **Verification**: Configure a static route and a dynamic route for the same pattern; send a matching message.
- **Expected Result**: The static route target is used for delivery.

### AC-408
- **Requirement**: The Routing Engine MUST validate all routing rules at startup and reject invalid rules.
- **Verification**: Inject a rule with a missing required field and restart the Routing Engine.
- **Expected Result**: The invalid rule is rejected; the Routing Engine starts with the remaining valid rules.

### AC-409
- **Requirement**: Broadcast messages with TTL=0 MUST be dropped immediately.
- **Verification**: Send a broadcast message with TTL set to 0.
- **Expected Result**: The message is dropped; no endpoints receive it.

### AC-410
- **Requirement**: Priority inheritance MUST propagate priority exactly one generation.
- **Verification**: Send a Critical message that triggers a follow-up message which triggers a second follow-up.
- **Expected Result**: The first follow-up inherits Critical priority; the second follow-up defaults to Normal.
### AC-411
- **Requirement**: The Routing Engine MUST maintain separate priority queues per outbound channel.
- **Verification**: Configure two outbound channels; enqueue mixed-priority messages on both.
- **Expected Result**: Each channel dequeues messages in strict priority order independently.

### AC-412
- **Requirement**: A message older than the configured aging threshold MUST have its priority boosted by one level.
- **Verification**: Set aging threshold to 5 seconds; enqueue an Idle message and wait 6 seconds.
- **Expected Result**: The message priority is promoted from Idle to Low.

### AC-413
- **Requirement**: The DLQ MUST persist messages in durable storage with full retry history.
- **Verification**: Divert a message to the DLQ; inspect the stored entry.
- **Expected Result**: The entry contains the original payload, routing metadata, retry history, and all error conditions.

### AC-414
- **Requirement**: DLQ entries MUST be automatically purged after the retention period elapses.
- **Verification**: Set retention to 1 second; insert an entry and wait 2 seconds.
- **Expected Result**: The entry is removed from the DLQ.

### AC-415
- **Requirement**: The Routing Engine MUST support pattern matching using exact, prefix, suffix, and wildcard operators.
- **Verification**: Register routes with each pattern type and send messages matching each.
- **Expected Result**: Each message is routed to the correct target based on its pattern type.

### AC-416
- **Requirement**: Endpoint registration MUST include a lease with a configurable duration.
- **Verification**: Register an endpoint with a 30-second lease and observe deregistration at 30 seconds.
- **Expected Result**: The endpoint is automatically deregistered after lease expiry.

### AC-417
- **Requirement**: The Routing Engine MUST support rule composition using AND and OR operators.
- **Verification**: Create a rule group with AND composition where one rule does not match.
- **Expected Result**: The group does not match; the OR composition group with at least one matching rule does match.

### AC-418
- **Requirement**: Dynamic routes MUST be created when a new endpoint is discovered.
- **Verification**: Start an endpoint that advertises a capability matching an active dynamic rule.
- **Expected Result**: A new dynamic route entry is created pointing to the discovered endpoint.

### AC-419
- **Requirement**: Dynamic routes MUST be removed when an endpoint becomes unavailable.
- **Verification**: Stop an endpoint that has active dynamic routes.
- **Expected Result**: All dynamic routes pointing to that endpoint are removed within the health probe interval.

### AC-420
- **Requirement**: The Routing Engine MUST compute composite route scores using configurable weights.
- **Verification**: Configure unequal weights for latency and reliability; send messages to two endpoints with different scores.
- **Expected Result**: The endpoint with the higher weighted composite score is selected.
### AC-421
- **Requirement**: Full routing table updates MUST be atomic.
- **Verification**: Perform a bulk table update while messages are being routed.
- **Expected Result**: No message observes a partially updated table; all messages see either the old or new table.

### AC-422
- **Requirement**: The Routing Engine MUST reject messages from unregistered endpoints.
- **Verification**: Send a message from an endpoint that has not registered.
- **Expected Result**: The message is dropped with an UnauthorizedSource error.

### AC-423
- **Requirement**: Broadcast loop detection MUST terminate propagation when an endpoint is visited twice.
- **Verification**: Configure a broadcast pattern that would cause a message to reach the same endpoint via two paths.
- **Expected Result**: The second delivery attempt is suppressed; the broadcast terminates at that branch.

### AC-424
- **Requirement**: The Routing Engine MUST support at least 1,000 concurrent static route entries.
- **Verification**: Load 1,000 static routes and send messages matching each.
- **Expected Result**: All messages are routed correctly within the latency budget.

### AC-425
- **Requirement**: Retry policies MUST distinguish between retryable and non-retryable errors.
- **Verification**: Send a message that receives a non-retryable error code.
- **Expected Result**: The message is immediately diverted to the DLQ without retry.

### AC-426
- **Requirement**: The Routing Engine MUST log all broadcast truncation events.
- **Verification**: Send a broadcast exceeding the fan-out limit.
- **Expected Result**: A log entry is created documenting the truncation, the number of endpoints reached, and the sequence number.

### AC-427
- **Requirement**: Endpoint capabilities MUST be matchable against routing rule conditions.
- **Verification**: Register an endpoint with capability orders.created; create a rule matching that capability.
- **Expected Result**: The rule matches and routes messages to the endpoint.

### AC-428
- **Requirement**: The DLQ MUST support manual replay of individual messages.
- **Verification**: Retrieve a message from the DLQ and replay it.
- **Expected Result**: The message re-enters the routing pipeline and is delivered to the appropriate target.

### AC-429
- **Requirement**: The Routing Engine MUST support batch deletion of DLQ entries matching a filter.
- **Verification**: Insert 100 DLQ entries; delete those matching a specific source pattern.
- **Expected Result**: Exactly the matching entries are removed; non-matching entries remain.

### AC-430
- **Requirement**: Route selection MUST be deterministic when multiple endpoints have identical composite scores.
- **Verification**: Register two endpoints with identical metrics; send 100 messages targeting both.
- **Expected Result**: The same endpoint is selected for all 100 messages (lowest registered ID tie-break).
### AC-431
- **Requirement**: The Routing Engine MUST support the continue action in routing rules to allow subsequent rule evaluation.
- **Verification**: Create two rules; the first has action continue, the second has action forward.
- **Expected Result**: Both rules are evaluated; the second rule forward action is applied.

### AC-432
- **Requirement**: Registration leases MUST support a renewal window that triggers auto-renewal.
- **Verification**: Register an endpoint with a 10-second lease and 2-second renewal window.
- **Expected Result**: The lease is automatically renewed at or before 8 seconds remaining.

### AC-433
- **Requirement**: The Routing Engine MUST enforce a global default route that catches all unmatched messages.
- **Verification**: Send a message that matches no configured static or dynamic rules.
- **Expected Result**: The message is routed to the configured default endpoint.

### AC-434
- **Requirement**: Dynamic route adaptation MUST redistribute routes when endpoint load exceeds a threshold.
- **Verification**: Configure a load threshold of 80 percent; simulate one endpoint exceeding it.
- **Expected Result**: Routes are redistributed to lighter endpoints.

### AC-435
- **Requirement**: The Routing Engine MUST support rate limiting of broadcast messages per pattern.
- **Verification**: Send broadcasts at 20/sec against a pattern with a 10/sec rate limit.
- **Expected Result**: Only 10 broadcasts per second are forwarded; the rest are queued or dropped per policy.

### AC-436
- **Requirement**: Priority preemption MUST return preempted messages to the bottom of their original priority queue.
- **Verification**: Fill a Normal queue; inject a Critical message to trigger preemption.
- **Expected Result**: Normal messages are returned to the bottom of the Normal queue after the Critical messages drain.

### AC-437
- **Requirement**: The Routing Engine MUST validate routing table checksums on every load.
- **Verification**: Tamper with a persisted routing table entry and restart the Routing Engine.
- **Expected Result**: The checksum mismatch is detected; the table is rebuilt from the configuration store.

### AC-438
- **Requirement**: DLQ entries MUST include timestamps for receipt, each retry, and DLQ insertion.
- **Verification**: Divert a message to the DLQ; inspect the entry timestamps.
- **Expected Result**: All timestamps are present and chronologically ordered.

### AC-439
- **Requirement**: The Routing Engine MUST support at least four broadcast pattern types (exact, prefix, suffix, wildcard).
- **Verification**: Configure each pattern type and send a broadcast.
- **Expected Result**: Each pattern correctly identifies its matching endpoints.

### AC-440
- **Requirement**: Endpoint deregistration MUST occur within 2 heartbeat intervals after health probe failure.
- **Verification**: Configure a 5-second heartbeat; stop an endpoint and observe deregistration.
- **Expected Result**: The endpoint is deregistered within 10 seconds of the last missed heartbeat.
### AC-441
- **Requirement**: The Routing Engine MUST support rule groups with at least 100 composed rules.
- **Verification**: Create a rule group with 100 rules and activate it.
- **Expected Result**: The group evaluates correctly within the routing latency budget.

### AC-442
- **Requirement**: Static route weights MUST influence load distribution proportionally.
- **Verification**: Create two static routes with weights 3 and 1; send 400 messages.
- **Expected Result**: Up to 300 messages are routed to the weight-3 target and 100 to the weight-1 target.

### AC-443
- **Requirement**: The Routing Engine MUST expose routing metrics at a configurable collection interval.
- **Verification**: Set the collection interval to 5 seconds and observe metric exports.
- **Expected Result**: Metrics are exported at the configured interval with all defined metric types.

### AC-444
- **Requirement**: Retry jitter MUST be regenerated on every retry attempt.
- **Verification**: Send a message that requires 3 retries; measure each retry delay.
- **Expected Result**: Each retry delay differs due to regenerated jitter; all delays remain within the exponential backoff bounds.

### AC-445
- **Requirement**: The Routing Engine MUST support table partitioning by route pattern prefix.
- **Verification**: Create two partitions with prefix-based boundaries; send messages matching each.
- **Expected Result**: Messages are routed to the correct partition and resolved to the correct target.

### AC-446
- **Requirement**: DLQ access MUST be restricted to operators with the admin role.
- **Verification**: Attempt DLQ inspection with a non-admin credential.
- **Expected Result**: Access is denied with an AuthorizationDenied error.

### AC-447
- **Requirement**: The Routing Engine MUST support the drop action in routing rules.
- **Verification**: Create a rule with action drop matching a specific source; send a message from that source.
- **Expected Result**: The message is silently dropped; no delivery attempt is made.

### AC-448
- **Requirement**: The Routing Engine MUST support the redirect action in routing rules.
- **Verification**: Create a rule with action redirect to a different target; send a matching message.
- **Expected Result**: The message is rerouted to the redirect target instead of the original destination.

### AC-449
- **Requirement**: The DLQ MUST enforce a maximum size limit and apply the configured eviction policy when reached.
- **Verification**: Fill the DLQ to its maximum size; insert one additional message.
- **Expected Result**: The oldest message is evicted per the FIFO policy; the new message is accepted.

### AC-450
- **Requirement**: The Routing Engine MUST support capability-based route filtering where endpoints only receive messages matching their advertised capabilities.
- **Verification**: Register two endpoints with different capabilities; send a message matching only one.
- **Expected Result**: Only the endpoint with the matching capability receives the message.
### AC-451
- **Requirement**: The Routing Engine MUST record the complete route history for every message in the DLQ.
- **Verification**: Send a message that traverses 3 routes before failing; inspect the DLQ entry.
- **Expected Result**: The DLQ entry contains all 3 route attempts in chronological order.

### AC-452
- **Requirement**: Broadcast messages MUST be delivered in a single pass; no endpoint receives duplicates.
- **Verification**: Configure a broadcast pattern that matches 50 endpoints; inspect each recipient received count.
- **Expected Result**: Each endpoint receives exactly one copy of the broadcast message.

### AC-453
- **Requirement**: The Routing Engine MUST support at least 10,000 concurrent dynamic route entries.
- **Verification**: Discover 10,000 endpoints with matching capabilities and send routing traffic.
- **Expected Result**: All dynamic routes are created and messages are routed correctly within latency bounds.

### AC-454
- **Requirement**: The Routing Engine MUST support the backoff_multiplier parameter configurable per retry policy.
- **Verification**: Create two retry policies with different backoff multipliers; measure retry intervals.
- **Expected Result**: Retry intervals grow at different exponential rates matching the configured multipliers.

### AC-455
- **Requirement**: The Routing Engine MUST support rule evaluation logging for audit purposes.
- **Verification**: Enable rule evaluation logging; send a message and inspect logs.
- **Expected Result**: Logs record the rule ID, priority, match result, and action taken for every evaluated rule.

### AC-456
- **Requirement**: Endpoint registration MUST include a unique lease ID for tracking and renewal.
- **Verification**: Register two endpoints and inspect their lease IDs.
- **Expected Result**: Each endpoint has a distinct, non-colliding lease ID.

### AC-457
- **Requirement**: The Routing Engine MUST reject registration requests from endpoints with expired credentials.
- **Verification**: Attempt registration with expired credentials.
- **Expected Result**: The registration is rejected with an AuthenticationExpired error.

### AC-458
- **Requirement**: Dynamic routes MUST support a minimum health score threshold below which endpoints are excluded.
- **Verification**: Set the health threshold to 50 percent; mark an endpoint at 40 percent health.
- **Expected Result**: The endpoint is excluded from dynamic route selection.

### AC-459
- **Requirement**: The Routing Engine MUST support atomic rule group deletion.
- **Verification**: Create a rule group with 50 rules; delete the group atomically.
- **Expected Result**: All 50 rules are removed simultaneously; no partial state is observable.

### AC-460
- **Requirement**: The Routing Engine MUST support per-rule TTL expiration for automatic cleanup.
- **Verification**: Create a rule with a 60-second TTL and wait 61 seconds.
- **Expected Result**: The rule is automatically removed from the active rule set.
### AC-461
- **Requirement**: Broadcast messages MUST include the originating endpoint identifier for traceability.
- **Verification**: Send a broadcast and inspect the message metadata at recipients.
- **Expected Result**: The originating endpoint identifier is present in all broadcast messages.

### AC-462
- **Requirement**: The Routing Engine MUST support the dlq action in routing rules for direct DLQ diversion.
- **Verification**: Create a rule with action dlq matching a specific error condition.
- **Expected Result**: Messages matching the condition are directly diverted to the DLQ without retry.

### AC-463
- **Requirement**: The Routing Engine MUST enforce a maximum message TTL at the routing layer.
- **Verification**: Send a message with TTL=0.
- **Expected Result**: The message is dropped immediately at the routing layer.

### AC-464
- **Requirement**: DLQ notification MUST be sent when a new entry is created.
- **Verification**: Divert a message to the DLQ with notifications enabled; monitor the notification channel.
- **Expected Result**: A notification is delivered to the admin notification channel.

### AC-465
- **Requirement**: The Routing Engine MUST support route pattern compilation to an optimized lookup structure.
- **Verification**: Load 10,000 static routes with mixed pattern types; measure lookup latency.
- **Expected Result**: Average lookup latency is under 100 microseconds per message.

### AC-466
- **Requirement**: The Routing Engine MUST maintain a version number for each routing table that increments on every update.
- **Verification**: Perform three sequential table updates and inspect the version.
- **Expected Result**: The version increments by 1 after each update.

### AC-467
- **Requirement**: Priority queues MUST support a configurable preemption threshold.
- **Verification**: Set the preemption threshold to 10; fill the queue to 11 with Low messages; inject a Critical message.
- **Expected Result**: Lower-priority messages are preempted and returned to the bottom of their queue.

### AC-468
- **Requirement**: The Routing Engine MUST support metric-based route scoring with at least four weighted factors.
- **Verification**: Configure scores based on latency, reliability, load, and hop count; send messages to multiple endpoints.
- **Expected Result**: Routes are selected according to the computed composite scores.

### AC-469
- **Requirement**: The Routing Engine MUST log all rule evaluation failures with the offending message metadata.
- **Verification**: Send a message that causes a rule evaluation to fail (e.g., missing attribute).
- **Expected Result**: A log entry is created with the rule ID, failure reason, and complete message metadata.

### AC-470
- **Requirement**: The Routing Engine MUST support graceful degradation to directed-only routing when the routing table is corrupted.
- **Verification**: Corrupt the routing table; send a mix of broadcast, dynamic, and directed messages.
- **Expected Result**: Only directed messages are routed; broadcast and dynamic messages are dropped or sent to the DLQ.
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
| 1.0.0 | Accepted | 2026-06-30 | Atlas Team | Initial publication |
| 1.1.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






