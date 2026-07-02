# RFC-0421: Storage Domains

RFC: RFC-0421
Title: Storage Domains
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
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0010 Contract-First Specification
Related JSON Schema:
  - schemas/storage/domains.json
Related Catalog:
  - catalog/storage-domains.md
Layer: Core
Audience: Storage developers, architects, specification reviewers
Target Release: 1.0.0
Review Cycle: Quarterly
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas implementation MUST conform to the domain model, isolation guarantees, namespace assignment, and cross-domain interaction rules defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Authority
This RFC is the authoritative specification for the Storage Domains domain.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301.

| Term | Definition | Source |
|---|---|---|
| Domain | A logical partition of storage resources with independent namespace and quota. | RFC-0421 |
| Domain Isolation | The guarantee that resources in one domain cannot access resources in another domain without explicit permission. | RFC-0421 |
| Domain Boundary | The conceptual and operational limit separating one domain from another. | RFC-0421 |
| Cross-Domain Operation | An operation that accesses resources spanning multiple domains. | RFC-0421 |
| Namespace | The hierarchical addressing scheme for resources within a domain. | RFC-0422 |
| Quota | A limit on the amount of storage resources a domain or user may consume. | RFC-0424 |
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

## 1 Introduction

The Atlas Storage subsystem organizes resources into logical partitions called domains. Each domain provides an isolated namespace, independent quota management, and distinct security boundaries. Domains enable multi-tenant storage where different subsystems or users operate within their own storage context without interfering with each other.

This RFC defines the domain model, isolation guarantees, and cross-domain interaction rules that govern how domains are created, managed, and accessed.

### 1.1 Domain Model

A domain is a first-class storage entity that encapsulates:

- **Namespace**: A hierarchical addressing space unique within the domain.
- **Quota**: A configurable limit on resource consumption.
- **Security Boundary**: Access control policies that isolate resources from other domains.
- **Schema Binding**: Association with schema definitions for data validation.

### 1.2 Domain Isolation

Domain isolation is a fundamental security and operational guarantee. Resources in one domain MUST NOT be accessible from another domain without explicit cross-domain authorization. Isolation is enforced at every layer of the Storage stack.

### 1.3 Cross-Domain Operations

Cross-domain operations are permitted only when explicitly authorized. They require elevated permissions and produce audit log entries documenting the cross-domain access.

---

## 2 Domain Lifecycle

Domains follow a formal lifecycle:

1. **Created**: A domain is registered with its initial configuration (namespace root, quota limits, access policies).
2. **Active**: The domain is operational and accepting storage operations.
3. **Paused**: The domain is temporarily disabled; no new operations are accepted but existing data is preserved.
4. **Archived**: The domain is archived for historical preservation; data is read-only.
5. **Deleted**: The domain is removed; all resources are deleted or transferred according to policy.

---

## 3 Namespace Assignment

Each domain is assigned a namespace root. All resources within the domain are addressed through paths under this root. Namespace assignment follows the rules defined in RFC-0422.

---

## 4 Quota Management

Each domain has associated quota limits defined in RFC-0424. Quotas apply to resource count, data volume, and operational throughput.

---

## 5 Cross-Domain Interaction

Cross-domain operations follow these rules:

- **Explicit Authorization**: Every cross-domain operation MUST be explicitly authorized by the target domain's access control policy.
- **Audit Logging**: All cross-domain operations MUST produce audit log entries.
- **Isolation Enforcement**: Cross-domain operations MUST NOT compromise domain isolation guarantees.

---

## 6 Domain Configuration

Domains are configured with:

- **Name**: A unique identifier within the Storage subsystem.
- **Description**: Human-readable description of the domain's purpose.
- **Namespace Root**: The top-level path for resources in this domain.
- **Quota Limits**: Maximum resource count, data volume, and throughput.
- **Access Policies**: Rules governing who can access the domain and what operations are permitted.
- **Schema Bindings**: Default schemas for resources created in this domain.

---

## 7 Domain Enumeration

Consumers MUST be able to enumerate available domains, retrieve domain configuration, and query domain status. Domain enumeration is subject to the same access control as other Storage operations.

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for:
- Defining the domain model including domain creation, configuration, and lifecycle.
- Specifying domain isolation guarantees and cross-domain interaction rules.
- Defining namespace assignment within domains.
- Establishing quota enforcement boundaries per domain.

### Non-Responsibilities
This specification IS NOT responsible for:
- Defining namespace hierarchy (delegated to RFC-0422).
- Defining resource models (delegated to RFC-0423).
- Managing quota enforcement (delegated to RFC-0424).
- Implementing domain-level storage backends (delegated to the Provider interface).

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0401 | Consumed | Storage Overview (domain context) |
| RFC-0402 | Consumed | Storage Architecture (domain layer placement) |
| RFC-0422 | Consumed | Storage Namespace (namespace within domains) |
| RFC-0423 | Consumed | Storage Resource Model (resources within domains) |
| RFC-0424 | Consumed | Storage Quota (quota per domain) |

### Consumers
- RFC-0422 Storage Namespace (namespaces belong to domains)
- RFC-0423 Storage Resource Model (resources belong to domains)
- RFC-0424 Storage Quota (quotas apply to domains)
- RFC-0425 Storage Capability Discovery (capabilities scoped to domains)

### Providers
- schemas/storage/domains.json (domain schema)
- catalog/storage-domains.md (domains catalog)

### Forbidden Dependencies
- Domains MUST NOT depend on implementation-specific namespace schemes.
- Cross-domain operations MUST be explicitly authorized and audited.

---

## Security

This specification defines security requirements for domains:

- **Domain Isolation**: Resources in one domain MUST NOT be accessible from another domain without explicit cross-domain authorization.
- **Cross-Domain Audit**: All cross-domain operations MUST be recorded in the audit log with full details.
- **Domain Boundary Enforcement**: Domain boundaries MUST be enforced at every layer of the Storage stack.

---

## Performance

This specification defines performance requirements for domains:

- **Domain Lookup Efficiency**: Domain resolution MUST be efficient with O(1) access to domain configuration.
- **Cross-Domain Overhead**: Cross-domain operations MUST incur bounded overhead relative to intra-domain operations.
- **Isolation Efficiency**: Domain isolation enforcement MUST not significantly degrade performance.

---

## Compatibility

This specification defines compatibility requirements:

- **Domain Model Stability**: The domain model MUST remain stable within a major version.
- **Isolation Semantics**: Domain isolation guarantees MUST remain consistent across minor versions.

---

## Compliance

This specification requires compliance with:

- The Atlas Development System (ADS) Constitution.
- ADR-0010 (Contract-First Specification-Driven Development).
- ADR-0012 (Security Architecture).
- All normative requirements defined in this RFC and its dependent RFCs.

---

## Future Evolution

Future specifications will address:
- **Domain Hierarchies**: Support for nested domains with inherited policies.
- **Domain Federation**: Cross-cluster domain coordination for distributed deployments.
- **Domain Analytics**: Metrics and insights into domain usage patterns.

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

### AC-0421-01: Domain Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Domain isolation MUST prevent cross-domain resource access without authorization. | Isolation enforcement test. |
| AC-02 | Cross-domain operations MUST be recorded in the audit log. | Audit log verification test. |
| AC-03 | Domain boundaries MUST be enforced at every Storage layer. | Layer boundary verification test. |
| AC-04 | Domain lookup MUST complete within bounded time. | Domain lookup performance test. |
| AC-05 | Cross-domain operations MUST incur bounded overhead. | Cross-domain overhead test. |
| AC-06 | Domain configuration MUST remain stable within major versions. | Configuration stability test. |

---

## References

| Reference | Description |
|---|---|
| RFC-0401 | Storage Overview |
| RFC-0402 | Storage Architecture |
| RFC-0422 | Storage Namespace |
| RFC-0423 | Storage Resource Model |
| RFC-0424 | Storage Quota |
| RFC-0425 | Storage Capability Discovery |
| ADR-0010 | Contract-First Specification |
| ADR-0012 | Security Architecture |
| schemas/storage/domains.json | Domain Schema Definition |
| catalog/storage-domains.md | Domains Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0401, RFC-0402, RFC-0422, RFC-0423, RFC-0424, RFC-0425 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/storage/domains.json |
| Related Catalog | catalog/storage-domains.md |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.0.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Security, Performance, Compatibility, Compliance, Runtime Independence, Acceptance Criteria, References, Compliance Matrix, Revision History |



