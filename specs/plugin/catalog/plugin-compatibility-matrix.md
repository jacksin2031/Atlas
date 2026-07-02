---
id: ATLAS-PLUGINSPEC-CATALOG-COMPAT
title: Plugin Compatibility Matrix Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Compatibility Matrix Catalog

## 1. Purpose

This catalog documents the compatibility dimensions, version negotiation algorithm, and matrix format for the Atlas Plugin subsystem.

## 2. Compatibility Dimensions

| Dimension         | Scope                          | Versioning Scheme     | Breaking Change Policy              |
|-------------------|--------------------------------|-----------------------|-------------------------------------|
| Runtime API       | Core runtime interface         | SemVer                | Major = breaking, Minor = compat    |
| Workflow Schema   | Pipeline definition format     | SemVer                | Major = breaking, Minor = compat    |
| Plugin Capability | Declared capability contract   | Capability version    | New version = opt-in               |
| Extension Point   | Extension registration format  | SemVer                | Major = breaking, Minor = compat    |
| Data Format       | Serialized data structures     | Schema version        | Backward compatible within major    |

## 3. Version Negotiation Algorithm

`
check_compatibility(plugin_manifest, runtime_env):
  1. Extract runtime_min, runtime_max from plugin manifest
  2. Compare runtime_env.version against [runtime_min, runtime_max]
  3. If outside range → reject with COMPAT_001
  4. For each dependency:
     a. Look up resolved version in runtime
     b. Compare against dependency.version_range
     c. If no match → reject with COMPAT_002
  5. For each feature_gate in plugin manifest:
     a. Check if runtime has feature gate enabled
     b. If disabled and required → reject with COMPAT_003
  6. If all checks pass → return Compatible
`

## 4. Breaking Change Classification

| Change Type              | Version Bump | Backward Compat | Example                         |
|--------------------------|--------------|-----------------|---------------------------------|
| API addition             | Minor        | Yes             | New method on PluginAPI         |
| API deprecation          | Minor        | Yes             | Mark method as deprecated       |
| API removal              | Major        | No              | Delete PluginAPI.method()       |
| Schema format change     | Major        | No              | Change workflow JSON structure  |
| Capability addition      | Minor        | Yes             | New capability in catalog       |
| Capability removal       | Major        | No              | Remove capability from catalog  |
| Permission level change  | Major        | No              | Elevate permission for endpoint |
| Configuration schema add | Minor        | Yes             | Add optional config field       |
| Configuration schema remove | Major     | No              | Remove required config field    |

## 5. Deprecation Timeline

1. A feature is marked deprecated for a minimum of 2 minor versions.
2. During deprecation, the feature MUST still function with a warning log.
3. After 2 minor versions, the feature MAY be removed in the next major version.
4. Removal MUST be documented in the changelog with migration guide.

## 6. Feature Gates

Feature gates allow opt-in of unstable features:

`json
{
  \"feature_gates\": [
    { \"name\": \"ipc-streaming\", \"required\": false, \"min_runtime\": \"2.1.0\" },
    { \"name\": \"ai-model-v3\", \"required\": true, \"min_runtime\": \"2.3.0\" }
  ]
}
`

- equired: false → Plugin works without the feature (graceful degradation)
- equired: true → Plugin fails to load if the feature gate is disabled

## 7. Reject Reason Taxonomy

| Reject Reason          | Code      | Description                                      |
|------------------------|-----------|--------------------------------------------------|
| runtime-mismatch       | COMPAT_001| Runtime version outside declared range           |
| api-incompatible       | COMPAT_002| Plugin API version mismatch                      |
| capability-missing     | COMPAT_003| Required capability not available                |
| feature-gate-conflict  | COMPAT_004| Required feature gate is disabled                |
| dependency-conflict    | COMPAT_005| Plugin dependency version conflict               |

## 8. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0218 Plugin Compatibility
- RFC-0212 Plugin Versioning
