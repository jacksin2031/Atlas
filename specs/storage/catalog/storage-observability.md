---
id: ATLAS-STORAGE-CATALOG-OBSERVABILITY
title: Storage Observability Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Observability Catalog

## 1. Purpose

This catalog defines the canonical observability categories, dashboard views, and alerting configurations used by the Atlas Storage subsystem.

## 2. Observability Pillar Catalog

| Pillar ID | Name | Description | Data Source | RFC Reference |
|---|---|---|---|---|
| OBS-METRICS | Metrics | Numerical measurements of storage operations over time. | Prometheus-compatible exporters. | RFC-0414 |
| OBS-TRACES | Traces | End-to-end request flow visualization across subsystems. | OpenTelemetry-compatible propagators. | RFC-0414 |
| OBS-LOGS | Logs | Structured textual records of storage operations. | JSON-structured log output. | RFC-0414 |
| OBS-HEALTH | Health Checks | Liveness and readiness probes for subsystem components. | HTTP probe endpoints. | RFC-0414 |
| OBS-ALERTS | Alerts | Threshold-based notifications for anomalous conditions. | Metric evaluation engine. | RFC-0414 |
| OBS-AUDIT | Audit Trails | Immutable records of security-relevant operations. | Append-only audit log. | RFC-0409 |
| OBS-DASHBOARDS | Dashboards | Curated views of observability data for operators. | Metric and trace aggregation. | RFC-0414 |
| OBS-PROFILING | Profiling | CPU and memory usage analysis for performance tuning. | Sampling profilers. | RFC-0415 |
| OBS-CAPACITY | Capacity Planning | Trend analysis of storage consumption over time. | Historical metric aggregation. | RFC-0415 |

## 3. Dashboard View Catalog

| Dashboard ID | Name | Description | Primary Audience | RFC Reference |
|---|---|---|---|---|
| DB-OPERATIONAL | Operational Overview | Real-time health, throughput, and error rates. | Operators | RFC-0414 |
| DB-LATENCY | Latency Analysis | P50/P95/P99 latency distributions per operation. | Engineers | RFC-0414 |
| DB-TRANSACTION | Transaction Health | Commit/abort rates, conflict frequency, lock wait times. | Engineers | RFC-0406 |
| DB-CACHE | Cache Performance | Hit ratios, eviction rates, memory utilization. | Engineers | RFC-0410 |
| DB-SECURITY | Security Posture | Auth failures, policy violations, audit trail summary. | Security Officers | RFC-0409 |
| DB-BACKUP | Backup Status | Backup schedules, success rates, storage consumption. | Operators | RFC-0411 |
| DB-RECOVERY | Recovery Readiness | RPO/RTO compliance, recovery drill results. | Operators | RFC-0412 |
| DB-REPLICATION | Replication Health | Lag, divergence, sync status across nodes. | Operators | RFC-0418 |
| DB-CAPACITY | Capacity Trends | Growth projections, quota utilization, tier distribution. | Architects | RFC-0415 |
| DB-COMPLIANCE | Compliance Status | Policy adherence, audit completeness, classification coverage. | Auditors | RFC-0420 |

## 4. Alert Threshold Catalog

| Alert ID | Name | Metric | Condition | Severity | RFC Reference |
|---|---|---|---|---|---|
| ALT-LATENCY-P99 | P99 Latency High | Operation Latency | P99 > target for 5 min | Warning | RFC-0414 |
| ALT-LATENCY-P99-CRIT | P99 Latency Critical | Operation Latency | P99 > 2x target for 2 min | Critical | RFC-0414 |
| ALT-ERROR-RATE | Error Rate High | Error Rate | Error rate > 1% for 3 min | Warning | RFC-0414 |
| ALT-ERROR-RATE-CRIT | Error Rate Critical | Error Rate | Error rate > 5% for 1 min | Critical | RFC-0414 |
| ALT-CACHE-HIT | Cache Hit Low | Cache Hit Ratio | Ratio < 50% for 10 min | Warning | RFC-0410 |
| ALT-TX-CONFLICT | High Conflict Rate | Conflict Rate | Conflicts > threshold for 5 min | Warning | RFC-0406 |
| ALT-LOCK-DEADLOCK | Deadlock Detected | Deadlock Count | Count > 0 | Critical | RFC-0417 |
| ALT-REP-LAG | Replication Lag High | Replication Lag | Lag > threshold for 2 min | Warning | RFC-0418 |
| ALT-REP-LAG-CRIT | Replication Lag Critical | Replication Lag | Lag > 2x threshold for 1 min | Critical | RFC-0418 |
| ALT-CAPACITY | Capacity High | Usage Percent | Usage > 80% | Warning | RFC-0415 |
| ALT-CAPACITY-CRIT | Capacity Critical | Usage Percent | Usage > 95% | Critical | RFC-0415 |
| ALT-BKP-FAILED | Backup Failed | Backup Status | Any backup fails | Critical | RFC-0411 |
| ALT-REC-FAILED | Recovery Failed | Recovery Status | Recovery test fails | Critical | RFC-0412 |
| ALT-SEC-VIOLATION | Security Violation | Violation Count | Count > 0 | Critical | RFC-0409 |
| ALT-HEALTH-DEGRADED | Health Degraded | Health Status | Status != running | Warning | RFC-0414 |

## 5. Validation Rules

1. Every observability pillar identifier MUST match the regex ^OBS-[A-Z]+$.
2. Every dashboard identifier MUST match the regex ^DB-[A-Z]+$.
3. Every alert identifier MUST match the regex ^ALT-[A-Z][A-Z0-9]*$.
4. Alert thresholds MUST be configurable per deployment environment.
5. Dashboard views MUST be readable by all roles with PERM-STOR-OBSERVE permission.
6. Audit trail data MUST be immutable once written.
7. Profiling data MUST NOT be collected in production without explicit authorization.
