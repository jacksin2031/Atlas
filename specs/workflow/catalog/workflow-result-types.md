---
title: Workflow Result Types Taxonomy
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Result Types Taxonomy

## Overview

This document defines the result type taxonomy for the Atlas Development System (ADS) workflow engine. Results are the normalized output entities produced by action completion. Every action, regardless of type, produces a result that follows this taxonomy. Results serve as the contract between actions and the downstream nodes that consume their outputs.

Results MUST be treated as immutable once committed. A result entity reference MUST NOT be reassigned or modified after the action reaches a terminal state.

## Result Type Categories

The workflow engine defines seven result types. Each type represents a distinct outcome category with specific propagation and transformation semantics.

| Result Type | Trigger Condition | Propagation | Compensation |
|-------------|------------------|-------------|--------------|
| Success | Action completed without error | Forward to dependents | Not applicable |
| Failure | Action terminated with an unhandled error | To error handlers | MAY trigger compensation |
| Partial | Action completed with incomplete output | Forward partial data; flag remaining | MAY retry remaining |
| Timeout | Action exceeded its time budget | To timeout handler | MAY extend or abort |
| Cancelled | Action was explicitly cancelled | To cancellation handler | Triggers compensation |
| Skipped | Action was bypassed by conditional logic | No data forwarded | Not applicable |
| Compensated | Action's effects were reversed | To compensation handler | Terminal |

## Detailed Result Type Definitions

### Success

The action completed all declared operations and produced the expected output.

| Attribute | Type | Description |
|-----------|------|-------------|
| `output_data` | Object | Action-specific output payload |
| `output_schema` | Object | Schema that output_data conforms to |
| `execution_time` | Duration | Actual time taken for execution |
| `resource_usage` | Object | Resources consumed during execution |
| `metrics` | Object | Performance metrics collected during execution |
| `checksum` | String | Integrity hash of output_data |

**Propagation Rules:**
- Output data is forwarded to all downstream nodes that declare compatible inputs.
- The result is recorded in the workflow state store.
- Success events are emitted per `workflow-events.md`.

### Failure

The action terminated due to an error that was not handled by retries or error hooks.

| Attribute | Type | Description |
|-----------|------|-------------|
| `error_ref` | EntityReference | Reference to the error entity |
| `error_category` | Enum | Category of the error per `workflow-errors.md` |
| `error_severity` | Enum | Severity level of the error |
| `partial_output` | Object | Any output produced before failure |
| `compensation_triggered` | Boolean | Whether compensation was initiated |
| `retry_exhausted` | Boolean | Whether all retry attempts were consumed |

**Propagation Rules:**
- The error is propagated to the nearest error handler (on-error hook).
- If no handler exists, the error propagates to the workflow level.
- Partial output, if present, is forwarded to downstream nodes that accept it.
- Failure events are emitted per `workflow-events.md`.

### Partial

The action produced some output but could not complete all declared operations.

| Attribute | Type | Description |
|-----------|------|-------------|
| `produced_outputs` | Array | List of output entity references that were produced |
| `missing_outputs` | Array | List of output entity references that were NOT produced |
| `completion_percentage` | Float | Fraction of declared operations completed |
| `error_ref` | EntityReference | Reference to the error causing partial completion, if any |
| `recoverable` | Boolean | Whether the missing outputs can be recovered |

**Propagation Rules:**
- Produced outputs are forwarded to downstream nodes.
- Missing outputs are flagged; downstream nodes MUST declare whether partial inputs are acceptable.
- If all downstream nodes accept partial input, the workflow continues.
- If any downstream node requires complete input, the workflow enters a recovery state.

### Timeout

The action exceeded its declared timeout without completing.

| Attribute | Type | Description |
|-----------|------|-------------|
| `timeout_duration` | Duration | The configured timeout value |
| `elapsed_duration` | Duration | The actual time elapsed |
| `progress_at_timeout` | Float | Fraction of work completed before timeout |
| `timeout_action` | Enum | The declared timeout action: `fail`, `skip`, or `continue` |
| `partial_output` | Object | Any output produced before timeout |

**Propagation Rules:**
- The timeout action determines the result transformation:
  - `fail`: Transforms to a Failure result.
  - `skip`: Transforms to a Skipped result.
  - `continue`: Transforms to a Partial result with progress_at_timeout.
- Partial output is forwarded if the timeout action allows continuation.

### Cancelled

The action was explicitly cancelled by an operator, policy, or upstream cancellation.

| Attribute | Type | Description |
|-----------|------|-------------|
| `cancelled_by` | EntityReference | The actor or system that initiated cancellation |
| `cancellation_reason` | String | Human-readable reason for cancellation |
| `progress_at_cancel` | Float | Fraction of work completed before cancellation |
| `partial_output` | Object | Any output produced before cancellation |
| `compensation_required` | Boolean | Whether prior actions require compensation |

**Propagation Rules:**
- Cancellation propagates to all sibling and downstream nodes.
- Partial output is forwarded to nodes that accept it.
- Compensation is triggered if compensation_required is true.
- Cancelled events are emitted per `workflow-events.md`.

### Skipped

The action was bypassed due to conditional logic that evaluated to false.

| Attribute | Type | Description |
|-----------|------|-------------|
| `skipping_condition` | ConditionEntity | The condition that caused the skip |
| `condition_result` | Boolean | The evaluation result that caused skipping |
| `alternative_path` | String | The edge or path that was taken instead |
| `downstream_impact` | Array | IDs of downstream nodes affected by the skip |

**Propagation Rules:**
- No output data is forwarded.
- Downstream nodes that depend on the skipped action are either skipped or blocked.
- If a downstream node has alternative inputs, it proceeds with those inputs.
- If a downstream node has no alternative, it enters a Blocked state.

### Compensated

The effects of a prior action have been reversed through compensation.

| Attribute | Type | Description |
|-----------|------|-------------|
| `original_action_id` | String | ID of the action that was compensated |
| `compensation_action_id` | String | ID of the compensation action |
| `compensation_result` | Enum | `Success` or `Failure` |
| `compensation_output` | Object | Output from the compensation action |
| `irreversible_effects` | Array | Any effects that could NOT be compensated |

**Propagation Rules:**
- If compensation succeeded, the workflow proceeds to the next recovery step.
- If compensation failed, the workflow enters a manual intervention state.
- Irreversible effects are logged and reported to the observability system.

## Result Attributes

Every result instance, regardless of type, possesses the following core attributes:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | String | YES | Unique result identifier |
| `action_ref` | EntityReference | YES | Reference to the action that produced this result |
| `type` | Enum | YES | One of the seven result types |
| `status` | Enum | YES | Normalized status: `Success`, `Failure`, `Partial`, `Timeout`, `Cancelled`, `Skipped`, `Compensated` |
| `produced_at` | Timestamp | YES | Wall-clock time of result production |
| `action_duration` | Duration | YES | Total action execution time |
| `downstream_impact` | Array | NO | IDs of downstream nodes affected by this result |
| `metadata` | Object | NO | Additional diagnostic data |

## Result Propagation Rules

Results propagate through the workflow graph according to well-defined rules.

### Forward Propagation

1. A result is forwarded from the producing action to all downstream nodes connected by data edges.
2. Each downstream node evaluates whether it accepts the result type.
3. If accepted, the result becomes an input to the downstream node.
4. If rejected, the edge is not traversed; the downstream node is blocked or skipped.

### Error Propagation

1. Failure and Compensated results trigger error propagation per `workflow-errors.md`.
2. On-error hooks at the producing node are invoked first.
3. If unhandled, the error propagates to the workflow level.
4. Workflow-level error handlers are invoked next.
5. If still unhandled, the workflow enters a terminal state.

### Conditional Propagation

1. Skipped results cause downstream conditional nodes to evaluate their alternative paths.
2. Partial results cause downstream nodes to check their input completeness requirements.
3. Timeout results cause downstream nodes to check their timeout tolerance.

## Result Transformation

Results MAY be transformed as they flow through the workflow graph.

### Transformation Rules

| Transformation | Description | When Applied |
|---------------|-------------|-------------|
| Enrichment | Additional metadata is appended to the result | At node boundaries |
| Filtering | Selected fields are extracted from the result | At edge crossings |
| Aggregation | Multiple results are combined into one | At fan-in nodes |
| Conversion | Result type is converted (e.g., Partial to Success) | At transformation nodes |
| Projection | Result is mapped to a different schema | At interface boundaries |

### Transformation Guarantees

1. Transformations are deterministic; identical inputs produce identical outputs.
2. Transformations do not alter the original result entity; they produce a new result entity.
3. Transformation chains are bounded by the manifest's maximum transformation depth.
4. Failed transformations produce a Failure result at the transformation node.
