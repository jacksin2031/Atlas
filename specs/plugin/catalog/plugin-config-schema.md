---
id: ATLAS-PLUGINSPEC-CATALOG-CONFIGSCH
title: Plugin Configuration Schema Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Configuration Schema Catalog

## 1. Purpose

This catalog documents the configuration hierarchy, schema validation rules, and management format for plugin configuration.

## 2. Configuration Levels (Priority Order, Highest First)

| Level       | Scope        | Persistence    | Mutated By           | Typical Path                                    |
|-------------|--------------|----------------|----------------------|-------------------------------------------------|
| session   | Editor session| Volatile      | User/editor          | In-memory only                                  |
| 	emporary | Temporal     | Auto-expire    | System               | Temp directory with TTL                         |
| user      | User-global  | Persistent     | User settings UI     | ~/.atlas/config/users/<user_id>/              |
| project   | Workspace    | Versioned      | Project config file  | <workspace>/.atlas/config.json                |
| workspace | Folder-level | Persistent     | Workspace settings   | <folder>/.atlas/settings/                     |
| global    | Runtime-wide | Persistent     | Runtime installer    | ~/.atlas/config/global.json                   |
| default   | Plugin code  | Hardcoded      | None (code constant) | Embedded in plugin binary                       |

## 3. Configuration Resolution Algorithm

`
resolve(key, plugin_id):
  1. Load plugin's default config (hardcoded)
  2. Overlay global config
  3. Overlay workspace config
  4. Overlay project config
  5. Overlay user config
  6. Overlay session config (highest priority)
  7. Return merged result
`

Rules:
- Later overlays override earlier values for the same key.
- Arrays are replaced, not merged.
- Objects are deep-merged recursively.
- Missing keys fall through to the next lower priority level.
- default level MUST NEVER leak into global config.

## 4. Schema Validation

Each plugin declares config_schema in its manifest (JSON Schema Draft 2020-12).

Validation rules:
1. Configuration MUST conform to the declared schema on load.
2. Invalid configuration MUST cause plugin load to fail with CONFIG_001.
3. Schema changes require a migration entry in config_migrations.
4. Runtime MUST reject configuration updates that violate the schema.

## 5. Migration Format

`json
{
  \"config_migrations\": [
    {
      \"from_version\": 1,
      \"to_version\": 2,
      \"script\": \"function migrate(config) { ... }\",
      \"safe_to_hot_reload\": true
    }
  ]
}
`

## 6. Secret Handling

- Secrets MUST be stored at the user level or higher priority.
- Secret values MUST be encrypted at rest using runtime-managed keys.
- Secret keys use the prefix __secret__. in configuration paths.
- Secret values MUST NEVER appear in logs or error messages.

## 7. Hot-Reload Safety

- If safe_to_hot_reload is 	rue, config changes apply without restart.
- If alse, config changes require plugin reload.
- Unsafe configs include: network endpoints, API keys, model paths.

## 8. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0222 Plugin Configuration
- RFC-0202 Plugin Manifest
