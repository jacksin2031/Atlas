---
id: ATLAS-PLUGINSPEC-CATALOG-STORAGETYPES
title: Plugin Storage Types Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Storage Types Catalog

## 1. Purpose

This catalog defines the canonical set of storage backends available to plugins. Each storage type has distinct retention, persistence, encryption, and access characteristics.

## 2. Complete Storage Types Table

| Stable ID | Type        | Purpose                          | Lifetime          | Persistence Guarantee | Encryption at Rest | Typical Use Case                    |
|-----------|-------------|----------------------------------|-------------------|----------------------|--------------------|-------------------------------------|
| STR-CACHE   | Cache       | Fast temporary data              | TTL-based (configurable) | No (evicted on miss) | No (performance)   | API response cache, computed results |
| STR-PERSIST | Persistent  | Durable plugin data              | Until deleted      | Yes (flushed to disk) | Optional          | User preferences, plugin state       |
| STR-SECRET  | Secret      | Encrypted credentials            | Until revoked      | Yes (encrypted)       | Yes (AES-256-GCM) | API keys, tokens, passwords          |
| STR-SESS    | Session     | Per-editor-session data          | Session end        | No                   | No                 | Temporary workflow state             |
| STR-DB      | Database    | Structured queryable data        | Until deleted      | Yes (WAL)            | Optional          | Plugin-relational data               |
| STR-BLOB    | Blob        | Binary large objects             | Until deleted      | Yes                  | Optional          | Uploaded files, images               |
| STR-BIN     | Binary      | Typed binary storage             | Until deleted      | Yes                  | Optional          | Serialized objects, snapshots        |

## 3. Storage Path Convention

Each plugin gets an isolated storage namespace:

`
<runtime_data>/<plugin_id>/<type>/
`

Example:
`
~/.atlas/data/my-plugin/cache/
~/.atlas/data/my-plugin/persistent/
~/.atlas/data/my-plugin/secret/
`

## 4. Storage API

| Method           | Parameters              | Returns            | Description                          |
|------------------|-------------------------|--------------------|--------------------------------------|
| store(key, val)| string, any           | oid             | Store a value                        |
| etrieve(key)  | string                | ny \| null      | Get a value by key                   |
| delete(key)    | string                | oolean          | Remove a value                       |
| list(prefix)   | string                | string[]         | List keys with optional prefix       |
| exists(key)    | string                | oolean          | Check if a key exists                |
| clear()        | —                       | oid             | Clear all data for this storage type |

## 5. Quota Limits

| Type        | Default Quota | Max Quota | Eviction Policy    |
|-------------|---------------|-----------|--------------------|
| Cache       | 100 MB        | 1 GB      | LRU + TTL          |
| Persistent  | 500 MB        | 5 GB      | Manual delete      |
| Secret      | 10 KB         | 50 KB     | Manual revoke      |
| Session     | 50 MB         | 200 MB    | Auto-clear on exit |
| Database    | 500 MB        | 5 GB      | Manual delete      |
| Blob        | 1 GB          | 10 GB     | Manual delete      |
| Binary      | 500 MB        | 5 GB      | Manual delete      |

Quotas are configurable per-plugin by the workspace administrator.

## 6. Storage Lifecycle

`
Plugin Init → Storage Allocated → Plugin Ready → Data Operations → Plugin Stop → Cleanup
                                                         ↓
                                                    (Cache/Session auto-evict)
`

1. Storage is allocated when the plugin is loaded.
2. Cache and Session storage are auto-evicted on plugin unload.
3. Persistent, Secret, Database, Blob, and Binary storage survive plugin unload.
4. On plugin uninstall, Persistent/DB/Blob/Binary data MUST be offered for user confirmation.
5. Secret data MUST be securely wiped on uninstall (no user prompt needed).

## 7. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0223 Plugin Storage
- RFC-0208 Plugin Sandbox
