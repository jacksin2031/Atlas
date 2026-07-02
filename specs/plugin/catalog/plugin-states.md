# Plugin States Catalog

## 1. Purpose

This catalog defines the canonical set of plugin lifecycle state identifiers used throughout the Atlas Plugin subsystem. Every plugin instance MUST be assigned exactly one state at any point in time, and state transitions MUST comply with the state machine defined in the plugin lifecycle specification.

## 2. Stable ID Prefix

All state identifiers use the prefix `PSTATE-`. This prefix is reserved exclusively for plugin lifecycle state definitions within the Atlas ecosystem.

## 3. Naming Convention

State identifiers MUST conform to the pattern `PSTATE-<NAME>` where `<NAME>` consists of uppercase ASCII letters and hyphens, representing the semantic meaning of the state. Names MUST be self-describing and MUST NOT abbreviate beyond common industry practice.

## 4. Canonical State Table

| Stable ID | Description | Semantics |
|---|---|---|
| `PSTATE-DISCOVERED` | Plugin binary located | The plugin manifest or binary has been detected on disk or in a registry source but has not yet undergone validation. |
| `PSTATE-VALIDATING` | Schema and content checks | The plugin manifest and associated resources are being validated against the catalog schema and policy constraints. |
| `PSTATE-LOADED` | Manifest parsed into memory | The plugin manifest has been successfully parsed and the plugin metadata is resident in the runtime. |
| `PSTATE-INITIALIZING` | Static initialization phase | The plugin is performing one-time setup such as registering extension points, loading configuration, and allocating static resources. |
| `PSTATE-ACTIVATING` | Activation gate | The plugin is transitioning from initialized to active, acquiring runtime dependencies and notifying dependent plugins. |
| `PSTATE-ACTIVE` | Ready to serve requests | The plugin is fully initialized, its capabilities are registered, and it is available to handle incoming requests or events. |
| `PSTATE-RUNNING` | Actively executing work | The plugin is executing operational logic, processing events, or servicing requests beyond mere readiness. |
| `PSTATE-SUSPENDING` | Graceful pause in progress | The plugin is in the process of halting active work, flushing buffers, and releasing transient resources. |
| `PSTATE-SUSPENDED` | Paused but intact | The plugin is paused with all state preserved; it MAY resume without reinitialization. |
| `PSTATE-RESUMING` | Restart from pause | The plugin is transitioning from a suspended state back to active or running. |
| `PSTATE-DEACTIVATING` | Shutdown preparation | The plugin is in the process of releasing capabilities, unregistering extensions, and cleaning up resources. |
| `PSTATE-DEACTIVATED` | Stopped but not removed | The plugin has been deactivated and its capabilities are unregistered, but its manifest and metadata remain loaded. |
| `PSTATE-UNLOADING` | Memory cleanup | The plugin is in the process of releasing its in-memory representation and freeing allocated resources. |
| `PSTATE-UNLOADED` | Removed from memory | The plugin has been fully unloaded and is no longer represented in the runtime. |
| `PSTATE-UPDATING` | Version upgrade in progress | The plugin is undergoing a version upgrade, with the old version being replaced by the new version. |
| `PSTATE-ROLLING-BACK` | Upgrade rollback in progress | The plugin upgrade failed and the system is reverting to the previous version. |
| `PSTATE-REMOVING` | Deletion in progress | The plugin is being uninstalled or removed from the system entirely. |
| `PSTATE-REMOVED` | Deleted from system | The plugin has been fully removed and is no longer present in any registry or on disk. |
| `PSTATE-ERROR` | Error condition detected | An error has been detected in the plugin that does not necessarily imply permanent failure; recovery MAY be attempted. |
| `PSTATE-FAILED` | Unrecoverable failure | The plugin has encountered a fatal error and cannot continue operation; removal or reinstallation is REQUIRED. |

## 5. State Machine Rules

A plugin instance MUST adhere to the following transition constraints:

1. The initial state of any plugin MUST be `PSTATE-DISCOVERED`.
2. From `PSTATE-DISCOVERED`, the plugin MUST transition to either `PSTATE-VALIDATING` or `PSTATE-ERROR`.
3. From `PSTATE-VALIDATING`, the plugin MUST transition to `PSTATE-LOADED` upon success, or `PSTATE-FAILED` upon validation failure.
4. From `PSTATE-LOADED`, the plugin MUST transition to `PSTATE-INITIALIZING`.
5. From `PSTATE-INITIALIZING`, the plugin MUST transition to `PSTATE-ACTIVATING` upon success, or `PSTATE-ERROR` upon failure.
6. From `PSTATE-ACTIVATING`, the plugin MUST transition to `PSTATE-ACTIVE` upon success, or `PSTATE-ERROR` upon failure.
7. From `PSTATE-ACTIVE`, the plugin MAY transition to `PSTATE-RUNNING`, `PSTATE-SUSPENDING`, `PSTATE-DEACTIVATING`, `PSTATE-UPDATING`, or `PSTATE-ERROR`.
8. From `PSTATE-RUNNING`, the plugin MUST transition to `PSTATE-SUSPENDING` when suspension is requested, or `PSTATE-DEACTIVATING` when deactivation is requested.
9. From `PSTATE-SUSPENDING`, the plugin MUST transition to `PSTATE-SUSPENDED` upon completion.
10. From `PSTATE-SUSPENDED`, the plugin MUST transition to `PSTATE-RESUMING` when resumption is requested.
11. From `PSTATE-RESUMING`, the plugin MUST transition to `PSTATE-ACTIVE` upon completion.
12. From `PSTATE-DEACTIVATING`, the plugin MUST transition to `PSTATE-DEACTIVATED` upon completion.
13. From `PSTATE-DEACTIVATED`, the plugin MUST transition to `PSTATE-UNLOADING`.
14. From `PSTATE-UNLOADING`, the plugin MUST transition to `PSTATE-UNLOADED` upon completion.
15. From `PSTATE-UPDATING`, the plugin MUST transition to either `PSTATE-ACTIVE` (successful update) or `PSTATE-ROLLING-BACK` (failed update).
16. From `PSTATE-ROLLING-BACK`, the plugin MUST transition to either `PSTATE-DEACTIVATING` (rollback succeeded) or `PSTATE-FAILED` (rollback also failed).
17. From `PSTATE-REMOVING`, the plugin MUST transition to `PSTATE-REMOVED` upon completion.
18. From `PSTATE-ERROR`, the plugin MUST transition to `PSTATE-FAILED` if recovery is not possible, or to the state from which the error occurred if recovery succeeds.
19. From `PSTATE-FAILED`, the plugin MUST transition to `PSTATE-REMOVING` or `PSTATE-UNLOADING`.

## 6. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin Lifecycle Specification: Defines the operational behavior associated with each state.
- Atlas Plugin Registry Specification: Defines how state information is persisted and queried.

## 7. Usage Guidelines

Implementations MUST assign a state to every plugin instance upon discovery and MUST update the state synchronously with each lifecycle transition. State transitions MUST be atomic with respect to observable behavior: no plugin capability MAY be exposed or consumed while a transition is in progress. Observability layers MUST record every state transition with a timestamp and the initiating cause. Systems MUST NOT permit direct assignment of a state; all assignments MUST occur through the state machine transition mechanism.
