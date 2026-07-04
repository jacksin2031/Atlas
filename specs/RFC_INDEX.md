# Atlas Specification RFC Index

> **Master Registry** — All Atlas specifications are registered here.  
> ****Last Updated**: 2026-07-04  
> **Owner**: Atlas Specification Committee  `n> **Related Policies**: [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md), [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md), [RFC_STYLE_GUIDE.md](RFC_STYLE_GUIDE.md), [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md)  

---

## Legend

| Symbol | Meaning |
|---|---|
| **Frozen** | Architecture complete. Only bug fixes allowed. |
| **Active** | Implemented and deployed in current release. |
| **Accepted** | Approved, ready for implementation. |
| **Review** | Under active review by architecture board. |
| **Draft** | Under active design and community review. |
| **Proposed** | Initial proposal, not yet reviewed. |
| **Superseded** | Replaced by a newer specification. |
| **Deprecated** | Planned for removal in future versions. |

---

## Runtime Specifications (RFC-0001 through RFC-0014)

### Core Runtime

| RFC ID | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| [RFC-0001](specs/runtime/RFC-0001-runtime-overview.md) | Runtime Overview | Frozen | 1.0.0 | Foundation | — | Runtime Arch Board |
| [RFC-0002](specs/runtime/RFC-0002-runtime-lifecycle.md) | Runtime Lifecycle | Frozen | 1.1.0 | Core | RFC-0001 | Runtime Arch Board |
| [RFC-0003](specs/runtime/RFC-0003-runtime-service-model.md) | Runtime Service Model | Frozen | 1.1.0 | Core | RFC-0001, RFC-0002 | Runtime Arch Board |
| [RFC-0004](specs/runtime/RFC-0004-runtime-scheduler.md) | Runtime Scheduler | Frozen | 1.1.0 | Execution | RFC-0001–RFC-0003, RFC-0005 | Runtime Arch Board |
| [RFC-0005](specs/runtime/RFC-0005-runtime-eventbus.md) | Runtime Event Bus | Frozen | 1.1.0 | Execution | RFC-0001–RFC-0003 | Runtime Arch Board |
| [RFC-0006](specs/runtime/RFC-0006-runtime-state.md) | Runtime State Management | Frozen | 1.1.0 | Execution | RFC-0001–RFC-0005 | Runtime Arch Board |
| [RFC-0007](specs/runtime/RFC-0007-runtime-ipc.md) | Runtime IPC Architecture | Frozen | 1.1.0 | Communication | RFC-0001, RFC-0002, RFC-0003, RFC-0005 | Runtime Arch Board |
| [RFC-0008](specs/runtime/RFC-0008-runtime-plugin.md) | Runtime Plugin Host | Frozen | 1.1.0 | Extensibility | RFC-0001–RFC-0007, RFC-0009 | Runtime Arch Board |
| [RFC-0009](specs/runtime/RFC-0009-runtime-resource.md) | Runtime Resource Management | Frozen | 1.1.0 | Execution | RFC-0001–RFC-0006 | Runtime Arch Board |
| [RFC-0010](specs/runtime/RFC-0010-runtime-manifest.md) | Runtime Manifest Specification | Frozen | 1.1.0 | Metadata | RFC-0001, RFC-0002, RFC-0003, RFC-0005 | Runtime Arch Board |
| [RFC-0011](specs/runtime/RFC-0011-runtime-errors.md) | Runtime Error Taxonomy | Frozen | 1.0.0 | Metadata | RFC-0001, RFC-0002 | Runtime Arch Board |
| [RFC-0012](specs/runtime/RFC-0012-runtime-capability.md) | Runtime Capability Registry | Frozen | 1.0.0 | Metadata | RFC-0001, RFC-0002, RFC-0010 | Runtime Arch Board |
| [RFC-0013](specs/runtime/RFC-0013-runtime-contracts.md) | Runtime Contracts | Frozen | 1.0.0 | Contracts | RFC-0001–RFC-0012 | Runtime Arch Board |
| [RFC-0014](specs/runtime/RFC-0014-runtime-reference-architecture.md) | Runtime Reference Architecture | Frozen | 1.0.0 | Reference | RFC-0001–RFC-0013 | Runtime Arch Board |

### Runtime Summary

- **Total RFCs**: 14
- **Total Lines**: 6,500+
- **Status**: All Frozen
- **Architecture Freeze Date**: 2026-06-30

---

# Workflow Engine Specifications (RFC-0301 through RFC-0333)

> **NEW**: Complete workflow RFC series replacing the legacy RFC-0101 through RFC-0107.

| RFC ID | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-0301 | Workflow Overview | Proposed | 1.0.0 | Core | RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-1001, RFC-1002, RFC-1003, RFC-1004, RFC-1005, RFC-1006 | Workflow Team |
| RFC-0302 | Workflow Language | Proposed | 1.0.0 | Standard | RFC-0301 | Workflow Team |
| RFC-0303 | Workflow Execution | Proposed | 1.0.0 | Execution | RFC-0301, RFC-0004, RFC-0005 | Workflow Team |
| RFC-0304 | Workflow Runtime | Proposed | 1.0.0 | Execution | RFC-0301, RFC-0002, RFC-0003 | Workflow Team |
| RFC-0305 | Workflow Lifecycle | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0006 | Workflow Team |
| RFC-0306 | Workflow State | Proposed | 1.0.0 | Standard | RFC-0301, RFC-1002 | Workflow Team |
| RFC-0307 | Workflow Context | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0306 | Workflow Team |
| RFC-0308 | Workflow Events | Proposed | 1.0.0 | Standard | RFC-0301, RFC-1001 | Workflow Team |
| RFC-0309 | Workflow Actions | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0307 | Workflow Team |
| RFC-0310 | Workflow Conditions | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0302 | Workflow Team |
| RFC-0311 | Workflow Triggers | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0312 | Workflow Team |
| RFC-0312 | Workflow Scheduler | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0004 | Workflow Team |
| RFC-0313 | Workflow Parallelism | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0312 | Workflow Team |
| RFC-0314 | Workflow Error Handling | Proposed | 1.0.0 | Standard | RFC-0301, RFC-1006 | Workflow Team |
| RFC-0315 | Workflow Recovery | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0314 | Workflow Team |
| RFC-0316 | Workflow Debugging | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0303 | Workflow Team |
| RFC-0317 | Workflow Validation | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0302 | Workflow Team |
| RFC-0318 | Workflow Versioning | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0329 | Workflow Team |
| RFC-0319 | Workflow Security | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0008 | Workflow Team |
| RFC-0320 | Workflow Performance | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0312 | Workflow Team |
| RFC-0321 | Workflow Observability | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0005 | Workflow Team |
| RFC-0322 | Workflow Extension | Proposed | 1.0.0 | Standard | RFC-0301 | Workflow Team |
| RFC-0323 | Workflow Plugin Integration | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0201+ | Workflow Team |
| RFC-0324 | Workflow Storage | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0401+ | Workflow Team |
| RFC-0325 | Workflow AI | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0301+ | Workflow Team |
| RFC-0326 | Workflow Vision | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0201+ | Workflow Team |
| RFC-0327 | Workflow IPC | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0101+ | Workflow Team |
| RFC-0328 | Workflow Serialization | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0106 | Workflow Team |
| RFC-0329 | Workflow Compatibility | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0318 | Workflow Team |



---\
| RFC-0331 | Workflow Testing | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0303, RFC-0312, RFC-0315, RFC-0316 | Workflow Team |
| RFC-0332 | Workflow Migration | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0318, RFC-0329 | Workflow Team |
| RFC-0333 | Workflow Extension SDK | Proposed | 1.0.0 | Standard | RFC-0301, RFC-0322, RFC-0323 | Workflow Team |n
## Storage System Specifications (RFC-0401 through RFC-0425)

| RFC ID | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-0401 | Storage Overview | Proposed | 0.1.0 | Core | RFC-0001, RFC-0002, RFC-0006, RFC-0009, RFC-0201, RFC-1001, RFC-1006 | Storage Team |
| RFC-0402 | Storage Architecture | Proposed | 0.1.0 | Core | RFC-0401, RFC-0001, RFC-0009 | Storage Team |
| RFC-0403 | Storage Provider | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0013 | Storage Team |
| RFC-0404 | Storage Lifecycle | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403 | Storage Team |
| RFC-0405 | Storage Schema | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403 | Storage Team |
| RFC-0406 | Storage Transactions | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403, RFC-0404 | Storage Team |
| RFC-0407 | Storage Versioning | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0405, RFC-0406 | Storage Team |
| RFC-0408 | Storage Migration | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0405, RFC-0406, RFC-0407 | Storage Team |
| RFC-0409 | Storage Security | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403, RFC-0404 | Storage Team |
| RFC-0410 | Storage Cache | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403, RFC-0404 | Storage Team |
| RFC-0411 | Storage Backup | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0404, RFC-0409 | Storage Team |
| RFC-0412 | Storage Recovery | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0411, RFC-0409 | Storage Team |
| RFC-0413 | Storage Events | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-1001 | Storage Team |
| RFC-0414 | Storage Observability | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0413 | Storage Team |
| RFC-0415 | Storage Performance | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0414 | Storage Team |
| RFC-0416 | Storage Consistency | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0406, RFC-0418 | Storage Team |
| RFC-0417 | Storage Locking | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0406, RFC-0416 | Storage Team |
| RFC-0418 | Storage Replication | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0416, RFC-0417 | Storage Team |
| RFC-0419 | Storage Extension | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403 | Storage Team |
| RFC-0420 | Storage Compliance | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0409, RFC-0414 | Storage Team 
| RFC-0421 | Storage Domains | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0421, RFC-0422 | Storage Team 
| RFC-0422 | Storage Namespace | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0421 | Storage Team 
| RFC-0423 | Storage Resource Model | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0405, RFC-0421 | Storage Team 
| RFC-0424 | Storage Quota | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0409, RFC-0421, RFC-0422 | Storage Team 
| RFC-0425 | Storage Capability Discovery | Proposed | 0.1.0 | Standard | RFC-0401, RFC-0402, RFC-0403, RFC-0425 | Storage Team |

---
## Marketplace Infrastructure (Deferred)

> **Status**: Planned. No RFC files exist yet. RFC-0501 through RFC-0508 are reserved but not authored.

 | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-0501 | Marketplace Protocol Overview | Proposed | 0.1.0 | Standard | RFC-0405, RFC-0007 | Marketplace Team |
| RFC-0502 | Package Format and Manifest Spec | Proposed | 0.1.0 | Standard | RFC-0501, RFC-0010 | Marketplace Team |
| RFC-0503 | Version Resolution Mechanics | Proposed | 0.1.0 | Standard | RFC-0501, RFC-0012 | Marketplace Team |
| RFC-0504 | Cryptographic Package Signatures | Proposed | 0.1.0 | Standard | RFC-0501, RFC-0007 | Marketplace Team |

---

## Knowledge Management (Deferred)

> **Status**: Planned. No RFC files exist yet. RFC-0601 through RFC-0608 are reserved but not authored.

 | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-0601 | Knowledge Pack Protocol Overview | Proposed | 0.1.0 | Standard | RFC-0001, RFC-0003 | Knowledge Team |
| RFC-0602 | Vector and Semantic Search Indexing | Proposed | 0.1.0 | Standard | RFC-0601, RFC-0006 | Knowledge Team |
| RFC-0603 | Search Abstraction Layers | Proposed | 0.1.0 | Standard | RFC-0601, RFC-0007 | Knowledge Team |
| RFC-0604 | Knowledge Pack Package Format | Proposed | 0.1.0 | Standard | RFC-0601, RFC-0010 | Knowledge Team |

---

## Workspace and Project (Deferred)

> **Status**: Planned. No RFC files exist yet. RFC-0701 through RFC-0708 are reserved but not authored.

 | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-0701 | Project Package Format | Proposed | 0.1.0 | Standard | RFC-0010, RFC-0009 | Project Team |
| RFC-0702 | Workspace Boundary and Scope | Proposed | 0.1.0 | Core | RFC-0001, RFC-0006 | Project Team |
| RFC-0703 | Hierarchical Configuration Engine | Proposed | 0.1.0 | Core | RFC-0702, RFC-0010 | Project Team |

---

## Common Specifications (RFC-1001 through RFC-1006)

> These shared models are referenced by ALL subsystems.

| RFC ID | Title | Status | Version | Layer | Depends On | Owner |
|---|---|---|---|---|---|---|
| RFC-1001 | Event Model | Draft | 0.1.0 | Common | RFC-0005 | Spec Committee |
| RFC-1002 | State Model | Draft | 0.1.0 | Common | RFC-0006 | Spec Committee |
| RFC-1003 | Capability Model | Draft | 0.1.0 | Common | RFC-0012 | Spec Committee |
| RFC-1004 | Contract Model | Draft | 0.1.0 | Common | RFC-0013 | Spec Committee |
| RFC-1005 | Manifest Model | Draft | 0.1.0 | Common | RFC-0010 | Spec Committee |
| RFC-1006 | Error Model | Draft | 0.1.0 | Common | RFC-0011 | Spec Committee |

---

## Dependency Graph (Runtime Core)

`mermaid
graph LR
    RFC0001["RFC-0001<br/>Overview"] --> RFC0002["RFC-0002<br/>Lifecycle"]
    RFC0001 --> RFC0003["RFC-0003<br/>Service Model"]
    RFC0002 --> RFC0003
    RFC0003 --> RFC0004["RFC-0004<br/>Scheduler"]
    RFC0003 --> RFC0005["RFC-0005<br/>Event Bus"]
    RFC0002 --> RFC0005
    RFC0004 --> RFC0006["RFC-0006<br/>State Mgmt"]
    RFC0005 --> RFC0006
    RFC0005 --> RFC0007["RFC-0007<br/>IPC"]
    RFC0007 --> RFC0008["RFC-0008<br/>Plugin Host"]
    RFC0006 --> RFC0008
    RFC0006 --> RFC0009["RFC-0009<br/>Resources"]
    RFC0008 --> RFC0009
    RFC0005 --> RFC0010["RFC-0010<br/>Manifest"]
    RFC0002 --> RFC0011["RFC-0011<br/>Errors"]
    RFC0010 --> RFC0012["RFC-0012<br/>Capabilities"]
    RFC0003 --> RFC0013["RFC-0013<br/>Contracts"]
    RFC0011 --> RFC0013
    RFC0008 --> RFC0013
    RFC0009 --> RFC0013
    RFC0001 -.-> RFC0014["RFC-0014<br/>Reference Arch"]
    RFC0002 -.-> RFC0014
    RFC0003 -.-> RFC0014
    RFC0004 -.-> RFC0014
    RFC0005 -.-> RFC0014
    RFC0006 -.-> RFC0014
    RFC0007 -.-> RFC0014
    RFC0008 -.-> RFC0014
    RFC0009 -.-> RFC0014
    RFC0010 -.-> RFC0014
    RFC0011 -.-> RFC0014
    RFC0012 -.-> RFC0014
    RFC0013 -.-> RFC0014
`

---

## Specification Statistics

| Category | Count | Frozen | Active | Draft | Proposed |
|---|---|---|---|---|---|
| Runtime | 14 | 14 | 0 | 0 | 0 |
| Workflow | 33 | 0 | 0 | 0 | 33 |
| IPC | 12 | 0 | 12 | 0 | 0 |
| Plugin | 30 | 0 | 0 | 0 | 30 |
| Storage | 25 | 0 | 0 | 0 | 25 |
| Marketplace | 0 | 0 | 0 | 0 | 0 | (Deferred)
| Knowledge | 0 | 0 | 0 | 0 | 0 | (Deferred)
| Workspace | 0 | 0 | 0 | 0 | 0 | (Deferred)
| Common | 6 | 0 | 0 | 6 | 0 |
| ${Matches[0]} | **12** | **94** | **0** |`n`n---`n`n## Related Documents`n`n| Document | Purpose |`n|---|---|`n| [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md) | Allowed/forbidden dependencies between domains |`n| [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) | 6-layer dependency hierarchy |`n| [RFC_MAP.md](RFC_MAP.md) | Complete numbered RFC tree |`n| [SPECIFICATION_INDEX.md](SPECIFICATION_INDEX.md) | Concept-driven navigation index |`n| [ARCHITECTURE_MATRIX.md](ARCHITECTURE_MATRIX.md) | Domain ownership and contract matrix |`n| [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) | RFC lifecycle, review authority, voting |`n| [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md) | Vision→Mission→ADR→RFC→Spec→Code→Test→Release |`n| [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md) | Domain ownership registry |

---

## Related Documents

| Document | Purpose |
|---|---|
| [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md) | Allowed/forbidden dependencies between domains |
| [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) | 6-layer dependency hierarchy |
| [LAYER_MODEL.md](LAYER_MODEL.md) | 7-layer model with strict dependency rules |
| [RFC_MAP.md](RFC_MAP.md) | Complete numbered RFC tree |
| [SPECIFICATION_INDEX.md](SPECIFICATION_INDEX.md) | Concept-driven navigation index |
| [ARCHITECTURE_MATRIX.md](ARCHITECTURE_MATRIX.md) | Domain ownership and contract matrix |
| [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md) | RFC lifecycle, review authority, voting |
| [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md) | Vision→Mission→ADR→RFC→Spec→Code→Test→Release |
| [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md) | Per-RFC ownership registry |
| [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md) | 10 shared principles |
| [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md) | How to modify any spec artifact |


