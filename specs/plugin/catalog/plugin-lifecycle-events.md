---
id: ATLAS-PLUGINSPEC-CATALOG-LCEVENTS
title: Plugin Lifecycle Events Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Lifecycle Events Catalog

## 1. Purpose

This catalog defines the canonical set of lifecycle events emitted by the Atlas runtime during plugin discovery, loading, activation, and unloading. These events enable observability, debugging, and reactive plugin orchestration.

## 2. Stable ID Prefix

All lifecycle event identifiers use the prefix LCE-.

## 3. Complete Events Table

| Stable ID | Event Name            | Payload Schema                                            | When Emitted                              | Listeners                    | Ordering |
|-----------|-----------------------|-----------------------------------------------------------|-------------------------------------------|------------------------------|----------|
| LCE-DISC  | plugin.discovering    | { source: string, timestamp: ISO8601 }                  | Discovery scan begins for a source        | Registry, Logger             | Total    |
| LCE-FOUND | plugin.discovered     | { plugin_id: string, version: string, source: string }  | A plugin is found during discovery        | Registry, Marketplace        | Total    |
| LCE-INDEX | plugin.index-updated  | { added: string[], removed: string[], updated: string[] }| Plugin index cache is refreshed           | Registry, UI                 | Total    |
| LCE-LOAD  | plugin.loading        | { plugin_id: string, manifest_path: string }            | Plugin manifest is being parsed           | Logger, Security             | Causal   |
| LCE-LOADED| plugin.loaded         | { plugin_id: string, version: string, hooks: string[] } | Plugin manifest parsed successfully       | Registry, Lifecycle Manager  | Causal   |
| LCE-DEP   | plugin.resolving_deps | { plugin_id: string, dependencies: string[] }           | Plugin dependency resolution begins       | Dependency Manager           | Causal   |
| LCE-READY | plugin.ready          | { plugin_id: string, capabilities: string[] }           | All dependencies resolved, plugin ready   | Capability Manager, Registry | Causal   |
| LCE-START | plugin.started        | { plugin_id: string, start_time_ms: number }            | Plugin activation completed               | Logger, Metrics              | Causal   |
| LCE-STOP  | plugin.stopping       | { plugin_id: string, reason: string }                   | Plugin deactivation requested             | Lifecycle Manager            | Causal   |
| LCE-STOPS | plugin.stopped        | { plugin_id: string, stop_time_ms: number }             | Plugin deactivation completed             | Logger, Metrics              | Causal   |
| LCE-UNLD  | plugin.unloaded       | { plugin_id: string, unload_time_ms: number }           | Plugin resources fully released           | Registry, Storage Manager    | Causal   |
| LCE-ERR   | plugin.error          | { plugin_id: string, error_code: string, message: string, stack?: string } | Plugin encounters a fatal or non-fatal error | Logger, Security, UI | Causal   |
| LCE-UPDST | plugin.updating       | { plugin_id: string, from_version: string, to_version: string } | Plugin update initiated            | Registry, Marketplace        | Causal   |
| LCE-UPDOK | plugin.updated        | { plugin_id: string, new_version: string }              | Plugin update completed successfully      | Registry, UI                 | Causal   |
| LCE-DISBL | plugin.disabled       | { plugin_id: string, reason: string }                   | Plugin disabled (temporarily)             | Registry, UI                 | Causal   |
| LCE-ENBLD | plugin.enabled        | { plugin_id: string }                                   | Plugin re-enabled                         | Registry, Lifecycle Manager  | Causal   |

## 4. Ordering Guarantees

- **Total Order**: Events with Total ordering are globally ordered across all plugins.
- **Causal Order**: Events with Causal ordering are ordered within a single plugin's lifecycle. Cross-plugin causal chains are preserved.
- The sequence plugin.loading -> plugin.loaded -> plugin.ready -> plugin.started MUST always occur in this order for each plugin.
- The sequence plugin.stopping -> plugin.stopped -> plugin.unloaded MUST always occur in this order.

## 5. Event Bus Delivery

- Events are delivered synchronously to registered listeners by default.
- Async listeners MAY be registered via on_config_change hook.
- Dropped events MUST be logged with a warning.
- Maximum listener execution time per event: 3 seconds.

## 6. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0210 Plugin Events
- RFC-0203 Plugin Lifecycle
