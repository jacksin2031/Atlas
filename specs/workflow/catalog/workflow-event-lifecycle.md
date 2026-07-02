# Workflow Event Lifecycle

Catalog document for workflow-event-lifecycle.

This catalog document defines the lifecycle states and transitions for Workflow Events.

## Event Lifecycle States

| State | Description | Transitions To |
|---|---|---|
| Generated | Event is emitted by a workflow component | Queued, Dropped |
| Queued | Event is in the delivery queue | Delivered, Expired, Dropped |
| Delivered | Event has been delivered to all subscribers | Acknowledged, Failed |
| Acknowledged | Event was acknowledged by all subscribers | Resolved |
| Failed | Event delivery failed | Retrying, Dropped |
| Retrying | Event is being retried for delivery | Delivered, Failed, Expired |
| Expired | Event TTL elapsed before delivery | Dropped |
| Dropped | Event was discarded | Resolved |
| Resolved | Event lifecycle fully resolved | N/A |

## Event Delivery Guarantees

| Guarantee | Description | At-Least-Once | At-Most-Once | Exactly-Once |
|---|---|---|---|---|
| At-Least-Once | Event is delivered one or more times | Yes | No | Partial |
| At-Most-Once | Event is delivered zero or one time | No | Yes | No |
| Exactly-Once | Event is delivered precisely one time | No | No | Yes |

## Event Ordering

Events within a single workflow execution MUST maintain causal ordering. Events across independent workflow executions have no ordering guarantees unless explicitly correlated via correlation IDs.

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
