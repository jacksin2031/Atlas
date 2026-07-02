# Atlas Specification Hierarchy

> **Purpose**: Define the specification structure, reading order, and governance model for Project Atlas.
> **Owner**: Atlas Specification Committee
> **Last Updated**: 2026-07-01

---

## Specification Levels

Atlas specifications follow a four-level hierarchy. Each level has a distinct purpose and audience.

- **Level 1: Governance** — Constitution, ADRs, RFC Index, glossary, policies
- **Level 2: Runtime** — Core execution engine specifications
- **Level 3: Subsystems** — Workflow, Plugin, IPC, Storage, Vision, AI, Marketplace, Knowledge, Workspace
- **Level 4: Common Models** — Cross-cutting shared models referenced by all subsystems

---

## Level 1: Governance

Foundation documents that define how Atlas is built and governed.

| Document | Path | Purpose |
|---|---|---|
| [ADS Constitution](.ai/constitution.md) | .ai/constitution.md | Core values and principles |
| [Architecture Rules](.ai/architecture-rules.md) | .ai/architecture-rules.md | Layering and dependency constraints |
| [Coding Standards](.ai/coding-standard.md) | .ai/coding-standard.md | Code style and structure |
| [RFC Index](specs/RFC_INDEX.md) | specs/RFC_INDEX.md | Master registry of all RFCs |
| [Glossary](specs/glossary.md) | specs/glossary.md | Authoritative terminology |
| [ADR Collection](docs/adr/) | docs/adr/ | Architecture Decision Records |
| [RFC Template](specs/RFC_TEMPLATE.md) | specs/RFC_TEMPLATE.md | Standard template for all RFCs |
| [RFC Style Guide](specs/RFC_STYLE_GUIDE.md) | specs/RFC_STYLE_GUIDE.md | Canonical style rules for all RFCs |
| [RFC Review Checklist](specs/RFC_REVIEW_CHECKLIST.md) | specs/RFC_REVIEW_CHECKLIST.md | Quality checklist for RFC review |
| [RFC Change Policy](specs/RFC_CHANGE_POLICY.md) | specs/RFC_CHANGE_POLICY.md | RFC modification and review process |
| [RFC Versioning Policy](specs/RFC_VERSIONING_POLICY.md) | specs/RFC_VERSIONING_POLICY.md | Versioning and status lifecycle rules |

**Reading Order**: Constitution → Architecture Rules → RFC Index → Glossary → RFC Template → RFC Style Guide

---

## Level 2: Runtime

Core execution engine specifications. These define the foundation that all subsystems build upon.

| RFC | Title | Path | Status |
|---|---|---|---|
| RFC-0001 | Runtime Overview | [specs/runtime/RFC-0001-runtime-overview.md](specs/runtime/RFC-0001-runtime-overview.md) | Frozen |
| RFC-0002 | Runtime Lifecycle | [specs/runtime/RFC-0002-runtime-lifecycle.md](specs/runtime/RFC-0002-runtime-lifecycle.md) | Frozen |
| RFC-0003 | Runtime Service Model | [specs/runtime/RFC-0003-runtime-service-model.md](specs/runtime/RFC-0003-runtime-service-model.md) | Frozen |
| RFC-0004 | Runtime Scheduler | [specs/runtime/RFC-0004-runtime-scheduler.md](specs/runtime/RFC-0004-runtime-scheduler.md) | Frozen |
| RFC-0005 | Runtime Event Bus | [specs/runtime/RFC-0005-runtime-eventbus.md](specs/runtime/RFC-0005-runtime-eventbus.md) | Frozen |
| RFC-0006 | Runtime State Management | [specs/runtime/RFC-0006-runtime-state.md](specs/runtime/RFC-0006-runtime-state.md) | Frozen |
| RFC-0007 | Runtime IPC Architecture | [specs/runtime/RFC-0007-runtime-ipc.md](specs/runtime/RFC-0007-runtime-ipc.md) | Frozen |
| RFC-0008 | Runtime Plugin Host | [specs/runtime/RFC-0008-runtime-plugin.md](specs/runtime/RFC-0008-runtime-plugin.md) | Frozen |
| RFC-0009 | Runtime Resource Management | [specs/runtime/RFC-0009-runtime-resource.md](specs/runtime/RFC-0009-runtime-resource.md) | Frozen |
| RFC-0010 | Runtime Manifest Specification | [specs/runtime/RFC-0010-runtime-manifest.md](specs/runtime/RFC-0010-runtime-manifest.md) | Frozen |
| RFC-0011 | Runtime Error Taxonomy | [specs/runtime/RFC-0011-runtime-errors.md](specs/runtime/RFC-0011-runtime-errors.md) | Frozen |
| RFC-0012 | Runtime Capability Registry | [specs/runtime/RFC-0012-runtime-capability.md](specs/runtime/RFC-0012-runtime-capability.md) | Frozen |
| RFC-0013 | Runtime Contracts | [specs/runtime/RFC-0013-runtime-contracts.md](specs/runtime/RFC-0013-runtime-contracts.md) | Frozen |
| RFC-0014 | Runtime Reference Architecture | [specs/runtime/RFC-0014-runtime-reference-architecture.md](specs/runtime/RFC-0014-runtime-reference-architecture.md) | Frozen |

---

## Level 3: Subsystems

### IPC (Inter-Process Communication)

| RFC | Title | Status |
|---|---|---|
| RFC-0101 | IPC Overview | Accepted |
| RFC-0102 | IPC Message Model | Accepted |
| RFC-0103 | IPC Transport | Accepted |
| RFC-0104 | IPC Routing | Accepted |
| RFC-0105 | IPC Channel | Accepted |
| RFC-0106 | IPC Serialization | Accepted |
| RFC-0107 | IPC Security | Accepted |
| RFC-0108 | IPC Reliability | Accepted |
| RFC-0109 | IPC Lifecycle | Accepted |
| RFC-0110 | IPC Observability | Accepted |
| RFC-0111 | IPC Error Model | Accepted |
| RFC-0112 | IPC Extension | Accepted |

### Plugin System

| RFC | Title | Status |
|---|---|---|
| RFC-0201 | Plugin Overview | Proposed |
| RFC-0202 | Plugin Manifest | Proposed |
| RFC-0203 | Plugin Lifecycle | Proposed |
| RFC-0204 | Plugin Loader | Proposed |
| RFC-0205 | Plugin Registry | Proposed |
| RFC-0206 | Plugin Capability | Proposed |
| RFC-0207 | Plugin Security | Proposed |
| RFC-0208 | Plugin Sandbox | Proposed |
| RFC-0209 | Plugin API | Proposed |
| RFC-0210 | Plugin Events | Proposed |
| RFC-0211 | Plugin Dependency | Proposed |
| RFC-0212 | Plugin Versioning | Proposed |
| RFC-0213 | Plugin Marketplace | Proposed |
| RFC-0214 | Plugin Extension Model | Proposed |
| RFC-0215 | Plugin Service Model | Proposed |
| RFC-0216 | Plugin Discovery | Proposed |
| RFC-0217 | Plugin Packaging | Proposed |
| RFC-0218 | Plugin Compatibility | Proposed |
| RFC-0219 | Plugin Permission Model | Proposed |
| RFC-0220 | Plugin IPC | Proposed |
| RFC-0221 | Plugin Resources | Proposed |
| RFC-0222 | Plugin Configuration | Proposed |
| RFC-0223 | Plugin Storage | Proposed |
| RFC-0224 | Plugin Testing | Proposed |
| RFC-0225 | Plugin Hot Reload | Proposed |
| RFC-0226 | Plugin Dependency Resolution | Proposed |
| RFC-0227 | Plugin Service Discovery | Proposed |
| RFC-0228 | Plugin Migration | Proposed |
| RFC-0229 | Plugin Telemetry | Proposed |
| RFC-0230 | Plugin Diagnostics | Proposed |

### Workflow Engine

| RFC | Title | Status |
|---|---|---|
| RFC-0301 | Workflow Overview | Proposed |
| RFC-0302 | Workflow Language | Proposed |
| RFC-0303 | Workflow Execution | Proposed |
| RFC-0304 | Workflow Runtime | Proposed |
| RFC-0305 | Workflow Lifecycle | Proposed |
| RFC-0306 | Workflow State | Proposed |
| RFC-0307 | Workflow Context | Proposed |
| RFC-0308 | Workflow Events | Proposed |
| RFC-0309 | Workflow Actions | Proposed |
| RFC-0310 | Workflow Conditions | Proposed |
| RFC-0311 | Workflow Triggers | Proposed |
| RFC-0312 | Workflow Scheduler | Proposed |
| RFC-0313 | Workflow Parallelism | Proposed |
| RFC-0314 | Workflow Error Handling | Proposed |
| RFC-0315 | Workflow Recovery | Proposed |
| RFC-0316 | Workflow Debugging | Proposed |
| RFC-0317 | Workflow Validation | Proposed |
| RFC-0318 | Workflow Versioning | Proposed |
| RFC-0319 | Workflow Security | Proposed |
| RFC-0320 | Workflow Performance | Proposed |
| RFC-0321 | Workflow Observability | Proposed |
| RFC-0322 | Workflow Extension | Proposed |
| RFC-0323 | Workflow Plugin Integration | Proposed |
| RFC-0324 | Workflow Storage | Proposed |
| RFC-0325 | Workflow AI | Proposed |
| RFC-0326 | Workflow Vision | Proposed |
| RFC-0327 | Workflow IPC | Proposed |
| RFC-0328 | Workflow Serialization | Proposed |
| RFC-0329 | Workflow Compatibility | Proposed |
| RFC-0330 | Workflow Compliance | Proposed |
| RFC-0331 | Workflow Testing | Proposed |
| RFC-0332 | Workflow Migration | Proposed |
| RFC-0333 | Workflow SDK | Proposed |

### Storage

| RFC | Title | Status |
|---|---|---|
| RFC-0401 | Storage Overview | Proposed |
| RFC-0402 | Storage Architecture | Proposed |
| RFC-0403 | Storage Provider | Proposed |
| RFC-0404 | Storage Lifecycle | Proposed |
| RFC-0405 | Storage Schema | Proposed |
| RFC-0406 | Storage Transactions | Proposed |
| RFC-0407 | Storage Versioning | Proposed |
| RFC-0408 | Storage Migration | Proposed |
| RFC-0409 | Storage Security | Proposed |
| RFC-0410 | Storage Cache | Proposed |
| RFC-0411 | Storage Backup | Proposed |
| RFC-0412 | Storage Recovery | Proposed |
| RFC-0413 | Storage Events | Proposed |
| RFC-0414 | Storage Observability | Proposed |
| RFC-0415 | Storage Performance | Proposed |
| RFC-0416 | Storage Consistency | Proposed |
| RFC-0417 | Storage Locking | Proposed |
| RFC-0418 | Storage Replication | Proposed |
| RFC-0419 | Storage Extension | Proposed |
| RFC-0420 | Storage Compliance | Proposed |
| RFC-0421 | Storage Domains | Proposed |
| RFC-0422 | Storage Namespace | Proposed |
| RFC-0423 | Storage Resource Model | Proposed |
| RFC-0424 | Storage Quota | Proposed |
| RFC-0425 | Storage Capability Discovery | Proposed |

### Marketplace Infrastructure

| RFC | Title | Status |
|---|---|---|
| RFC-0501 | Marketplace Protocol Overview | Proposed |
| RFC-0502 | Package Format and Manifest Spec | Proposed |
| RFC-0503 | Version Resolution Mechanics | Proposed |
| RFC-0504 | Cryptographic Package Signatures | Proposed |

### Knowledge Management

| RFC | Title | Status |
|---|---|---|
| RFC-0601 | Knowledge Pack Protocol Overview | Proposed |
| RFC-0602 | Vector and Semantic Search Indexing | Proposed |
| RFC-0603 | Search Abstraction Layers | Proposed |
| RFC-0604 | Knowledge Pack Package Format | Proposed |

### Workspace and Project

| RFC | Title | Status |
|---|---|---|
| RFC-0701 | Project Package Format | Proposed |
| RFC-0702 | Workspace Boundary and Scope | Proposed |
| RFC-0703 | Hierarchical Configuration Engine | Proposed |

---

## Level 4: Common Models

Cross-cutting shared models that all subsystems MUST reference. These eliminate duplication.

| RFC | Title | Depends On | Referenced By |
|---|---|---|---|
| RFC-1001 | Event Model | RFC-0005 | All subsystems |
| RFC-1002 | State Model | RFC-0006 | All subsystems |
| RFC-1003 | Capability Model | RFC-0012 | All subsystems |
| RFC-1004 | Contract Model | RFC-0013 | All subsystems |
| RFC-1005 | Manifest Model | RFC-0010 | All subsystems |
| RFC-1006 | Error Model | RFC-0011 | All subsystems |

---

## Contracts Layer

Cross-cutting contracts that define interfaces between all components.

| Contract | Path | Purpose |
|---|---|---|
| Service Contracts | [RFC-0013](specs/runtime/RFC-0013-runtime-contracts.md) | Service interface signatures |
| IPC Contracts | [RFC-0007](specs/runtime/RFC-0007-runtime-ipc.md) | Inter-process message formats |
| Event Contracts | [RFC-0005](specs/runtime/RFC-0005-runtime-eventbus.md) | Event payload schemas |
| Error Contracts | [RFC-0011](specs/runtime/RFC-0011-runtime-errors.md) | Error code registry |
| Capability Contracts | [RFC-0012](specs/runtime/RFC-0012-runtime-capability.md) | Capability status maps |

---

## Implementation Layer

Code that implements the specifications. Specifications have higher priority than implementation.

`
specs/          ← Specifications (authoritative)
    runtime/    ← Runtime RFCs
    ipc/        ← IPC RFCs
    plugin/     ← Plugin RFCs
    workflow/   ← Workflow RFCs
    storage/    ← Storage RFCs
    common/     ← Shared models
docs/adr/       ← Architecture Decision Records
src/            ← Implementation code
`

**Rule**: Implementation MUST conform to specifications. When in conflict, the specification takes precedence.

---

## Reading Order for New Contributors

1. **Governance** (Level 1): Read the Constitution, Architecture Rules, and RFC Index.
2. **Common Models** (Level 4): Read RFC-1001 through RFC-1006 first — these define shared concepts.
3. **Runtime** (Level 2): Read RFC-0001 through RFC-0014 in order.
4. **Subsystems** (Level 3): Read the subsystem RFCs relevant to your work, in RFC number order.
5. **Contracts**: Read the contracts layer for interface signatures.
6. **Implementation**: Read the code that implements your area.

---

## Governance

- **Atlas Specification Committee**: Owns all RFCs in specs/ and governance documents.
- **Runtime Architecture Board**: Owns specs/runtime/.
- **Subsystem Teams**: Own their respective specs/*/ directories.
- **Change Process**: All changes to Frozen RFCs require ADR submission and Committee approval.
- **Conflict Resolution**: Conflicts between RFCs are resolved through the ADR process per RFC_CHANGE_POLICY.md section 8.
