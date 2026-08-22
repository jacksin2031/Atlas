# RFC-0219: Plugin Permission Model

RFC: RFC-0219
Title: Plugin Permission Model
Status: Proposed
Version: 1.0.0
Category: Plugin Security
Layer: Security
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0207 Plugin Security
  - RFC-0208 Plugin Sandbox
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0218 Plugin Compatibility
  - RFC-0220 Plugin IPC
Related ADR:
  - ADR-0019 Permission Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the permission levels, permission declaration, permission request flow, runtime enforcement, workflow elevation, permission revocation, audit trail, least privilege principle, permission groups, and emergency lockdown requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Permission Philosophy](#4-permission-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Permission Levels](#9-permission-levels)
10. [Permission Declaration](#10-permission-declaration)
11. [Permission Request Flow](#11-permission-request-flow)
12. [Runtime Enforcement](#12-runtime-enforcement)
13. [Workflow Elevation](#13-workflow-elevation)
14. [Permission Revocation](#14-permission-revocation)
15. [Audit Trail](#15-audit-trail)
16. [Least Privilege](#16-least-privilege)
17. [Permission Groups](#17-permission-groups)
18. [Emergency Lockdown](#18-emergency-lockdown)
19. [Performance Budgets](#19-performance-budgets)
20. [Glossary](#20-glossary)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Cross References](#22-cross-references)
23. [References](#23-references)
24. [Revision History](#24-revision-history)
25. [Future Evolution](#25-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Permission Levels**: Define six discrete permission levels with clear boundaries.
2. **Declaration**: Permissions declared in the plugin manifest.
3. **Request Flow**: Runtime evaluates and user approves elevated/privileged permissions.
4. **Enforcement**: Sandbox boundaries enforced per permission level.
5. **Workflow Elevation**: Temporary elevation for specific workflows.
6. **Revocation**: Runtime can revoke permissions dynamically.
7. **Audit**: All permission grants and denials logged.
8. **Least Privilege**: Default deny; explicit allow only.

---

- RFC-0323 Workflow Plugin Integration


## 4 Permission Philosophy

The permission model follows these principles:

- Default deny: plugins start with NO permissions.
- Explicit allow: every permission MUST be declared and granted.
- Least privilege: grant only what the plugin needs.
- Audit trail: every permission decision is logged.
- Revocable: permissions can be revoked at any time.

---


## 6 Boundaries

- Permission enforcement happens at the runtime boundary, not the plugin boundary.
- A plugin CANNOT bypass its declared permissions.
- Workflow elevation is temporary and scoped to the workflow duration.
- Emergency lockdown affects ALL privileged plugins simultaneously.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin
        PD[Permission Declaration]
    end
    subgraph Runtime
        SG[Security Gate]
        SB[Sandbox]
        AU[Audit Logger]
        EL[Emergency Lockdown]
    end
    PD -->|evaluate| SG
    SG -->|grant/deny| AU
    SG -->|enforce| SB
    SB -->|check| PL[Permission Level]
    PL -->|low| S1[Strict Sandbox]
    PL -->|normal| S2[Standard Sandbox]
    PL -->|elevated| S3[Relaxed Sandbox]
    PL -->|privileged| S4[Minimal Sandbox]
    PL -->|restricted| S5[Maximal Sandbox]
    PL -->|experimental| S6[Configurable Sandbox]
    EL -->|trigger| SB
    EL -->|notify| AU
`

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Permission Declaration

Permissions are declared in the manifest:

`json
{
  "permissions": [
    {
      "level": "normal",
      "resources": ["workspace:read", "workspace:write"],
      "actions": ["read", "write"],
      "groups": ["filesystem-full"]
    },
    {
      "level": "elevated",
      "resources": ["system:process"],
      "actions": ["execute"],
      "groups": [],
      "requires_approval": true
    }
  ]
}
`

Requirements:
- Each permission entry MUST declare level from the enum in Section 9.
- esources MUST match patterns in the permission schema catalog.
- ctions MUST be a subset of: read, write, execute, admin.
- groups MAY reference predefined permission groups.
- equires_approval defaults to 	rue for elevated+ levels.

---

            SG-->>R: Deny
            R-->>P: Reject (PERMISSION_002)
        end
    end
`

---


## 13 Workflow Elevation

Some workflows may temporarily elevate permissions:

`json
{
  "workflow_elevation": {
    "enabled": true,
    "max_duration_seconds": 300,
    "requires_confirmation": true,
    "auto_revoke": true
  }
}
`

Rules:
- Elevation is scoped to the workflow execution duration.
- Maximum elevation duration: configurable, default 300 seconds.
- User confirmation is REQUIRED for elevation to privileged+.
- Auto-revoke occurs when the workflow completes or times out.
- Elevated permissions are logged in the audit trail.

---



## 15 Audit Trail

Every permission decision is logged:

`json
{
  "timestamp": "ISO8601",
  "event": "permission.granted | permission.denied | permission.revoked | permission.elevated",
  "plugin_id": "string",
  "permission_level": "string",
  "resources": ["string"],
  "actor": "user | admin | system | workflow",
  "approval_status": "approved | denied",
  "reason": "string"
}
`

Requirements:
- Audit logs MUST be tamper-evident (cryptographic hash chain).
- Audit logs MUST be retained for a minimum of 90 days.
- Audit logs MUST be accessible to administrators.
- Sensitive data (API keys, tokens) MUST NOT appear in audit logs.

---

| RFC-0201 | Consumed | Plugin Overview |


## 17 Permission Groups

Predefined permission bundles:

| Group Name       | Permissions Included                                    | Typical Use         |
|------------------|---------------------------------------------------------|---------------------|
| ilesystem-full| workspace:read, workspace:write, system:process   | File manipulation   |
| 
etwork-all    | 
etwork:*                                             | API integrations    |
| 
etwork-local  | 
etwork:local                                         | Local services      |
| i-complete    | i:model, i:prompt, i:embed                     | AI plugins          |
| ision-complete| ision:ocr, ision:image                            | Vision plugins      |
| storage-full   | storage:cache, storage:persistent, storage:secret | Data plugins        |

---

- Workflow execution (covered by RFC-0301).


## 19 Performance Budgets

- Permission evaluation: < 5ms per plugin.
- Sandbox boundary check: < 0.1ms per operation.
- Audit log write: < 1ms (async).
- Emergency lockdown: < 1 second for all privileged plugins.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 21 Acceptance Criteria

1. GIVEN a plugin declares level: low, WHEN it attempts network access, THEN the sandbox blocks the connection.
2. GIVEN a plugin declares level: elevated, WHEN it loads, THEN the user is prompted for approval.
3. GIVEN a plugin declares level: privileged, WHEN it loads, THEN the administrator is prompted for approval.
4. GIVEN an emergency lockdown is triggered, WHEN 5 seconds elapse, THEN ALL privileged plugins are suspended.
5. GIVEN a workflow elevation is active, WHEN the workflow completes, THEN permissions are automatically revoked.
6. GIVEN a permission is granted, WHEN the audit log is checked, THEN the grant event is recorded with timestamp and actor.
7. GIVEN a plugin declares no permissions, WHEN it attempts any resource access, THEN access is denied by default.

---



## 23 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) — Saltzer and Schroeder, 1975.
- [RBAC](https://csrc.nist.gov/publications/detail/fips/184/final) — NIST FIPS 184, Role-Based Access Control.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 25 Future Evolution

1. Support for dynamic permission policies (policy-as-code).
2. Support for AI-assisted permission recommendation.
3. Support for permission auditing API for third-party compliance tools.

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All plugin contracts are defined as abstract behavioral interfaces.

---




---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |