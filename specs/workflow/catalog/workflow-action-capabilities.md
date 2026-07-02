# Workflow Action Capabilities

Catalog document for workflow-action-capabilities.

This catalog document enumerates the capability model for Workflow Actions.

## Action Capability Categories

| Capability | Description | Required |
|---|---|---|
| Compute | Performs computational work | Conditional |
| I/O | Reads or writes external data | Conditional |
| Network | Makes network requests | Conditional |
| Side Effect | Modifies external state | Declared |
| Idempotent | Safe to re-execute | Optional |
| Compensatable | Has a compensation action | For non-idempotent |
| Timeout-Controlled | Respects execution timeout | Required |
| Retryable | Can be retried on failure | Optional |

## Capability Declaration

Each action MUST declare its capabilities in the manifest. Capabilities determine:

1. **Resource requirements**: CPU, memory, network access.
2. **Security requirements**: Permission classes, secret access.
3. **Execution constraints**: Timeout, retry policy, idempotency.
4. **Observability requirements**: Tracing, metrics, audit logging.

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
