# Plugin Specification System - README

## Overview

The Atlas Plugin Specification System defines the **Platform Extension Framework** of the Atlas Platform. It specifies how plugins integrate with the Runtime while remaining isolated, secure, versioned, observable, and maintainable.

This is an architectural specification, NOT implementation documentation, and NOT SDK documentation.

All specifications are implementation-independent: they do NOT reference any programming language, framework, runtime, operating system, or third-party library.

RFC 2119 terminology (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) is used exclusively throughout all documents.

---

## Plugin as Platform Extension Framework

The Atlas Plugin System is NOT just a "plugin loader." It is a **Platform Extension Framework** where:

- **Runtime**, **Workflow**, **AI**, **Vision**, **UI**, **Storage**, **Scheduler**, and **IPC** are all Extension Points.
- Plugins are one type of **Package** among many.
- Every system capability can be extended, replaced, or augmented.

---

## Plugin Architecture

`mermaid
flowchart TD
    subgraph Distribution["Distribution Layer"]
        MP[Marketplace]
        PKG[Package .atlas-plugin]
        DIS[Discovery]
    end

    subgraph Loading["Loading Layer"]
        LDR[Loader]
        MAN[Manifest Parser]
        REG[Registry]
        DEP[Dependency Resolver]
    end

    subgraph Security["Security Layer"]
        PERM[Permission Model]
        SANDBOX[Sandbox]
        SIG[Signature Verify]
        COMPAT[Compatibility Check]
    end

    subgraph Runtime["Runtime Layer"]
        CAP[Capability]
        LIFE[Lifecycle]
        SVC[Service Model]
        API[Plugin API]
        EVT[Event Bus]
    end

    subgraph Operations["Operations Layer"]
        STR[Storage]
        RES[Resources]
        CFG[Configuration]
        IPC[IPC Router]
        DIAG[Diagnostics]
        TELE[Telemetry]
        HOT[Hot Reload]
        MIG[Migration]
        SDIS[Service Discovery]
        DRES[Dependency Resolution]
    end

    MP --> PKG
    PKG --> DIS
    DIS --> LDR
    LDR --> MAN
    MAN --> REG
    REG --> DEP
    DEP --> SIG
    SIG --> COMPAT
    COMPAT --> PERM
    PERM --> SANDBOX
    SANDBOX --> CAP
    CAP --> LIFE
    LIFE --> SVC
    SVC --> API
    API --> EVT
    EVT --> STR
    EVT --> RES
    EVT --> CFG
    EVT --> IPC
    IPC --> DIAG
    IPC --> TELE
    LIFE --> HOT
    LIFE --> MIG
    SVC --> SDIS
    DEP --> DRES
`

### Architecture Layers

| Layer | RFCs | Purpose |
|---|---|---|
| **Distribution** | RFC-0213, RFC-0216, RFC-0217 | Package, discover, and distribute plugins |
| **Loading** | RFC-0204, RFC-0205, RFC-0211, RFC-0226 | Parse, validate, resolve, and load plugins |
| **Security** | RFC-0207, RFC-0208, RFC-0218, RFC-0219 | Verify, isolate, and enforce permissions |
| **Runtime** | RFC-0201, RFC-0203, RFC-0206, RFC-0209, RFC-0210, RFC-0214, RFC-0215 | Core plugin lifecycle, capabilities, services, API, events |
| **Operations** | RFC-0220, RFC-0221, RFC-0222, RFC-0223, RFC-0224, RFC-0225, RFC-0227, RFC-0228, RFC-0229, RFC-0230 | IPC, resources, config, storage, testing, hot reload, service discovery, migration, telemetry, diagnostics |

---

## Reading Order

Read the RFCs in the following order for progressive understanding:

### Foundation (Core Concepts)
1. **RFC-0201** Plugin Overview - Start here for the big picture
2. **RFC-0202** Plugin Manifest - How plugins declare their identity and capabilities
3. **RFC-0203** Plugin Lifecycle - How plugins are managed throughout their lifetime

### Loading & Registry
4. **RFC-0204** Plugin Loader - How plugins are discovered and loaded
5. **RFC-0205** Plugin Registry - How plugin metadata is stored and queried

### Capabilities & Security
6. **RFC-0206** Plugin Capability - How plugins expose functional competencies
7. **RFC-0207** Plugin Security - Trust model and security enforcement
8. **RFC-0208** Plugin Sandbox - Isolation and resource boundaries

### API & Communication
9. **RFC-0209** Plugin API - Interface contracts and versioning
10. **RFC-0210** Plugin Events - Communication and notification system

### Dependencies & Distribution
11. **RFC-0211** Plugin Dependency - Relationship management between plugins
12. **RFC-0212** Plugin Versioning - Semantic versioning and compatibility
13. **RFC-0213** Plugin Marketplace - Distribution and verification

### Extension Model
14. **RFC-0214** Plugin Extension Model - Platform extensibility mechanism

### Platform Services
15. **RFC-0215** Plugin Service Model - Service registration, lifetime, and scope
16. **RFC-0216** Plugin Discovery - Multi-source plugin discovery and indexing
17. **RFC-0217** Plugin Packaging - The atlas-plugin package format
18. **RFC-0218** Plugin Compatibility - Compatibility matrix and version negotiation
19. **RFC-0219** Plugin Permission Model - Full permission hierarchy and enforcement

### Operational Concerns
20. **RFC-0220** Plugin IPC - Inter-plugin communication channel
21. **RFC-0221** Plugin Resources - Resource management (icons, translations, models)
22. **RFC-0222** Plugin Configuration - Configuration hierarchy and resolution
23. **RFC-0223** Plugin Storage - Storage backends and isolation
24. **RFC-0224** Plugin Testing - Testing framework and CI pipeline
25. **RFC-0225** Plugin Hot Reload - Zero-downtime plugin reloading
26. **RFC-0226** Plugin Dependency Resolution - Solver, cycles, version conflicts
27. **RFC-0227** Plugin Service Discovery - Find services by capability, not by name
28. **RFC-0228** Plugin Migration - Manifest, config, storage, permission migrations
29. **RFC-0229** Plugin Telemetry - Health, latency, memory, crash, usage metrics
30. **RFC-0230** Plugin Diagnostics - atlas doctor: comprehensive plugin health check

