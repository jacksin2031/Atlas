# Workflow Action Lifecycle

Catalog document for workflow-action-lifecycle.

This catalog document defines the lifecycle states and transitions for Workflow Actions.

## Action Lifecycle States

| State | Description | Transitions To |
|---|---|---|
| Declared | Action is declared in the workflow manifest | Registered, Invalid |
| Registered | Action is registered with the action registry | Ready |
| Ready | Action is ready to be executed by a node | Executing, Cancelled |
| Executing | Action is actively executing | Completed, Failed, TimedOut |
| Completed | Action completed successfully | Compensated (if non-idempotent) |
| Failed | Action failed with an error | Retrying, Compensated, Aborted |
| TimedOut | Action exceeded its timeout | Compensated, Aborted |
| Compensated | Action's compensation was executed | Resolved |
| Aborted | Action was aborted | Resolved |
| Resolved | Action lifecycle fully resolved | N/A |

## Lifecycle Transitions

Actions follow a directed state machine. Transitions are governed by:

1. **Execution Policy**: Determines retry behavior on failure.
2. **Timeout Policy**: Determines when an executing action is terminated.
3. **Idempotency**: Determines whether compensation is required.
4. **Error Category**: Determines whether the action is retried or aborted.

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
