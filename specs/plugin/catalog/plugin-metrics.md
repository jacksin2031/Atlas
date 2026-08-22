---
id: ATLAS-PLUGINSPEC-CATALOG-METRICS
title: Plugin Metrics Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Metrics Catalog

## 1. Purpose

Documents all standard metrics emitted by plugins and the runtime plugin subsystem.

## 2. Counter Metrics

| Metric Name              | Type   | Description                        |
|--------------------------|--------|------------------------------------|
| plugin_load_total        | Counter| Total plugin loads                 |
| plugin_load_success      | Counter| Successful plugin loads            |
| plugin_load_fail         | Counter| Failed plugin loads                |
| plugin_reload_total      | Counter| Total plugin reloads               |
| plugin_crash_total       | Counter| Total plugin crashes               |
| ipc_message_total        | Counter| Total IPC messages sent/received   |
| capability_call_total    | Counter| Total capability calls             |
| permission_grant_total   | Counter| Total permission grants            |
| permission_deny_total    | Counter| Total permission denials           |

## 3. Gauge Metrics

| Metric Name              | Type   | Description                        | Unit  |
|--------------------------|--------|------------------------------------|-------|
| plugin_memory_used       | Gauge  | Plugin memory usage                | MB    |
| plugin_cpu_usage         | Gauge  | Plugin CPU usage                   | %     |
| plugin_active_services   | Gauge  | Number of active services          | count |
| plugin_ipc_queue_depth   | Gauge  | IPC message queue depth            | count |
| plugin_cache_size        | Gauge  | Plugin resource cache size         | MB    |

## 4. Histogram Metrics

| Metric Name              | Type     | Description                        | Buckets          |
|--------------------------|----------|------------------------------------|------------------|
| plugin_load_duration     | Histogram| Plugin load time                   | 100ms-10s        |
| ipc_latency              | Histogram| IPC message latency                | 0.1ms-5s         |
| capability_latency       | Histogram| Capability call latency            | 0.1ms-10s        |
| permission_check_latency | Histogram| Permission check latency           | 0.01ms-100ms     |

## 5. Cross-References

- RFC-0229 Plugin Telemetry
