# Atlas Layer Model

> **Purpose**: Defines the 7-layer dependency hierarchy for all Atlas specifications with strict dependency rules.  
> **Applies to**: All RFCs and specification artifacts under specs/.  
> **Owner**: Atlas Specification Committee  
> **Last Updated**: 2026-07-02  
> **Related**: [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md), [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md), [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md)  

---

## Layering Principle

Atlas specifications are organized into **7 strict layers**. Each layer provides services to the layer above and depends only on layers below it.

**Golden Rule**: A specification in Layer N may ONLY reference specifications in Layer N or below.  
**Forbidden Rule**: A specification in Layer N may NEVER reference specifications in Layer N+1 or above.

---

## Layer 0: Governance

**Scope**: Rules for creating, reviewing, and evolving specifications. This layer governs itself and all other layers.

| Document | Purpose |
|---|---|
| [RFC_TEMPLATE.md](RFC_TEMPLATE.md) | Standard RFC structure |
| [RFC_STYLE_GUIDE.md](RFC_STYLE_GUIDE.md) | Writing conventions |
| [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md) | Modification procedures |
| [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md) | Version numbering |
| [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md) | Quality gate |
| [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) | Lifecycle, voting, review authority |
| [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md) | How to modify any spec artifact |
| [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md) | 10 shared principles |
| [glossary.md](glossary.md) | Authoritative terminology |

**Dependencies**: None (self-governing)  
**Depended on by**: ALL layers

---

## Layer 1: Common Models

**Scope**: Cross-cutting shared abstractions referenced by ALL subsystems.

| RFC | Title | File |
|---|---|---|
| RFC-1001 | Event Model | specs/common/RFC-1001-event-model.md |
| RFC-1002 | State Model | specs/common/RFC-1002-state-model.md |
| RFC-1003 | Capability Model | specs/common/RFC-1003-capability-model.md |
| RFC-1004 | Contract Model | specs/common/RFC-1004-contract-model.md |
| RFC-1005 | Manifest Model | specs/common/RFC-1005-manifest-model.md |
| RFC-1006 | Error Model | specs/common/RFC-1006-error-model.md |

**Dependencies**: Layer 0 (Governance), Layer 2 (Runtime — for wrapping Runtime concepts)  
**Depended on by**: ALL layers above

**Rules**:
- These are the ONLY specifications that may reference Runtime RFCs by number (RFC-0001–RFC-0014).
- No other layer may define its own event, state, capability, contract, manifest, or error model.
- All subsystem RFCs MUST reference these common models instead of defining domain-specific equivalents.

---

## Layer 2: Runtime

**Scope**: Core platform services — the foundation upon which all other layers are built.

| RFC | Title | File |
|---|---|---|
| RFC-0001 | Runtime Overview | specs/runtime/RFC-0001-runtime-overview.md |
| RFC-0002 | Runtime Lifecycle | specs/runtime/RFC-0002-runtime-lifecycle.md |
| RFC-0003 | Runtime Service Model | specs/runtime/RFC-0003-runtime-service-model.md |
| RFC-0004 | Runtime Scheduler | specs/runtime/RFC-0004-runtime-scheduler.md |
| RFC-0005 | Runtime Event Bus | specs/runtime/RFC-0005-runtime-eventbus.md |
| RFC-0006 | Runtime State Management | specs/runtime/RFC-0006-runtime-state.md |
| RFC-0007 | Runtime IPC Architecture | specs/runtime/RFC-0007-runtime-ipc.md |
| RFC-0008 | Runtime Plugin Host | specs/runtime/RFC-0008-runtime-plugin.md |
| RFC-0009 | Runtime Resource Management | specs/runtime/RFC-0009-runtime-resource.md |
| RFC-0010 | Runtime Manifest Specification | specs/runtime/RFC-0010-runtime-manifest.md |
| RFC-0011 | Runtime Error Taxonomy | specs/runtime/RFC-0011-runtime-errors.md |
| RFC-0012 | Runtime Capability Registry | specs/runtime/RFC-0012-runtime-capability.md |
| RFC-0013 | Runtime Contracts | specs/runtime/RFC-0013-runtime-contracts.md |
| RFC-0014 | Runtime Reference Architecture | specs/runtime/RFC-0014-runtime-reference-architecture.md |

**Dependencies**: Layer 0 (Governance), Layer 1 (Common Models — for wrapping Runtime concepts)  
**Depended on by**: ALL layers above

**Rules**:
- Runtime is **Frozen** — no new RFCs may be added without Core Architecture Group approval.
- Runtime may only reference Common Models (Layer 1) for shared abstractions.
- Runtime defines the service lifecycle that ALL upper layers must conform to.

---

## Layer 3: Infrastructure

**Scope**: Communication and persistence. These two domains are peers within the layer.

### IPC (Inter-Process Communication)

| RFC | Title | File |
|---|---|---|
| RFC-0101 | IPC Overview | specs/ipc/RFC-0101-ipc-overview.md |
| RFC-0102 | IPC Message Model | specs/ipc/RFC-0102-ipc-message-model.md |
| RFC-0103 | IPC Transport | specs/ipc/RFC-0103-ipc-transport.md |
| RFC-0104 | IPC Routing | specs/ipc/RFC-0104-ipc-routing.md |
| RFC-0105 | IPC Channel | specs/ipc/RFC-0105-ipc-channel.md |
| RFC-0106 | IPC Serialization | specs/ipc/RFC-0106-ipc-serialization.md |
| RFC-0107 | IPC Security | specs/ipc/RFC-0107-ipc-security.md |
| RFC-0108 | IPC Reliability | specs/ipc/RFC-0108-ipc-reliability.md |
| RFC-0109 | IPC Lifecycle | specs/ipc/RFC-0109-ipc-lifecycle.md |
| RFC-0110 | IPC Observability | specs/ipc/RFC-0110-ipc-observability.md |
| RFC-0111 | IPC Error Model | specs/ipc/RFC-0111-ipc-error-model.md |
| RFC-0112 | IPC Extension | specs/ipc/RFC-0112-ipc-extension.md |

### Storage

| RFC | Title | File |
|---|---|---|
| RFC-0401 | Storage Overview | specs/storage/RFC-0401-storage-overview.md |
| RFC-0402 | Storage Architecture | specs/storage/RFC-0402-storage-architecture.md |
| RFC-0403 | Storage Provider | specs/storage/RFC-0403-storage-provider.md |
| RFC-0404 | Storage Lifecycle | specs/storage/RFC-0404-storage-lifecycle.md |
| RFC-0405 | Storage Schema | specs/storage/RFC-0405-storage-schema.md |
| RFC-0406 | Storage Transactions | specs/storage/RFC-0406-storage-transactions.md |
| RFC-0407 | Storage Versioning | specs/storage/RFC-0407-storage-versioning.md |
| RFC-0408 | Storage Migration | specs/storage/RFC-0408-storage-migration.md |
| RFC-0409 | Storage Security | specs/storage/RFC-0409-storage-security.md |
| RFC-0410 | Storage Cache | specs/storage/RFC-0410-storage-cache.md |
| RFC-0411 | Storage Backup | specs/storage/RFC-0411-storage-backup.md |
| RFC-0412 | Storage Recovery | specs/storage/RFC-0412-storage-recovery.md |
| RFC-0413 | Storage Events | specs/storage/RFC-0413-storage-events.md |
| RFC-0414 | Storage Observability | specs/storage/RFC-0414-storage-observability.md |
| RFC-0415 | Storage Performance | specs/storage/RFC-0415-storage-performance.md |
| RFC-0416 | Storage Consistency | specs/storage/RFC-0416-storage-consistency.md |
| RFC-0417 | Storage Locking | specs/storage/RFC-0417-storage-locking.md |
| RFC-0418 | Storage Replication | specs/storage/RFC-0418-storage-replication.md |
| RFC-0419 | Storage Extension | specs/storage/RFC-0419-storage-extension.md |
| RFC-0420 | Storage Compliance | specs/storage/RFC-0420-storage-compliance.md |
| RFC-0421 | Storage Domains | specs/storage/RFC-0421-storage-domains.md |
| RFC-0422 | Storage Namespace | specs/storage/RFC-0422-storage-namespace.md |
| RFC-0423 | Storage Resource Model | specs/storage/RFC-0423-storage-resource-model.md |
| RFC-0424 | Storage Quota | specs/storage/RFC-0424-storage-quota.md |
| RFC-0425 | Storage Capability Discovery | specs/storage/RFC-0425-storage-capability-discovery.md |

**Dependencies**: Layer 0 (Governance), Layer 1 (Common Models), Layer 2 (Runtime)  
**Depended on by**: Layers 4–6

**Rules**:
- IPC and Storage are **peers within Layer 3**. Neither may depend on the other.
- IPC defines message transport; Storage defines persistence. Both are infrastructure concerns.
- Catalog files in both domains (e.g., ipc/catalog/messages.md, storage/catalog/providers.md) are normative extensions.

---

## Layer 4: Extension & Orchestration

**Scope**: Platform extension framework and task orchestration. These are application-level domains.

### Plugin

| RFC | Title | File |
|---|---|---|
| RFC-0201 | Plugin Overview | specs/plugin/RFC-0201-plugin-overview.md |
| RFC-0202 | Plugin Manifest | specs/plugin/RFC-0202-plugin-manifest.md |
| RFC-0203 | Plugin Lifecycle | specs/plugin/RFC-0203-plugin-lifecycle.md |
| RFC-0204 | Plugin Loader | specs/plugin/RFC-0204-plugin-loader.md |
| RFC-0205 | Plugin Registry | specs/plugin/RFC-0205-plugin-registry.md |
| RFC-0206 | Plugin Capability | specs/plugin/RFC-0206-plugin-capability.md |
| RFC-0207 | Plugin Security | specs/plugin/RFC-0207-plugin-security.md |
| RFC-0208 | Plugin Sandbox | specs/plugin/RFC-0208-plugin-sandbox.md |
| RFC-0209 | Plugin API | specs/plugin/RFC-0209-plugin-api.md |
| RFC-0210 | Plugin Events | specs/plugin/RFC-0210-plugin-events.md |
| RFC-0211 | Plugin Dependency | specs/plugin/RFC-0211-plugin-dependency.md |
| RFC-0212 | Plugin Versioning | specs/plugin/RFC-0212-plugin-versioning.md |
| RFC-0213 | Plugin Marketplace | specs/plugin/RFC-0213-plugin-marketplace.md |
| RFC-0214 | Plugin Extension Model | specs/plugin/RFC-0214-plugin-extension-model.md |
| RFC-0215 | Plugin Service Model | specs/plugin/RFC-0215-plugin-service-model.md |
| RFC-0216 | Plugin Discovery | specs/plugin/RFC-0216-plugin-discovery.md |
| RFC-0217 | Plugin Packaging | specs/plugin/RFC-0217-plugin-packaging.md |
| RFC-0218 | Plugin Compatibility | specs/plugin/RFC-0218-plugin-compatibility.md |
| RFC-0219 | Plugin Testing | specs/plugin/RFC-0219-plugin-testing.md |
| RFC-0220 | Plugin IPC | specs/plugin/RFC-0220-plugin-ipc.md |
| RFC-0221 | Plugin Resources | specs/plugin/RFC-0221-plugin-resources.md |
| RFC-0222 | Plugin Storage | specs/plugin/RFC-0222-plugin-storage.md |
| RFC-0223 | Plugin Configuration | specs/plugin/RFC-0223-plugin-configuration.md |
| RFC-0224 | Plugin Diagnostics | specs/plugin/RFC-0224-plugin-diagnostics.md |
| RFC-0225 | Plugin Hot Reload | specs/plugin/RFC-0225-plugin-hot-reload.md |
| RFC-0226 | Plugin Migration | specs/plugin/RFC-0226-plugin-migration.md |
| RFC-0227 | Plugin Service Discovery | specs/plugin/RFC-0227-plugin-service-discovery.md |
| RFC-0228 | Plugin Dependency Resolution | specs/plugin/RFC-0228-plugin-dependency-resolution.md |
| RFC-0229 | Plugin Telemetry | specs/plugin/RFC-0229-plugin-telemetry.md |
| RFC-0230 | Plugin Signature | specs/plugin/RFC-0230-plugin-signature.md |

### Workflow

| RFC | Title | File |
|---|---|---|
| RFC-0301 | Workflow Overview | specs/workflow/RFC-0301-workflow-overview.md |
| RFC-0302 | Workflow Language | specs/workflow/RFC-0302-workflow-language.md |
| RFC-0303 | Workflow Execution | specs/workflow/RFC-0303-workflow-execution.md |
| RFC-0304 | Workflow Runtime | specs/workflow/RFC-0304-workflow-runtime.md |
| RFC-0305 | Workflow Lifecycle | specs/workflow/RFC-0305-workflow-lifecycle.md |
| RFC-0306 | Workflow State | specs/workflow/RFC-0306-workflow-state.md |
| RFC-0307 | Workflow Context | specs/workflow/RFC-0307-workflow-context.md |
| RFC-0308 | Workflow Events | specs/workflow/RFC-0308-workflow-events.md |
| RFC-0309 | Workflow Actions | specs/workflow/RFC-0309-workflow-actions.md |
| RFC-0310 | Workflow Conditions | specs/workflow/RFC-0310-workflow-conditions.md |
| RFC-0311 | Workflow Triggers | specs/workflow/RFC-0311-workflow-triggers.md |
| RFC-0312 | Workflow Scheduler | specs/workflow/RFC-0312-workflow-scheduler.md |
| RFC-0313 | Workflow Parallelism | specs/workflow/RFC-0313-workflow-parallelism.md |
| RFC-0314 | Workflow Error Handling | specs/workflow/RFC-0314-workflow-error-handling.md |
| RFC-0315 | Workflow Recovery | specs/workflow/RFC-0315-workflow-recovery.md |
| RFC-0316 | Workflow Debugging | specs/workflow/RFC-0316-workflow-debugging.md |
| RFC-0317 | Workflow Validation | specs/workflow/RFC-0317-workflow-validation.md |
| RFC-0318 | Workflow Versioning | specs/workflow/RFC-0318-workflow-versioning.md |
| RFC-0319 | Workflow Security | specs/workflow/RFC-0319-workflow-security.md |
| RFC-0320 | Workflow Performance | specs/workflow/RFC-0320-workflow-performance.md |
| RFC-0321 | Workflow Observability | specs/workflow/RFC-0321-workflow-observability.md |
| RFC-0322 | Workflow Extension | specs/workflow/RFC-0322-workflow-extension.md |
| RFC-0323 | Workflow Plugin Integration | specs/workflow/RFC-0323-workflow-plugin-integration.md |
| RFC-0324 | Workflow Storage | specs/workflow/RFC-0324-workflow-storage.md |
| RFC-0325 | Workflow AI | specs/workflow/RFC-0325-workflow-ai.md |
| RFC-0326 | Workflow Vision | specs/workflow/RFC-0326-workflow-vision.md |
| RFC-0327 | Workflow IPC | specs/workflow/RFC-0327-workflow-ipc.md |
| RFC-0328 | Workflow Serialization | specs/workflow/RFC-0328-workflow-serialization.md |
| RFC-0329 | Workflow Compatibility | specs/workflow/RFC-0329-workflow-compatibility.md |
| RFC-0330 | Workflow Compliance | specs/workflow/RFC-0330-workflow-compliance.md |
| RFC-0331 | Workflow Testing | specs/workflow/RFC-0331-workflow-testing.md |
| RFC-0332 | Workflow Migration | specs/workflow/RFC-0332-workflow-migration.md |
| RFC-0333 | Workflow Extension SDK | specs/workflow/RFC-0333-workflow-sdk.md |

**Dependencies**: Layer 0 (Governance), Layer 1 (Common Models), Layer 2 (Runtime), Layer 3 (IPC, Storage)  
**Depended on by**: Layers 5–6

**Rules**:
- Plugin and Workflow are **peers within Layer 4**. Neither may depend on the other directly.
- Cross-domain integration RFCs (e.g., RFC-0220 plugin-ipc, RFC-0323 workflow-plugin-integration) require joint review per [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md).
- Plugin defines HOW the platform extends; Workflow defines HOW tasks are orchestrated. Both are application concerns.

---

## Layer 5: Intelligence

**Scope**: Perception, cognition, and data understanding. These domains consume infrastructure from Layers 0–4.

| Domain | RFC Range | Status |
|---|---|---|
| Vision | (reserved, no RFCs yet) | Placeholder |
| AI | (reserved, no RFCs yet) | Placeholder |
| Knowledge | RFC-0601 – RFC-0608 | Deferred |

**Dependencies**: Layer 0–4 (Governance, Common, Runtime, IPC, Plugin, Workflow, Storage)

**Rules**:
- Vision, AI, and Knowledge are **peers within Layer 5**.
- Knowledge may depend on Storage (Layer 3) for vector indexes.
- AI may depend on Knowledge (Layer 5) for semantic search.
- Vision may depend on Storage (Layer 3) for image cache.
- None may depend on Layer 6 (UI, Marketplace, Project).

---

## Layer 6: Presentation & Distribution

**Scope**: User interface, package distribution, and workspace scoping. The highest layer — consumer-facing concerns.

| Domain | RFC Range | Status |
|---|---|---|
| UI | (reserved, no RFCs yet) | Placeholder |
| Marketplace | RFC-0501 – RFC-0508 | Deferred |
| Project | RFC-0701 – RFC-0708 | Deferred |

**Dependencies**: Layers 0–5 (everything above)

**Rules**:
- UI is the **terminal layer** — nothing depends on UI.
- Marketplace distributes packages; Project scopes workspaces.
- Neither UI, Marketplace, nor Project may introduce new shared models (that belongs to Layer 1).

---

## Dependency Enforcement

### Allowed Dependencies

A specification in Layer N may reference specifications in:
- Layer 0 (Governance) — always allowed
- Layer N (peer specifications within the same layer) — allowed with peer review
- Layers 0 through N-1 (all layers below) — always allowed

### Forbidden Dependencies

| From Layer | Cannot Depend On | Reason |
|---|---|---|
| Layer 0 | Anything above | Governance is self-contained |
| Layer 1 (Common) | Layers 3–6 | Common models must not depend on domain implementations |
| Layer 2 (Runtime) | Layers 3–6 | Foundation must not depend on extensions |
| Layer 3 (IPC/Storage) | Layers 4–6 | Infrastructure must not depend on application logic |
| Layer 4 (Plugin/Workflow) | Layers 5–6 | Application layer must not depend on intelligence or presentation |
| Layer 5 (Vision/AI/Knowledge) | Layer 6 | Intelligence must not depend on presentation |
| Layer 6 (UI/Marketplace/Project) | *(nothing above)* | Terminal layer — nothing exists above |

### Peer Dependencies (Within Same Layer)

| Layer | Peers | Can They Reference Each Other? |
|---|---|---|
| Layer 3 | IPC ↔ Storage | No — they are independent infrastructure |
| Layer 4 | Plugin ↔ Workflow | No — cross-domain RFCs need joint review |
| Layer 5 | Vision ↔ AI ↔ Knowledge | Partial — Knowledge↔AI and Knowledge↔Storage are allowed |
| Layer 6 | UI ↔ Marketplace ↔ Project | No — each is independent |

---

## Visual Summary

`
Layer 6  ┃  UI · Marketplace · Project          ← Presentation & Distribution
─────────╫──────────────────────────────────────
Layer 5  ┃  Vision · AI · Knowledge              ← Intelligence
─────────╫──────────────────────────────────────
Layer 4  ┃  Plugin · Workflow                    ← Extension & Orchestration
─────────╫──────────────────────────────────────
Layer 3  ┃  IPC · Storage                        ← Infrastructure
─────────╫──────────────────────────────────────
Layer 2  ┃  Runtime                              ← Core Platform
─────────╫──────────────────────────────────────
Layer 1  ┃  Common Models                        ← Shared Abstractions
─────────╫──────────────────────────────────────
Layer 0  ┃  Governance                           ← Specification Rules
`

*Arrows flow upward. Lower layers cannot reference upper layers.*

---

*This document is part of the Atlas Specification hierarchy. For the RFC tree, see [RFC_MAP.md](RFC_MAP.md). For dependency rules, see [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For principles, see [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md).*

