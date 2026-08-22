---
id: ATLAS-STORAGE-CATALOG-CONSISTENCY-MODELS
title: Storage Consistency Models Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Consistency Models Catalog

## 1. Purpose

This catalog defines the canonical consistency models, guarantee levels, and conflict resolution strategies available within the Atlas Storage subsystem.

## 2. Consistency Model Catalog

| Model ID | Name | Read Guarantees | Write Guarantees | Ordering | RFC Reference | Latency Impact | Use Case |
|---|---|---|---|---|---|---|---|
| CONS-STRONG | Strong | Always sees latest write. | Immediately visible to all. | Total order | RFC-0416 | Critical financial data. |
| CONS-LINEARIZABLE | Linearizable | Sees most recent write. | Atomic across all replicas. | Total order | RFC-0416 | Resource coordination. |
| CONS-SEQUENTIAL | Sequential Consistent | Sees writes in global order. | Ordered per client. | Global total | RFC-0416 | Audit trail integrity. |
| CONS-CAUSAL | Causal | Sees causally related writes. | Causal order preserved. | Causal | RFC-0416 | Collaborative editing. |
| CONS-RELAXED | Relaxed Eventual | Eventually sees all writes. | Accepted by majority. | Eventual | RFC-0416 | Analytics dashboards. |
| CONS-SESSION | Session Sticky | Sees own writes immediately. | Per-session ordering. | Per-session | RFC-0416 | User preference storage. |

## 3. Guarantee Level Catalog

| Level ID | Name | Description | Verification Method | RFC Reference |
|---|---|---|---|---|
| GL-NONE | None | No ordering or visibility guarantees. | N/A | RFC-0416 |
| GL-BASIC | Basic | Writes eventually propagate to all replicas. | Timeout-based. | RFC-0416 |
| GL-CAUSAL | Causal | Causally related writes are observed in order. | Lamport clocks. | RFC-0416 |
| GL-STRONG | Strong | All operations appear atomic and total-ordered. | Quorum-based. | RFC-0416 |
| GL-LINEARIZABLE | Linearizable | Operations appear to execute atomically in real time. | Real-time clock. | RFC-0416 |

## 4. Conflict Type Catalog

| Conflict ID | Name | Description | Detection Method | RFC Reference |
|---|---|---|---|---|
| CONF-WRITE-WRITE | Write-Write | Two concurrent writes to the same resource. | Version vector comparison. | RFC-0416 |
| CONF-READ-WRITE | Read-Write | Read observes partially applied write. | Timestamp comparison. | RFC-0416 |
| CONF-CASCADE | Cascade | Conflict propagates through dependent resources. | Dependency graph traversal. | RFC-0416 |
| CONF-SCHEMA | Schema | Schema mismatch between reader and writer. | Schema version comparison. | RFC-0405 |

## 5. Conflict Resolution Strategy Catalog

| Strategy ID | Name | Description | RFC Reference |
|---|---|---|---|
| RES-LAST-WRITER | Last Writer Wins | Most recent timestamp wins. | RFC-0416 |
| RES-FIRST-WRITER | First Writer Wins | Earliest committed write wins. | RFC-0416 |
| RES-MERGE | Semantic Merge | Merges non-conflicting fields from both sides. | RFC-0416 |
| RES-CUSTOM | Custom Resolver | Application-defined resolution logic. | RFC-0416 |
| RES-HUMAN | Human Intervention | Conflict flagged for manual resolution. | RFC-0416 |

## 6. Validation Rules

1. Every consistency model identifier MUST match the regex ^CONS-[A-Z]+$.
2. Every guarantee level identifier MUST match the regex ^GL-[A-Z]+$.
3. Every conflict type identifier MUST match the regex ^CONF-[A-Z]+-[A-Z]+$.
4. Conflict resolution strategies MUST be declared at the resource type level.
5. Consistency models MUST be selectable per resource per RFC-0416.
6. Guarantee levels MUST be verifiable through automated health checks.
