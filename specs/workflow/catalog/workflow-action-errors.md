# Workflow Action Errors

Catalog document for workflow-action-errors.

This catalog document enumerates error types specific to Workflow Actions.

## Action Error Categories

| Error Code | Category | Description | Retryable |
|---|---|---|---|
| ACTION_INVALID_TYPE | Permanent | Action type not recognized | No |
| ACTION_TIMEOUT | Transient | Action exceeded timeout | Conditional |
| ACTION_RETRY_EXHAUSTED | Transient | Max retries exceeded | No |
| ACTION_COMPENSATION_FAILED | Fatal | Compensation action failed | No |
| ACTION_IDEMPOTENCY_MISMATCH | Permanent | Non-idempotent re-execution detected | No |
| ACTION_PERMISSION_DENIED | Permanent | Insufficient permissions | No |
| ACTION_SERIALIZATION_ERROR | Transient | Failed to serialize/deserialize payload | Conditional |
| ACTION_EXECUTION_ERROR | Transient | Action code threw exception | Conditional |
| ACTION_CANCELLED | Transient | Action was cancelled by workflow | No |

## Error Propagation

Action errors propagate through the workflow error handling model (RFC-0314):

1. **Node Level**: Error caught by the node's error handler.
2. **Workflow Level**: Error propagates to the workflow error handler.
3. **Recovery Level**: Error triggers recovery strategy (RFC-0315).

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
