# Atlas Architecture Matrix

> **Purpose**: Domain ownership, dependency, extension, and contract matrix for Atlas specifications.  
> **Inspired by**: Kubernetes component matrix, VSCode extension API matrix, LLVM subsystem matrix.  
> **Created**: 2026-07-02  
> **Owner**: Atlas Specification Committee  

---

## Domain Matrix

| Domain | Owns | Depends On | Extension Points | Contracts | RFC Range | Layer | Status |
|---|---|---|---|---|---|---|---|
| **Runtime** | Core lifecycle, scheduler, event bus, state mgmt, resources, manifest, capabilities, errors, contracts | *(Foundation — nothing below)* | Plugin Host (RFC-0008), Service Model (RFC-0003), Resource Manager (RFC-0009) | Contracts (RFC-0013), Manifest (RFC-0010), Error Taxonomy (RFC-0011) | RFC-0001 – RFC-0014 | 2 | Frozen |
| **Common** | Cross-cutting shared models | Runtime (RFC-0005, RFC-0006, RFC-0010–RFC-0013) | None (models are consumed, not extended) | Event Model (RFC-1001), State Model (RFC-1002), Capability Model (RFC-1003), Contract Model (RFC-1004), Manifest Model (RFC-1005), Error Model (RFC-1006) | RFC-1001 – RFC-1006 | 1 | Draft |
| **IPC** | Transport abstraction, channels, serialization, routing, security, reliability, observability | Runtime (RFC-0007), Common (RFC-1001, RFC-1006) | Extension via RFC-0112, Transport Abstraction (RFC-0104), Channel Types (RFC-0105) | Message Model (RFC-0102), Serialization Contract (RFC-0106), Security Levels (catalog) | RFC-0101 – RFC-0112 | 3 | Active |
| **Plugin** | Extension framework, loader, registry, lifecycle, sandbox, API, discovery, packaging | Runtime, Common, IPC, Storage | Extension Model (RFC-0214), Service Model (RFC-0215), Capability (RFC-0206) | Manifest (RFC-0202), API (RFC-0209), Packaging (RFC-0217), Signature (RFC-0230) | RFC-0201 – RFC-0230 | 4 | Proposed |
| **Workflow** | Orchestration engine, language, execution, actions, triggers, conditions, scheduling | Runtime, Common, IPC, Plugin, Storage | Extension Points (RFC-0322), SDK (RFC-0333), Action Types (catalog) | Language (RFC-0302), Execution (RFC-0303), Manifest (RFC-0301), Serialization (RFC-0328) | RFC-0301 – RFC-0333 | 4 | Proposed |
| **Storage** | Persistence abstraction, providers, transactions, schema, versioning, backup, recovery | Runtime, Common, IPC, Plugin | Provider Interface (RFC-0403), Extension Points (RFC-0419), Domains (RFC-0421) | Provider Contract (RFC-0403), Transaction Contract (RFC-0406), Schema (RFC-0405) | RFC-0401 – RFC-0425 | 3 | Proposed |
| **Marketplace** | Package distribution, version resolution, cryptographic signatures | Runtime, Common, IPC, Plugin, Storage, Workflow | TBD (deferred) | Package Format (RFC-0502), Version Protocol (RFC-0503), Signatures (RFC-0504) | RFC-0501 – RFC-0508 | 6 | Deferred |
| **Knowledge** | Semantic search, vector indexing, knowledge packs | Runtime, Common, IPC, Plugin, Storage, Workflow | TBD (deferred) | Pack Protocol (RFC-0601), Package Format (RFC-0604) | RFC-0601 – RFC-0608 | 5 | Deferred |
| **Vision** | Camera pipeline, OCR, image processing | Runtime, Common, IPC, Plugin, Storage, Workflow | TBD (placeholder) | TBD | RFC-0801 – RFC-0804 | 5 | Placeholder |
| **AI** | Language model routing, prompt management, context windows, tool calling | Runtime, Common, IPC, Plugin, Storage, Workflow, Knowledge, Vision | TBD (placeholder) | TBD | RFC-0901 – RFC-0904 | 5 | Placeholder |
| **UI** | User interface, themes, accessibility, components | Everything above | TBD (placeholder) | TBD | RFC-0810 – RFC-0812 | 6 | Placeholder |
| **Project** | Workspace boundaries, project packages, hierarchical configuration | Runtime, Common, IPC, Plugin, Storage, Workflow | TBD (deferred) | Project Format (RFC-0701), Config Engine (RFC-0703) | RFC-0701 – RFC-0708 | 6 | Deferred |

---

## Dependency Direction Matrix

X = direct dependency. Arrows show allowed dependency flow.

| Depends On → | Runtime | Common | IPC | Plugin | Workflow | Storage | Marketplace | Knowledge | Vision | AI | UI | Project |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Runtime** | — | | | | | | | | | | | |
| **Common** | X | — | | | | | | | | | | |
| **IPC** | X | X | — | | | | | | | | | |
| **Plugin** | X | X | X | — | | X | | | | | | |
| **Workflow** | X | X | X | X | — | X | | | | | | |
| **Storage** | X | X | X | X | | — | | | | | | |
| **Marketplace** | X | X | X | X | X | X | — | | | | | |
| **Knowledge** | X | X | X | X | X | X | | — | | | | |
| **Vision** | X | X | X | X | X | X | | | — | | | |
| **AI** | X | X | X | X | X | X | | X | X | — | | |
| **UI** | X | X | X | X | X | X | X | X | X | X | — | X |
| **Project** | X | X | X | X | X | X | | | | | | — |

---

## Extension Point Matrix

Which domains expose extension points, and what kind.

| Domain | Extension Type | Mechanism | Governed By |
|---|---|---|---|
| Runtime | Plugin Host | RFC-0008 | Runtime Arch Board |
| IPC | Transport Abstraction | RFC-0104, RFC-0112 | IPC Sub-team |
| IPC | Channel Types | RFC-0105, catalog/channels.md | IPC Sub-team |
| Plugin | Service Model | RFC-0215, RFC-0214 | Plugin Sub-team |
| Plugin | Capability | RFC-0206, RFC-0205 | Plugin Sub-team |
| Plugin | Discovery | RFC-0216 | Plugin Sub-team |
| Plugin | Extension Model | RFC-0214 | Plugin Sub-team |
| Workflow | Action Types | RFC-0309, catalog/workflow-action-types.md | Workflow Team |
| Workflow | Trigger Types | RFC-0311, catalog/workflow-trigger-types.md | Workflow Team |
| Workflow | Condition Types | RFC-0310, catalog/workflow-condition-types.md | Workflow Team |
| Workflow | Extension Points | RFC-0322, catalog/workflow-extension-points.md | Workflow Team |
| Workflow | Node Types | catalog/workflow-node-types.md | Workflow Team |
| Storage | Provider Interface | RFC-0403, catalog/storage-providers.md | Storage Team |
| Storage | Extension Points | RFC-0419, catalog/storage-extension-points.md | Storage Team |
| Marketplace | Package Format | RFC-0502 (deferred) | Marketplace Team |
| Knowledge | Pack Protocol | RFC-0601 (deferred) | Knowledge Team |

---

## Contract Matrix

Which domains define contracts, and what they contract.

| Contract Domain | Defined By | Consumed By | Format |
|---|---|---|---|
| Runtime Contracts | RFC-0013 | All domains | Interface definitions |
| IPC Message Contract | RFC-0102, catalog/messages.md | All domains with IPC | JSON schema + type IDs |
| IPC Channel Contract | RFC-0105, catalog/channels.md | All domains with IPC | Channel IDs |
| IPC Security Contract | RFC-0107, catalog/security-levels.md | All domains | Security levels L0–L4 |
| Plugin Manifest Contract | RFC-0202, RFC-0010 | Runtime, Plugin Loader | JSON schema |
| Plugin API Contract | RFC-0209 | Plugin authors | Interface definitions |
| Plugin Signature Contract | RFC-0230 | Runtime, Plugin Sandbox | Cryptographic |
| Workflow Language Contract | RFC-0302 | Workflow Engine | DSL schema |
| Workflow Action Contract | RFC-0309, catalog/workflow-actions.md | Workflow Engine | Action type IDs |
| Storage Provider Contract | RFC-0403 | Storage Layer | Interface definitions |
| Storage Transaction Contract | RFC-0406 | Storage Layer | ACID guarantees |
| Common Event Contract | RFC-1001 | All domains | Event envelope schema |
| Common State Contract | RFC-1002 | All domains | State scope model |
| Common Capability Contract | RFC-1003 | All domains | Capability declaration format |
| Common Error Contract | RFC-1006 | All domains | Error classification |

---

## RFC Count Summary

| Layer | Domain | RFC Count | Catalog Count | Total Files |
|---|---|---|---|---|
| 1 | Common | 6 | 0 | 7 |
| 2 | Runtime | 14 | 2 | 16 |
| 3 | IPC | 12 | 6 | 18 |
| 3 | Storage | 25 | 11 | 36 |
| 4 | Plugin | 30 | 4 | 34 |
| 4 | Workflow | 33 | 34 | 67 |
| 5 | Knowledge (deferred) | 0 | 0 | 1 |
| 5 | Vision (placeholder) | 0 | 0 | 1 |
| 5 | AI (placeholder) | 0 | 0 | 0 |
| 6 | Marketplace (deferred) | 0 | 0 | 1 |
| 6 | UI (placeholder) | 0 | 0 | 1 |
| 6 | Project (deferred) | 0 | 0 | 1 |
| Meta | Governance | 5 | 1 | 6 |
| **Total** | | **120** | **58** | **~180+** |

---

## Layer Compliance Rules

| Rule | Description | Enforced By |
|---|---|---|
| L1 | Common Models (Layer 1) may reference Runtime but nothing else | Spec Committee |
| L2 | Runtime is foundation — nothing may depend on upper layers | Spec Committee |
| L3 | IPC and Storage are peers — neither depends on the other | Spec Committee |
| L4 | Plugin and Workflow are peers — cross-domain RFCs need joint review | Spec Committee |
| L5 | Intelligence (Vision/AI/Knowledge) may not depend on UI | Spec Committee |
| L6 | UI is terminal — nothing depends on UI | Spec Committee |
| L7 | Catalog files are normative extensions of their domain RFCs | Domain owner |
| L8 | New RFC ranges require Spec Committee activation | Spec Committee |

---

*This document is part of the Atlas Specification hierarchy. For dependency rules, see [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md). For layers, see [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) and [LAYER_MODEL.md](LAYER_MODEL.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md).*


