---
id: ATLAS-STORAGE-CATALOG-PROVIDERS
title: Storage Providers Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Providers Catalog

## 1. Purpose

This catalog defines the canonical set of provider types that the Atlas Storage subsystem MAY instantiate. Each provider type represents a distinct persistence architecture with specific capabilities and deployment characteristics.

## 2. Provider ID Prefix

All provider identifiers use the prefix PRV-.

## 3. Provider Type Catalog

| Provider ID | Name | Description | Use Case | RFC Reference |
|---|---|---|---|---|
| PRV-EMBEDDED | Embedded Provider | Runs in-process with the consumer; lowest latency. | Single-node applications. | RFC-0403 |
| PRV-REMOTE | Remote Provider | Accessed over IPC; decoupled lifecycle. | Distributed deployments. | RFC-0403 |
| PRV-CLOUD | Cloud Provider | Managed service integration; elastic scaling. | Cloud-native workloads. | RFC-0403 |
| PRV-HYBRID | Hybrid Provider | Combines local and remote storage tiers. | Edge computing scenarios. | RFC-0403 |
| PRV-LOCAL | Local Provider | File-system or local-network persistence. | Desktop applications. | RFC-0403 |
| PRV-DISTRIBUTED | Distributed Provider | Multi-node consensus-based storage. | High-availability clusters. | RFC-0403 |
| PRV-INMEMORY | In-Memory Provider | Volatile RAM-based storage. | Caching and ephemeral state. | RFC-0403 |
| PRV-TIERED | Tiered Provider | Automatic data placement across storage tiers. | Large-scale archival workloads. | RFC-0403 |

## 4. Provider Capability Matrix

| Capability | EMBEDDED | REMOTE | CLOUD | HYBRID | LOCAL | DISTRIBUTED | INMEMORY | TIERED |
|---|---|---|---|---|---|---|---|---|
| Read | Y | Y | Y | Y | Y | Y | Y | Y |
| Write | Y | Y | Y | Y | Y | Y | Y | Y |
| Delete | Y | Y | Y | Y | Y | Y | Y | Y |
| List | Y | Y | Y | Y | Y | Y | Y | Y |
| Scan | Y | Y | Y | Y | Y | Y | Y | Y |
| Query | Y | Y | Y | Y | Y | Y | N | Y |
| Backup | Y | Y | Y | Y | Y | Y | N | Y |
| Recovery | Y | Y | Y | Y | Y | Y | N | Y |
| Versioning | Y | Y | Y | Y | Y | Y | N | Y |
| Transactions | Y | Y | Y | Y | Y | Y | N | Y |
| Locking | Y | Y | Y | Y | Y | Y | N | Y |
| Replication | N | Y | Y | Y | N | Y | N | Y |

## 5. Provider Selection Algorithm

1. The Runtime MUST evaluate available providers against the requested capability set.
2. Providers MUST declare their capabilities at initialization time.
3. The selection algorithm MUST prefer the provider with the lowest latency that satisfies all capability requirements.
4. If no single provider satisfies all requirements, a HYBRID composition MAY be constructed.
5. Provider selection MUST be re-evaluated on each Runtime restart.

## 6. Provider Configuration Fields

| Field | Type | Required | Description |
|---|---|---|---|
| provider_type | Enum | YES | One of the provider types in this catalog. |
| endpoint | String | NO | Network endpoint for remote providers. |
| connection_pool_size | Integer | NO | Maximum concurrent connections. |
| timeout_ms | Integer | NO | Operation timeout in milliseconds. |
| retry_count | Integer | NO | Number of retry attempts on failure. |
| tls_enabled | Boolean | YES | Whether TLS is required for transport. |
| credentials_ref | String | NO | Reference to credential store. |
| compression_enabled | Boolean | NO | Whether data is compressed in transit. |

## 7. Validation Rules

1. Every provider identifier MUST match the regex ^PRV-[A-Z]+$.
2. Provider types MUST be selected exclusively from this catalog.
3. Capability declarations MUST be truthful; misrepresentation is a security violation.
4. Provider configurations MUST be validated before instantiation.
5. Provider selection MUST be logged per RFC-0414.
