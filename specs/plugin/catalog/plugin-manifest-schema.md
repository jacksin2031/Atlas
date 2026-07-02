---
id: ATLAS-PLUGINSPEC-CATALOG-MANIFEST
title: Plugin Manifest Schema Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Manifest Schema Catalog

## 1. Purpose

This catalog documents the complete JSON schema for the tlas-plugin.json / manifest.json file. Every plugin MUST declare a manifest conforming to this schema.

## 2. Required Fields

| Field              | Type     | Description                                          | Validation Rule                                    |
|--------------------|----------|------------------------------------------------------|----------------------------------------------------|
| $schema          | string   | JSON Schema URI for this manifest                    | MUST match ^https://atlas.dev/schemas/plugin/v1$ |
| 
ame             | string   | Unique plugin identifier                             | MUST match ^[a-z][a-z0-9_-]*$, globally unique   |
| ersion          | string   | Semantic version                                     | MUST match ^\\d+\\.\\d+\\.\\d+$ (SemVer 2.0)      |
| 	itle            | string   | Human-readable display name                          | REQUIRED, 1-128 characters                         |
| description      | string   | Plugin description                                   | REQUIRED, 1-1024 characters                        |
| uthor           | object   | Author/contact information                           | MUST contain 
ame field                          |
| license          | string   | SPDX identifier or license file path                 | MUST be valid SPDX or relative path                |
| capabilities     | array    | Declared capabilities                               | EACH item MUST match a stable ID in capabilities catalog |
| extensions       | array    | Extension points provided                            | EACH item MUST declare 	ype and id             |
| dependencies     | array    | Plugin dependencies                                  | EACH item MUST declare 
ame, ersion_range     |
| permissions      | array    | Permission declarations                              | EACH item MUST declare level from permission catalog |
| config_schema    | object   | JSON Schema for plugin configuration                 | MUST be valid JSON Schema Draft 2020-12            |
| hooks            | object   | Lifecycle hook registration                          | KEYS MUST match hook IDs from hooks catalog        |
| storage          | array    | Storage type declarations                            | EACH item MUST match a storage type from storage catalog |
| esources        | object   | Resource manifest                                    | MUST include icons, 	ranslations if applicable |
| compatibility    | object   | Compatibility matrix entries                         | MUST declare untime_min, untime_max          |
| ipc              | object   | IPC channel declarations                             | MUST declare channels array                      |

## 3. Optional Fields

| Field               | Type     | Description                                       |
|---------------------|----------|---------------------------------------------------|
| homepage          | string   | Plugin website URL                                |
| icon              | string   | Resource path to icon file                        |
| epository        | string   | Source code repository URL                        |
| ugs              | string   | Issue tracker URL                                 |
| keywords          | array    | Search keywords for marketplace                   |
| main              | string   | Entry point file (bin/main)                       |
| exports           | object   | Public API exports                                |
| ssets            | object   | Bundled assets (models, OCR data)                 |
| config_migrations | array    | Config schema migration scripts                   |
| eature_gates     | array    | Opt-in unstable features                          |
| 	est_suite        | string   | Test suite path                                   |

## 4. Validation Rules

1. The manifest MUST be valid UTF-8 encoded JSON.
2. The $schema field MUST be present and valid.
3. The 
ame field MUST be globally unique across all registered plugins.
4. The ersion field MUST follow Semantic Versioning 2.0.0.
5. All declared capabilities MUST be listed in the capabilities catalog.
6. All declared permissions MUST be listed in the permission catalog.
7. All declared hooks MUST be listed in the hooks catalog.
8. The manifest MUST pass JSON Schema validation against the schema in Section 2.
9. Missing required fields MUST cause plugin load to fail with MANIFEST_001.
10. Duplicate plugin names in the same scope MUST be rejected with MANIFEST_002.

## 5. Example Valid Manifest

`json
{
  \"\\": \"https://atlas.dev/schemas/plugin/v1\",
  \"name\": \"my-awesome-plugin\",
  \"version\": \"1.0.0\",
  \"title\": \"My Awesome Plugin\",
  \"description\": \"Provides awesome functionality\",
  \"author\": { \"name\": \"Developer\", \"email\": \"dev@example.com\" },
  \"license\": \"MIT\",
  \"capabilities\": [\"PT-UTILITY\"],
  \"permissions\": [{ \"level\": \"normal\", \"resources\": [\"workspace:read\"] }],
  \"config_schema\": { \"type\": \"object\", \"properties\": {} }
}
`

## 6. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0202 Plugin Manifest
- RFC-0217 Plugin Packaging
