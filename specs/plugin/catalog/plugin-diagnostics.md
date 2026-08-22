---
id: ATLAS-PLUGINSPEC-CATALOG-DIAG
title: Plugin Diagnostics Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Diagnostics Catalog

## 1. Purpose

Documents diagnostic check categories and their findings taxonomy.

## 2. Diagnostic Categories

| Category       | Check Items                                    | Severity Levels     |
|----------------|------------------------------------------------|---------------------|
| Dependency     | Missing, version conflict, circular            | Error, Warning      |
| API            | Deprecated, removed, experimental              | Error, Warning, Info|
| Permission     | Mismatch, escalation, boundary violation       | Error, Warning      |
| Manifest       | Missing fields, schema validation              | Error, Warning      |
| Capability     | Non-functional, unused, degraded               | Error, Warning      |
| Version        | Runtime mismatch, outdated                     | Error, Warning      |
| Signature      | Verification failed, test key                  | Error, Warning      |
| Sandbox        | Boundary violation, resource leak              | Error, Warning      |
| Performance    | Load time, memory, latency, throughput         | Error, Warning      |

## 3. Finding Severity Levels

| Level   | Action Required                  | Auto-Recovery |
|---------|----------------------------------|---------------|
| Error   | Immediate operator intervention  | No            |
| Warning | Scheduled investigation          | Maybe         |
| Info    | Informational, no action needed  | No            |

## 4. Cross-References

- RFC-0230 Plugin Diagnostics
