# Workflow Trigger Types

Catalog document for workflow-trigger-types.

This catalog document enumerates all Workflow Trigger types.

## Trigger Categories

| Category | Type | Description | Example |
|---|---|---|---|
| Temporal | Cron | Recurring schedule | Every 5 minutes |
| Temporal | Delay | One-time delay | After 30 seconds |
| Temporal | Deadline | Time-based expiration | After 1 hour |
| Event | WorkflowCompleted | Fired when a workflow completes | Workflow A -> Workflow B |
| Event | NodeCompleted | Fired when a node completes | Node X -> Trigger Y |
| Event | ErrorOccurred | Fired on error events | Error -> Alert |
| Event | Custom | User-defined event | External webhook |
| Manual | Approval | Requires human approval | Approve button |
| Manual | API | API-triggered execution | REST call |
| Condition | Expression | Evaluates a condition | Value > threshold |
| Condition | StateChange | Fires on state transitions | Status = Ready |
| Condition | ResourceThreshold | Fires on resource metrics | CPU > 80% |

## Trigger Registration

Triggers are registered with:

| Field | Type | Required | Description |
|---|---|---|---|
| trigger_id | string | Yes | Unique trigger identifier |
| type | enum | Yes | Trigger category |
| source | string | Yes | Event or condition source |
| target | string | Yes | Workflow/node to activate |
| condition | expression | No | Additional filter |
| priority | int | No | Firing priority (lower = higher priority) |

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
