---
id: ATLAS-PLUGINSPEC-CATALOG-TELEM
title: Plugin Telemetry Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Telemetry Catalog

## 1. Purpose

Documents telemetry event types and their payload schemas.

## 2. Telemetry Event Types

| Event                    | Payload Schema                                     |
|--------------------------|----------------------------------------------------|
| plugin.health_changed    | `{ plugin_id, status, score, timestamp }`          |
| plugin.latency_sample    | `{ plugin_id, operation, latency_ms, timestamp }`  |
| plugin.memory_snapshot   | `{ plugin_id, heap_used_mb, rss_mb, timestamp }`   |
| plugin.crash_reported    | `{ plugin_id, crash_type, stack_trace, timestamp }`|
| plugin.warning_emitted   | `{ plugin_id, warning_type, message, timestamp }`  |
| plugin.capability_used   | `{ plugin_id, capability, call_count, timestamp }` |

## 3. Telemetry Collection Intervals

| Metric Type    | Default Interval | Min    | Max     |
|----------------|------------------|--------|---------|
| Health         | 10 seconds       | 1 sec  | 60 sec  |
| Latency        | 5 seconds        | 1 sec  | 30 sec  |
| Memory         | 30 seconds       | 5 sec  | 120 sec |
| Capability     | 60 seconds       | 10 sec | 300 sec |

## 4. Cross-References

- RFC-0229 Plugin Telemetry
