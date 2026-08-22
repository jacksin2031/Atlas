---
id: ATLAS-STORAGE-CATALOG-TRANSACTIONS
title: Storage Transactions Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Transactions Catalog

## 1. Purpose

This catalog defines the canonical set of transaction types and isolation levels used by the Atlas Storage subsystem.

## 2. Transaction Type Catalog

| Transaction ID | Name | Description | Isolation Level | Durability | RFC Reference | Use Case |
|---|---|---|---|---|---|---|
| TX-ATOMIC | Atomic | Single-operation transaction with full ACID guarantees. | Serializable | Full | RFC-0406 | Single resource mutation. |
| TX-SERIALIZABLE | Serializable | Guaranteed conflict-free execution order. | Serializable | Full | RFC-0406 | Critical financial operations. |
| TX-SNAPSHOT-ISOLATION | Snapshot Isolation | Repeatable reads with snapshot consistency. | Snapshot | Full | RFC-0406 | Read-heavy workloads. |
| TX-READ-COMMITTED | Read Committed | Reads see only committed data. | Read Committed | Full | RFC-0406 | General-purpose operations. |
| TX-OPTIMISTIC | Optimistic Concurrent | Commits validated at end; conflicts retried. | Optimistic | Full | RFC-0406 | Low-contention scenarios. |
| TX-BATCH | Batch | Multiple operations committed atomically. | Read Committed | Full | RFC-0406 | Bulk data operations. |
| TX-DIST-2PC | Distributed Two-Phase | Cross-node transaction with prepare/commit protocol. | Serializable | Full | RFC-0406 | Multi-provider operations. |
| TX-NESTED | Nested | Sub-transactions within a parent transaction. | Serializable | Full | RFC-0406 | Complex multi-step operations. |
| TX-READ-ONLY | Read Only | No modifications; optimized for scanning. | Read Committed | N/A | RFC-0406 | Reporting and analytics. |
| TX-WRITE-ONLY | Write Only | Modifications without subsequent reads. | Serializable | Full | RFC-0406 | Event ingestion pipelines. |
| TX-CHECKPOINT | Checkpoint | Marks a consistent point for recovery. | Serializable | Full | RFC-0406 | Periodic state snapshots. |
| TX-SAVEPOINT | Savepoint | Intermediate rollback point within a transaction. | Serializable | Partial | RFC-0406 | Long-running complex transactions. |

## 3. Isolation Level Comparison

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Write Skew | Serialization Anomaly |
|---|---|---|---|---|---|
| Serializable | No | No | No | No | No |
| Snapshot Isolation | No | No | No | Yes | No |
| Read Committed | No | Yes | Yes | Yes | Yes |
| Optimistic | No | No | No | No | Conditional |
| Read Only | No | No | No | No | No |
| Write Only | N/A | N/A | N/A | N/A | N/A |
| Checkpoint | N/A | N/A | N/A | N/A | N/A |
| Savepoint | N/A | N/A | N/A | N/A | N/A |

## 4. Transaction Lifecycle States

| State | Description |
|---|---|
| Pending | Transaction initiated but not yet assigned a provider. |
| In-Flight | Transaction executing operations against the provider. |
| Preparing | Transaction in two-phase commit prepare phase. |
| Committed | All operations successfully applied. |
| Aborted | Transaction rolled back due to error or conflict. |
| Rolled Back | Explicit rollback completed. |
| Checkpointed | A savepoint or checkpoint was created. |

## 5. Validation Rules

1. Every transaction type identifier MUST match the regex ^TX-[A-Z][A-Z0-9]*$.
2. Transaction types MUST be selected exclusively from this catalog.
3. Isolation levels MUST be declared at transaction initiation.
4. Distributed transactions MUST use the two-phase commit protocol defined in RFC-0406.
5. Savepoints MUST be numbered sequentially within a transaction.
6. Transaction durability guarantees MUST be enforced by the provider.
