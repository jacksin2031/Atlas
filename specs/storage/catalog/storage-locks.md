---
id: ATLAS-STORAGE-CATALOG-LOCKS
title: Storage Locks Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Locks Catalog

## 1. Purpose

This catalog defines the canonical set of lock types, compatibility rules, and granularity levels used by the Atlas Storage subsystem for concurrency control.

## 2. Lock Type Prefix

All lock identifiers use the prefix LCK-.

## 3. Lock Type Catalog

| Lock ID | Name | Description | Shared | Upgradeable | RFC Reference |
|---|---|---|---|---|---|
| LCK-READ | Read Lock | Permits concurrent reads; blocks writers. | Yes | No | RFC-0417 |
| LCK-WRITE | Write Lock | Exclusive access; blocks all other operations. | No | No | RFC-0417 |
| LCK-SCHEMA | Schema Lock | Prevents schema modifications during operation. | No | No | RFC-0405 |
| LCK-SNAPSHOT | Snapshot Lock | Freezes state at a point in time for consistency. | Yes | No | RFC-0407 |
| LCK-INTENT | Intent Lock | Signals intention to acquire a finer-grained lock. | Yes | Partial | RFC-0417 |

## 4. Lock Compatibility Matrix

Rows = requesting lock, Columns = held lock. Y = compatible, N = incompatible.

| Requested \\ Held | LCK-READ | LCK-WRITE | LCK-SCHEMA | LCK-SNAPSHOT | LCK-INTENT |
|---|---|---|---|---|---|
| LCK-READ | Y | N | N | Y | Y |
| LCK-WRITE | N | N | N | N | N |
| LCK-SCHEMA | N | N | N | N | N |
| LCK-SNAPSHOT | Y | N | N | Y | Y |
| LCK-INTENT | Y | N | N | Y | Y |

## 5. Lock Granularity Levels

| Level | Scope | Description | RFC Reference |
|---|---|---|---|
| ROW | Single resource | Locks an individual resource record. | RFC-0417 |
| TABLE | Resource collection | Locks all resources sharing a schema. | RFC-0417 |
| PARTITION | Named subset | Locks a partition or shard of the dataset. | RFC-0417 |
| DATABASE | Full dataset | Locks the entire storage namespace. | RFC-0417 |

## 6. Lock Escalation Rules

1. Locks MAY escalate from Row to Table when more than N resources are locked simultaneously.
2. Locks MAY escalate from Table to Partition when more than M partitions are affected.
3. Escalation MUST wait for all existing locks to be released before proceeding.
4. Escalation MUST NOT occur during an active transaction.
5. Escalation policies MUST be configurable per provider.

## 7. Lock Timeout Configuration

| Parameter | Default | Description | RFC Reference |
|---|---|---|---|
| acquire_timeout | 30s | Maximum time to wait for lock acquisition. | RFC-0417 |
| hold_timeout | 60s | Maximum time a lock may be held. | RFC-0417 |
| deadlock_timeout | 10s | Time before deadlock detection runs. | RFC-0417 |
| escalation_threshold | 100 | Number of row locks before table escalation. | RFC-0417 |

## 8. Validation Rules

1. Every lock identifier MUST match the regex ^LCK-[A-Z]+$.
2. Locks MUST be acquired in ascending granularity order (Row -> Table -> Partition -> Database).
3. Write locks MUST NOT be granted while any Read lock is held on the same resource.
4. Deadlock detection MUST run at least every deadlock_timeout interval.
5. Lock state MUST be durable across provider restarts for in-flight transactions.
