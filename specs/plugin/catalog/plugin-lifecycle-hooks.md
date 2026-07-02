---
id: ATLAS-PLUGINSPEC-CATALOG-LCHOOKS
title: Plugin Lifecycle Hooks Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Lifecycle Hooks Catalog

## 1. Purpose

Documents all lifecycle hooks available to plugins during their lifetime.

## 2. Hook Categories

### Initialization Hooks
| Hook              | When Called              | Required |
|-------------------|--------------------------|----------|
| on_manifest_parse | Manifest loaded          | No       |
| on_init           | Before service creation  | No       |
| on_ready          | All deps resolved        | No       |

### Runtime Hooks
| Hook              | When Called              | Required |
|-------------------|--------------------------|----------|
| on_start          | Plugin activation        | No       |
| on_stop           | Plugin deactivation      | No       |
| on_error          | Plugin error occurs      | No       |

### Teardown Hooks
| Hook              | When Called              | Required |
|-------------------|--------------------------|----------|
| on_drain          | In-flight work completing| No       |
| on_dispose        | Resources releasing      | No       |
| on_uninstall      | Plugin removal           | No       |

## 3. Hook Execution Order

on_manifest_parse -> on_init -> on_ready -> on_start -> [running] -> on_stop -> on_drain -> on_dispose -> on_uninstall

## 4. Cross-References

- RFC-0203 Plugin Lifecycle
- catalog/plugin-hooks.md
