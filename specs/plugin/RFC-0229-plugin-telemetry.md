# RFC-0229: Plugin Telemetry

RFC: RFC-0229
Title: Plugin Telemetry
Status: Proposed
Version: 1.0.0
Category: Plugin Operations
Layer: Observability
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0210 Plugin Events
  - RFC-0207 Plugin Security
Related RFC:
  - RFC-0220 Plugin IPC
  - RFC-0230 Plugin Diagnostics
  - RFC-0224 Plugin Testing
Related ADR:
  - ADR-0029 Telemetry Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the telemetry types (health, latency, memory, crash, warnings, capability usage), telemetry collection, telemetry aggregation, telemetry privacy, telemetry export, telemetry retention, telemetry alerting, and telemetry dashboard requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Telemetry Philosophy](#4-telemetry-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Telemetry Types](#9-telemetry-types)
10. [Telemetry Collection](#10-telemetry-collection)
11. [Telemetry Aggregation](#11-telemetry-aggregation)
12. [Telemetry Privacy](#12-telemetry-privacy)
13. [Telemetry Export](#13-telemetry-export)
14. [Telemetry Retention](#14-telemetry-retention)
15. [Telemetry Alerting](#15-telemetry-alerting)
16. [Telemetry Dashboard](#16-telemetry-dashboard)
17. [Performance Budgets](#17-performance-budgets)
18. [Glossary](#18-glossary)
19. [Acceptance Criteria](#19-acceptance-criteria)
20. [Cross References](#20-cross-references)
21. [References](#21-references)
22. [Revision History](#22-revision-history)
23. [Future Evolution](#23-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Health Monitoring**: Track plugin health status (healthy, degraded, unhealthy).
2. **Latency Measurement**: Measure and report operation latencies.
3. **Memory Tracking**: Monitor plugin memory usage over time.
4. **Crash Reporting**: Capture and report plugin crashes with stack traces.
5. **Warning Collection**: Aggregate plugin warnings and anomalies.
6. **Capability Usage**: Track which capabilities are used and how often.
7. **Privacy Controls**: Ensure no sensitive data is collected.
8. **Enterprise Ready**: Support SLA monitoring and capacity planning.

---

- RFC-0323 Workflow Plugin Integration


## 4 Telemetry Philosophy

Telemetry follows these principles:

- Telemetry is COLLECTED by the runtime, NOT sent by plugins directly.
- Plugins expose metrics through a standard interface; the runtime collects them.
- Privacy is paramount: no user data, no secrets, no PII.
- Telemetry is OPTIONAL for plugins but REQUIRED for marketplace submission.
- Enterprise editions have enhanced telemetry requirements.

---


## 6 Boundaries

- Telemetry data is collected by the runtime, not pushed by plugins.
- Telemetry is scoped to the runtime instance.
- Telemetry data does NOT leave the runtime without explicit operator consent.
- Telemetry collection has a strict performance budget (< 1% of plugin CPU).

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugins
        P1[Plugin A]
        P2[Plugin B]
        P3[Plugin C]
    end
    subgraph Runtime Telemetry
        TC[Telemetry Collector]
        TA[Telemetry Aggregator]
        TE[Telemetry Exporter]
        AL[Alert Engine]
        DB[(Telemetry Store)]
    end
    P1 -->|exposes metrics| TC
    P2 -->|exposes metrics| TC
    P3 -->|exposes metrics| TC
    TC --> TA
    TA --> DB
    TA --> AL
    DB --> TE
    TE -->|export| EXT[External Systems]
`

---

| service_latency   | Average service resolution time      | ms      |
| startup_latency   | Time from load to ready              | ms      |
| p50_latency       | 50th percentile operation latency    | ms      |
| p95_latency       | 95th percentile operation latency    | ms      |
| p99_latency       | 99th percentile operation latency    | ms      |

### 9.3 Memory

Memory usage tracking:

| Metric              | Description                          | Unit    |
|---------------------|--------------------------------------|---------|
| heap_used         | Current heap memory usage            | MB      |
| heap_max          | Maximum heap memory allocation       | MB      |
| ss               | Resident set size                    | MB      |
| gc_count          | Garbage collection count             | count   |
| gc_pause_ms       | Total GC pause time                  | ms      |
|  leaked_objects   | Detected object leaks                | count   |

### 9.4 Crash

Crash report data:

`json
{
  "plugin_id": "my-plugin",
  "crash_time": "ISO8601",
  "crash_type": "exception | oom | segfault | hang",
  "stack_trace": "string",
  "error_message": "string",
  "error_code": "string",
  "uptime_before_crash_seconds": number,
  "active_operations": ["op1", "op2"],
  "memory_at_crash_mb": number
}
`

### 9.5 Warnings

Non-fatal issues that should be monitored:

| Warning Type          | Severity | Description                        |
|-----------------------|----------|------------------------------------|
| high_memory_usage   | Medium   | Memory usage exceeds 80% of quota  |
| slow_operation      | Low      | Operation exceeds latency threshold|
| deprecated_api      | Low      | Using deprecated API method        |
| permission_warning  | High     | Permission boundary near violation |
| cache_eviction      | Low      | Cache eviction rate increasing     |
| ipc_timeout         | Medium   | IPC call approaching timeout       |

### 9.6 Capability Usage

Tracks which capabilities are used and how often:

| Metric              | Description                          | Unit    |
|---------------------|--------------------------------------|---------|
| calls_total       | Total number of capability calls     | count   |
| calls_success     | Successful calls                     | count   |
| calls_failed      | Failed calls                         | count   |
| calls_latency_avg | Average call latency                 | ms      |
| calls_latency_p95 | 95th percentile call latency         | ms      |
| last_called       | Last time the capability was used    | ISO8601 |

---

Collection rules:
- Default collection interval: 10 seconds.
- Minimum collection interval: 1 second.
- Maximum collection interval: 60 seconds.
- Collection is PUSH-based (plugins expose metrics, runtime pulls).
- Collection timeout: 500ms per plugin.

---




## 13 Telemetry Export

Telemetry can be exported for external analysis:

`ash
atlas telemetry export --format json --range 24h --output telemetry.json
atlas telemetry export --format csv --range 7d --output metrics.csv
`

Export formats:
- JSON: Machine-readable, full detail.
- CSV: Spreadsheet-compatible, summary data.
- Prometheus: Prometheus exposition format.
- OpenTelemetry: OTLP format for external systems.

Export rules:
- Export requires operator authorization.
- Exported data excludes sensitive fields.
- Export is logged to the audit trail.

---


## 15 Telemetry Alerting

Alerts are triggered when metrics exceed thresholds:

| Alert                     | Condition                        | Severity | Action                    |
|---------------------------|----------------------------------|----------|---------------------------|
| Plugin Unhealthy          | Health status = unhealthy for 5min | Critical | Notify operator           |
| High Error Rate           | Error rate > 10% for 1min        | High     | Notify operator           |
| Memory Quota Exceeded     | Memory > 90% of quota            | Medium   | Log warning               |
| Crash Detected            | Plugin crash reported            | Critical | Auto-restart plugin       |
| Slow Operations           | p95 latency > 2x baseline        | Low      | Log warning               |
| Deprecated API Usage      | Plugin uses deprecated API       | Low      | Log warning               |

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 17 Performance Budgets

- Telemetry collection per plugin: < 1ms.
- Aggregation (all plugins): < 100ms.
- Export (1 hour of data): < 2 seconds.
- Dashboard rendering: < 500ms.
- Alert evaluation: < 10ms.
- Total telemetry overhead: < 1% of plugin CPU.

---

| RFC-0201 | Consumed | Plugin Overview |


## 19 Acceptance Criteria

1. GIVEN a plugin is running, WHEN telemetry collection runs, THEN health, latency, memory, and capability usage are all reported.
2. GIVEN a plugin crashes, WHEN the crash is detected, THEN a crash report is generated within 1 second.
3. GIVEN telemetry export is requested, WHEN the export completes, THEN no sensitive data (API keys, tokens) is included.
4. GIVEN a plugin's error rate exceeds 10% for 1 minute, WHEN the alert engine evaluates, THEN a High severity alert is triggered.
5. GIVEN telemetry collection is running, WHEN plugin CPU is measured, THEN the overhead is less than 1%.
6. GIVEN the retention policy is 30 days, WHEN 31 days elapse, THEN the telemetry data is deleted.

---



## 21 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [OpenTelemetry](https://opentelemetry.io/) — Open source telemetry framework.
- [Prometheus](https://prometheus.io/) — Monitoring system and time series database.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 23 Future Evolution

1. Support for distributed telemetry collection across multiple runtime instances.
2. Support for AI-assisted anomaly detection in telemetry data.
3. Support for custom telemetry exporters (Splunk, Datadog, Grafana).

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All plugin contracts are defined as abstract behavioral interfaces.

---




---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |