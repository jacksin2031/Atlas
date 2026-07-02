---
id: ATLAS-PLUGINSPEC-CATALOG-HEALTH
title: Plugin Health Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Health Catalog

## 1. Purpose

Documents health status definitions and health check procedures for plugins.

## 2. Health Status Values

| Status      | Numeric Code | Description                        |
|-------------|--------------|------------------------------------|
| healthy     | 0            | Operating normally                 |
| degraded    | 1            | Operating with reduced capability  |
| unhealthy   | 2            | Failing or unresponsive            |
| unknown     | 3            | Status cannot be determined        |

## 3. Health Check Types

| Check         | Interval | Timeout | Method                          |
|---------------|----------|---------|---------------------------------|
| Liveness      | 30s      | 5s      | Ping endpoint / heartbeat       |
| Readiness     | 10s      | 2s      | Capability availability check   |
| Startup       | Once     | 30s     | Init hook completion            |
| Dependency    | 60s      | 10s     | Dependency resolution check     |

## 4. Health Score Calculation

```
health_score = (uptime_ratio * 0.4) + (error_rate * -0.3) + (latency_factor * 0.2) + (capability_factor * 0.1)
```

Score range: 0.0 (dead) to 1.0 (perfect).

## 5. Cross-References

- RFC-0229 Plugin Telemetry
- RFC-0230 Plugin Diagnostics
