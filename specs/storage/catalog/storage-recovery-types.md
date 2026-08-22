---
id: ATLAS-STORAGE-CATALOG-RECOVERY-TYPES
title: Storage Recovery Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Recovery Types Catalog

## 1. Purpose

This catalog defines the canonical recovery types, source priorities, and automation levels used by the Atlas Storage subsystem for data restoration and disaster recovery.

## 2. Recovery Type Catalog

| Recovery ID | Name | Description | Source Priority | Dependencies | RFC Reference | RPO Impact | RTO Impact | Automation Level |
|---|---|---|---|---|---|---|---|---|
| REC-PIT | Point-In-Time | Restore to a specific moment. | Highest | Backup chain | RFC-0412 | Low | Moderate | Automated |
| REC-CRASH | Crash Recovery | Rebuild state after unexpected shutdown. | Highest | WAL / journal | RFC-0412 | None | Low | Automated |
| REC-DISASTER | Disaster Recovery | Restore from off-site backup after catastrophic failure. | Medium | Off-site backup | RFC-0412 | High | High | Semi-automated |
| REC-PARTIAL | Partial Resource | Restore a single resource or subset. | High | Latest backup | RFC-0412 | Low | Low | Automated |
| REC-FAILOVER | Failover | Switch to standby replica. | Highest | Standby replica | RFC-0418 | None | Very Low | Automated |
| REC-ROLLFORWARD | Roll-Forward | Apply transaction logs to latest state. | High | Transaction log | RFC-0412 | Low | Moderate | Automated |
| REC-ROLLBACK | Rollback | Revert to a previous known-good state. | Medium | Previous snapshot | RFC-0412 | Moderate | Low | Semi-automated |
| REC-SELECTIVE | Selective Restore | Restore specific resources from a backup. | Medium | Backup set | RFC-0412 | Low | Moderate | Manual |
| REC-STAGED | Staged Recovery | Multi-phase recovery with validation gates. | Low | Multiple sources | RFC-0412 | Low | High | Semi-automated |
| REC-AUTO-FAILOVER | Automated Failover | Automatic switch to secondary on health check failure. | Highest | Secondary replica | RFC-0418 | None | Very Low | Fully Automated |
| REC-MANUAL | Manual Intervention | Recovery requiring human decision at each step. | Lowest | Any available source | RFC-0412 | Variable | Variable | Manual |

## 3. Recovery Source Priority

| Priority | Source | Availability | Freshness | RFC Reference |
|---|---|---|---|---|
| 1 | Live replica | Always available | Current | RFC-0412 |
| 2 | Local backup | Available after startup | Recent | RFC-0411 |
| 3 | Remote backup | Available after network setup | Recent | RFC-0411 |
| 4 | Off-site backup | Available after transfer | Stale | RFC-0411 |
| 5 | Cloud archive | Available after retrieval | Very stale | RFC-0411 |

## 4. Testing Type Catalog

| Test ID | Name | Description | Frequency | RFC Reference |
|---|---|---|---|---|
| TEST-UNIT | Unit Recovery | Test single-resource recovery in isolation. | Per deployment | RFC-0412 |
| TEST-INTEGRATION | Integration Recovery | Test multi-resource recovery with dependencies. | Weekly | RFC-0412 |
| TEST-DRILL | Recovery Drill | Full disaster recovery simulation. | Quarterly | RFC-0412 |
| TEST-CHAOS | Chaos Recovery | Recovery under adverse conditions. | Monthly | RFC-0412 |
| TEST-RPO | RPO Verification | Verify recovery point objective compliance. | Per compliance cycle | RFC-0412 |
| TEST-RTO | RTO Verification | Verify recovery time objective compliance. | Per compliance cycle | RFC-0412 |

## 5. Validation Rules

1. Every recovery type identifier MUST match the regex ^REC-[A-Z][A-Z0-9]*$.
2. Every test type identifier MUST match the regex ^TEST-[A-Z][A-Z0-9]*$.
3. Recovery source priority MUST be enforced in the order defined in Section 3.
4. Automated recoveries MUST include post-recovery validation.
5. Recovery procedures MUST be tested at frequencies defined in Section 4.
6. RPO and RTO impacts MUST be documented for every recovery type.
