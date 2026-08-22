# Workflow Error Lifecycle

Catalog document for workflow-error-lifecycle.

This catalog document defines the lifecycle states and transitions for Workflow Errors.

## Error Lifecycle States

| State | Description | Transitions To |
|---|---|---|
| Raised | Error is thrown or detected | Caught, Unhandled |
| Caught | Error is intercepted by error handler | Classified, Ignored |
| Classified | Error category determined | Handled, Escalated |
| Handled | Error resolved by handler | Resolved |
| Escalated | Error propagated to parent scope | Retried, Compensated, Aborted |
| Retried | Retry policy applied | Handled, Exhausted |
| Exhausted | All retries consumed | Compensated, Aborted |
| Compensated | Compensation action executed | Resolved |
| Aborted | Workflow execution terminated | Terminal |
| Resolved | Error fully resolved | N/A |

## Error Classification

Errors are classified by two orthogonal dimensions:

| Dimension | Values |
|---|---|
| Transience | Transient, Permanent |
| Recoverability | Recoverable, Fatal |

This yields four error categories:

1. **Transient-Recoverable**: Retry with backoff (network timeout, rate limit).
2. **Transient-Fatal**: Log and escalate (out of memory, disk full).
3. **Permanent-Recoverable**: Compensation or skip (validation error, missing dependency).
4. **Permanent-Fatal**: Abort (schema corruption, invariant violation).

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
