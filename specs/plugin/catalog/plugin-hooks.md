---
id: ATLAS-PLUGINSPEC-CATALOG-HOOKS
title: Plugin Hooks Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Hooks Catalog

## 1. Purpose

This catalog defines the canonical set of extension hooks in the Atlas Plugin subsystem. Hooks are callback points where the runtime notifies plugins of lifecycle events, configuration changes, permission requests, and system-level transitions.

## 2. Stable ID Prefix

All hook identifiers use the prefix HKN-.

### 2.1 Naming Convention

Hook identifiers SHALL follow the pattern:

`
HKN-<CATEGORY>-<NAME>
`

where <CATEGORY> is one of LC (lifecycle), CAP (capability), EXT (extension), EVT (event), SVC (service), CFG (configuration), STR (storage), SEC (security).

## 3. Complete Hooks Table

| Stable ID            | Hook Name              | Category    | Trigger Point                                  | Required | Handler Signature                                    |
|----------------------|------------------------|-------------|--------------------------------------------------|----------|------------------------------------------------------|
| HKN-LC-ON_INIT       | on_init                | Lifecycle   | Plugin manifest loaded, before initialization    | No       | n() -> Result<(), Error>                          |
| HKN-LC-ON_READY      | on_ready               | Lifecycle   | All dependencies resolved, plugin ready to start | No       | n() -> Result<(), Error>                          |
| HKN-LC-ON_START      | on_start               | Lifecycle   | Plugin activation requested                      | No       | n() -> Result<(), Error>                          |
| HKN-LC-ON_STOP       | on_stop                | Lifecycle   | Plugin deactivation requested                    | No       | n() -> Result<(), Error>                          |
| HKN-LC-ON_UNINSTALL  | on_uninstall           | Lifecycle   | Plugin uninstall initiated                       | No       | n() -> Result<(), Error>                          |
| HKN-CAP-REQUEST      | on_capability_request  | Capability  | Another plugin requests a declared capability    | Yes      | n(capability_id: &str, requester: &str) -> Result<bool, Error> |
| HKN-CAP-AVAILABLE    | on_capability_available| Capability  | Plugin capability becomes available              | No       | n(capability_id: &str) -> ()                      |
| HKN-EXT-LOAD         | on_extension_load      | Extension   | Extension point registered                       | No       | n(extension_point: &str) -> Result<(), Error>     |
| HKN-EXT-REGISTER     | on_extension_point_register | Extension | New extension point defined by runtime          | No       | n(point: ExtensionPoint) -> Result<(), Error>     |
| HKN-EVT-SUBSCRIBE    | on_event_subscribe     | Event       | Plugin subscribes to an event channel            | No       | n(channel: &str) -> Result<(), Error>             |
| HKN-EVT-EMIT         | on_event_emit          | Event       | Event emitted to subscribed plugins              | No       | n(event: &Event) -> Result<(), Error>             |
| HKN-SVC-REGISTER     | on_service_register    | Service     | Plugin registers a service                       | No       | n(service: &ServiceDef) -> Result<(), Error>      |
| HKN-SVC-RESOLVE      | on_service_resolve     | Service     | Service resolution requested                     | No       | n(service_name: &str) -> Result<ServiceInstance, Error> |
| HKN-CFG-CHANGE       | on_config_change       | Configuration| Plugin configuration updated                   | No       | n(changes: &[ConfigChange]) -> Result<(), Error>  |
| HKN-CFG-VALIDATE     | on_config_validate     | Configuration| Plugin configuration validation triggered        | No       | n(config: &Value) -> Result<(), ValidationError>  |
| HKN-STR-MIGRATE      | on_storage_migrate     | Storage     | Storage schema version change detected           | No       | n(from_version: u32, to_version: u32) -> Result<(), Error> |
| HKN-STR-CLEANUP      | on_storage_cleanup     | Storage     | Garbage collection triggered                     | No       | n() -> Result<CleanupStats, Error>                |
| HKN-SEC-PERMISSION   | on_permission_request  | Security    | Plugin requests elevated permissions             | Yes      | n(request: &PermissionRequest) -> Result<bool, Error> |
| HKN-SEC-SANDBOX      | on_sandbox_check       | Security    | Sandbox boundary check triggered                 | No       | n(check: &SandboxCheck) -> Result<bool, Error>    |

## 4. Hook Execution Guarantees

1. Hooks MUST execute in the order listed in Section 3 within each category.
2. Lifecycle hooks (HKN-LC-*) MUST complete before capability hooks (HKN-CAP-*) are invoked.
3. If a hook returns an error, the runtime MUST log the error and continue to the next hook unless the hook is marked Required.
4. Required hooks that return errors MUST cause the plugin load to fail.
5. Hooks MUST NOT block the runtime event loop for more than 5 seconds without yielding.

## 5. Hook Chaining

Hooks MAY be chained. When chaining:

`
hook_a() -> Result<ChainState>
hook_b(chain_state) -> Result<ChainState>
final_hook(chain_state) -> Result<(), Error>
`

The runtime provides a chain context object that carries state between hooks.

## 6. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- RFC-0203 Plugin Lifecycle
- RFC-0210 Plugin Events
- RFC-0206 Plugin Capability
