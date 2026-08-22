---
id: ATLAS-STORAGE-CATALOG-EVENTS
title: Storage Events Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Events Catalog

## 1. Purpose

This catalog defines the canonical set of event types emitted by the Atlas Storage subsystem during resource operations, transaction processing, lifecycle transitions, and administrative activities. Events provide the basis for audit trails, reactive workflows, and observability dashboards.

## 2. Stable ID Prefix

All event type identifiers use the prefix EVT-STOR-.

### 2.1 Naming Convention

Event type identifiers SHALL follow the pattern:

`
EVT-STOR-<CATEGORY>-<ACTION>
`

where <CATEGORY> identifies the functional domain and <ACTION> describes the specific event.

## 3. Complete Event Type Catalog

| Stable ID | Event Name | Category | Trigger Condition | RFC Reference |
|---|---|---|---|---|
| EVT-STOR-RES-CREATED | Resource Created | RESOURCE | A new resource is successfully stored. | RFC-0404 |
| EVT-STOR-RES-STORED | Resource Stored | RESOURCE | A resource is persisted to backing store. | RFC-0404 |
| EVT-STOR-RES-UPDATED | Resource Updated | RESOURCE | An existing resource is modified. | RFC-0404 |
| EVT-STOR-RES-DELETED | Resource Deleted | RESOURCE | A resource is removed from storage. | RFC-0404 |
| EVT-STOR-RES-ARCHIVED | Resource Archived | RESOURCE | A resource transitions to archived state. | RFC-0404 |
| EVT-STOR-RES-PURGED | Resource Purged | RESOURCE | A resource is permanently removed. | RFC-0404 |
| EVT-STOR-TX-BEGIN | Transaction Begin | TRANSACTION | A new transaction is initiated. | RFC-0406 |
| EVT-STOR-TX-COMMIT | Transaction Commit | TRANSACTION | A transaction is successfully committed. | RFC-0406 |
| EVT-STOR-TX-ROLLBACK | Transaction Rollback | TRANSACTION | A transaction is rolled back. | RFC-0406 |
| EVT-STOR-TX-CONFLICT | Transaction Conflict | TRANSACTION | A conflict is detected during commit. | RFC-0406 |
| EVT-STOR-SCHEMA-VALIDATED | Schema Validated | SCHEMA | A resource passes schema validation. | RFC-0405 |
| EVT-STOR-SCHEMA-EVOLVED | Schema Evolved | SCHEMA | A schema is migrated to a new version. | RFC-0405 |
| EVT-STOR-BKP-STARTED | Backup Started | BACKUP | A backup operation begins. | RFC-0411 |
| EVT-STOR-BKP-COMPLETED | Backup Completed | BACKUP | A backup finishes successfully. | RFC-0411 |
| EVT-STOR-BKP-FAILED | Backup Failed | BACKUP | A backup operation encounters an error. | RFC-0411 |
| EVT-STOR-REC-STARTED | Recovery Started | RECOVERY | A recovery operation begins. | RFC-0412 |
| EVT-STOR-REC-COMPLETED | Recovery Completed | RECOVERY | A recovery finishes successfully. | RFC-0412 |
| EVT-STOR-REC-FAILED | Recovery Failed | RECOVERY | A recovery operation encounters an error. | RFC-0412 |
| EVT-STOR-CACHE-HIT | Cache Hit | CACHE | A cached resource is served. | RFC-0410 |
| EVT-STOR-CACHE-MISS | Cache Miss | CACHE | A resource is not found in cache. | RFC-0410 |
| EVT-STOR-CACHE-EVICTED | Cache Evicted | CACHE | A cache entry is removed by eviction policy. | RFC-0410 |
| EVT-STOR-CACHE-CLEARED | Cache Cleared | CACHE | The entire cache is flushed. | RFC-0410 |
| EVT-STOR-LOCK-ACQUIRED | Lock Acquired | LOCK | A lock is successfully obtained. | RFC-0417 |
| EVT-STOR-LOCK-RELEASED | Lock Released | LOCK | A lock is released or expires. | RFC-0417 |
| EVT-STOR-LOCK-DEADLOCK | Lock Deadlock | LOCK | A deadlock is detected between lock holders. | RFC-0417 |
| EVT-STOR-REP-SYNCED | Replication Synced | REPLICATION | A replication sync completes. | RFC-0418 |
| EVT-STOR-REP-LAG | Replication Lag | REPLICATION | Replication lag exceeds threshold. | RFC-0418 |
| EVT-STOR-EXT-INSTALLED | Extension Installed | EXTENSION | A custom extension is registered. | RFC-0419 |
| EVT-STOR-EXT-DISABLED | Extension Disabled | EXTENSION | A custom extension is deactivated. | RFC-0419 |
| EVT-STOR-MIG-STARTED | Migration Started | MIGRATION | A migration operation begins. | RFC-0408 |
| EVT-STOR-MIG-COMPLETED | Migration Completed | MIGRATION | A migration finishes successfully. | RFC-0408 |
| EVT-STOR-MIG-FAILED | Migration Failed | MIGRATION | A migration operation encounters an error. | RFC-0408 |
| EVT-STOR-SEC-ENCRYPT | Security Encryption | SECURITY | Data is encrypted at rest or in transit. | RFC-0409 |
| EVT-STOR-SEC-AUDIT | Security Audit | SECURITY | An audit log entry is recorded. | RFC-0409 |
| EVT-STOR-SEC-VIOLATION | Security Violation | SECURITY | A security policy is breached. | RFC-0409 |

## 4. Event Ordering Dimensions

Events are ordered along four independent dimensions:

| Dimension | Description | Ordering Guarantee |
|---|---|---|
| Temporal | Wall-clock time of emission. | Monotonically increasing per node. |
| Sequence | Monotonically increasing counter per resource. | Strictly ordered per resource. |
| Causal | Dependency-based ordering across resources. | Causal consistency enforced. |
| Partition | Logical grouping by resource namespace. | Ordered within partition. |

## 5. Validation Rules

1. Every event type identifier MUST match the regex ^EVT-STOR-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$.
2. Event names MUST be unique within their category.
3. Event emitters MUST include at minimum: event type, timestamp, sequence number, and resource identifier.
4. Implementations MUST NOT drop events under normal operating conditions.
5. Event retention periods MUST comply with RFC-0413 and RFC-0420.
6. Two or more event type identifiers MUST NOT share identical trigger semantics.
