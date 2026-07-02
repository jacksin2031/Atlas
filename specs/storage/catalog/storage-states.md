---
id: ATLAS-STORAGE-CATALOG-STATES
title: Storage Operational States Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Operational States Catalog

## 1. Purpose

This catalog defines the canonical set of operational states for the Storage subsystem and its constituent components. These states describe the health and readiness of the subsystem as a whole, distinct from resource-level lifecycle states defined in storage-lifecycle.md.

## 2. State ID Prefix

All operational state identifiers use the prefix OST-.

## 3. Complete State Catalog

| State ID | Name | Type | Description | Entering From | Exiting To | RFC Reference |
|---|---|---|---|---|---|---|
| OST-IDLE | Idle | Operational | Subsystem is running but not actively processing. | Initializing, Running | Initializing, Running | RFC-0414 |
| OST-INITIALIZING | Initializing | Transient | Provider loading and configuration validation in progress. | None | Running, Failed | RFC-0403 |
| OST-RUNNING | Running | Operational | Subsystem is fully operational and accepting requests. | Idle, Initializing, Recovering | Idle, Paused, Stopped, Degraded | RFC-0414 |
| OST-PAUSED | Paused | Operational | Processing suspended by external signal. | Running | Running, Stopped | RFC-0414 |
| OST-STOPPED | Stopped | Operational | Subsystem is shut down; no processing. | Running, Paused | Initializing | RFC-0414 |
| OST-DEGRADED | Degraded | Operational | Reduced functionality; some providers unavailable. | Running, Recovering | Running, Failed, Stopped | RFC-0414 |
| OST-FAILED | Failed | Terminal | Unrecoverable error; manual intervention required. | Initializing, Running, Degraded | Recovering | RFC-0414 |
| OST-RECOVERING | Recovering | Transient | Automatic recovery procedure in progress. | Failed, Degraded | Running, Failed | RFC-0412 |
| OST-MIGRATING | Migrating | Transient | Schema or data migration in progress. | Running | Running, Degraded, Failed | RFC-0408 |
| OST-BACKING_UP | Backing Up | Transient | Backup operation in progress. | Running | Running, Degraded | RFC-0411 |
| OST-RESTORING | Restoring | Transient | Recovery from backup in progress. | Running, Failed | Running, Failed | RFC-0412 |
| OST-SYNCING | Syncing | Transient | Replication synchronization in progress. | Running | Running, Degraded | RFC-0418 |
| OST-REPLICATING | Replicating | Transient | Active data replication to peers. | Syncing | Running, Degraded | RFC-0418 |
| OST-SCALING | Scaling | Transient | Adding or removing storage capacity. | Running | Running, Degraded | RFC-0415 |
| OST-DRAINING | Draining | Transient | Gracefully shutting down while completing in-flight operations. | Running | Stopped | RFC-0414 |
| OST-MAINTENANCE | Maintenance | Operational | Subsystem in maintenance mode; limited operations. | Running | Running, Stopped | RFC-0414 |

## 4. State Classification

| Classification | States | Characteristics |
|---|---|---|
| Operational | Idle, Running, Paused, Stopped, Degraded, Maintenance | Sustained states that persist across request boundaries. |
| Transient | Initializing, Recovering, Migrating, Backing Up, Restoring, Syncing, Replicating, Scaling, Draining | Short-lived states that transition to a definitive outcome. |
| Terminal | Failed | Requires explicit human or automated intervention to exit. |

## 5. State Transition Rules

1. OST-FAILED MUST transition to OST-RECOVERING or OST-STOPPED.
2. OST-INITIALIZING MUST transition to OST-RUNNING, OST-DEGRADED, or OST-FAILED.
3. OST-DRAINING MUST transition to OST-STOPPED.
4. OST-MIGRATING MUST transition to OST-RUNNING, OST-DEGRADED, or OST-FAILED.
5. OST-RECOVERING MUST transition to OST-RUNNING or OST-FAILED.
6. OST-SCALING MUST transition to OST-RUNNING or OST-DEGRADED.

## 6. Validation Rules

1. Every operational state identifier MUST match the regex ^OST-[A-Z]+$.
2. State names MUST be unique.
3. Transient states MUST have a defined exit path; they MUST NOT be terminal.
4. Operational states MUST be reportable via the health check endpoint.
5. State transitions MUST be logged per RFC-0413.
