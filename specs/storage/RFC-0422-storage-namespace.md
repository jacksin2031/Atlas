# RFC-0422: Storage Namespace

RFC: RFC-0422
Title: Storage Namespace
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
  - RFC-0421 Storage Domains
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0010 Contract-First Specification
Related JSON Schema:
  - schemas/storage/namespace.json
Related Catalog:
  - catalog/storage-namespace.md
Layer: Core
Audience: Storage developers, architects, specification reviewers
Target Release: 1.0.0
Review Cycle: Quarterly
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas implementation MUST conform to the namespace model, hierarchical addressing, path resolution, and namespace isolation rules defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Authority
This RFC is the authoritative specification for the Storage Namespace domain.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301.

| Term | Definition | Source |
|---|---|---|
| Namespace | The hierarchical addressing scheme for resources within a domain. | RFC-0422 |
| Namespace Path | A hierarchical identifier resolving to a resource within a namespace. | RFC-0422 |
| Namespace Root | The top-level entry point of a namespace within a domain. | RFC-0422 |
| Namespace Isolation | The guarantee that namespaces in different domains do not conflict. | RFC-0422 |
| Path Resolution | The process of resolving a namespace path to a specific resource. | RFC-0422 |
| Namespace Entry | A node in the namespace hierarchy representing a resource or a sub-namespace. | RFC-0422 |
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

The Storage namespace provides a hierarchical addressing scheme for resources within each domain. Namespaces enable intuitive resource location through path-based addressing while maintaining strict isolation between domains.

### 1.1 Namespace Hierarchy

Namespaces are organized as a tree structure rooted at the domain level. Each node in the tree represents either a resource or a sub-namespace. Paths are resolved from the namespace root through successive hierarchy levels.

### 1.2 Path Resolution

Path resolution converts a hierarchical path string into a resource identifier. The resolver traverses the namespace tree from the root, validating each segment, and returns the target resource or an error if the path is invalid.

### 1.3 Namespace Isolation

Namespaces in different domains are fully isolated. The same path in different domains resolves to different resources. Cross-domain path resolution is prohibited.

---

## 2 Namespace Operations

The namespace supports the following operations:

- **Resolve**: Convert a namespace path to a resource identifier.
- **Create**: Create a new namespace entry (resource or sub-namespace).
- **Delete**: Remove a namespace entry and all its children.
- **List**: Enumerate entries under a namespace path.
- **Exists**: Check if a path resolves to an existing entry.
- **Move**: Relocate an entry to a different path.
- **Copy**: Duplicate an entry to a different path.

---

## 3 Path Validation

All namespace paths MUST be validated before resolution. Validation rules include:

- Paths MUST use a consistent separator convention.
- Path segments MUST not contain reserved characters.
- Paths MUST not contain parent directory references.
- Paths MUST not exceed the maximum allowed depth.

---

## 4 Namespace Entries

Each namespace entry has:

- **Type**: Resource or sub-namespace.
- **Path**: The full hierarchical path within the domain.
- **Resource ID**: The identifier of the target resource (for resource entries).
- **Metadata**: System-managed attributes including creation time and modification time.

---

## 5 Namespace Lifecycle

Namespace entries follow the resource lifecycle defined in RFC-0404. Deleting a namespace entry triggers the resource deletion lifecycle. Sub-namespaces are recursively deleted when their parent is deleted.

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for:
- Defining the namespace model including hierarchy, path resolution, and entry management.
- Specifying namespace isolation between domains.
- Defining path validation and normalization rules.
- Establishing namespace lifecycle management (creation, modification, deletion).

### Non-Responsibilities
This specification IS NOT responsible for:
- Defining domain boundaries (delegated to RFC-0421).
- Managing resource data content (delegated to the Resource Model).
- Enforcing quotas (delegated to RFC-0424).

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0401 | Consumed | Storage Overview (namespace context) |
| RFC-0402 | Consumed | Storage Architecture (namespace layer placement) |
| RFC-0421 | Consumed | Storage Domains (namespaces within domains) |
| RFC-0423 | Consumed | Storage Resource Model (resources addressed by namespace) |

### Consumers
- RFC-0423 Storage Resource Model (resources addressed through namespace paths)
- RFC-0424 Storage Quota (quota enforcement per namespace)
- RFC-0425 Storage Capability Discovery (capability scoping by namespace)

### Providers
- schemas/storage/namespace.json (namespace schema)
- catalog/storage-namespace.md (namespace catalog)

### Forbidden Dependencies
- Namespace paths MUST NOT depend on any specific path separator convention.
- Namespace resolution MUST NOT assume any specific underlying storage structure.

---

## Security

This specification defines security requirements for namespaces:

- **Namespace Isolation**: Resources in one namespace MUST NOT be accessible from another namespace without explicit authorization.
- **Path Injection Prevention**: Namespace path inputs MUST be validated against path injection attacks.
- **Namespace Audit Trail**: All namespace operations (create, modify, delete, resolve) MUST be recorded in the audit log.

---

## Performance

This specification defines performance requirements for namespaces:

- **Path Resolution Efficiency**: Namespace path resolution MUST complete within bounded time proportional to path depth.
- **Namespace Lookup Efficiency**: Namespace entry lookup MUST be efficient with logarithmic or better complexity.
- **Hierarchical Depth**: Namespace hierarchies MUST support defined maximum depths without performance degradation.

---

## Compatibility

This specification defines compatibility requirements:

- **Path Format Stability**: Namespace path formats MUST remain stable within a major version.
- **Resolution Semantics**: Path resolution semantics MUST remain consistent across minor versions.

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
- **Namespace Aliases**: Support for multiple path names resolving to the same resource.
- **Namespace Templates**: Reusable namespace definitions for common organizational patterns.
- **Namespace Search**: Full-text search within namespace hierarchies.

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

### AC-0422-01: Namespace Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Namespace isolation MUST prevent cross-namespace access without authorization. | Isolation enforcement test. |
| AC-02 | Path resolution MUST correctly resolve all valid namespace paths. | Path resolution test suite. |
| AC-03 | Namespace operations MUST be recorded in the audit log. | Audit log verification test. |
| AC-04 | Path injection attacks MUST be prevented. | Path injection test. |
| AC-05 | Path resolution latency MUST be bounded by path depth. | Resolution latency test. |
| AC-06 | Namespace hierarchies MUST support defined maximum depths. | Depth limit test. |

---

## References

| Reference | Description |
|---|---|
| RFC-0401 | Storage Overview |
| RFC-0402 | Storage Architecture |
| RFC-0421 | Storage Domains |
| RFC-0423 | Storage Resource Model |
| RFC-0424 | Storage Quota |
| RFC-0425 | Storage Capability Discovery |
| ADR-0010 | Contract-First Specification |
| ADR-0012 | Security Architecture |
| schemas/storage/namespace.json | Namespace Schema Definition |
| catalog/storage-namespace.md | Namespace Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0401, RFC-0402, RFC-0421, RFC-0423, RFC-0424, RFC-0425 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/storage/namespace.json |
| Related Catalog | catalog/storage-namespace.md |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.0.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Security, Performance, Compatibility, Compliance, Runtime Independence, Acceptance Criteria, References, Compliance Matrix, Revision History |



