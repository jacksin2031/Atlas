# Atlas RFC Map

> **Purpose**: Complete numbered tree of all Atlas RFCs, organized by domain and layer.  
> **Created**: 2026-07-02  
> **Owner**: Atlas Specification Committee  

---

## Tree Structure

`
Atlas Specifications
├── Layer 1: Common Models (RFC-1xxx)
│   ├── RFC-1001 Event Model
│   ├── RFC-1002 State Model
│   ├── RFC-1003 Capability Model
│   ├── RFC-1004 Contract Model
│   ├── RFC-1005 Manifest Model
│   └── RFC-1006 Error Model
│
├── Layer 2: Runtime (RFC-00xx)
│   ├── RFC-0001 Runtime Overview
│   ├── RFC-0002 Runtime Lifecycle
│   ├── RFC-0003 Runtime Service Model
│   ├── RFC-0004 Runtime Scheduler
│   ├── RFC-0005 Runtime Event Bus
│   ├── RFC-0006 Runtime State Management
│   ├── RFC-0007 Runtime IPC Architecture
│   ├── RFC-0008 Runtime Plugin Host
│   ├── RFC-0009 Runtime Resource Management
│   ├── RFC-0010 Runtime Manifest Specification
│   ├── RFC-0011 Runtime Error Taxonomy
│   ├── RFC-0012 Runtime Capability Registry
│   ├── RFC-0013 Runtime Contracts
│   └── RFC-0014 Runtime Reference Architecture
│
├── Layer 3a: IPC (RFC-01xx)
│   ├── RFC-0101 IPC Overview
│   ├── RFC-0102 IPC Message Model
│   ├── RFC-0103 IPC Transport
│   ├── RFC-0104 IPC Routing
│   ├── RFC-0105 IPC Channel
│   ├── RFC-0106 IPC Serialization
│   ├── RFC-0107 IPC Security
│   ├── RFC-0108 IPC Reliability
│   ├── RFC-0109 IPC Lifecycle
│   ├── RFC-0110 IPC Observability
│   ├── RFC-0111 IPC Error Model
│   └── RFC-0112 IPC Extension
│
├── Layer 3b: Storage (RFC-04xx)
│   ├── RFC-0401 Storage Overview
│   ├── RFC-0402 Storage Architecture
│   ├── RFC-0403 Storage Provider
│   ├── RFC-0404 Storage Lifecycle
│   ├── RFC-0405 Storage Schema
│   ├── RFC-0406 Storage Transactions
│   ├── RFC-0407 Storage Versioning
│   ├── RFC-0408 Storage Migration
│   ├── RFC-0409 Storage Security
│   ├── RFC-0410 Storage Cache
│   ├── RFC-0411 Storage Backup
│   ├── RFC-0412 Storage Recovery
│   ├── RFC-0413 Storage Events
│   ├── RFC-0414 Storage Observability
│   ├── RFC-0415 Storage Performance
│   ├── RFC-0416 Storage Consistency
│   ├── RFC-0417 Storage Locking
│   ├── RFC-0418 Storage Replication
│   ├── RFC-0419 Storage Extension
│   ├── RFC-0420 Storage Compliance
│   ├── RFC-0421 Storage Domains
│   ├── RFC-0422 Storage Namespace
│   ├── RFC-0423 Storage Resource Model
│   ├── RFC-0424 Storage Quota
│   └── RFC-0425 Storage Capability Discovery
│
├── Layer 4a: Plugin (RFC-02xx)
│   ├── RFC-0201 Plugin Overview
│   ├── RFC-0202 Plugin Manifest
│   ├── RFC-0203 Plugin Lifecycle
│   ├── RFC-0204 Plugin Loader
│   ├── RFC-0205 Plugin Registry
│   ├── RFC-0206 Plugin Capability
│   ├── RFC-0207 Plugin Security
│   ├── RFC-0208 Plugin Sandbox
│   ├── RFC-0209 Plugin API
│   ├── RFC-0210 Plugin Events
│   ├── RFC-0211 Plugin Dependency
│   ├── RFC-0212 Plugin Versioning
│   ├── RFC-0213 Plugin Marketplace
│   ├── RFC-0214 Plugin Extension Model
│   ├── RFC-0215 Plugin Service Model
│   ├── RFC-0216 Plugin Discovery
│   ├── RFC-0217 Plugin Packaging
│   ├── RFC-0218 Plugin Compatibility
│   ├── RFC-0219 Plugin Testing
│   ├── RFC-0220 Plugin IPC
│   ├── RFC-0221 Plugin Resources
│   ├── RFC-0222 Plugin Storage
│   ├── RFC-0223 Plugin Configuration
│   ├── RFC-0224 Plugin Diagnostics
│   ├── RFC-0225 Plugin Hot Reload
│   ├── RFC-0226 Plugin Migration
│   ├── RFC-0227 Plugin Service Discovery
│   ├── RFC-0228 Plugin Dependency Resolution
│   ├── RFC-0229 Plugin Telemetry
│   └── RFC-0230 Plugin Signature
│
├── Layer 4b: Workflow (RFC-03xx)
│   ├── RFC-0301 Workflow Overview
│   ├── RFC-0302 Workflow Language
│   ├── RFC-0303 Workflow Execution
│   ├── RFC-0304 Workflow Runtime
│   ├── RFC-0305 Workflow Lifecycle
│   ├── RFC-0306 Workflow State
│   ├── RFC-0307 Workflow Context
│   ├── RFC-0308 Workflow Events
│   ├── RFC-0309 Workflow Actions
│   ├── RFC-0310 Workflow Conditions
│   ├── RFC-0311 Workflow Triggers
│   ├── RFC-0312 Workflow Scheduler
│   ├── RFC-0313 Workflow Parallelism
│   ├── RFC-0314 Workflow Error Handling
│   ├── RFC-0315 Workflow Recovery
│   ├── RFC-0316 Workflow Debugging
│   ├── RFC-0317 Workflow Validation
│   ├── RFC-0318 Workflow Versioning
│   ├── RFC-0319 Workflow Security
│   ├── RFC-0320 Workflow Performance
│   ├── RFC-0321 Workflow Observability
│   ├── RFC-0322 Workflow Extension
│   ├── RFC-0323 Workflow Plugin Integration
│   ├── RFC-0324 Workflow Storage
│   ├── RFC-0325 Workflow AI
│   ├── RFC-0326 Workflow Vision
│   ├── RFC-0327 Workflow IPC
│   ├── RFC-0328 Workflow Serialization
│   ├── RFC-0329 Workflow Compatibility
│   ├── RFC-0330 Workflow Compliance
│   ├── RFC-0331 Workflow Testing
│   ├── RFC-0332 Workflow Migration
│   └── RFC-0333 Workflow Extension SDK
│
├── Layer 5: Intelligence (Deferred)
│   ├── [Vision] — no RFCs yet
│   ├── [AI] — no RFCs yet
│   ├── RFC-0601 Knowledge Pack Protocol Overview
│   ├── RFC-0602 Vector and Semantic Search Indexing
│   ├── RFC-0603 Search Abstraction Layers
│   └── RFC-0604 Knowledge Pack Package Format
│
├── Layer 6: Presentation & Distribution (Deferred)
│   ├── [UI] — no RFCs yet
│   ├── RFC-0501 Marketplace Protocol Overview
│   ├── RFC-0502 Package Format and Manifest Spec
│   ├── RFC-0503 Version Resolution Mechanics
│   ├── RFC-0504 Cryptographic Package Signatures
│   ├── RFC-0701 Project Package Format
│   ├── RFC-0702 Workspace Boundary and Scope
│   └── RFC-0703 Hierarchical Configuration Engine
│
├── Catalogs (not numbered as RFCs)
│   ├── IPC Catalogs
│   │   ├── catalog/interfaces.md
│   │   ├── catalog/messages.md
│   │   ├── catalog/channels.md
│   │   ├── catalog/errors.md
│   │   ├── catalog/capabilities.md
│   │   └── catalog/security-levels.md
│   ├── Plugin Catalogs
│   │   ├── catalog/plugin-service-lifecycle.md
│   │   ├── catalog/plugin-service-types.md
│   │   ├── catalog/plugin-signature.md
│   │   ├── catalog/plugin-release-management.md
│   │   └── catalog/plugin-extension-points.md
│   ├── Storage Catalogs
│   │   ├── catalog/storage-providers.md
│   │   ├── catalog/storage-observability.md
│   │   ├── catalog/storage-metrics.md
│   │   ├── catalog/storage-pipeline.md
│   │   ├── catalog/storage-locks.md
│   │   ├── catalog/storage-manifest-fields.md
│   │   ├── catalog/storage-extension-points.md
│   │   ├── catalog/storage-capability-flags.md
│   │   ├── catalog/storage-permissions.md
│   │   └── catalog/storage-quota.md
│   └── Workflow Catalogs (~30 files)
│       ├── catalog/workflow-actions.md
│       ├── catalog/workflow-conditions.md
│       ├── catalog/workflow-triggers.md
│       ├── catalog/workflow-events.md
│       ├── catalog/workflow-error-codes.md
│       ├── catalog/workflow-state-types.md
│       ├── catalog/workflow-variable-types.md
│       └── ... (many more)
│
└── Non-RFC Specifications
    ├── specs/glossary.md
    ├── specs/README.md
    ├── specs/RFC_CHANGE_POLICY.md
    ├── specs/RFC_REVIEW_CHECKLIST.md
    ├── specs/RFC_STYLE_GUIDE.md
    ├── specs/RFC_TEMPLATE.md
    ├── specs/RFC_VERSIONING_POLICY.md
    ├── specs/capabilities/capability-catalog.md
    ├── specs/errors/runtime-errors.md
    └── specs/events/runtime-event-catalog.md
`

---

## Quick Reference by Layer

| Layer | RFC Prefix | Count | Status |
|---|---|---|---|
| 1 — Common Models | RFC-1xxx | 6 | Draft |
| 2 — Runtime | RFC-00xx | 14 | Frozen |
| 3a — IPC | RFC-01xx | 12 | Active |
| 3b — Storage | RFC-04xx | 25 | Proposed |
| 4a — Plugin | RFC-02xx | 30 | Proposed |
| 4b — Workflow | RFC-03xx | 33 | Proposed |
| 5 — Intelligence | RFC-06xx | 4 reserved | Deferred |
| 6 — Presentation | RFC-05xx, RFC-07xx | 11 reserved | Deferred |
| **Total RFCs** | | **120+** | |

---

*This document is part of the Atlas Specification hierarchy. For layers, see [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) and [LAYER_MODEL.md](LAYER_MODEL.md). For dependency rules, see [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md).*


