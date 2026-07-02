---
id: ATLAS-PLUGINSPEC-CATALOG-CAPSCHEMA
title: Plugin Capabilities Schema Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Capabilities Schema Catalog

## 1. Purpose

This catalog documents the schema for declaring plugin capabilities in the manifest. Capabilities define what the plugin CAN DO and what permissions it REQUIRES.

## 2. Capability Declaration Schema

Each capability entry in the manifest MUST conform to:

`json
{
  \"id\": \"string\",
  \"type\": \"read | write | execute | network | ai | vision | storage | scheduler\",
  \"resources\": [\"string\"],
  \"permissions\": [\"string\"],
  \"features\": [\"string\"],
  \"description\": \"string\"
}
`

## 3. Complete Capabilities Table

| Capability ID              | Type     | Required Permissions              | Runtime Features Needed        | Manifest Declaration Format                  |
|----------------------------|----------|-----------------------------------|--------------------------------|----------------------------------------------|
| ead:workspace           | read     | filesystem:read                   | None                           | { \"id\": \"read:workspace\", \"type\": \"read\" } |
| write:workspace          | write    | filesystem:write                  | None                           | { \"id\": \"write:workspace\", \"type\": \"write\" } |
| execute:code             | execute  | security:elevated                 | Sandboxed VM                   | { \"id\": \"execute:code\", \"type\": \"execute\" } |
| 
etwork:all              | network  | security:privileged               | Full network stack             | { \"id\": \"network:all\", \"type\": \"network\" } |
| 
etwork:local            | network  | security:normal                   | Local network only             | { \"id\": \"network:local\", \"type\": \"network\" } |
| i:model                 | ai       | security:elevated                 | ML runtime, GPU (optional)     | { \"id\": \"ai:model\", \"type\": \"ai\" } |
| i:prompt                | ai       | None                              | Prompt template engine         | { \"id\": \"ai:prompt\", \"type\": \"ai\" } |
| ision:ocr               | vision   | security:normal                   | OCR engine                     | { \"id\": \"vision:ocr\", \"type\": \"vision\" } |
| ision:image             | vision   | security:normal                   | Image processing pipeline      | { \"id\": \"vision:image\", \"type\": \"vision\" } |
| storage:persistent       | storage  | None                              | Persistent storage backend     | { \"id\": \"storage:persistent\", \"type\": \"storage\" } |
| storage:secret           | storage  | security:elevated                 | Encrypted storage              | { \"id\": \"storage:secret\", \"type\": \"storage\" } |
| scheduler:timer          | scheduler| None                              | Timer service                  | { \"id\": \"scheduler:timer\", \"type\": \"scheduler\" } |
| scheduler:queue          | scheduler| None                              | Job queue service              | { \"id\": \"scheduler:queue\", \"type\": \"scheduler\" } |

## 4. Capability Validation Rules

1. A plugin MUST declare at least one capability.
2. Capability types MUST match the enum: ead, write, execute, 
etwork, i, ision, storage, scheduler.
3. If a capability requires permissions, those permissions MUST be declared in the permissions array.
4. If a capability requires runtime features, the runtime MUST verify availability before loading.
5. Capabilities are additive: declaring write:workspace implies ead:workspace.
6. Declaring execute:code requires explicit user approval at installation time.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0206 Plugin Capability
- RFC-0207 Plugin Security
