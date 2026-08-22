# Workflow Condition Types

Catalog document for workflow-condition-types.

This catalog document enumerates all Workflow Condition types.

## Condition Categories

| Category | Type | Description | Evaluation |
|---|---|---|---|
| Boolean | Expression | Arbitrary boolean expression | Immediate |
| Comparison | Equality | Value equality check | Immediate |
| Comparison | Range | Value within range | Immediate |
| Comparison | Pattern | Regex pattern match | Immediate |
| Temporal | Before | Time before deadline | Time-based |
| Temporal | After | Time elapsed since event | Time-based |
| Temporal | Duration | Duration between events | Time-based |
| State | NodeState | Node in specific state | Event-based |
| State | WorkflowState | Workflow in specific state | Event-based |
| State | ContextValue | Context variable has value | Immediate |
| Resource | CPU | CPU utilization threshold | Polling |
| Resource | Memory | Memory utilization threshold | Polling |
| Resource | QueueDepth | Queue depth threshold | Polling |
| External | HTTP | HTTP response condition | Request-based |
| External | Message | Message queue condition | Event-based |

## Condition Composition

Conditions can be composed using boolean operators:

| Operator | Symbol | Description |
|---|---|---|
| AND | && | Both conditions must be true |
| OR | \|\| | At least one condition must be true |
| NOT | ! | Negate condition |
| XOR | ^ | Exactly one condition must be true |

## Classification

| Attribute | Value |
|---|---|
| Category | Workflow |
| Type | Catalog |
| Status | Proposed |
| Version | 1.0.0 |
