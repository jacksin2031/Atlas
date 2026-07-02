# Atlas Specification Index

> **Purpose**: Concept-driven navigation index for the Atlas specification hierarchy.  
> **NOT a README.** This is a lookup index organized by domain concept, not by file path.  
> **Created**: 2026-07-02  
> **Owner**: Atlas Specification Committee  

---

## How to Use This Index

Each section groups specifications by **concept**, not by RFC number. Use this index when you need to understand:

- **"How does the event system work?"** → Go to [Events](#events)
- **"What are the security levels?"** → Go to [Security](#security)
- **"How do plugins load?"** → Go to [Plugin Lifecycle](#plugin-lifecycle)
- **"What storage backends are supported?"** → Go to [Storage Providers](#storage-providers)

---

## Governance

| Concept | RFC / Document | Layer |
|---|---|---|
| Specification Template | [RFC_TEMPLATE.md](RFC_TEMPLATE.md) | Meta |
| Style Guide | [RFC_STYLE_GUIDE.md](RFC_STYLE_GUIDE.md) | Meta |
| Versioning Policy | [RFC_VERSIONING_POLICY.md](RFC_VERSIONING_POLICY.md) | Meta |
| Change Policy | [RFC_CHANGE_POLICY.md](RFC_CHANGE_POLICY.md) | Meta |
| Review Checklist | [RFC_REVIEW_CHECKLIST.md](RFC_REVIEW_CHECKLIST.md) | Meta |
| Glossary | [glossary.md](glossary.md) | Meta |
| Master Index | [RFC_INDEX.md](RFC_INDEX.md) | Meta |
| Architecture Matrix | [ARCHITECTURE_MATRIX.md](ARCHITECTURE_MATRIX.md) | Meta |
| Dependency Graph | [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md) | Meta |
| Specification Layers | [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) | Meta |
| RFC Map | [RFC_MAP.md](RFC_MAP.md) | Meta |

---

## Models

Shared abstractions used across all domains.

| Concept | RFC | Layer |
|---|---|---|
| Event Model | [RFC-1001](common/RFC-1001-event-model.md) | 1 |
| State Model | [RFC-1002](common/RFC-1002-state-model.md) | 1 |
| Capability Model | [RFC-1003](common/RFC-1003-capability-model.md) | 1 |
| Contract Model | [RFC-1004](common/RFC-1004-contract-model.md) | 1 |
| Manifest Model | [RFC-1005](common/RFC-1005-manifest-model.md) | 1 |
| Error Model | [RFC-1006](common/RFC-1006-error-model.md) | 1 |
| Capability Catalog | [capability-catalog.md](capabilities/capability-catalog.md) | 1 |

---

## Runtime

Core platform services. All other domains build on Runtime.

| Concept | RFC | Layer |
|---|---|---|
| Overview & Architecture | [RFC-0001](runtime/RFC-0001-runtime-overview.md) | 2 |
| Lifecycle | [RFC-0002](runtime/RFC-0002-runtime-lifecycle.md) | 2 |
| Service Model | [RFC-0003](runtime/RFC-0003-runtime-service-model.md) | 2 |
| Scheduler | [RFC-0004](runtime/RFC-0004-runtime-scheduler.md) | 2 |
| Event Bus | [RFC-0005](runtime/RFC-0005-runtime-eventbus.md) | 2 |
| State Management | [RFC-0006](runtime/RFC-0006-runtime-state.md) | 2 |
| IPC Architecture | [RFC-0007](runtime/RFC-0007-runtime-ipc.md) | 2 |
| Plugin Host | [RFC-0008](runtime/RFC-0008-runtime-plugin.md) | 2 |
| Resource Management | [RFC-0009](runtime/RFC-0009-runtime-resource.md) | 2 |
| Manifest Specification | [RFC-0010](runtime/RFC-0010-runtime-manifest.md) | 2 |
| Error Taxonomy | [RFC-0011](runtime/RFC-0011-runtime-errors.md) | 2 |
| Capability Registry | [RFC-0012](runtime/RFC-0012-runtime-capability.md) | 2 |
| Contracts | [RFC-0013](runtime/RFC-0013-runtime-contracts.md) | 2 |
| Reference Architecture | [RFC-0014](runtime/RFC-0014-runtime-reference-architecture.md) | 2 |
| Runtime Errors | [runtime-errors.md](errors/runtime-errors.md) | 2 |
| Runtime Events | [runtime-event-catalog.md](events/runtime-event-catalog.md) | 2 |

---

## IPC

Inter-process communication infrastructure.

| Concept | RFC | Layer |
|---|---|---|
| Overview & Principles | [RFC-0101](ipc/RFC-0101-ipc-overview.md) | 3 |
| Message Model | [RFC-0102](ipc/RFC-0102-ipc-message-model.md) | 3 |
| Channel Abstraction | [RFC-0103](ipc/RFC-0103-ipc-transport.md) | 3 |
| Transport Layer | [RFC-0104](ipc/RFC-0104-ipc-routing.md) | 3 |
| Channel Types | [RFC-0105](ipc/RFC-0105-ipc-channel.md) | 3 |
| Serialization | [RFC-0106](ipc/RFC-0106-ipc-serialization.md) | 3 |
| Access Control | [RFC-0107](ipc/RFC-0107-ipc-security.md) | 3 |
| Encryption | [RFC-0108](ipc/RFC-0108-ipc-reliability.md) | 3 |
| Lifecycle | [RFC-0109](ipc/RFC-0109-ipc-lifecycle.md) | 3 |
| Observability | [RFC-0110](ipc/RFC-0110-ipc-observability.md) | 3 |
| Error Model | [RFC-0111](ipc/RFC-0111-ipc-error-model.md) | 3 |
| Extension | [RFC-0112](ipc/RFC-0112-ipc-extension.md) | 3 |
| Interfaces Catalog | [catalog/interfaces.md](ipc/catalog/interfaces.md) | 3 |
| Messages Catalog | [catalog/messages.md](ipc/catalog/messages.md) | 3 |
| Channels Catalog | [catalog/channels.md](ipc/catalog/channels.md) | 3 |
| Errors Catalog | [catalog/errors.md](ipc/catalog/errors.md) | 3 |
| Capabilities Catalog | [catalog/capabilities.md](ipc/catalog/capabilities.md) | 3 |
| Security Levels | [catalog/security-levels.md](ipc/catalog/security-levels.md) | 3 |

---

## Plugin

Platform extension framework.

| Concept | RFC | Layer |
|---|---|---|
| Overview | [RFC-0201](plugin/RFC-0201-plugin-overview.md) | 4 |
| Manifest | [RFC-0202](plugin/RFC-0202-plugin-manifest.md) | 4 |
| Lifecycle | [RFC-0203](plugin/RFC-0203-plugin-lifecycle.md) | 4 |
| Loader | [RFC-0204](plugin/RFC-0204-plugin-loader.md) | 4 |
| Registry | [RFC-0205](plugin/RFC-0205-plugin-registry.md) | 4 |
| Capability | [RFC-0206](plugin/RFC-0206-plugin-capability.md) | 4 |
| Security | [RFC-0207](plugin/RFC-0207-plugin-security.md) | 4 |
| Sandbox | [RFC-0208](plugin/RFC-0208-plugin-sandbox.md) | 4 |
| API | [RFC-0209](plugin/RFC-0209-plugin-api.md) | 4 |
| Events | [RFC-0210](plugin/RFC-0210-plugin-events.md) | 4 |
| Dependency | [RFC-0211](plugin/RFC-0211-plugin-dependency.md) | 4 |
| Versioning | [RFC-0212](plugin/RFC-0212-plugin-versioning.md) | 4 |
| Marketplace Integration | [RFC-0213](plugin/RFC-0213-plugin-marketplace.md) | 4 |
| Extension Model | [RFC-0214](plugin/RFC-0214-plugin-extension-model.md) | 4 |
| Service Model | [RFC-0215](plugin/RFC-0215-plugin-service-model.md) | 4 |
| Discovery | [RFC-0216](plugin/RFC-0216-plugin-discovery.md) | 4 |
| Packaging | [RFC-0217](plugin/RFC-0217-plugin-packaging.md) | 4 |
| Compatibility | [RFC-0218](plugin/RFC-0218-plugin-compatibility.md) | 4 |
| Testing | [RFC-0219](plugin/RFC-0219-plugin-testing.md) | 4 |
| IPC Integration | [RFC-0220](plugin/RFC-0220-plugin-ipc.md) | 4 |
| Resources | [RFC-0221](plugin/RFC-0221-plugin-resources.md) | 4 |
| Storage Integration | [RFC-0222](plugin/RFC-0222-plugin-storage.md) | 4 |
| Configuration | [RFC-0223](plugin/RFC-0223-plugin-configuration.md) | 4 |
| Diagnostics | [RFC-0224](plugin/RFC-0224-plugin-diagnostics.md) | 4 |
| Hot Reload | [RFC-0225](plugin/RFC-0225-plugin-hot-reload.md) | 4 |
| Migration | [RFC-0226](plugin/RFC-0226-plugin-migration.md) | 4 |
| Service Discovery | [RFC-0227](plugin/RFC-0227-plugin-service-discovery.md) | 4 |
| Dependency Resolution | [RFC-0228](plugin/RFC-0228-plugin-dependency-resolution.md) | 4 |
| Telemetry | [RFC-0229](plugin/RFC-0229-plugin-telemetry.md) | 4 |
| Signature | [RFC-0230](plugin/RFC-0230-plugin-signature.md) | 4 |
| Service Lifecycle Catalog | [catalog/plugin-service-lifecycle.md](plugin/catalog/plugin-service-lifecycle.md) | 4 |
| Service Types Catalog | [catalog/plugin-service-types.md](plugin/catalog/plugin-service-types.md) | 4 |
| Signature Catalog | [catalog/plugin-signature.md](plugin/catalog/plugin-signature.md) | 4 |
| Release Management Catalog | [catalog/plugin-release-management.md](plugin/catalog/plugin-release-management.md) | 4 |

---

## Workflow

Orchestration and execution engine.

| Concept | RFC | Layer |
|---|---|---|
| Overview | [RFC-0301](workflow/RFC-0301-workflow-overview.md) | 4 |
| Language | [RFC-0302](workflow/RFC-0302-workflow-language.md) | 4 |
| Execution | [RFC-0303](workflow/RFC-0303-workflow-execution.md) | 4 |
| Runtime | [RFC-0304](workflow/RFC-0304-workflow-runtime.md) | 4 |
| Lifecycle | [RFC-0305](workflow/RFC-0305-workflow-lifecycle.md) | 4 |
| State | [RFC-0306](workflow/RFC-0306-workflow-state.md) | 4 |
| Context | [RFC-0307](workflow/RFC-0307-workflow-context.md) | 4 |
| Events | [RFC-0308](workflow/RFC-0308-workflow-events.md) | 4 |
| Actions | [RFC-0309](workflow/RFC-0309-workflow-actions.md) | 4 |
| Conditions | [RFC-0310](workflow/RFC-0310-workflow-conditions.md) | 4 |
| Triggers | [RFC-0311](workflow/RFC-0311-workflow-triggers.md) | 4 |
| Scheduler | [RFC-0312](workflow/RFC-0312-workflow-scheduler.md) | 4 |
| Parallelism | [RFC-0313](workflow/RFC-0313-workflow-parallelism.md) | 4 |
| Error Handling | [RFC-0314](workflow/RFC-0314-workflow-error-handling.md) | 4 |
| Recovery | [RFC-0315](workflow/RFC-0315-workflow-recovery.md) | 4 |
| Debugging | [RFC-0316](workflow/RFC-0316-workflow-debugging.md) | 4 |
| Validation | [RFC-0317](workflow/RFC-0317-workflow-validation.md) | 4 |
| Versioning | [RFC-0318](workflow/RFC-0318-workflow-versioning.md) | 4 |
| Security | [RFC-0319](workflow/RFC-0319-workflow-security.md) | 4 |
| Performance | [RFC-0320](workflow/RFC-0320-workflow-performance.md) | 4 |
| Observability | [RFC-0321](workflow/RFC-0321-workflow-observability.md) | 4 |
| Extension | [RFC-0322](workflow/RFC-0322-workflow-extension.md) | 4 |
| Plugin Integration | [RFC-0323](workflow/RFC-0323-workflow-plugin-integration.md) | 4 |
| Storage | [RFC-0324](workflow/RFC-0324-workflow-storage.md) | 4 |
| AI Integration | [RFC-0325](workflow/RFC-0325-workflow-ai.md) | 4 |
| Vision Integration | [RFC-0326](workflow/RFC-0326-workflow-vision.md) | 4 |
| IPC Integration | [RFC-0327](workflow/RFC-0327-workflow-ipc.md) | 4 |
| Serialization | [RFC-0328](workflow/RFC-0328-workflow-serialization.md) | 4 |
| Compatibility | [RFC-0329](workflow/RFC-0329-workflow-compatibility.md) | 4 |
| Compliance | [RFC-0330](workflow/RFC-0330-workflow-compliance.md) | 4 |
| Testing | [RFC-0331](workflow/RFC-0331-workflow-testing.md) | 4 |
| Migration | [RFC-0332](workflow/RFC-0332-workflow-migration.md) | 4 |
| Extension SDK | [RFC-0333](workflow/RFC-0333-workflow-sdk.md) | 4 |
| Actions Catalog | [catalog/workflow-actions.md](workflow/catalog/workflow-actions.md) | 4 |
| Action Types Catalog | [catalog/workflow-action-types.md](workflow/catalog/workflow-action-types.md) | 4 |
| Conditions Catalog | [catalog/workflow-conditions.md](workflow/catalog/workflow-conditions.md) | 4 |
| Condition Types Catalog | [catalog/workflow-condition-types.md](workflow/catalog/workflow-condition-types.md) | 4 |
| Triggers Catalog | [catalog/workflow-triggers.md](workflow/catalog/workflow-triggers.md) | 4 |
| Trigger Types Catalog | [catalog/workflow-trigger-types.md](workflow/catalog/workflow-trigger-types.md) | 4 |
| Events Catalog | [catalog/workflow-events.md](workflow/catalog/workflow-events.md) | 4 |
| Event Types Catalog | [catalog/workflow-event-types.md](workflow/catalog/workflow-event-types.md) | 4 |
| Event Delivery Catalog | [catalog/workflow-event-delivery.md](workflow/catalog/workflow-event-delivery.md) | 4 |
| Event Lifecycle Catalog | [catalog/workflow-event-lifecycle.md](workflow/catalog/workflow-event-lifecycle.md) | 4 |
| Debug Events Catalog | [catalog/workflow-debug-events.md](workflow/catalog/workflow-debug-events.md) | 4 |
| Errors Catalog | [catalog/workflow-errors.md](workflow/catalog/workflow-errors.md) | 4 |
| Error Codes Catalog | [catalog/workflow-error-codes.md](workflow/catalog/workflow-error-codes.md) | 4 |
| Error Lifecycle Catalog | [catalog/workflow-error-lifecycle.md](workflow/catalog/workflow-error-lifecycle.md) | 4 |
| States Catalog | [catalog/workflow-state-types.md](workflow/catalog/workflow-state-types.md) | 4 |
| Variables Catalog | [catalog/workflow-variable-types.md](workflow/catalog/workflow-variable-types.md) | 4 |
| Results Catalog | [catalog/workflow-result-types.md](workflow/catalog/workflow-result-types.md) | 4 |
| Resources Catalog | [catalog/workflow-resource-types.md](workflow/catalog/workflow-resource-types.md) | 4 |
| Nodes Catalog | [catalog/workflow-node-types.md](workflow/catalog/workflow-node-types.md) | 4 |
| Context Catalog | [catalog/workflow-context.md](workflow/catalog/workflow-context.md) | 4 |
| Lifecycle Catalog | [catalog/workflow-lifecycle.md](workflow/catalog/workflow-lifecycle.md) | 4 |
| Time Model Catalog | [catalog/workflow-time-model.md](workflow/catalog/workflow-time-model.md) | 4 |
| Operators Catalog | [catalog/workflow-operators.md](workflow/catalog/workflow-operators.md) | 4 |
| Hooks Catalog | [catalog/workflow-hooks.md](workflow/catalog/workflow-hooks.md) | 4 |
| Extension Points Catalog | [catalog/workflow-extension-points.md](workflow/catalog/workflow-extension-points.md) | 4 |
| Capabilities Catalog | [catalog/workflow-capabilities.md](workflow/catalog/workflow-capabilities.md) | 4 |
| Action Capabilities Catalog | [catalog/workflow-action-capabilities.md](workflow/catalog/workflow-action-capabilities.md) | 4 |
| Action Constraints Catalog | [catalog/workflow-action-constraints.md](workflow/catalog/workflow-action-constraints.md) | 4 |
| Action Errors Catalog | [catalog/workflow-action-errors.md](workflow/catalog/workflow-action-errors.md) | 4 |
| Action Lifecycle Catalog | [catalog/workflow-action-lifecycle.md](workflow/catalog/workflow-action-lifecycle.md) | 4 |
| Recovery Types Catalog | [catalog/workflow-recovery-types.md](workflow/catalog/workflow-recovery-types.md) | 4 |
| Recovery Lifecycle Catalog | [catalog/workflow-recovery-lifecycle.md](workflow/catalog/workflow-recovery-lifecycle.md) | 4 |
| Permissions Catalog | [catalog/workflow-permissions.md](workflow/catalog/workflow-permissions.md) | 4 |
| Observability Catalog | [catalog/workflow-observability.md](workflow/catalog/workflow-observability.md) | 4 |
| Metrics Catalog | [catalog/workflow-metrics.md](workflow/catalog/workflow-metrics.md) | 4 |
| Manifest Fields Catalog | [catalog/workflow-manifest.md](workflow/catalog/workflow-manifest.md) | 4 |
| Schedulers Catalog | [catalog/workflow-schedulers.md](workflow/catalog/workflow-schedulers.md) | 4 |
| Validation Rules Catalog | [catalog/workflow-validation-rules.md](workflow/catalog/workflow-validation-rules.md) | 4 |
| Versioning Catalog | [catalog/workflow-versioning.md](workflow/catalog/workflow-versioning.md) | 4 |
| Status Catalog | [catalog/workflow-status.md](workflow/catalog/workflow-status.md) | 4 |

---

## Storage

Persistence abstraction layer.

| Concept | RFC | Layer |
|---|---|---|
| Overview | [RFC-0401](storage/RFC-0401-storage-overview.md) | 3 |
| Architecture | [RFC-0402](storage/RFC-0402-storage-architecture.md) | 3 |
| Provider Interface | [RFC-0403](storage/RFC-0403-storage-provider.md) | 3 |
| Lifecycle | [RFC-0404](storage/RFC-0404-storage-lifecycle.md) | 3 |
| Schema | [RFC-0405](storage/RFC-0405-storage-schema.md) | 3 |
| Transactions | [RFC-0406](storage/RFC-0406-storage-transactions.md) | 3 |
| Versioning | [RFC-0407](storage/RFC-0407-storage-versioning.md) | 3 |
| Migration | [RFC-0408](storage/RFC-0408-storage-migration.md) | 3 |
| Security | [RFC-0409](storage/RFC-0409-storage-security.md) | 3 |
| Cache | [RFC-0410](storage/RFC-0410-storage-cache.md) | 3 |
| Backup | [RFC-0411](storage/RFC-0411-storage-backup.md) | 3 |
| Recovery | [RFC-0412](storage/RFC-0412-storage-recovery.md) | 3 |
| Events | [RFC-0413](storage/RFC-0413-storage-events.md) | 3 |
| Observability | [RFC-0414](storage/RFC-0414-storage-observability.md) | 3 |
| Performance | [RFC-0415](storage/RFC-0415-storage-performance.md) | 3 |
| Consistency | [RFC-0416](storage/RFC-0416-storage-consistency.md) | 3 |
| Locking | [RFC-0417](storage/RFC-0417-storage-locking.md) | 3 |
| Replication | [RFC-0418](storage/RFC-0418-storage-replication.md) | 3 |
| Extension | [RFC-0419](storage/RFC-0419-storage-extension.md) | 3 |
| Compliance | [RFC-0420](storage/RFC-0420-storage-compliance.md) | 3 |
| Domains | [RFC-0421](storage/RFC-0421-storage-domains.md) | 3 |
| Namespace | [RFC-0422](storage/RFC-0422-storage-namespace.md) | 3 |
| Resource Model | [RFC-0423](storage/RFC-0423-storage-resource-model.md) | 3 |
| Quota | [RFC-0424](storage/RFC-0424-storage-quota.md) | 3 |
| Capability Discovery | [RFC-0425](storage/RFC-0425-storage-capability-discovery.md) | 3 |
| Providers Catalog | [catalog/storage-providers.md](storage/catalog/storage-providers.md) | 3 |
| Observability Catalog | [catalog/storage-observability.md](storage/catalog/storage-observability.md) | 3 |
| Metrics Catalog | [catalog/storage-metrics.md](storage/catalog/storage-metrics.md) | 3 |
| Pipeline Catalog | [catalog/storage-pipeline.md](storage/catalog/storage-pipeline.md) | 3 |
| Locks Catalog | [catalog/storage-locks.md](storage/catalog/storage-locks.md) | 3 |
| Manifest Fields Catalog | [catalog/storage-manifest-fields.md](storage/catalog/storage-manifest-fields.md) | 3 |
| Extension Points Catalog | [catalog/storage-extension-points.md](storage/catalog/storage-extension-points.md) | 3 |
| Capability Flags Catalog | [catalog/storage-capability-flags.md](storage/catalog/storage-capability-flags.md) | 3 |
| Permissions Catalog | [catalog/storage-permissions.md](storage/catalog/storage-permissions.md) | 3 |
| Quota Catalog | [catalog/storage-quota.md](storage/catalog/storage-quota.md) | 3 |

---

## Marketplace

Package distribution and version resolution. *(Deferred — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| Protocol Overview | RFC-0501 | Marketplace communication protocol |
| Package Format | RFC-0502 | .atlas-plugin package specification |
| Version Resolution | RFC-0503 | Semver and dependency resolution |
| Cryptographic Signatures | RFC-0504 | Package signing and verification |

---

## Knowledge

Semantic data management and search. *(Deferred — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| Pack Protocol Overview | RFC-0601 | Knowledge pack format |
| Vector Search Indexing | RFC-0602 | Embedding and index management |
| Search Abstraction | RFC-0603 | Query layer abstraction |
| Pack Package Format | RFC-0604 | Knowledge pack distribution |

---

## Vision

Camera, OCR, and image processing. *(Placeholder — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| TBD | RFC-0801 | Vision camera pipeline |
| TBD | RFC-0802 | Vision OCR engine |
| TBD | RFC-0803 | Vision image processing |
| TBD | RFC-0804 | Vision frame buffer |

---

## AI

Language model integration and reasoning. *(Placeholder — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| TBD | RFC-0901 | AI model routing |
| TBD | RFC-0902 | AI prompt management |
| TBD | RFC-0903 | AI context window |
| TBD | RFC-0904 | AI tool calling |

---

## UI

User interface and presentation. *(Placeholder — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| TBD | RFC-0810 | UI component model |
| TBD | RFC-0811 | UI theme system |
| TBD | RFC-0812 | UI accessibility |

---

## Project / Workspace

Workspace boundaries and configuration. *(Deferred — no RFCs yet)*

| Concept | Reserved RFC | Purpose |
|---|---|---|
| Project Package Format | RFC-0701 | .atlas project specification |
| Workspace Boundaries | RFC-0702 | Scope and isolation rules |
| Configuration Engine | RFC-0703 | Hierarchical config resolution |

---

## Cross-Domain Integration Points

These RFCs bridge multiple domains and require joint review.

| RFC | Domains | Purpose |
|---|---|---|
| RFC-0007 | Runtime + IPC | Runtime IPC architecture |
| RFC-0008 | Runtime + Plugin | Runtime plugin host |
| RFC-0220 | Plugin + IPC | Plugin IPC integration |
| RFC-0222 | Plugin + Storage | Plugin state persistence |
| RFC-0323 | Workflow + Plugin | Workflow plugin actions |
| RFC-0324 | Workflow + Storage | Workflow state persistence |
| RFC-0325 | Workflow + AI | AI-powered workflows |
| RFC-0326 | Workflow + Vision | Vision-triggered workflows |
| RFC-0327 | Workflow + IPC | Workflow IPC channels |
| RFC-0328 | Workflow + IPC | Workflow serialization |

---

*This document is part of the Atlas Specification hierarchy. For the RFC tree, see [RFC_MAP.md](RFC_MAP.md). For layer definitions, see [SPECIFICATION_LAYERS.md](SPECIFICATION_LAYERS.md) and [LAYER_MODEL.md](LAYER_MODEL.md). For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md).*


