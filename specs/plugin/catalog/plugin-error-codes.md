---
id: ATLAS-PLUGINSPEC-CATALOG-ERRORS
title: Plugin Error Codes Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Error Codes Catalog

## 1. Purpose

This catalog documents all error codes used by the Atlas Plugin subsystem. Errors are grouped by category for systematic diagnosis and recovery.

## 2. Loading Errors (LOAD_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| LOAD_001    | ManifestParseError      | Failed to parse plugin manifest JSON     | Check manifest syntax, verify encoding   |
| LOAD_002    | SignatureVerification   | Plugin signature failed verification     | Re-download plugin, check integrity      |
| LOAD_003    | DependencyMissing       | Required dependency not found            | Install missing dependency               |
| LOAD_004    | DependencyConflict      | Dependency version conflict              | Resolve version conflict manually        |
| LOAD_005    | EntryPointNotFound      | Main entry point file not found          | Check bin/main path in manifest          |
| LOAD_006    | LoadTimeout             | Plugin load exceeded timeout             | Increase timeout or reduce plugin size   |
| LOAD_007    | SandboxViolation        | Plugin violated sandbox during load      | Quarantine plugin, review permissions    |

## 3. Manifest Errors (MANIFEST_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| MANIFEST_001| RequiredFieldMissing    | A required manifest field is absent      | Add missing field to manifest            |
| MANIFEST_002| DuplicatePluginName     | Plugin name conflicts with existing      | Rename plugin or uninstall conflicting   |
| MANIFEST_003| InvalidCapability       | Declared capability not in catalog       | Update to valid capability ID            |
| MANIFEST_004| InvalidPermission       | Declared permission not recognized       | Update to valid permission level         |
| MANIFEST_005| SchemaValidationError   | Manifest fails JSON Schema validation    | Fix schema violations                    |
| MANIFEST_006| VersionMalformed        | Version string not valid SemVer          | Correct version format                   |

## 4. Capability Errors (CAPABILITY_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| CAPABILITY_001| CapabilityNotFound    | Requested capability not registered      | Check capability declaration in manifest |
| CAPABILITY_002| CapabilityUnavailable | Capability runtime feature missing       | Install required runtime feature         |
| CAPABILITY_003| CapabilityConflict    | Two plugins claim same capability        | Resolve conflict via registry            |
| CAPABILITY_004| CapabilityDenied      | Permission insufficient for capability   | Request permission escalation            |

## 5. Permission Errors (PERMISSION_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| PERMISSION_001| AccessDenied        | Plugin lacks required permission         | Review and update permission grants      |
| PERMISSION_002| EscalationFailed      | Permission escalation rejected           | Contact admin for approval               |
| PERMISSION_003| Revoked               | Permission was revoked at runtime        | Plugin must degrade gracefully           |
| PERMISSION_004| SandboxEscape         | Plugin attempted to escape sandbox       | Terminate plugin immediately             |

## 6. IPC Errors (IPC_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| IPC_001     | ChannelNotFound         | IPC channel does not exist               | Check channel declaration in manifest    |
| IPC_002     | MessageTimeout          | IPC message exceeded timeout             | Retry with exponential backoff           |
| IPC_003     | RateLimited             | IPC rate limit exceeded                  | Throttle calls, implement batching       |
| IPC_004     | CircuitBreakerOpen      | Circuit breaker tripped                  | Wait for recovery period                 |
| IPC_005     | SerializationError      | Message failed to serialize/deserialize  | Check message schema compatibility       |

## 7. Storage Errors (STORAGE_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| STORAGE_001 | QuotaExceeded           | Plugin exceeded storage quota            | Clean up storage, request quota increase |
| STORAGE_002 | CorruptedData           | Stored data integrity check failed       | Restore from backup                      |
| STORAGE_003 | EncryptionError         | Failed to encrypt/decrypt data           | Check encryption key availability        |
| STORAGE_004 | MigrationFailed         | Storage schema migration failed          | Rollback to previous schema version      |

## 8. Configuration Errors (CONFIG_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| CONFIG_001  | SchemaMismatch          | Config does not match declared schema    | Fix configuration values                 |
| CONFIG_002  | MigrationNeeded         | Config requires migration                | Run config migration                     |
| CONFIG_003  | SecretNotFound          | Referenced secret does not exist         | Check secret key path                    |

## 9. Compatibility Errors (COMPAT_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| COMPAT_001  | RuntimeMismatch         | Plugin requires unsupported runtime      | Update runtime or downgrade plugin       |
| COMPAT_002  | APIIncompatible         | Plugin API version incompatible          | Update plugin to compatible version      |
| COMPAT_003  | FeatureGateConflict     | Required feature gate disabled           | Enable feature gate or remove dependency |

## 10. Testing Errors (TEST_*)

| Code        | Error Name              | Description                              | Recovery Action                          |
|-------------|-------------------------|------------------------------------------|------------------------------------------|
| TEST_001    | ManifestTestFail        | Manifest validation failed               | Fix manifest per error details           |
| TEST_002    | APITestFail             | API integration test failed              | Debug API call sequence                  |
| TEST_003    | SandboxTestFail         | Sandbox boundary violation detected      | Review permissions and resource access   |

## 11. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0207 Plugin Security
- RFC-0224 Plugin Testing
