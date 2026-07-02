---
title: Workflow State Types Taxonomy
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow State Types Taxonomy

## Overview

This document defines the state type taxonomy for the Atlas Development System (ADS) workflow engine. States represent the discrete conditions of workflow and node entities throughout their lifecycles. The state model provides the formal state machine that governs all workflow execution behavior.

States MUST be treated as immutable snapshots. Once a workflow or node enters a state, that state record is permanent. Transitions between states produce new state records; the original state is never modified.

## State Type Categories

The workflow engine defines nine state types. Each type represents a distinct phase in the workflow execution lifecycle.

| State Type | Category | Reversible | Terminal | Persistence Required |
|-----------|----------|-----------|----------|---------------------|
| Active | Execution | YES | NO | YES |
| Paused | Suspension | YES | NO | YES |
| Suspended | Forced Stop | NO | NO | YES |
| Completed | Success | NO | YES | YES |
| Failed | Error | Conditional | YES | YES |
| Cancelled | Termination | NO | YES | YES |
| TimedOut | Timeout | NO | YES | YES |
| Compensating | Rollback | YES | NO | YES |
| Compensated | Rollback Complete | NO | YES | YES |

## Detailed State Type Definitions

### Active

The workflow or node is currently executing.

| Attribute | Type | Description |
|-----------|------|-------------|
| `entered_at` | Timestamp | Time when the active state was entered |
| `execution_id` | String | Unique execution identifier within this state |
| `progress` | Float | Fraction of declared work completed (0.0 to 1.0) |
| `active_actions` | Array | IDs of actions currently running |
| `resource_bindings` | Object | Resources currently allocated |

**Transition Rules:**
- An active workflow MAY transition to `Paused` at any time.
- An active workflow MAY transition to `Suspended` only through administrative action.
- An active workflow transitions to `Completed` when all nodes reach terminal states.
- An active workflow transitions to `Failed` when an unhandled error occurs.
- An active workflow transitions to `Cancelled` when a cancellation request is processed.

**Persistence Requirements:**
- The active state MUST be persisted to the state store on every action completion.
- Progress updates are batched and persisted at configurable intervals.
- Resource bindings are persisted atomically with state transitions.

### Paused

Execution has been voluntarily suspended by the workflow operator.

| Attribute | Type | Description |
|-----------|------|-------------|
| `paused_by` | EntityReference | The actor who initiated the pause |
| `pause_reason` | String | Human-readable reason for pausing |
| `paused_at` | Timestamp | Time when the paused state was entered |
| `resume_allowed` | Boolean | Whether automatic resume is permitted |
| `checkpoint_ref` | EntityReference | Reference to the checkpoint at pause time |

**Transition Rules:**
- A paused workflow MAY transition back to `Active` through resume.
- A paused workflow MAY transition to `Suspended` through administrative action.
- A paused workflow MAY transition to `Cancelled` through cancellation.
- A paused workflow CANNOT transition directly to `Completed` or `Failed`.

**Persistence Requirements:**
- The paused state MUST be persisted immediately upon entry.
- A checkpoint is taken at pause time for potential resume.
- All active action states are frozen at the pause point.

### Suspended

Execution has been forcibly stopped, typically by the engine or an administrator.

| Attribute | Type | Description |
|-----------|------|-------------|
| `suspended_by` | EntityReference | The actor or system that initiated suspension |
| `suspend_reason` | String | Reason for suspension |
| `suspended_at` | Timestamp | Time when the suspended state was entered |
| `recovery_possible` | Boolean | Whether the workflow can be resumed |
| `blocking_condition` | String | Condition that must be resolved before resume |

**Transition Rules:**
- A suspended workflow MAY transition to `Active` if recovery is possible and the blocking condition is resolved.
- A suspended workflow MAY transition to `Cancelled` through administrative cancellation.
- A suspended workflow MAY transition to `Failed` if the blocking condition cannot be resolved.
- A suspended workflow CANNOT transition to `Completed`.

**Persistence Requirements:**
- The suspended state MUST be persisted immediately.
- The blocking condition is recorded for diagnostic purposes.
- Resource allocations are held (not released) while suspended.

### Completed

The workflow or node has finished all operations successfully.

| Attribute | Type | Description |
|-----------|------|-------------|
| `completed_at` | Timestamp | Time when the completed state was entered |
| `total_duration` | Duration | Total time from creation to completion |
| `final_output` | Object | Aggregated output from all actions |
| `actions_completed` | Integer | Number of actions that completed successfully |
| `actions_failed` | Integer | Number of actions that failed and were compensated |

**Transition Rules:**
- Completed is a terminal state; no further transitions are permitted.
- The completed state is immutable; it CANNOT be modified or reverted.

**Persistence Requirements:**
- The completed state MUST be persisted immediately upon entry.
- Final output is persisted to the result store.
- The workflow entity is marked as complete in the active registry.

### Failed

The workflow or node has terminated due to an unhandled error.

| Attribute | Type | Description |
|-----------|------|-------------|
| `failed_at` | Timestamp | Time when the failed state was entered |
| `error_ref` | EntityReference | Reference to the terminating error |
| `error_category` | Enum | Error category per `workflow-errors.md` |
| `compensation_status` | Enum | Status of any compensation: `none`, `in_progress`, `completed`, `failed` |
| `retry_count` | Integer | Number of retry attempts consumed |

**Transition Rules:**
- A failed workflow MAY transition to `Compensating` if compensation is required.
- A failed node with retry eligibility MAY transition back to `Active` through retry.
- Failed is a terminal state for workflows (unless compensation is pending).
- Failed is a terminal state for nodes unless compensation is triggered.

**Persistence Requirements:**
- The failed state MUST be persisted immediately upon error detection.
- The error entity reference is persisted with the state record.
- Diagnostic data is captured in the state metadata.

### Cancelled

The workflow or node has been explicitly cancelled.

| Attribute | Type | Description |
|-----------|------|-------------|
| `cancelled_at` | Timestamp | Time when the cancelled state was entered |
| `cancelled_by` | EntityReference | The actor who initiated cancellation |
| `cancellation_reason` | String | Human-readable reason |
| `progress_at_cancel` | Float | Fraction of work completed before cancellation |
| `compensation_required` | Boolean | Whether prior actions need compensation |

**Transition Rules:**
- Cancelled is a terminal state; no further transitions are permitted.
- Cancellation of a parent workflow triggers cascading cancellation of active child nodes.
- Cancellation does NOT automatically trigger compensation; compensation is triggered separately if required.

**Persistence Requirements:**
- The cancelled state MUST be persisted immediately.
- Progress at cancellation is recorded for audit purposes.
- Compensation requirements are recorded for the compensation engine.

### TimedOut

The workflow or node exceeded its declared timeout.

| Attribute | Type | Description |
|-----------|------|-------------|
| `timed_out_at` | Timestamp | Time when the timeout was detected |
| `timeout_duration` | Duration | The configured timeout value |
| `elapsed_duration` | Duration | Actual time elapsed |
| `timeout_action` | Enum | The declared timeout action: `fail`, `skip`, or `continue` |
| `partial_progress` | Float | Fraction of work completed before timeout |

**Transition Rules:**
- A timed-out workflow transitions based on the timeout action:
  - `fail`: Transitions to `Failed`.
  - `skip`: Transitions to `Cancelled`.
  - `continue`: Transitions back to `Active`.
- A timed-out node follows the same transition rules based on its timeout action.

**Persistence Requirements:**
- The timed-out state MUST be persisted immediately upon timeout detection.
- Partial progress is recorded for potential resume.
- Timeout events are emitted per `workflow-events.md`.

### Compensating

Compensation is in progress to reverse the effects of prior actions.

| Attribute | Type | Description |
|-----------|------|-------------|
| `compensation_started_at` | Timestamp | Time when compensation began |
| `compensating_actions` | Array | IDs of actions currently being compensated |
| `compensated_actions` | Array | IDs of actions already compensated |
| `remaining_actions` | Array | IDs of actions yet to be compensated |
| `compensation_order` | Enum | `reverse_topological` or `explicit` |

**Transition Rules:**
- A compensating workflow transitions to `Compensated` when all compensations succeed.
- A compensating workflow transitions to `Failed` if any compensation fails.
- A compensating workflow MAY be interrupted by administrative cancellation, transitioning to `Cancelled`.

**Persistence Requirements:**
- The compensating state MUST be persisted on each action compensation.
- Compensation progress is tracked in the state record.
- Compensation events are emitted per `workflow-events.md`.

### Compensated

All required compensations have been completed successfully.

| Attribute | Type | Description |
|-----------|------|-------------|
| `compensated_at` | Timestamp | Time when the compensated state was entered |
| `compensated_actions` | Array | IDs of all compensated actions |
| `failed_compensations` | Array | IDs of actions whose compensation failed |
| `irreversible_effects` | Array | Effects that could not be compensated |

**Transition Rules:**
- Compensated is a terminal state; no further transitions are permitted.
- The compensated state is immutable.
- Irreversible effects are logged for audit and monitoring.

**Persistence Requirements:**
- The compensated state MUST be persisted immediately.
- The list of irreversible effects is persisted for audit.
- The workflow entity is marked as compensated in the registry.

## State Transition Matrix

The following matrix shows all permitted state transitions:

| From \ To | Active | Paused | Suspended | Completed | Failed | Cancelled | TimedOut | Compensating | Compensated |
|-----------|--------|--------|-----------|-----------|--------|-----------|----------|-------------|-------------|
| Active | - | YES | YES | YES | YES | YES | YES | - | - |
| Paused | YES | - | YES | NO | NO | YES | NO | - | - |
| Suspended | Conditional | - | - | NO | YES | YES | NO | - | - |
| Completed | NO | NO | NO | - | NO | NO | NO | NO | NO |
| Failed | Conditional | NO | NO | NO | - | NO | NO | YES | NO |
| Cancelled | NO | NO | NO | NO | NO | - | NO | NO | NO |
| TimedOut | Conditional | NO | NO | NO | YES | YES | - | NO | NO |
| Compensating | NO | NO | NO | NO | YES | YES | NO | - | YES |
| Compensated | NO | NO | NO | NO | NO | NO | NO | NO | - |

## State Persistence Requirements

All states are subject to the following persistence requirements:

1. **Atomicity**: State transitions are atomic; partial transitions are rolled back.
2. **Durability**: Persisted states survive engine restarts.
3. **Immutability**: State records are append-only; existing records are never modified.
4. **Versioning**: Each state transition increments the state version per `workflow-versioning.md`.
5. **Recovery**: State stores support recovery to any previous state version.

## State Observability

State transitions are observable through the following mechanisms:

1. **Events**: Each state transition emits a state change event per `workflow-events.md`.
2. **Metrics**: State duration is recorded as a latency metric per `workflow-metrics.md`.
3. **Logs**: State transitions are recorded in the audit log.
4. **Dashboards**: Current states are displayed on observability dashboards per `workflow-observability.md`.
