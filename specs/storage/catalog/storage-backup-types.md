---
id: ATLAS-STORAGE-CATALOG-BACKUP-TYPES
title: Storage Backup Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Backup Types Catalog

## 1. Purpose

This catalog defines the canonical backup types, scheduling modes, and target destinations used by the Atlas Storage subsystem.

## 2. Backup Type Catalog

| Backup ID | Name | Description | Storage Overhead | Restore Speed | RFC Reference | Retention Compatible | Encryption Required |
|---|---|---|---|---|---|---|---|
| BKP-FULL | Full | Complete copy of all data at a point in time. | High | Fast | RFC-0411 | Daily, Weekly, Monthly, Yearly | Yes |
| BKP-INCREMENTAL | Incremental | Only changes since the last backup of any type. | Low | Slow | RFC-0411 | Daily, Weekly | Yes |
| BKP-DIFFERENTIAL | Differential | Changes since the last full backup. | Medium | Moderate | RFC-0411 | Daily, Weekly, Monthly | Yes |
| BKP-CONTINUOUS | Continuous | Real-time change log capture. | Low | Fast | RFC-0411 | Continuous | Yes |
| BKP-SNAPSHOT | Snapshot-Based | Point-in-time volume snapshot. | Low | Fast | RFC-0411 | Per snapshot policy | Yes |
| BKP-STREAM | Stream-Based | Continuous stream of change events. | Low | Moderate | RFC-0411 | Continuous | Yes |
| BKP-LOGICAL | Logical | Export of structured data representations. | High | Slow | RFC-0411 | Daily, Weekly | Recommended |
| BKP-PHYSICAL | Physical | Byte-level copy of storage media. | Medium | Fast | RFC-0411 | Per media policy | Yes |
| BKP-COMPRESSED | Compressed | Backup with data compression applied. | Very Low | Moderate | RFC-0411 | Same as base | Yes |
| BKP-ENCRYPTED | Encrypted | Backup with cryptographic protection applied. | Medium | Moderate | RFC-0411 | Same as base | Yes |
| BKP-DEDUP | Deduplicated | Backup with duplicate block elimination. | Very Low | Moderate | RFC-0411 | Same as base | Yes |
| BKP-DISTRIBUTED | Distributed | Backup spread across multiple storage nodes. | Low | Fast | RFC-0411 | Same as base | Yes |

## 3. Scheduling Mode Catalog

| Schedule ID | Name | Description | RFC Reference |
|---|---|---|---|
| SCHED-PERIODIC | Periodic | Fixed interval (e.g., every 6 hours). | RFC-0411 |
| SCHED-EVENT | Event-Triggered | Triggered by specific storage events. | RFC-0411 |
| SCHED-CONTINUOUS | Continuous | Always-on change capture. | RFC-0411 |
| SCHED-MANUAL | Manual | Operator-initiated on demand. | RFC-0411 |

## 4. Target Destination Catalog

| Target ID | Name | Description | Availability | RFC Reference |
|---|---|---|---|---|
| TGT-LOCAL | Local | Storage on the same node. | Low | RFC-0411 |
| TGT-REMOTE | Remote | Storage on a nearby node. | Medium | RFC-0411 |
| TGT-OFFSITE | Off-Site | Storage in a geographically distant location. | High | RFC-0411 |
| TGT-CLOUD | Cloud | Storage in a cloud provider region. | High | RFC-0411 |

## 5. Backup Priority Catalog

| Priority ID | Name | Description | Preemption | RFC Reference |
|---|---|---|---|---|
| PRI-CRITICAL | Critical | Must complete before any other backup. | Yes | RFC-0411 |
| PRI-HIGH | High | Completes before moderate and low. | Yes | RFC-0411 |
| PRI-MODERATE | Moderate | Completes before low priority. | No | RFC-0411 |
| PRI-LOW | Low | Runs when system capacity is available. | No | RFC-0411 |

## 6. Validation Rules

1. Every backup type identifier MUST match the regex ^BKP-[A-Z]+$.
2. Every schedule identifier MUST match the regex ^SCHED-[A-Z]+$.
3. Every target identifier MUST match the regex ^TGT-[A-Z]+$.
4. Every priority identifier MUST match the regex ^PRI-[A-Z]+$.
5. Backup types MUST be combined with a scheduling mode and target destination.
6. Encryption MUST be applied to all backups classified as Confidential or Restricted.
7. Backup integrity MUST be verified after every completion event.
