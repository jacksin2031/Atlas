---
id: ATLAS-STORAGE-CATALOG-METRICS
title: Storage Metrics Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Metrics Catalog

## 1. Purpose

This catalog defines the canonical set of metric names collected by the Atlas Storage subsystem for observability, performance monitoring, and compliance reporting.

## 2. Metric ID Prefix

All metric identifiers use the prefix MTR-STOR-.

## 3. Complete Metric Catalog

### 3.1 Operation Latency Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-READ-LATENCY | Read Latency | microseconds | Time from read request to response. | RFC-0414 |
| MTR-STOR-WRITE-LATENCY | Write Latency | microseconds | Time from write request to acknowledgment. | RFC-0414 |
| MTR-STOR-DELETE-LATENCY | Delete Latency | microseconds | Time from delete request to confirmation. | RFC-0414 |
| MTR-STOR-QUERY-LATENCY | Query Latency | microseconds | Time from query to result delivery. | RFC-0414 |
| MTR-STOR-TX-LATENCY | Transaction Latency | microseconds | End-to-end transaction duration. | RFC-0414 |

### 3.2 Operation Throughput Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-READ-TPS | Read Throughput | ops/sec | Read operations per second. | RFC-0414 |
| MTR-STOR-WRITE-TPS | Write Throughput | ops/sec | Write operations per second. | RFC-0414 |
| MTR-STOR-QUERY-TPS | Query Throughput | ops/sec | Query operations per second. | RFC-0414 |
| MTR-STOR-TX-COMMIT-TPS | Commit Throughput | ops/sec | Committed transactions per second. | RFC-0414 |
| MTR-STOR-TX-ABORT-TPS | Abort Throughput | ops/sec | Aborted transactions per second. | RFC-0414 |

### 3.3 Cache Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-CACHE-HIT-RATE | Cache Hit Ratio | percentage | Percentage of hits vs total lookups. | RFC-0410 |
| MTR-STOR-CACHE-EVICT-RATE | Eviction Rate | evictions/sec | Cache entries evicted per second. | RFC-0410 |
| MTR-STOR-CACHE-SIZE | Cache Size | bytes | Current memory footprint of cache. | RFC-0410 |
| MTR-STOR-CACHE-ELEMENTS | Cache Elements | count | Number of entries in cache. | RFC-0410 |

### 3.4 Transaction Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-TX-COMMIT-RATE | Commit Rate | tx/sec | Successful commits per second. | RFC-0406 |
| MTR-STOR-TX-ABORT-RATE | Abort Rate | tx/sec | Aborted transactions per second. | RFC-0406 |
| MTR-STOR-TX-CONFLICT-RATE | Conflict Rate | conflicts/sec | Detected conflicts per second. | RFC-0406 |
| MTR-STOR-TX-ACTIVE-COUNT | Active Transactions | count | Currently open transactions. | RFC-0406 |

### 3.5 Lock Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-LOCK-WAIT-TIME | Lock Wait Time | microseconds | Average time waiting for lock acquisition. | RFC-0417 |
| MTR-STOR-LOCK-HELD-COUNT | Held Locks | count | Number of currently held locks. | RFC-0417 |
| MTR-STOR-LOCK-DEADLOCK-COUNT | Deadlocks | count | Total deadlocks detected. | RFC-0417 |

### 3.6 Replication Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-REP-LAG | Replication Lag | seconds | Time delay between primary and replica. | RFC-0418 |
| MTR-STOR-REP-SYNC-RATE | Sync Rate | records/sec | Replication synchronization throughput. | RFC-0418 |
| MTR-STOR-REP-DIVERGENCE-COUNT | Divergences | count | Detected replica divergences. | RFC-0418 |

### 3.7 Backup and Recovery Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-BKP-DURATION | Backup Duration | seconds | Time to complete a backup. | RFC-0411 |
| MTR-STOR-BKP-SIZE | Backup Size | bytes | Total size of backup data. | RFC-0411 |
| MTR-STOR-REC-DURATION | Recovery Duration | seconds | Time to complete a recovery. | RFC-0412 |
| MTR-STOR-REC-SUCCESS-RATE | Recovery Success Rate | percentage | Percentage of successful recoveries. | RFC-0412 |

### 3.8 Capacity Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-USAGE-TOTAL | Total Usage | bytes | Overall storage consumption. | RFC-0415 |
| MTR-STOR-USAGE-TENANT | Tenant Usage | bytes | Per-tenant storage consumption. | RFC-0409 |
| MTR-STOR-USAGE-PERCENT | Usage Percent | percentage | Percentage of capacity utilized. | RFC-0415 |

### 3.9 Error and Health Metrics

| Metric ID | Name | Unit | Description | RFC Reference |
|---|---|---|---|---|
| MTR-STOR-ERROR-RATE | Error Rate | errors/sec | Storage operation error rate. | RFC-0414 |
| MTR-STOR-HEALTH-STATUS | Health Status | enum | Overall subsystem health indicator. | RFC-0414 |
| MTR-STOR-PROVIDER-HEALTH | Provider Health | enum | Individual provider health status. | RFC-0403 |

## 4. Collection Methods

| Method | Description | Applicable Metrics |
|---|---|---|
| Counter | Monotonically increasing value. | Throughput, error counts. |
| Gauge | Current value at time of measurement. | Cache size, held locks. |
| Histogram | Distribution of values across buckets. | Latency metrics. |
| Summary | Pre-computed quantiles. | Latency metrics. |
| Enum | Discrete state value. | Health status. |

## 5. Validation Rules

1. Every metric identifier MUST match the regex ^MTR-STOR-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$.
2. Metric names MUST be unique within their category.
3. Collectors MUST report metrics at intervals no greater than the configured flush period.
4. Metrics MUST include at minimum: identifier, value, timestamp, and dimension labels.
5. Implementations MUST NOT introduce metric identifiers outside this catalog.
