# RFC-0230: Plugin Diagnostics

RFC: RFC-0230
Title: Plugin Diagnostics
Status: Proposed
Version: 1.0.0
Category: Plugin Operations
Layer: Observability
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0229 Plugin Telemetry
  - RFC-0207 Plugin Security
Related RFC:
  - RFC-0220 Plugin IPC
  - RFC-0224 Plugin Testing
  - RFC-0225 Plugin Hot Reload
Related ADR:
  - ADR-0030 Diagnostics Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the diagnostics commands, diagnostics categories (dependency, API, permission, manifest, capability, version, signature, sandbox, performance), diagnostic output format, diagnostic report generation, and diagnostic remediation suggestions requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Diagnostics Philosophy](#4-diagnostics-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Diagnostics Commands](#9-diagnostics-commands)
10. [Diagnostics Categories](#10-diagnostics-categories)
11. [Diagnostic Output Format](#11-diagnostic-output-format)
12. [Diagnostic Report](#12-diagnostic-report)
13. [Remediation Suggestions](#13-remediation-suggestions)
14. [Performance Budgets](#14-performance-budgets)
15. [Glossary](#15-glossary)
16. [Acceptance Criteria](#16-acceptance-criteria)
17. [Cross References](#17-cross-references)
18. [References](#18-references)
19. [Revision History](#19-revision-history)
20. [Future Evolution](#20-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Comprehensive Diagnostics**: Cover all 9 diagnostic categories.
2. **CLI Interface**: tlas doctor command for quick health checks.
3. **Structured Output**: Machine-readable and human-readable output formats.
4. **Report Generation**: Full diagnostic reports for debugging and support.
5. **Remediation Suggestions**: Actionable guidance for each diagnostic finding.
6. **Real-Time Diagnosis**: Diagnose running plugins without restart.

---

- RFC-0323 Workflow Plugin Integration


## 4 Diagnostics Philosophy

Diagnostics follow these principles:

- Diagnosis is NON-INTRUSIVE: it does NOT modify plugin state.
- Remediation suggestions are ACTIONABLE: each finding has a clear fix.
- Output is STRUCTURED: machine-parseable for automation.
- Reports are COMPREHENSIVE: include all relevant context for debugging.

---


## 6 Boundaries

- Diagnostics read plugin state only; they do NOT modify it.
- Diagnostic data is scoped to the local runtime instance.
- Diagnostic reports include only plugin-level data (no user data).
- Diagnostics do NOT access other subsystems (runtime, workflow) beyond plugin scope.

---



## 8 Architecture

`mermaid
graph TB
    CLI[atlas doctor]
    subgraph Diagnostics Engine
        DE[Diagnostics Engine]
        DC[Dependency Checker]
        DAC[API Checker]
        PC[Permission Checker]
        MC[Manifest Checker]
        CC[Capability Checker]
        VC[Version Checker]
        SC[Signature Checker]
        BC[Sandbox Checker]
        PercC[Performance Checker]
    end
    subgraph Output
        HO[Human Output]
        JO[JSON Output]
        DR[Diagnostic Report]
    end
    CLI --> DE
    DE --> DC
    DE --> DAC
    DE --> PC
    DE --> MC
    DE --> CC
    DE --> VC
    DE --> SC
    DE --> BC
    DE --> PercC
    DE --> HO
    DE --> JO
    DE --> DR
`

---

This specification IS responsible for:
- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 10 Diagnostics Categories

### 10.1 Missing Dependency

Checks if all declared dependencies are satisfied:

`
Checking dependencies for plugin 'my-plugin'...
  [FAIL] core-utils >=2.0.0 - NOT FOUND
  [WARN] optional-ai-engine >=1.0.0 - FOUND (v0.9.5, below minimum)
  [PASS] workspace-storage >=1.0.0 - FOUND (v1.2.0)
`

### 10.2 Broken API

Checks if the plugin calls runtime APIs correctly:

`
Checking API compatibility for plugin 'my-plugin'...
  [FAIL] Plugin calls deprecated API: runtime.services.unregister() - REMOVED in v2.0
  [WARN] Plugin uses experimental API: runtime.experimental.feature() - MAY CHANGE
  [PASS] All stable API calls are valid
`

### 10.3 Permission

Checks permission declarations and enforcement:

`
Checking permissions for plugin 'my-plugin'...
  [FAIL] Plugin requests 'network:all' but declares 'network:local' in manifest
  [WARN] Plugin has 'elevated' permission but no audit logging configured
  [PASS] All declared permissions are valid
`

### 10.4 Manifest

Checks manifest structure and validity:

`
Checking manifest for plugin 'my-plugin'...
  [FAIL] Required field 'homepage' is missing
  [WARN] Icon file 'resources/icons/icon.svg' not found in package
  [PASS] All required fields are present
  [PASS] Schema validation passed
`

### 10.5 Capability

Checks capability declarations and functionality:

`
Checking capabilities for plugin 'my-plugin'...
  [FAIL] Declared capability 'vision:ocr' not functional - OCR engine not found
  [WARN] Capability 'ai:prompt' has not been used in 7 days
  [PASS] All capabilities are functional
`

### 10.6 Version

Checks version compatibility:

`
Checking version compatibility for plugin 'my-plugin'...
  [FAIL] Plugin requires runtime >=2.0.0 but runtime is 1.9.5
  [WARN] Plugin is 3 minor versions behind latest (v1.0.0 vs v1.3.0)
  [PASS] Version compatibility OK
`

### 10.7 Signature

Checks plugin signature and integrity:

`
Checking signature for plugin 'my-plugin'...
  [FAIL] Signature verification failed - possible tampering
  [WARN] Plugin signed with test key (not production-ready)
  [PASS] Signature verified with production key
`

### 10.8 Sandbox

Checks sandbox boundary compliance:

`
Checking sandbox compliance for plugin 'my-plugin'...
  [FAIL] Plugin attempted filesystem access outside workspace boundary
  [WARN] Plugin opened 15 network connections (threshold: 10)
  [PASS] All sandbox boundaries respected
`

### 10.9 Performance

Checks plugin performance metrics:

`
Checking performance for plugin 'my-plugin'...
  [FAIL] Plugin load time: 5.2s (threshold: 2.0s)
  [WARN] Plugin memory usage: 180MB (threshold: 100MB)
  [WARN] Average IPC latency: 15ms (threshold: 5ms)
  [PASS] Plugin performance within thresholds
`

---

{
  "diagnostic_run": {
    "timestamp": "2026-07-01T12:00:00Z",
    "runtime_version": "2.1.0",
    "plugins_checked": 15,
    "summary": { "healthy": 12, "warnings": 2, "errors": 1 },
    "findings": [
      {
        "plugin_id": "my-plugin",
        "category": "dependency",
        "severity": "error",
        "message": "Missing dependency 'core-utils >=2.0.0'",
        "remediation": "Install core-utils v2.0.0 or later"
      }
    ]
  }
}
`

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 13 Remediation Suggestions

Every diagnostic finding includes a remediation suggestion:

| Finding                        | Remediation                                    |
|--------------------------------|------------------------------------------------|
| Missing dependency             | Install the missing dependency or update version range |
| Broken API call                | Update to the current API version              |
| Permission mismatch            | Fix permission declaration in manifest         |
| Missing manifest field         | Add the required field to the manifest         |
| Non-functional capability      | Check capability dependencies and runtime features |
| Runtime version mismatch       | Update runtime or downgrade plugin             |
| Signature verification failed  | Re-download the plugin from a trusted source   |
| Sandbox boundary violation     | Review and fix plugin permission declarations  |
| Performance threshold exceeded | Profile plugin and optimize resource usage     |

---



## 15 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Diagnostics       | Tooling to diagnose plugin health and issues.        |
| Finding           | A specific issue identified during diagnostics.      |
| Remediation       | Suggested fix for a diagnostic finding.              |

---

| RFC-0201 | Consumed | Plugin Overview |


## 17 Cross References

- RFC-0201 Plugin Overview
- RFC-0207 Plugin Security
- RFC-0211 Plugin Dependency
- RFC-0229 Plugin Telemetry
- RFC-0224 Plugin Testing

---



## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

---

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## 19 Revision History

| Date       | Version | Author                    | Change                           |
|------------|---------|---------------------------|----------------------------------|
| 2026-07-01 | 1.0.0   | Atlas Specification Committee | Initial proposal               |

---


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

All contracts in this specification are defined as abstract behavioral interfaces.

---




