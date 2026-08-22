# Workflow Action Constraints

Catalog document for workflow-action-constraints.

This catalog document defines constraints on Workflow Actions.

## Execution Constraints

| Constraint | Type | Description | Default |
|---|---|---|---|
| Timeout | Time-based | Maximum execution duration | Unlimited |
| Retry Count | Numeric | Maximum retry attempts | 3 |
| Retry Backoff | Strategy | Exponential, linear, or fixed | Exponential |
| Concurrency | Numeric | Maximum concurrent executions | 1 |
| Memory | Size-based | Maximum memory allocation | Unlimited |
| CPU | Percentage | Maximum CPU allocation | Unlimited |
| Idempotency | Boolean | Whether re-execution is safe | Declared |

## Structural Constraints

| Constraint | Type | Description |
|---|---|---|
| Input Schema | Schema | Action inputs must conform to declared schema |
| Output Schema | Schema | Action outputs must conform to declared schema |
| Side Effects | Declaration | All side effects must be declared |
| Dependencies | List | External service dependencies must be declared |
| Secret Access | List | Required secrets must be declared |

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
