# Workflow Event Delivery

Catalog document for workflow-event-delivery.

This catalog document defines event delivery models for the workflow system.

## Delivery Models

| Model | Description | Use Case |
|---|---|---|
| Synchronous | Event processed before continuation | Critical path events |
| Asynchronous | Event processed in background | Logging, metrics |
| Fan-Out | Event delivered to multiple subscribers | Broadcast notifications |
| Fan-In | Multiple events aggregated before processing | Barrier synchronization |
| Stream | Continuous event stream | Real-time monitoring |

## Event Deduplication

To prevent duplicate event processing, implementations MUST support event deduplication via:

1. **Event ID**: Unique event identifiers (UUID v7) enable exact-duplicate detection.
2. **Correlation Chain**: Full correlation ID chains enable contextual deduplication.
3. **Idempotency Keys**: Application-level deduplication for at-least-once delivery.

## Event Replay

Events MUST support replay for debugging and testing purposes:

- Event stores MUST retain events for at least 24 hours by default.
- Replay MUST preserve event ordering within correlation chains.
- Replay MUST be configurable per event category.

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
