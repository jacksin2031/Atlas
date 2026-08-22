# Workflow Event Types

Catalog document for workflow-event-types.

This catalog document enumerates all Workflow Event types.

## Event Categories

| Category | Prefix | Description |
|---|---|---|
| Execution | EXEC_* | Workflow execution lifecycle events |
| Node | NODE_* | Node state change events |
| Action | ACTION_* | Action execution events |
| Trigger | TRIGGER_* | Trigger firing events |
| Condition | COND_* | Condition evaluation events |
| Error | ERR_* | Error events |
| Recovery | RECOV_* | Recovery events |
| Debug | DBG_* | Debug events |
| Lifecycle | LC_* | Runtime lifecycle events |
| Security | SEC_* | Security events |

## Event Schema

All events conform to the base event schema:

| Field | Type | Required | Description |
|---|---|---|---|
| event_id | UUID v7 | Yes | Unique event identifier |
| event_type | string | Yes | Event type code |
| category | enum | Yes | Event category |
| timestamp_ns | uint64 | Yes | Nanosecond timestamp |
| workflow_id | string | Yes | Associated workflow ID |
| execution_id | string | Yes | Associated execution ID |
| correlation_id | string | Yes | Correlation chain |
| source | string | Yes | Event source component |
| payload | object | Yes | Event-specific data |
| metadata | object | No | Additional context |

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
