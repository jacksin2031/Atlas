---
id: ATLAS-STORAGE-CATALOG-DOMAINS
title: Storage Domains Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Domains Catalog

## 1. Purpose

This catalog defines the canonical set of Storage domains that partition the Atlas data platform into isolated, independently governed data spaces.

## 2. Domain ID Prefix

All domain identifiers use the prefix DM-.

## 3. Complete Domain Catalog

| Domain ID | Name | Description | Permission Scope | Backup Policy | Versioning | Classification | RFC Reference |
|---|---|---|---|---|---|---|---|
| DM-RUNTIME | Runtime | Runtime execution state, service health, and lifecycle data. | Runtime Team | Continuous | Disabled | Internal | RFC-0421 |
| DM-PLUGIN | Plugin | Plugin registry, configuration, and runtime state. | Plugin Team | Daily | Enabled | Confidential | RFC-0421 |
| DM-WORKFLOW | Workflow | Workflow execution state, node outputs, and trigger data. | Workflow Team | Per workflow | Enabled | Internal | RFC-0421 |
| DM-AI | AI | AI context, conversation history, and model state. | AI Team | Hourly | Enabled | Confidential | RFC-0421 |
| DM-VISION | Vision | Vision engine captures, templates, and detection results. | Vision Team | Daily | Disabled | Internal | RFC-0421 |
| DM-PROJECT | Project | Project configuration and workspace settings. | Project Team | Weekly | Enabled | Restricted | RFC-0421 |
| DM-WORKSPACE | Workspace | Workspace boundary state and user preferences. | User | Daily | Disabled | Internal | RFC-0421 |
| DM-KNOWLEDGE | Knowledge | Knowledge packs, vector indices, and semantic search data. | Knowledge Team | Continuous | Enabled | Confidential | RFC-0421 |
| DM-MARKETPLACE | Marketplace | Marketplace packages, signatures, and version manifests. | Marketplace Team | Daily | Enabled | Restricted | RFC-0421 |
| DM-USER | User | User profiles, sessions, credentials, and preferences. | Security | Per session | Disabled | Restricted | RFC-0421 |
| DM-SYSTEM | System | System-level configuration, audit logs, and metrics. | Admin | Permanent | Append-only | Restricted | RFC-0421 |
| DM-ADMIN | Admin | Administrative data, compliance records, and policy configurations. | Super Admin | Permanent | Disabled | Restricted | RFC-0421 |

## 4. Domain Permission Matrix

| Permission | RUNTIME | PLUGIN | WORKFLOW | AI | VISION | PROJECT | WORKSPACE | KNOWLEDGE | MARKETPLACE | USER | SYSTEM | ADMIN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| READ | Runtime | Plugin | Workflow | AI | Vision | Project | User | Knowledge | Marketplace | Admin | Admin | Super Admin |
| WRITE | Runtime | Plugin | Workflow | AI | Vision | Project | User | Knowledge | Marketplace | Admin | Admin | Super Admin |
| DELETE | Runtime | Plugin | Workflow | AI | Vision | Project | User | Knowledge | Marketplace | Admin | Admin | Super Admin |
| ADMIN | Runtime | Plugin | Workflow | AI | Vision | Project | User | Knowledge | Marketplace | Admin | Admin | Super Admin |

## 5. Validation Rules

1. Every domain identifier MUST match the regex ^DM-[A-Z]+$.
2. Domain names MUST be unique.
3. Domains MUST be fully isolated at the namespace level per RFC-0422.
4. Cross-domain access MUST require explicit permission grants.
5. New domains MUST be registered through RFC-0419 extension mechanism.
