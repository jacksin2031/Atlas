# Workflow Recovery Lifecycle

Catalog document for workflow-recovery-lifecycle.

This catalog document defines the lifecycle states and transitions for Workflow Recovery.

## Recovery Lifecycle States

| State | Description | Transitions To |
|---|---|---|
| FailureDetected | Error triggers recovery | StrategySelected, Abort |
| StrategySelected | Recovery strategy chosen | CheckpointPrepared, CompensationExecuted |
| CheckpointPrepared | Last valid checkpoint identified | StateRestored, RollbackFailed |
| StateRestored | Workflow state restored from checkpoint | ExecutionResumed, ValidationFailed |
| ValidationFailed | Restored state fails validation | RollbackFailed, PartialRecovery |
| PartialRecovery | Partial state recovery attempted | ExecutionResumed, Abort |
| RollbackFailed | Recovery failed completely | Abort |
| CompensationExecuted | Compensating transactions applied | StateRestored |
| ExecutionResumed | Workflow resumed from recovery point | NormalExecution |
| Abort | Recovery aborted, workflow terminated | Terminal |
| NormalExecution | Workflow continues normally | Terminal |

## Recovery Strategy Selection

Recovery strategies are selected based on:

1. **Error Category**: Transient errors trigger retry; permanent errors trigger rollback.
2. **Checkpoint Availability**: If no valid checkpoint exists, abort.
3. **Recovery Window**: If the error occurred outside the recovery window, abort.
4. **Resource Availability**: If recovery resources are unavailable, delay or abort.

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
