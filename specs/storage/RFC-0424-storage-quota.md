# RFC-0424: Storage Quota

RFC: RFC-0424
Title: Storage Quota
Status: Accepted
Category: Standard
Owner: Storage Team
Authors: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADS Version: 1.0.0
Spec Version: 0.1.0
Normative: YES
Depends On:
  - RFC-0401 Storage Overview
  - RFC-0402 Storage Architecture
  - RFC-0409 Storage Security
  - RFC-0421 Storage Domains
  - RFC-0422 Storage Namespace
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0010 Contract-First Specification
Related JSON Schema:
  - schemas/storage/quota.json
Related Catalog:
  - catalog/storage-quota.md
Layer: Core
Audience: Storage developers, architects, specification reviewers
Target Release: 1.0.0
Review Cycle: Quarterly
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas implementation MUST conform to the quota model, enforcement mechanisms, allocation policies, and violation handling defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Authority
This RFC is the authoritative specification for the Storage Quota domain.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301.

| Term | Definition | Source |
|---|---|---|
| Quota | A limit on the amount of storage resources a domain or user may consume. | RFC-0424 |
| Quota Enforcement | The mechanism by which quota limits are checked and violations are prevented. | RFC-0424 |
| Quota Allocation | The process of assigning quota limits to domains, users, or namespaces. | RFC-0424 |
| Quota Violation | An attempt to exceed the allocated quota limit. | RFC-0424 |
| Quota Reservation | A portion of quota reserved for future use, preventing overcommitment. | RFC-0424 |
| Quota Utilization | The proportion of allocated quota currently consumed. | RFC-0424 |
| Resource | A unit of data managed by Storage, identified by a unique resource identifier. | RFC-0401 |
| Workflow | A declarative directed graph specification expressing WHAT must happen, not HOW. | RFC-0301 |
| Execution | The process of evaluating a workflow graph and activating nodes to produce results. | RFC-0303 |
 RFC-0301 |
| Task | An atomic unit of work within a workflow, represented as a node. | RFC-0301 |
| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |
| Context | The scoped data environment available to nodes during execution. | RFC-0307 |
| Frame | A discrete unit of visual data processed by vision nodes. | RFC-0301 |
| Tick | A single evaluation cycle of the workflow scheduler. | RFC-0301 |
| Scheduler | The component that determines WHEN and WHERE each node is executed. | RFC-0312 |
| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |

---

| Provider | Infrastructure adapters implementing storage backends. | Glossary |

---
This specification is Normative. Every Atlas implementation MUST enforce storage quotas at every hierarchy level as defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0001, ADR-0010, and all active ADRs.

---



## Layer Boundaries

### Responsibilities

This specification IS responsible for:

- Defining the architectural contract for this domain.
- Specifying behavioral requirements that all implementations MUST satisfy.
- Establishing extension points and their contracts.

### Non-Responsibilities

This specification IS NOT responsible for:

- Implementation details (see related RFCs for implementation guidance).
- Runtime platform specifics.
- User-facing UI behavior.

### Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview — foundational runtime architecture |

### Consumers

- See related RFCs for consumer listings.

### Providers

- This specification provides domain-specific contracts and behavioral models.

### Forbidden Dependencies

- This specification MUST NOT depend on any specific programming language.
- This specification MUST NOT depend on any specific storage backend.
- This specification MUST NOT depend on any specific operating system.
## Table of Contents
1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Quota Architecture](#4-quota-architecture)
5. [Quota Hierarchy](#5-quota-hierarchy)
6. [Quota Types](#6-quota-types)
7. [Quota Enforcement](#7-quota-enforcement)
8. [Quota Monitoring](#8-quota-monitoring)
9. [Quota Escalation](#9-quota-escalation)
10. [Quota Override Procedure](#10-quota-override-procedure)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [References](#12-references)
13. [Future Evolution](#13-future-evolution)

---

This specification IS responsible for:
- Defining the requirements for this storage subsystem component.
- Establishing the boundaries between storage layers.


## 2 Goals

1. **Hierarchical Quota Enforcement**: Quotas MUST be enforceable at every level of the Storage hierarchy: system, domain, namespace, tenant, and resource. Each level inherits limits from its parent and may impose stricter sub-limits.

2. **Multiple Quota Types**: Storage MUST support ten distinct quota types covering disk, memory, blob, snapshot, backup, cache, operations, connections, entities, and bandwidth. Each type addresses a specific resource constraint.

3. **Enforcement Modes**: Quotas MUST support four enforcement modes: hard (reject), soft (warn), grace (delayed rejection), and throttle (rate limiting). The enforcement mode is configurable per quota.

4. **Real-Time Monitoring**: Quota utilization MUST be monitored in real time with metrics emitted at configurable intervals. Utilization data MUST be available through the observability layer (RFC-0414).

5. **Escalation Procedures**: When quotas approach their limits, the Storage subsystem MUST follow a defined escalation procedure that progresses from informational warnings through soft alerts to hard rejections.

6. **Override Mechanism**: Administrators MUST be able to override quotas under exceptional circumstances, with every override recorded in the audit log and subject to approval workflows.

7. **Cross-Level Consistency**: Quotas at different hierarchy levels MUST be consistent. The sum of all child quotas MUST NOT exceed the parent quota, and the sum of all enforced usage MUST NOT exceed any applicable quota.

8. **Provider Transparency**: Providers MUST NOT need to understand quota semantics. Quota enforcement occurs at the Storage layer before operations reach the Provider. Providers report their own capacity limits to the Storage layer for quota calculations.

---



## 4 Quota Architecture

The quota architecture consists of five layers, each responsible for a different aspect of quota management:

### 4.1 Quota Policy Layer

The policy layer defines quota policies as declarative documents. Each policy specifies:
- The quota type (disk, memory, blob, etc.)
- The target scope (system, domain, namespace, tenant, resource)
- The limit value and unit
- The enforcement mode (hard, soft, grace, throttle)
- The escalation thresholds (warning, critical levels)
- The override requirements (approval level, audit trail)

### 4.2 Quota Enforcement Layer

The enforcement layer evaluates every storage operation against applicable quotas before the operation reaches the Provider. It maintains a real-time utilization counter for each quota and applies the configured enforcement mode when limits are approached or exceeded.

### 4.3 Quota Monitoring Layer

The monitoring layer collects utilization data from the enforcement layer and emits metrics through the observability subsystem (RFC-0414). It tracks utilization percentages, trend rates, and quota violation counts.

### 4.4 Quota Escalation Layer

The escalation layer manages the progression from informational states through warnings to hard rejections. It triggers events (RFC-0413) at each escalation level and notifies operators through the alerting system.

### 4.5 Quota Override Layer

The override layer handles administrative quota exceptions. Overrides require authentication, authorization, audit logging, and optional approval workflows depending on the quota sensitivity level.

\\\mermaid
graph TB
    subgraph Quota Architecture
        P["Policy Layer<br/>Declarative quota documents"]
        E["Enforcement Layer<br/>Real-time limit evaluation"]
        M["Monitoring Layer<br/>Utilization metrics"]
        S["Escalation Layer<br/>Warning-to-rejection progression"]
        O["Override Layer<br/>Administrative exceptions"]
    end

    P --> E
    E --> M
    M --> S
    S --> E
    O --> E
    
    style Policy Layer fill:#e3f2fd
    style Enforcement Layer fill:#fff3e0
    style Monitoring Layer fill:#e8f5e9
    style Escalation Layer fill:#fce4ec
    style Override Layer fill:#f3e5f5
\\\

---

| WORKSPACE | 3% | 2% | 3% | User preferences |
| KNOWLEDGE | 10% | 10% | 10% | Vector indices are large |
| MARKETPLACE | 5% | 2% | 5% | Package metadata |
| USER | 5% | 5% | 10% | Sessions and credentials |
| SYSTEM | 5% | 10% | 10% | Audit logs accumulate |
| ADMIN | 2% | 1% | 4% | Policy and compliance data |

### 5.3 Namespace Level

Namespaces (RFC-0422) within each domain share the domain's quota allocation. Sub-namespaces may further partition the namespace quota.

### 5.4 Tenant Level

Tenants within a namespace share the namespace quota. Multi-tenant deployments MUST enforce per-tenant quotas to prevent resource monopolization.

### 5.5 Resource Level

Individual resource types within a tenant may have specific quota limits (e.g., maximum snapshot count per resource, maximum blob size).

---


### 6.7 Cache Entry Quota (QT-CACHE-ENTRIES)

Maximum number of cache entries across all cache layers. Prevents unbounded cache growth.

### 6.8 Operations Per Second Quota (QT-OPERATIONS)

Maximum sustained and burst operation rates. Enforced at the namespace or tenant level to prevent individual consumers from overwhelming the system.

### 6.9 Connection Pool Quota (QT-CONNECTIONS)

Maximum concurrent provider connections per namespace or tenant. Prevents connection exhaustion.

### 6.10 Entity Count Quota (QT-ENTITIES)

Maximum number of managed entities (resources) per namespace or tenant. Limits the total addressable resource count.

### 6.11 Bandwidth Quota (QT-BANDWIDTH)

Data transfer rate limit in bytes per second. Primarily applies to replication (RFC-0418) and backup/restore (RFC-0411, RFC-0412) operations.

---

    C -->|"No"| E{"Enforcement Mode"}
    E -->|"Hard"| F["Reject: STOR-CAP-EXCEEDED"]
    E -->|"Soft"| G["Allow + Emit Warning"]
    E -->|"Grace"| H["Allow + Start Grace Timer"]
    E -->|"Throttle"| I["Queue + Increase Wait Time"]
    G --> J["Continue"]
    H --> K{"Grace Period Expired?"}
    K -->|"No"| J
    K -->|"Yes"| F
    I --> J
    
    style Within fill:#c8e6c9
    style Reject fill:#ffcdd2
    style Warning fill:#fff9c4
    style Throttle fill:#e1f5fe
\\\

---

---

    Critical --> Warning : Utilization decreases
    Warning --> Monitored : Utilization decreases
    Monitored --> Normal : Utilization decreases
    
    note right of Normal
        Standard operation
        No alerts
    end note
    note right of Warning
        Warning events
        Operator notification
    end note
    note right of Critical
        Grace period
        Throttling may engage
    end note
    note right of Emergency
        Hard enforcement
        Writes rejected
    end note
    note right of Blocked
        Manual intervention
        Required
    end note
\\\

---

### AC-0424-06: Override Audit Trail
- **Requirement**: Every quota override MUST be recorded in the audit log with full justification and approval details.
- **Verification**: Perform overrides and inspect audit logs.
- **Expected Result**: Complete audit records for all override actions.

---

- Runtime core lifecycle (covered by RFC-0002).
- Plugin loading (covered by RFC-0201).


## 13 Future Evolution

Future specifications will address advanced quota topics:

- **Dynamic Quota Adjustment**: Automatic quota resizing based on utilization trends and workload patterns.
- **Quota Borrowing**: Temporary quota sharing between domains during peak demand.
- **Cross-Region Quotas**: Quota management across geographically distributed storage deployments.
- **AI-Driven Quota Optimization**: Machine learning-based quota recommendations and anomaly detection.
- **Quota Marketplaces**: Internal quota trading between tenants in multi-tenant environments.
- **Carbon-Aware Quotas**: Quota limits incorporating energy consumption and sustainability metrics.


\\\

    style Warn fill:#fff9c4
    style Critical fill:#ffab91
\\\


---


- All normative requirements defined in this RFC and its dependent RFCs.

---

## Future Evolution

Future specifications will address:
- **Dynamic Quota Adjustment**: Automated quota adjustment based on usage patterns.
- **Quota Forecasting**: Predictive quota planning based on utilization trends.
- **Cross-Quota Policies**: Policies governing quota interactions across organizational boundaries.

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

---

## Acceptance Criteria

### AC-0424-01: Quota Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Quota enforcement MUST prevent all quota violations. | Quota bypass test. |
| AC-02 | Quota modifications MUST require elevated authorization. | Authorization test. |
| AC-03 | Quota operations MUST be recorded in the audit log. | Audit log verification test. |
| AC-04 | Quota enforcement latency MUST not block storage operations. | Enforcement latency test. |
| AC-05 | Quota utilization tracking MUST be efficient. | Utilization tracking performance test. |
| AC-06 | Quota violation responses MUST complete within bounded time. | Violation response test. |

---

## References

| Reference | Description |
|---|---|
| RFC-0401 | Storage Overview |
| RFC-0402 | Storage Architecture |
| RFC-0409 | Storage Security |
| RFC-0421 | Storage Domains |
| RFC-0422 | Storage Namespace |
| RFC-0423 | Storage Resource Model |
| ADR-0010 | Contract-First Specification |
| ADR-0012 | Security Architecture |
| schemas/storage/quota.json | Quota Schema Definition |
| catalog/storage-quota.md | Quota Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0401, RFC-0402, RFC-0409, RFC-0421, RFC-0422, RFC-0423 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/storage/quota.json |
| Related Catalog | catalog/storage-quota.md |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.0.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Security, Performance, Compatibility, Compliance, Runtime Independence, Acceptance Criteria, References, Compliance Matrix, Revision History |





