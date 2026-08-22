---
id: ATLAS-PLUGINSPEC-CATALOG-RECOVERY
title: Plugin Recovery Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Recovery Catalog

## 1. Purpose

Documents recovery strategies for failed plugins.

## 2. Recovery Strategies

| Strategy          | Description                              | Use Case                        |
|-------------------|------------------------------------------|---------------------------------|
| Restart           | Reload the plugin from disk              | Transient errors                |
| Rollback          | Restore previous version                 | Bad update                      |
| Disable           | Temporarily disable the plugin           | Persistent errors               |
| Quarantine        | Isolate the plugin, prevent loading      | Security concerns               |
| Uninstall         | Remove the plugin entirely               | Unrecoverable state             |

## 3. Recovery Decision Tree

```
Plugin Error
  |
  +--> Transient? --> Yes --> Restart (max 3 times)
  |                      |
  |                      No
  |                      v
  +--> Update-related? --> Yes --> Rollback
  |                          |
  |                          No
  |                          v
  +--> Security issue? --> Yes --> Quarantine
  |                          |
  |                          No
  |                          v
  +--> Persistent? --> Yes --> Disable
```

## 4. Recovery Limits

- Max restart attempts: 3 (configurable).
- Max restart window: 5 minutes (cooldown after 3 failures).
- Quarantine duration: Until operator intervention.

## 5. Cross-References

- RFC-0225 Plugin Hot Reload
- RFC-0230 Plugin Diagnostics
