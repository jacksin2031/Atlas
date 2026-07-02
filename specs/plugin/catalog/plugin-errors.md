---
id: ATLAS-PLUGINSPEC-CATALOG-PERR
title: Plugin Errors Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Errors Catalog

## 1. Purpose

This catalog defines the canonical set of error codes that the Atlas Plugin subsystem MAY return to indicate failures during plugin installation, loading, activation, execution, update, rollback, removal, or health monitoring. Error codes provide a stable, machine-parseable mechanism for diagnosing and responding to plugin subsystem failures.

## 2. Stable ID Prefix

All error code identifiers use the prefix `PERR-`.

### 2.1 Naming Convention

Error code identifiers SHALL follow the pattern:

```
PERR-<CATEGORY>-<FAILURE>
```

where `<CATEGORY>` identifies the failure domain and `<FAILURE>` describes the specific error condition. The approved combinations are listed in Section 3.

## 3. Complete Catalog Table

| Stable ID                   | Error Name                  | Category      | Failure              | Description                                                   |
|-----------------------------|-----------------------------|---------------|----------------------|---------------------------------------------------------------|
| PERR-MANIFEST-INVALID       | Manifest Invalid            | MANIFEST      | INVALID              | Plugin manifest failed structural or semantic validation.     |
| PERR-DEPENDENCY-UNRESOLVED  | Dependency Unresolved       | DEPENDENCY    | UNRESOLVED           | A required plugin dependency could not be resolved.           |
| PERR-SANDBOX-EXCEEDED       | Sandbox Exceeded            | SANDBOX       | EXCEEDED             | A plugin exceeded its allocated sandbox boundaries.           |
| PERR-SECURITY-VIOLATION     | Security Violation          | SECURITY      | VIOLATION            | A plugin violated a security policy or access control rule.   |
| PERR-LIFECYCLE-TIMEOUT      | Lifecycle Timeout           | LIFECYCLE     | TIMEOUT              | A plugin lifecycle operation exceeded its allotted time.      |
| PERR-INITIALIZATION-FAILED  | Initialization Failed       | LIFECYCLE     | INIT_FAILED          | The plugin initialization routine returned an error.          |
| PERR-ACTIVATION-FAILED      | Activation Failed           | LIFECYCLE     | ACTIVATION_FAILED    | The plugin could not transition to the active state.          |
| PERR-CAPABILITY-UNAVAILABLE | Capability Unavailable      | CAPABILITY    | UNAVAILABLE          | A required plugin capability is not available at runtime.     |
| PERR-VERSION-INCOMPATIBLE   | Version Incompatible        | VERSION       | INCOMPATIBLE         | The plugin version is incompatible with the host system.      |
| PERR-REGISTRY-DUPLICATE     | Registry Duplicate          | REGISTRY      | DUPLICATE            | A plugin with the same identity is already registered.        |
| PERR-LOAD-FAILED            | Load Failed                 | LOAD          | FAILED               | The plugin binary or module could not be loaded.              |
| PERR-UNLOAD-FAILED          | Unload Failed               | LOAD          | UNLOAD_FAILED        | The plugin could not be cleanly unloaded from memory.         |
| PERR-UPDATE-FAILED          | Update Failed               | UPDATE        | FAILED               | The plugin update operation encountered an error.             |
| PERR-ROLLBACK-FAILED        | Rollback Failed             | UPDATE        | ROLLBACK_FAILED      | Reverting the plugin to a previous version failed.            |
| PERR-REMOVAL-FAILED         | Removal Failed              | REMOVE        | FAILED               | The plugin uninstallation operation encountered an error.     |
| PERR-INTEGRITY-FAIL         | Integrity Fail              | INTEGRITY     | FAIL                 | Plugin file integrity verification did not pass.              |
| PERR-SIGNATURE-INVALID      | Signature Invalid           | INTEGRITY     | SIGNATURE_INVALID    | The plugin cryptographic signature is invalid or expired.     |
| PERR-RESOURCE-EXHAUSTED     | Resource Exhausted          | RESOURCE      | EXHAUSTED            | System resources required by the plugin are unavailable.      |
| PERR-IPC-DISCONNECTED       | IPC Disconnected            | IPC           | DISCONNECTED         | The inter-process communication channel was lost.             |
| PERR-CIRCULAR-DEPENDENCY    | Circular Dependency         | DEPENDENCY    | CIRCULAR             | A circular dependency cycle was detected among plugins.       |

## 4. Validation Rules

1. Every error code identifier MUST match the regex `^PERR-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$`.
2. Error codes MUST be reported as immutable, opaque strings; implementations MUST NOT parse the string structure.
3. Error code emitters MUST select the most specific error code from this catalog that accurately describes the failure condition.
4. Two or more error code identifiers MUST NOT share identical failure semantics.
5. Implementations MUST NOT introduce error code identifiers outside this catalog.
6. Removing an error code from this catalog is prohibited once any consumer references it.
7. Error codes MUST be accompanied by a human-readable message and, where applicable, the affected plugin identifier.
8. Error code values MUST NOT be reused for different failure conditions across subsystem versions.
9. Error codes related to the same failure domain (for example, DEPENDENCY) SHOULD be reported consistently by all subsystem components.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- ATLAS-PLUGINSPEC-CATALOG-CAP — Capabilities Catalog (capability failures MUST report PERR-CAPABILITY-UNAVAILABLE).
- ATLAS-PLUGINSPEC-CATALOG-PEVT — Plugin Events Catalog (error conditions MUST emit corresponding event identifiers).
- ATLAS-PLUGINSPEC-CATALOG-PERM — Permissions Catalog (security violations MUST report PERR-SECURITY-VIOLATION).

## 6. Usage Guidelines

6.1 Error handlers SHOULD map error codes to recovery actions defined in the lifecycle management specification.

6.2 Diagnostic tools SHOULD aggregate error codes by category to identify systemic issues.

6.3 Error codes related to manifest validation (PERR-MANIFEST-INVALID, PERR-SIGNATURE-INVALID) MUST be reported before any loading attempt.

6.4 Error codes related to dependency resolution (PERR-DEPENDENCY-UNRESOLVED, PERR-CIRCULAR-DEPENDENCY) MUST prevent plugin activation.

6.5 Error codes related to sandbox enforcement (PERR-SANDBOX-EXCEEDED) MUST trigger immediate plugin suspension.

6.6 Error codes related to integrity (PERR-INTEGRITY-FAIL, PERR-SIGNATURE-INVALID) MUST prevent plugin installation.

6.7 Update-related error codes (PERR-UPDATE-FAILED, PERR-ROLLBACK-FAILED) MUST trigger the rollback procedure defined in the lifecycle specification.

6.8 Resource exhaustion errors (PERR-RESOURCE-EXHAUSTED) SHOULD be retried after a configurable backoff interval before reporting failure.

6.9 IPC disconnection errors (PERR-IPC-DISCONNECTED) SHOULD initiate a reconnection attempt before escalating to a fatal failure.
