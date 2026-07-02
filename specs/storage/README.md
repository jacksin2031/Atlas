# Specifications: STORAGE

## Table of Contents
- [Overview](#overview)
- [Purpose](#purpose)
- [Relationship with Other Subsystems](#relationship-with-other-subsystems)
- [RFC Hierarchy](#rfc-hierarchy)
- [Catalog](#catalog)
- [Design Documents](#design-documents)

## Overview

The Storage subsystem is Atlas's persistence abstraction layer. It does not implement a database; it defines the contracts that every persistence mechanism MUST satisfy within the Atlas platform.

Storage owns persistence, schemas, transactions, snapshots, versioning, migration, backup, recovery, caching, resource lifecycle, consistency, replication, security, observability, extension points, compliance, domains, namespaces, quotas, resource models, and capability discovery.

## Purpose

The Storage subsystem provides:

1. **A Unified Persistence Contract**: Every storage backend—whether embedded, networked, local, or cloud-based—MUST implement the Storage Provider interface defined in RFC-0403.
2. **Abstract Resource Lifecycle**: Resources created, updated, and deleted through Storage MUST follow the lifecycle defined in RFC-0404, independent of the backing store.
3. **Schema Evolution**: Data structures evolve through the versioning and migration mechanisms defined in RFC-0407 and RFC-0408.
4. **Transaction Guarantees**: ACID-like properties are abstracted through the transaction model in RFC-0406.
5. **Consistency Models**: Multiple consistency guarantees (strong, causal, eventual) are defined in RFC-0416.
6. **Observability and Compliance**: Every storage operation is observable and auditable per RFC-0414 and RFC-0420.

## Relationship with Other Subsystems

\\\mermaid
graph TD
    Runtime[\"Runtime (RFC-0001)\"] --> Storage[\"Storage (RFC-0401)\"]
    Runtime --> StateMgr[\"State Manager (RFC-0006)\"]
    StateMgr --> Storage
    Workflow[\"Workflow (RFC-0101)\"] --> Storage
    Plugin[\"Plugin (RFC-0201)\"] --> Storage
    AI[\"AI Integration (RFC-0301)\"] --> Storage
    Knowledge[\"Knowledge (RFC-0601)\"] --> Storage
    Marketplace[\"Marketplace (RFC-0501)\"] --> Storage
    Project[\"Project (RFC-0701)\"] --> Storage
    
    Storage --> Provider[\"Storage Provider Interface\"]
    Storage --> Tx[\"Transaction Layer\"]
    Storage --> Schema[\"Schema Layer\"]
    Storage --> Cache[\"Cache Layer\"]
    Storage --> Version[\"Versioning Layer\"]
    Storage --> Backup[\"Backup Layer\"]
    Storage --> Recover[\"Recovery Layer\"]
    
    Style Runtime fill:#e1f5fe
    Style Storage fill:#fff3e0
    Style Provider fill:#f3e5f5
    Style Tx fill:#f3e5f5
    Style Schema fill:#f3e5f5
    Style Cache fill:#f3e5f5
\\\

- **Runtime**: Storage operates as a Runtime service. The Runtime Lifecycle (RFC-0002) governs Storage initialization and shutdown. The State Manager (RFC-0006) delegates persistent state to Storage.
- **Plugins**: Plugins MAY declare storage capabilities. The Plugin subsystem (RFC-0201) uses Storage for plugin state persistence.
- **Workflows**: Workflow execution state, node outputs, and trigger data are persisted through Storage (RFC-0404).
- **AI Integration**: AI context, conversation history, and model state are stored via Storage abstractions.
- **Knowledge**: Knowledge Packs use Storage for vector indices and semantic search backends.
- **Marketplace**: Marketplace packages, signatures, and version manifests are stored through Storage.
- **Projects**: Project configuration, workspace state, and user preferences persist via Storage.

## RFC Hierarchy

The Storage specification series comprises 20 RFCs organized into six functional domains:

| Domain | RFCs | Description |
|---|---|---|
| **Foundation** | RFC-0401, RFC-0402 | Overview and Architecture |
| **Core Contracts** | RFC-0403, RFC-0404, RFC-0405 | Provider, Lifecycle, Schema |
| **Data Integrity** | RFC-0406, RFC-0407, RFC-0408, RFC-0416 | Transactions, Versioning, Migration, Consistency |
| **Reliability** | RFC-0409, RFC-0410, RFC-0411, RFC-0412 | Security, Cache, Backup, Recovery |
| **Observability** | RFC-0413, RFC-0414, RFC-0415 | Events, Observability, Performance |
| **Advanced** | RFC-0417, RFC-0418, RFC-0419, RFC-0420 | Locking, Replication, Extension, Compliance |

### Foundation Domain

- **[RFC-0401](RFC-0401-storage-overview.md)**: Storage subsystem overview, philosophy, ownership, and boundaries.
- **[RFC-0402](RFC-0402-storage-architecture.md)**: Layered architecture, component interactions, and data flow.

### Core Contracts Domain

- **[RFC-0403](RFC-0403-storage-provider.md)**: Provider interface, plugin contract, and adapter pattern.
- **[RFC-0404](RFC-0404-storage-lifecycle.md)**: Resource lifecycle states, transitions, and management.
- **[RFC-0405](RFC-0405-storage-schema.md)**: Schema definitions, evolution, and validation.

### Data Integrity Domain

- **[RFC-0406](RFC-0406-storage-transactions.md)**: Transaction model, isolation, and atomicity.
- **[RFC-0407](RFC-0407-storage-versioning.md)**: Document and schema versioning strategies.
- **[RFC-0408](RFC-0408-storage-migration.md)**: Schema and data migration procedures.
- **[RFC-0416](RFC-0416-storage-consistency.md)**: Consistency models and guarantees.

### Reliability Domain

- **[RFC-0409](RFC-0409-storage-security.md)**: Access control, encryption, and audit.
- **[RFC-0410](RFC-0410-storage-cache.md)**: Caching layers, invalidation, and eviction.
- **[RFC-0411](RFC-0411-storage-backup.md)**: Backup strategies and scheduling.
- **[RFC-0412](RFC-0412-storage-recovery.md)**: Recovery procedures and RPO/RTO guarantees.

### Observability Domain

- **[RFC-0413](RFC-0413-storage-events.md)**: Storage event taxonomy and publishing.
- **[RFC-0414](RFC-0414-storage-observability.md)**: Metrics, tracing, and logging.
- **[RFC-0415](RFC-0415-storage-performance.md)**: Performance targets and benchmarks.

### Advanced Domain

- **[RFC-0417](RFC-0417-storage-locking.md)**: Concurrency control and locking protocols.
- **[RFC-0418](RFC-0418-storage-replication.md)**: Replication topology and synchronization.
- **[RFC-0419](RFC-0419-storage-extension.md)**: Extension points and hooks.
- **[RFC-0420](RFC-0420-storage-compliance.md)**: Compliance checks and validation.

## Catalog

The \catalog/\ directory contains dictionary-style reference documents:

| File | Description |
|---|---|
| [storage-capabilities.md](catalog/storage-capabilities.md) | Canonical capability names |
| [storage-events.md](catalog/storage-events.md) | Event type enumeration |
| [storage-errors.md](catalog/storage-errors.md) | Error code catalog |
| [storage-lifecycle.md](catalog/storage-lifecycle.md) | Resource lifecycle states |
| [storage-locks.md](catalog/storage-locks.md) | Lock type enumeration |
| [storage-manifest-fields.md](catalog/storage-manifest-fields.md) | Manifest field definitions |
| [storage-metrics.md](catalog/storage-metrics.md) | Metric name registry |
| [storage-permissions.md](catalog/storage-permissions.md) | Permission name catalog |
| [storage-providers.md](catalog/storage-providers.md) | Provider type enumeration |
| [storage-resource-types.md](catalog/storage-resource-types.md) | Resource type registry |
| [storage-schema.md](catalog/storage-schema.md) | Schema structure definitions |
| [storage-states.md](catalog/storage-states.md) | State name enumeration |
| [storage-transactions.md](catalog/storage-transactions.md) | Transaction type catalog |
| [storage-versioning.md](catalog/storage-versioning.md) | Versioning strategy enumeration |
| [storage-consistency-models.md](catalog/storage-consistency-models.md) | Consistency model definitions |
| [storage-migration-types.md](catalog/storage-migration-types.md) | Migration type catalog |
| [storage-backup-types.md](catalog/storage-backup-types.md) | Backup type enumeration |
| [storage-recovery-types.md](catalog/storage-recovery-types.md) | Recovery type catalog |
| [storage-extension-points.md](catalog/storage-extension-points.md) | Extension point registry |
| [storage-observability.md](catalog/storage-observability.md) | Observability category definitions |

## Design Documents

The Storage subsystem follows a layered, contract-first architecture:

\\\mermaid
graph TB
    subgraph Consumer Layer
        Runtime[\"Runtime Services\"]
        Workflow[\"Workflow Engine\"]
        Plugin[\"Plugin Host\"]
        AI[\"AI Coordinator\"]
        Knowledge[\"Knowledge Manager\"]
    end

    subgraph Storage Layer
        API[\"Storage API\"]
        Tx[\"Transaction Manager\"]
        Schema[\"Schema Validator\"]
        Cache[\"Cache Manager\"]
        Version[\"Version Manager\"]
        Lock[\"Lock Manager\"]
        Replicate[\"Replication Manager\"]
    end

    subgraph Provider Layer
        ProviderA[\"Provider A\"]
        ProviderB[\"Provider B\"]
        ProviderN[\"Provider N\"]
    end

    subgraph Persistence Layer
        Local[\"Local Persistence\"]
        Remote[\"Remote Persistence\"]
        Hybrid[\"Hybrid Persistence\"]
    end

    Runtime --> API
    Workflow --> API
    Plugin --> API
    AI --> API
    Knowledge --> API

    API --> Tx
    API --> Schema
    API --> Cache
    API --> Version
    API --> Lock
    API --> Replicate

    ProviderA --> Local
    ProviderB --> Remote
    ProviderN --> Hybrid
    
    style Storage Layer fill:#fff3e0
    style Provider Layer fill:#f3e5f5
    style Persistence Layer fill:#e8f5e9
\\\

## Normative References

- [ADS Constitution](../README.md)
- [Architecture Decision Records](../README.md)
- [RFC-0001 Runtime Overview](../runtime/RFC-0001-runtime-overview.md)
- [RFC-0002 Runtime Lifecycle](../runtime/RFC-0002-runtime-lifecycle.md)
- [RFC-0006 Runtime State Management](../runtime/RFC-0006-runtime-state.md)
- [RFC-0009 Runtime Resource Management](../runtime/RFC-0009-runtime-resource.md)
- [RFC-0201 Plugin Overview](../plugin/RFC-0201-plugin-overview.md)
- [RFC-1001 Common Event Model](../common/RFC-1001-event-model.md)
- [RFC-1006 Common Error Model](../common/RFC-1006-error-model.md)
- [Security Standards](../README.md)
- [Performance Standards](../README.md)
- [Architecture Rules](../README.md)

