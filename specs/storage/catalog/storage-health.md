---
id: ATLAS-STORAGE-CATALOG-HEALTH
title: Storage Health States Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Health States Catalog

## 1. Purpose

This catalog defines the canonical set of health states for the Storage subsystem and its providers.

## 2. Health State Prefix

All health state identifiers use the prefix HLTH-.

## 3. Complete Health State Catalog

| State ID | Name | Description | Auto-Recovery | Operator Action Required | RFC Reference |
|---|---|---|---|---|---|
| HLTH-HEALTHY | Healthy | All systems operational. | N/A | No | RFC-0414 |
| HLTH-WARNING | Warning | Degraded performance or approaching limits. | Partial | Monitoring | RFC-0414 |
| HLTH-DEGRADED | Degraded | Reduced functionality; some providers unavailable. | Partial | Assessment | RFC-0414 |
| HLTH-RECOVERY | Recovery | Automatic recovery procedure in progress. | Yes | Monitoring | RFC-0412 |
| HLTH-READONLY | Read Only | Write operations suspended; reads continue. | Yes | Investigation | RFC-0414 |
| HLTH-OFFLINE | Offline | Subsystem not accepting any operations. | No | Manual restart | RFC-0414 |
| HLTH-CORRUPTED | Corrupted | Data integrity violation detected. | No | Manual repair | RFC-0412 |
| HLTH-DRAINING | Draining | Completing in-flight operations before shutdown. | No | Monitoring | RFC-0414 |
| HLTH-MAINTENANCE | Maintenance | Scheduled maintenance mode; limited operations. | No | Scheduled window | RFC-0414 |
| HLTH-QUARANTINED | Quarantined | Provider isolated pending investigation. | No | Investigation | RFC-0403 |

## 4. Health State Transitions

| From | To | Trigger |
|---|---|---|
| HEALTHY | WARNING | Metric threshold breach |
| WARNING | DEGRADED | Multiple threshold breaches |
| DEGRADED | RECOVERY | Auto-recovery initiated |
| RECOVERY | HEALTHY | Recovery succeeded |
| RECOVERY | CORRUPTED | Recovery detected corruption |
| DEGRADED | READONLY | Write safety protocol engaged |
| READONLY | RECOVERY | Recovery initiated |
| CORRUPTED | RECOVERY | Repair initiated |
| OFFLINE | MAINTENANCE | Scheduled maintenance |
| QUARANTINED | OFFLINE | Full isolation required |

## 5. Validation Rules

1. Every health state identifier MUST match the regex ^HLTH-[A-Z]+$.
2. Health state transitions MUST follow the defined transition table.
3. CORRUPTED and OFFLINE states require operator acknowledgment.
4. Health state changes MUST produce events per RFC-0413.
