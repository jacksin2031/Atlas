---
title: Workflow Time Model Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Time Model Reference

## Overview

This document defines the time model reference for the Atlas Development System (ADS) workflow engine. The time model provides the abstract framework for all temporal reasoning within workflows, including scheduling, timeout enforcement, duration calculation, and time-based condition evaluation.

Time is treated as an abstract entity with well-defined types, resolution guarantees, and synchronization protocols. All time values are immutable once created.

## Time Types

The workflow engine defines six time types. Each type represents a distinct temporal concept used in workflow operations.

| Time Type | Description | Format | Example |
|-----------|-------------|--------|---------|
| Absolute | A specific point in wall-clock time | ISO 8601 timestamp | `2026-07-01T12:00:00Z` |
| Relative | A duration measured from a reference point | Duration string | `PT5M` (5 minutes) |
| Cron | A recurring schedule expressed in cron syntax | Cron expression | `0 9 * * 1` (Monday 9 AM) |
| Interval | A fixed-period repetition with a start time | Start + Period | Start: `2026-07-01T00:00:00Z`, Period: `PT1H` |
| Deadline | A time by which an operation MUST complete | Absolute or relative | `2026-07-01T18:00:00Z` or `PT8H` |
| Duration | An elapsed time interval | Duration string | `PT30S` (30 seconds) |

### Absolute Time

Absolute time represents a specific instant on the global timeline.

| Attribute | Type | Description |
|-----------|------|-------------|
| `timestamp` | String | ISO 8601 formatted timestamp |
| `timezone` | String | IANA timezone identifier |
| `utc_offset` | Duration | Offset from UTC |
| `precision` | Enum | `second`, `millisecond`, or `microsecond` |

Absolute times are used for scheduling, deadline declaration, and event timestamping. They are always normalized to UTC internally.

### Relative Time

Relative time represents an offset from a reference point, typically the current wall-clock time or a workflow event timestamp.

| Attribute | Type | Description |
|-----------|------|-------------|
| `offset` | Duration | The time offset |
| `reference` | EntityReference | The reference point entity |
| `direction` | Enum | `forward` or `backward` |

Relative times are used for wait actions, delayed triggers, and scheduling offsets.

### Cron Time

Cron time represents a recurring schedule using the standard five-field cron expression syntax.

| Attribute | Type | Description |
|-----------|------|-------------|
| `expression` | String | Five-field cron expression |
| `year_field` | String | Optional sixth field for year |
| `timezone` | String | Timezone for interpretation |
| `start_bound` | Absolute | Optional earliest execution time |
| `end_bound` | Absolute | Optional latest execution time |

Cron schedules are used for periodic workflow invocation and recurring node activation.

### Interval Time

Interval time represents a fixed-period repetition starting from a specific point.

| Attribute | Type | Description |
|-----------|------|-------------|
| `start` | Absolute | The initial start time |
| `period` | Duration | The repeating interval |
| `count` | Integer | Optional maximum number of repetitions |
| `timezone` | String | Timezone for start interpretation |

Interval schedules are used for batch processing windows and periodic maintenance tasks.

### Deadline Time

Deadline time represents a time constraint that must be satisfied.

| Attribute | Type | Description |
|-----------|------|-------------|
| `target` | Absolute or Relative | The deadline point |
| `slack` | Duration | Buffer time before the deadline |
| `consequence` | Enum | Action on deadline miss: `fail`, `warn`, or `extend` |

Deadlines are used for SLA enforcement and time-critical workflow segments.

### Duration

Duration represents an elapsed time interval independent of any calendar point.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Float | Numeric duration value |
| `unit` | Enum | `nanosecond`, `microsecond`, `millisecond`, `second`, `minute`, `hour`, `day` |
| `precision` | Enum | `exact` or `approximate` |

Durations are used for timeouts, wait periods, and scheduling intervals.

## Time Resolution Requirements

The workflow engine enforces the following time resolution guarantees:

### Resolution Levels

| Level | Resolution | Use Case | Precision |
|-------|-----------|----------|----------|
| Coarse | 1 second | Cron scheduling, daily batches | +/- 0.5 seconds |
| Standard | 100 milliseconds | Node scheduling, wait actions | +/- 50 milliseconds |
| Fine | 10 milliseconds | High-frequency triggers | +/- 5 milliseconds |
| Ultra | 1 millisecond | Real-time processing | +/- 0.5 milliseconds |

### Resolution Selection

1. The default resolution level is `Standard`.
2. Nodes MAY declare a finer resolution requirement in their definition.
3. The engine uses the finest resolution required by any node in the workflow.
4. Resolution requirements that exceed the engine's capability result in a validation error.

### Clock Sources

| Clock Type | Source | Accuracy | Drift |
|-----------|--------|----------|-------|
| Wall Clock | System wall-clock time | Depends on OS | Variable |
| Monotonic | Monotonic counter | High | None |
| External | External time service | Depends on service | Bounded |

The engine uses monotonic clocks for duration measurement and wall-clock clocks for absolute time reference. External clocks are used for cron scheduling and deadline enforcement.

## Timezone Handling

Timezone management follows these rules:

### Timezone Resolution

1. Absolute times without an explicit timezone are interpreted as UTC.
2. Cron expressions without an explicit timezone use the workflow's declared timezone.
3. Node-level timezone declarations override the workflow-level timezone.
4. The engine converts all times to UTC internally for comparison and scheduling.

### Timezone Database

The engine maintains a timezone database compliant with IANA timezone rules. The database includes:

| Entry | Description |
|-------|-------------|
| `UTC` | Coordinated Universal Time |
| Regional zones | All IANA regional timezone identifiers |
| Fixed offsets | Named fixed-offset zones (e.g., `EST`, `PST`) |
| Historical transitions | DST change dates for all zones |

### DST Handling

1. Wall-clock times during a DST transition are interpreted using the spring-forward / fall-back rules.
2. Monotonic durations are unaffected by DST changes.
3. Cron expressions are evaluated in the declared timezone; DST changes are automatically handled.
4. Ambiguous times (during fall-back) are resolved using the earlier occurrence by default.

## Clock Synchronization Guarantees

The workflow engine provides the following clock synchronization guarantees:

### Intra-Engine Synchronization

1. All clocks within a single engine instance are synchronized to the system monotonic clock.
2. Wall-clock times are synchronized to the system wall-clock through periodic NTP-style adjustments.
3. Clock drift within an engine instance is bounded to less than 1 millisecond.

### Inter-Engine Synchronization

1. Distributed engine instances synchronize through a consensus-based clock protocol.
2. Logical clocks (vector clocks) are used for causal ordering of events across instances.
3. Physical clock synchronization is achieved through NTP; accuracy is bounded by the network latency.
4. Clock skew between engine instances is bounded by the manifest's declared maximum skew.

### Causal Ordering

1. Events causally related to each other are strictly ordered by logical clocks.
2. Concurrent events (no causal relationship) are ordered by engine instance ID and sequence number.
3. Causal ordering is preserved across engine restarts through clock state persistence.

## Time Operations

The following operations are defined on time entities:

| Operation | Operands | Result | Description |
|-----------|----------|--------|-------------|
| `add` | Time + Duration | Time | Adds duration to time |
| `subtract` | Time - Duration | Time | Subtracts duration from time |
| `difference` | Time - Time | Duration | Computes elapsed time between two times |
| `compare` | Time vs Time | Enum | Returns `before`, `equal`, or `after` |
| `next_occurrence` | Cron + Time | Time | Computes the next cron occurrence after the given time |
| `interval_count` | Interval + Start + End | Integer | Counts occurrences within a range |
| `is_within` | Time + Interval | Boolean | Tests whether time falls within the interval |
| `normalize` | Time | Time | Converts to UTC with standard precision |

## Time Validation

Time values are validated against the following rules:

| Rule | Description | Severity |
|------|-------------|----------|
| Non-negative Duration | Durations MUST be zero or positive | Critical |
| Valid Timestamp | Absolute times MUST be parseable ISO 8601 | Critical |
| Valid Cron | Cron expressions MUST have five or six valid fields | Critical |
| Bounded Duration | Durations MUST not exceed the manifest's maximum | Error |
| Future Deadline | Deadlines MUST be in the future relative to the reference time | Warning |
| Non-overlapping Intervals | Concurrent interval schedules MUST not overlap | Warning |
| Timezone Valid | Timezone identifiers MUST exist in the timezone database | Critical |

## Time in Conditions

Time-based conditions use the time types defined in this document.

| Condition Type | Time Type Used | Example |
|---------------|---------------|---------|
| Time | Absolute vs Absolute | `current_time >= 2026-07-01T09:00:00Z` |
| Time | Duration vs Duration | `elapsed_duration > PT1H` |
| Time | Cron vs Current | `cron_expression matches current_time` |
| Threshold | Duration vs Duration | `wait_duration > threshold_duration` |

Time conditions are evaluated per the operator semantics defined in `workflow-operators.md`.
