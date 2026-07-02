---
id: ATLAS-STORAGE-CATALOG-NAMESPACES
title: Storage Namespaces Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Namespaces Catalog

## 1. Purpose

This catalog defines the canonical set of Storage namespaces that provide hierarchical isolation for all stored resources.

## 2. Namespace ID Prefix

All namespace identifiers use the prefix NS-.

## 3. Complete Namespace Catalog

| Namespace ID | Namespace Path | Parent | Sub-namespace Pattern | Resource Types | RFC Reference |
|---|---|---|---|---|---|
| NS-RUNTIME | atlas.runtime | atlas | atlas.runtime.{service_id} | state, metric, event | RFC-0422 |
| NS-PLUGIN | atlas.plugin | atlas | atlas.plugin.{plugin_id} | manifest, state, config | RFC-0422 |
| NS-WORKFLOW | atlas.workflow | atlas | atlas.workflow.{workflow_id} | state, event, output | RFC-0422 |
| NS-AI | atlas.ai | atlas | atlas.ai.{conversation_id} | context, prompt, response | RFC-0422 |
| NS-VISION | atlas.vision | atlas | atlas.vision.{capture_id} | image, template, detection | RFC-0422 |
| NS-PROJECT | atlas.project | atlas | atlas.project.{project_id} | config, preference | RFC-0422 |
| NS-WORKSPACE | atlas.workspace | atlas | atlas.workspace.{workspace_id} | state, preference | RFC-0422 |
| NS-KNOWLEDGE | atlas.knowledge | atlas | atlas.knowledge.{pack_id} | vector, index, document | RFC-0422 |
| NS-MARKETPLACE | atlas.marketplace | atlas | atlas.marketplace.{package_id} | package, signature, manifest | RFC-0422 |
| NS-USER | atlas.user | atlas | atlas.user.{user_id} | profile, session, credential | RFC-0422 |
| NS-SYSTEM | atlas.system | atlas | atlas.system.{component} | config, audit, metric | RFC-0422 |
| NS-ADMIN | atlas.admin | atlas | atlas.admin.{area} | policy, compliance, record | RFC-0422 |

## 4. Namespace Resolution Rules

1. Paths are resolved from most specific to least specific parent.
2. Wildcard matching uses * at any namespace level.
3. Inheritance flows from parent to child for permissions and policies.
4. Namespace trees are immutable except for adding sub-namespaces.

## 5. Validation Rules

1. Every namespace path MUST start with tlas..
2. Namespace segments MUST match the regex ^[a-z][a-z0-9]*$.
3. Maximum namespace depth is 8 levels.
4. Each segment MUST be between 1 and 64 characters.
