---
id: ATLAS-PLUGINSPEC-CATALOG-PEVT
title: Plugin Events Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Events Catalog

## 1. Purpose

This catalog defines the canonical set of events emitted by the Atlas Plugin subsystem to communicate plugin state changes, capability modifications, dependency resolution outcomes, security incidents, and health transitions to subscribers.

## 2. Stable ID Prefix

All event identifiers use the prefix `PEVT-`.

### 2.1 Naming Convention

Event identifiers SHALL follow the pattern:

```
PEVT-<CATEGORY>-<TRANSITION>
```

where `<CATEGORY>` identifies the event domain and `<TRANSITION>` describes the state change. The approved combinations are listed in Section 3.

## 3. Complete Catalog Table

| Stable ID                | Event Name                 | Category       | Transition       | Description                                                    |
|--------------------------|----------------------------|----------------|------------------|----------------------------------------------------------------|
| PEVT-INSTALLED           | Installed                  | LIFECYCLE      | INSTALLED        | Plugin has been successfully installed.                        |
| PEVT-LOADED              | Loaded                     | LIFECYCLE      | LOADED           | Plugin binary or module has been loaded into memory.           |
| PEVT-INITIALIZED         | Initialized                | LIFECYCLE      | INITIALIZED      | Plugin initialization routine has completed.                   |
| PEVT-ACTIVATED           | Activated                  | LIFECYCLE      | ACTIVATED        | Plugin is active and operational.                              |
| PEVT-RUNNING             | Running                    | LIFECYCLE      | RUNNING          | Plugin is executing its primary functions.                     |
| PEVT-SUSPENDED           | Suspended                  | LIFECYCLE      | SUSPENDED        | Plugin execution has been temporarily paused.                  |
| PEVT-RESUMED             | Resumed                    | LIFECYCLE      | RESUMED          | Plugin execution has been restored after suspension.           |
| PEVT-DEACTIVATED         | Deactivated                | LIFECYCLE      | DEACTIVATED      | Plugin has stopped accepting new operations.                   |
| PEVT-UNLOADED            | Unloaded                   | LIFECYCLE      | UNLOADED         | Plugin has been removed from memory.                           |
| PEVT-UPDATED             | Updated                    | LIFECYCLE      | UPDATED          | Plugin has been upgraded to a newer version.                   |
| PEVT-ROLLBACK            | Rollback                   | LIFECYCLE      | ROLLBACK         | Plugin has been reverted to a previous version.                |
| PEVT-REMOVED             | Removed                    | LIFECYCLE      | REMOVED          | Plugin has been uninstalled from the system.                   |
| PEVT-FAILED              | Failed                     | LIFECYCLE      | FAILED           | Plugin has encountered a fatal error.                          |
| PEVT-RECOVERED           | Recovered                  | LIFECYCLE      | RECOVERED        | Plugin has recovered from a previous failure.                  |
| PEVT-HEALTH-DEGRADED     | Health Degraded            | HEALTH         | DEGRADED         | Plugin health has fallen below acceptable thresholds.          |
| PEVT-HEALTH-OK           | Health OK                  | HEALTH         | OK               | Plugin health has returned to acceptable levels.               |
| PEVT-CAPABILITY-ADDED    | Capability Added           | CAPABILITY     | ADDED            | A new capability has been registered for the plugin.           |
| PEVT-CAPABILITY-REMOVED  | Capability Removed         | CAPABILITY     | REMOVED          | A capability has been unregistered from the plugin.            |
| PEVT-DEPENDENCY-RESOLVED | Dependency Resolved        | DEPENDENCY     | RESOLVED         | All plugin dependencies have been satisfied.                   |
| PEVT-DEPENDENCY-FAILED   | Dependency Failed          | DEPENDENCY     | FAILED           | One or more plugin dependencies could not be satisfied.        |
| PEVT-SECURITY-VIOLATION  | Security Violation         | SECURITY       | VIOLATION        | A security policy breach has been detected.                    |
| PEVT-MANIFEST-VALIDATED  | Manifest Validated         | MANIFEST       | VALIDATED        | Plugin manifest has passed all validation checks.              |
| PEVT-MANIFEST-INVALID    | Manifest Invalid           | MANIFEST       | INVALID          | Plugin manifest has failed validation.                         |
| PEVT-REGISTRY-REGISTERED | Registry Registered        | REGISTRY       | REGISTERED       | Plugin has been registered in the plugin registry.             |
| PEVT-REGISTRY-UNREGISTERED| Registry Unregistered      | REGISTRY       | UNREGISTERED     | Plugin has been removed from the plugin registry.              |

## 4. Validation Rules

1. Every event identifier MUST match the regex `^PEVT-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$`.
2. The category and transition components of every event MUST correspond exactly to the values in the catalog table.
3. Event emitters MUST NOT fabricate event identifiers not present in this catalog.
4. Event subscribers MUST accept events from this catalog and MAY filter by category or transition.
5. Two or more event identifiers MUST NOT share identical semantic meaning.
6. Implementations MUST NOT introduce event identifiers outside this catalog.
7. Removing an event from this catalog is prohibited once any subscriber has registered for it.
8. Event payloads MUST include at minimum the emitting plugin identifier and a timestamp.
9. Event ordering MUST preserve causality within a single plugin instance.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- ATLAS-PLUGINSPEC-CATALOG-CAP — Capabilities Catalog (capability changes emit PEVT-CAPABILITY-ADDED and PEVT-CAPABILITY-REMOVED).
- ATLAS-PLUGINSPEC-CATALOG-PERM — Permissions Catalog (security events correlate with permission enforcement).
- ATLAS-PLUGINSPEC-CATALOG-PERR — Plugin Errors Catalog (failure events MUST be accompanied by the relevant error code).

## 6. Usage Guidelines

6.1 Event consumers SHOULD subscribe to events using category-based filters to reduce processing overhead.

6.2 The plugin lifecycle manager MUST emit events in Section 3 for every state transition described in the plugin lifecycle specification.

6.3 Health events (PEVT-HEALTH-DEGRADED, PEVT-HEALTH-OK) SHOULD be emitted at intervals defined by the observability configuration.

6.4 Security violation events (PEVT-SECURITY-VIOLATION) MUST be emitted synchronously before the violating operation completes.

6.5 Manifest validation events (PEVT-MANIFEST-VALIDATED, PEVT-MANIFEST-INVALID) MUST be emitted before the plugin loader proceeds with loading.

6.6 Dependency resolution events (PEVT-DEPENDENCY-RESOLVED, PEVT-DEPENDENCY-FAILED) MUST precede the plugin activation event.

6.7 Registry events (PEVT-REGISTRY-REGISTERED, PEVT-REGISTRY-UNREGISTERED) MUST be emitted as the final step of registration and de-registration operations.

6.8 Event subscribers that cannot process an event SHOULD discard it rather than blocking the emitter.
