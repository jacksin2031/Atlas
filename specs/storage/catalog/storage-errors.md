---
id: ATLAS-STORAGE-CATALOG-ERRORS
title: Storage Errors Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Errors Catalog

## 1. Purpose

This catalog defines the canonical set of error codes that the Atlas Storage subsystem MAY return to indicate failures during resource operations, transaction processing, lifecycle management, schema validation, backup, recovery, caching, security enforcement, versioning, migration, consistency checks, locking, replication, extension loading, observability collection, performance degradation, and compliance violations.

## 2. Stable ID Prefix

All error code identifiers use the prefix STOR-.

### 2.1 Naming Convention

Error code identifiers SHALL follow the pattern:

`
STOR-<CATEGORY>-<FAILURE>
`

where <CATEGORY> identifies the failure domain and <FAILURE> describes the specific error condition.

## 3. Complete Error Code Catalog

### 3.1 Provider Errors (STOR-PROVIDER)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-PROVIDER-NOT-FOUND | Provider Not Found | PROVIDER | No provider matched the requested configuration. |
| STOR-PROVIDER-UNAVAILABLE | Provider Unavailable | PROVIDER | The provider is not reachable or healthy. |
| STOR-PROVIDER-INIT-FAILED | Provider Init Failed | PROVIDER | Provider initialization returned an error. |
| STOR-PROVIDER-CAP-MISMATCH | Provider Cap Mismatch | PROVIDER | Provider lacks a required capability. |
| STOR-PROVIDER-CONFIG-INVALID | Provider Config Invalid | PROVIDER | Provider configuration failed validation. |

### 3.2 Transaction Errors (STOR-TX)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-TX-ABORTED | Transaction Aborted | TRANSACTION | Transaction was aborted by the system. |
| STOR-TX-CONFLICT | Transaction Conflict | TRANSACTION | Write-write conflict detected. |
| STOR-TX-TIMEOUT | Transaction Timeout | TRANSACTION | Transaction exceeded its allotted duration. |
| STOR-TX-NESTED-INVALID | Nested Invalid | TRANSACTION | Nested transaction violates depth rules. |
| STOR-TX-ISOLATION-LOW | Isolation Below Threshold | TRANSACTION | Current isolation level insufficient for operation. |

### 3.3 Schema Errors (STOR-SCHEMA)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-SCHEMA-INVALID | Schema Invalid | SCHEMA | Resource failed schema validation. |
| STOR-SCHEMA-VERSION-MISMATCH | Schema Version Mismatch | SCHEMA | Resource schema version does not match declared version. |
| STOR-SCHEMA-FIELD-REQUIRED | Field Required | SCHEMA | A required field is missing from the resource. |
| STOR-SCHEMA-FIELD-TYPE | Field Type Error | SCHEMA | A field value has an incorrect type. |
| STOR-SCHEMA-EVOLUTION-INVALID | Evolution Invalid | SCHEMA | Schema change violates evolution rules. |

### 3.4 Lifecycle Errors (STOR-LIFECYCLE)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-LC-TRANSITION-INVALID | Invalid Transition | LIFECYCLE | State transition is not permitted. |
| STOR-LC-TIMEOUT | Lifecycle Timeout | LIFECYCLE | Lifecycle hook exceeded its time limit. |
| STOR-LC-STATE-UNKNOWN | Unknown State | LIFECYCLE | Resource is in an unrecognized state. |
| STOR-LC-PENDING-DEPS | Pending Dependencies | LIFECYCLE | Required dependencies are not yet satisfied. |

### 3.5 Cache Errors (STOR-CACHE)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-CACHE-MISS | Cache Miss | CACHE | Resource not found in any cache layer. |
| STOR-CACHE-EVICTED | Cache Evicted | CACHE | Cached resource was evicted before access. |
| STOR-CACHE-CORRUPT | Cache Corrupt | CACHE | Cache entry failed integrity check. |
| STOR-CACHE-OVERFLOW | Cache Overflow | CACHE | Cache capacity exceeded; eviction failed. |
| STOR-CACHE-INCOHERENT | Cache Incoherent | CACHE | Cache state inconsistent with persistent store. |

### 3.6 Backup Errors (STOR-BACKUP)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-BKP-FAILED | Backup Failed | BACKUP | Backup operation encountered an error. |
| STOR-BKP-INTEGRITY | Backup Integrity Fail | BACKUP | Backup checksum verification failed. |
| STOR-BKP-RETENTION-EXCEEDED | Retention Exceeded | BACKUP | Backup count exceeds retention policy. |
| STOR-BKP-TARGET-UNAVAILABLE | Target Unavailable | BACKUP | Backup destination is not accessible. |

### 3.7 Recovery Errors (STOR-RECOVERY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-REC-FAILED | Recovery Failed | RECOVERY | Recovery operation encountered an error. |
| STOR-REC-SOURCE-INVALID | Source Invalid | RECOVERY | Recovery source is corrupted or incomplete. |
| STOR-REC-DEPS-UNMET | Dependencies Unmet | RECOVERY | Recovery dependencies not satisfied. |
| STOR-REC-RPO-EXCEEDED | RPO Exceeded | RECOVERY | Recovery point exceeds the RPO threshold. |

### 3.8 Security Errors (STOR-SECURITY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-SEC-AUTH-FAILED | Auth Failed | SECURITY | Authentication verification failed. |
| STOR-SEC-AUTHZ-DENIED | Authz Denied | SECURITY | Authorization check denied the operation. |
| STOR-SEC-ENCRYPTION-FAILED | Encryption Failed | SECURITY | Cryptographic operation failed. |
| STOR-SEC-KEY-EXPIRED | Key Expired | SECURITY | Encryption key has passed its validity period. |
| STOR-SEC-CLASSIFICATION-MISSING | Classification Missing | SECURITY | Resource lacks required data classification. |

### 3.9 Versioning Errors (STOR-VERSION)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-VER-CONFLICT | Version Conflict | VERSIONING | Concurrent version updates detected. |
| STOR-VER-RESOLVE-AMBIGUOUS | Resolve Ambiguous | VERSIONING | Multiple versions match resolution criteria. |
| STOR-VER-TAMPER-DETECTED | Tamper Detected | VERSIONING | Version chain integrity compromised. |
| STOR-VER-PRUNE-ACTIVE | Prune Active | VERSIONING | Attempted to prune an active version. |

### 3.10 Migration Errors (STOR-MIGRATION)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-MIG-FAILED | Migration Failed | MIGRATION | Migration operation encountered an error. |
| STOR-MIG-ROLLBACK-FAILED | Rollback Failed | MIGRATION | Reverting migration failed. |
| STOR-MIG-VALIDATION-FAIL | Validation Failed | MIGRATION | Post-migration validation did not pass. |
| STOR-MIG-CANARY-ABORT | Canary Abort | MIGRATION | Canary deployment triggered abort. |

### 3.11 Consistency Errors (STOR-CONSISTENCY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-CONS-CONFLICT | Conflict Detected | CONSISTENCY | Conflicting writes to the same resource. |
| STOR-CONS-ORDER-VIOLATION | Order Violation | CONSISTENCY | Event ordering constraint violated. |
| STOR-CONS-STALE-READ | Stale Read | CONSISTENCY | Read returned data older than expected. |
| STOR-CONS-DIVERGENCE | Divergence Detected | CONSISTENCY | Data diverged across replicas. |

### 3.12 Locking Errors (STOR-LOCK)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-LCK-ACQUIRE-FAILED | Acquire Failed | LOCKING | Lock could not be obtained. |
| STOR-LCK-DEADLOCK | Deadlock Detected | LOCKING | Circular lock dependency detected. |
| STOR-LCK-EXPIRED | Lock Expired | LOCKING | Lock lease elapsed before operation completed. |
| STOR-LCK-ESCALATION-FAILED | Escalation Failed | LOCKING | Lock escalation to coarser granularity failed. |

### 3.13 Replication Errors (STOR-REPLICATION)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-REP-SYNC-FAILED | Sync Failed | REPLICATION | Replication synchronization failed. |
| STOR-REP-LAG-CRITICAL | Lag Critical | REPLICATION | Replication lag exceeds critical threshold. |
| STOR-REP-FAILOVER-FAILED | Failover Failed | REPLICATION | Automatic failover could not complete. |
| STOR-REP-DIVERGENCE | Divergence | REPLICATION | Replicas hold conflicting data. |

### 3.14 Extension Errors (STOR-EXTENSION)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-EXT-INSTALL-FAILED | Install Failed | EXTENSION | Extension registration failed validation. |
| STOR-EXT-HOOK-FAILED | Hook Failed | EXTENSION | Custom hook returned an error. |
| STOR-EXT-VERSION-MISMATCH | Version Mismatch | EXTENSION | Extension version incompatible with host. |

### 3.15 Observability Errors (STOR-OBSERVABILITY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-OBS-METRIC-FAILED | Metric Failed | OBSERVABILITY | Metric collection encountered an error. |
| STOR-OBS-TRACE-LOST | Trace Lost | OBSERVABILITY | Distributed trace context was dropped. |
| STOR-OBS-LOG-DROPPED | Log Dropped | OBSERVABILITY | Log entry dropped due to backpressure. |

### 3.16 Performance Errors (STOR-PERFORMANCE)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-PERF-LATENCY-EXCEEDED | Latency Exceeded | PERFORMANCE | Operation latency exceeds target. |
| STOR-PERF-THROUGHPUT-LOW | Throughput Low | PERFORMANCE | Throughput falls below minimum threshold. |
| STOR-PERF-DEGRADED | Degraded | PERFORMANCE | System entered degradation tier. |

### 3.17 Compliance Errors (STOR-COMPLIANCE)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-COMP-FAILED | Compliance Failed | COMPLIANCE | Compliance check did not pass. |
| STOR-COMP-AUDIT-MISSING | Audit Missing | COMPLIANCE | Required audit trail is incomplete. |

### 3.18 Capacity Errors (STOR-CAPACITY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-CAP-EXCEEDED | Capacity Exceeded | CAPACITY | Storage capacity limit reached. |
| STOR-CAP-QUOTA-EXCEEDED | Quota Exceeded | CAPACITY | Tenant quota limit reached. |

### 3.19 Integrity Errors (STOR-INTEGRITY)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-INT-CORRUPTION | Data Corruption | INTEGRITY | Data integrity check failed. |
| STOR-INT-METADATA-MISMATCH | Metadata Mismatch | INTEGRITY | Metadata and payload are inconsistent. |

### 3.20 Permission Errors (STOR-PERMISSION)

| Stable ID | Error Name | Category | Description |
|---|---|---|---|
| STOR-PERM-DENIED | Permission Denied | PERMISSION | Insufficient permissions for operation. |
| STOR-PERM-ROLE-UNKNOWN | Role Unknown | PERMISSION | Requested role is not recognized. |

## 4. Validation Rules

1. Every error code identifier MUST match the regex ^STOR-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$.
2. Error codes MUST be reported as immutable, opaque strings.
3. Implementations MUST NOT introduce error codes outside this catalog.
4. Two or more error codes MUST NOT share identical failure semantics.
5. Error codes MUST include at minimum: code identifier, category, and a machine-readable description.
