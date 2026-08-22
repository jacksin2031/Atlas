---
id: ATLAS-PLUGINSPEC-CATALOG-PERMSCH
title: Plugin Permission Schema Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Permission Schema Catalog

## 1. Purpose

This catalog documents the permission declaration format used in plugin manifests. Permissions define what resources a plugin can access and what actions it can perform.

## 2. Permission Level Enum

| Level        | Description                                              | Approval Required | Sandbox Boundary   |
|--------------|----------------------------------------------------------|-------------------|--------------------|
| low        | Read-only workspace data, no network access              | None              | Strict             |
| 
ormal     | Read/write workspace files, local network only           | None              | Standard           |
| elevated   | System access, registry modification, elevated processes | User confirmation | Relaxed            |
| privileged | Kernel-level access, driver loading, full system access  | Admin confirmation| Minimal            |
| estricted | Sandboxed, no filesystem, no network                     | None              | Maximal            |
| experimental| Requires explicit user approval, full audit logging     | User + Audit      | Configurable       |

## 3. Resource Patterns

Resources are declared using glob-like patterns:

`
<domain>:<action>[.<resource>]
`

| Pattern               | Meaning                                  | Examples                                    |
|-----------------------|------------------------------------------|---------------------------------------------|
| workspace:*         | All workspace operations                 | workspace:read, workspace:write         |
| workspace:read      | Read-only workspace access               | File reads, directory listing               |
| workspace:write     | Modify workspace files                   | File writes, deletes, renames               |
| 
etwork:*           | All network operations                   | 
etwork:http, 
etwork:websocket         |
| 
etwork:local       | Localhost/private network only           | 127.0.0.1, localhost, 10.x.x.x        |
| 
etwork:all         | Unrestricted network access              | Any outbound connection                     |
| system:registry     | Read/write system registry               | Windows Registry, macOS plist               |
| system:process      | Process management                       | Start, stop, signal processes               |
| storage:*           | All storage operations                   | storage:cache, storage:persistent       |
| storage:secret      | Encrypted credential storage             | API keys, tokens, passwords                 |
| i:*                | All AI operations                        | i:model, i:prompt, i:embed         |
| ision:*            | All vision operations                    | ision:ocr, ision:image                |
| scheduler:*         | All scheduling operations                | scheduler:timer, scheduler:queue        |

## 4. Action Enum

| Action    | Description                                    |
|-----------|------------------------------------------------|
| ead    | Read-only access to resources                  |
| write   | Modify or create resources                     |
| execute | Run code or binaries                           |
| dmin   | Administrative operations (delete, configure)  |

## 5. Permission Groups

Commonly bundled permission sets:

| Group Name       | Permissions Included                                    | Use Case              |
|------------------|---------------------------------------------------------|-----------------------|
| ilesystem-full| workspace:read, workspace:write, system:process   | File manipulation     |
| 
etwork-all    | 
etwork:*                                             | API integrations      |
| 
etwork-local  | 
etwork:local                                         | Local services        |
| i-complete    | i:model, i:prompt, i:embed                     | AI plugins            |
| ision-complete| ision:ocr, ision:image                            | Vision plugins        |
| storage-full   | storage:cache, storage:persistent, storage:secret | Data plugins          |

## 6. Escalation Rules

1. A plugin MAY request permission escalation during runtime via on_permission_request hook.
2. Escalation from 
ormal to elevated requires user confirmation.
3. Escalation from elevated to privileged requires administrator confirmation.
4. Escalation from any level to experimental requires explicit opt-in and audit logging.
5. Temporary elevation for a specific workflow MUST be revoked after workflow completion.

## 7. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0207 Plugin Security
- RFC-0219 Plugin Permission Model
