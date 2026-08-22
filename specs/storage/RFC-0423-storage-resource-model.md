# RFC-0423: Storage Resource Model

RFC: RFC-0423
Title: Storage Resource Model
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
  - RFC-0405 Storage Schema
  - RFC-0421 Storage Domains
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0010 Contract-First Specification
Related JSON Schema:
  - schemas/storage/resource.json
Related Catalog:
  - catalog/storage-resource-model.md
Layer: Core
Audience: Storage developers, architects, specification reviewers
Target Release: 1.0.0
Review Cycle: Quarterly
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas implementation MUST conform to the resource model, resource identification, attribute management, and resource relationship rules defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Authority
This RFC is the authoritative specification for the Storage Resource Model domain.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301.

| Term | Definition | Source |
|---|---|---|
| Resource | A unit of data managed by Storage, identified by a unique resource identifier. | RFC-0423 |
| Resource Identifier | A unique identifier assigned to a resource within a namespace. | RFC-0423 |
| Resource Attribute | A named property associated with a resource, carrying structured data. | RFC-0423 |
| Resource Relationship | A defined association between two or more resources. | RFC-0423 |
| Resource Type | A classification of resources based on their schema and behavior. | RFC-0423 |
| Resource Metadata | System-managed attributes associated with a resource, including creation time and version. | RFC-0423 |
| Schema | A declarative definition of the structure, types, and constraints for stored resources. | RFC-0405 |
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

The Storage Resource Model defines how data is organized, identified, and managed within the Atlas platform. Every unit of stored data is a resource, characterized by a unique identifier, a set of attributes, relationships to other resources, and metadata managed by the Storage subsystem.

### 1.1 Resource Identification

Each resource has a unique identifier within its namespace. The identifier is assigned at resource creation and remains constant throughout the resource lifecycle. Identifiers are opaque to consumers; they MUST NOT be interpreted or constructed by consumers.

### 1.2 Resource Attributes

Resources carry a set of named attributes that define their data content. Attributes are typed and validated against the resource's bound schema. Attribute values are immutable once set; modifications create new resource versions.

### 1.3 Resource Relationships

Resources MAY be associated with other resources through defined relationship types. Relationships are directional and subject to integrity constraints. Circular relationships are prohibited.

### 1.4 Resource Metadata

The Storage subsystem manages system-level metadata for each resource, including creation timestamp, modification timestamp, version number, and lifecycle state. This metadata is managed automatically and MUST NOT be modified by consumers.

---

## 2 Resource Types

Resources are classified into types based on their schema and behavior. Each type defines:

- **Schema**: The data structure and validation rules.
- **Attributes**: The set of attribute names and their types.
- **Relationships**: Allowed relationship types and cardinality.
- **Lifecycle**: Applicable state transitions.

---

## 3 Resource Operations

The resource model supports the following operations:

- **Create**: Create a new resource with specified attributes and relationships.
- **Read**: Retrieve a resource by identifier, including attributes and metadata.
- **Update**: Modify resource attributes (creates a new version).
- **Delete**: Remove a resource and its relationships.
- **List**: Enumerate resources matching specified criteria.
- **Relate**: Create or remove a relationship between resources.
- **Version**: Retrieve a specific version of a resource.

---

## 4 Attribute Management

Attributes are managed as typed key-value pairs. Each attribute has:

- **Name**: A unique identifier within the resource type.
- **Type**: The data type of the attribute value.
- **Value**: The current attribute value.
- **Constraints**: Validation rules and mutability flags.

---

## 5 Relationship Management

Relationships between resources are managed through a relationship store. Each relationship has:

- **Source**: The originating resource identifier.
- **Target**: The target resource identifier.
- **Type**: The relationship type (e.g., depends-on, contains, references).
- **Metadata**: Additional relationship attributes.

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for:
- Defining the resource model including resource identification, attributes, and relationships.
- Specifying resource type classification and schema binding.
- Defining resource metadata management including system-managed attributes.
- Establishing resource lifecycle integration with the domain model.

### Non-Responsibilities
This specification IS NOT responsible for:
- Defining schema structure (delegated to RFC-0405).
- Managing namespace resolution (delegated to RFC-0422).
- Enforcing quotas (delegated to RFC-0424).
- Implementing storage backends (delegated to the Provider interface).

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0401 | Consumed | Storage Overview (resource context) |
| RFC-0402 | Consumed | Storage Architecture (resource layer placement) |
| RFC-0405 | Consumed | Storage Schema (resource schema binding) |
| RFC-0421 | Consumed | Storage Domains (resources within domains) |
| RFC-0422 | Consumed | Storage Namespace (resource addressing) |

### Consumers
- RFC-0424 Storage Quota (quota enforcement on resources)
- RFC-0425 Storage Capability Discovery (capability scoping to resource types)
- All Storage consumers operating on resources

### Providers
- schemas/storage/resource.json (resource schema)
- catalog/storage-resource-model.md (resource model catalog)

### Forbidden Dependencies
- Resource identifiers MUST NOT depend on any specific identifier scheme.
- Resource attributes MUST NOT be tied to any specific data serialization format.

---

## Security

This specification defines security requirements for resources:

- **Resource Access Control**: Every resource operation MUST be subject to authorization checks.
- **Metadata Integrity**: System-managed resource metadata MUST be tamper-evident.
- **Relationship Integrity**: Resource relationships MUST be validated before creation to prevent circular or unauthorized associations.

---

## Performance

This specification defines performance requirements for resources:

- **Resource Lookup Efficiency**: Resource identification and lookup MUST be efficient with bounded latency.
- **Attribute Access**: Resource attribute access MUST complete within bounded time.
- **Relationship Traversal**: Resource relationship traversal MUST be efficient for common access patterns.

---

## Compatibility

This specification defines compatibility requirements:

- **Resource Model Stability**: The resource model MUST remain stable within a major version.
- **Identifier Format Stability**: Resource identifier formats MUST remain compatible across minor versions.

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
- **Resource Templates**: Predefined resource definitions for common use cases.
- **Resource Inheritance**: Support for resource type inheritance hierarchies.
- **Resource Indexing**: Optimized indexing for resource attribute queries.

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

### AC-0423-01: Resource Model Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Every resource MUST have a unique identifier within its namespace. | Uniqueness verification test. |
| AC-02 | Resource attributes MUST be validated against the bound schema. | Schema validation test. |
| AC-03 | Resource relationships MUST be validated for integrity. | Relationship integrity test. |
| AC-04 | Resource metadata MUST be tamper-evident. | Metadata integrity test. |
| AC-05 | Resource lookup MUST complete within bounded latency. | Lookup performance test. |
| AC-06 | Resource access MUST be subject to authorization checks. | Authorization test. |

---

## References

| Reference | Description |
|---|---|
| RFC-0401 | Storage Overview |
| RFC-0402 | Storage Architecture |
| RFC-0405 | Storage Schema |
| RFC-0421 | Storage Domains |
| RFC-0422 | Storage Namespace |
| RFC-0424 | Storage Quota |
| RFC-0425 | Storage Capability Discovery |
| ADR-0010 | Contract-First Specification |
| ADR-0012 | Security Architecture |
| schemas/storage/resource.json | Resource Schema Definition |
| catalog/storage-resource-model.md | Resource Model Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0401, RFC-0402, RFC-0405, RFC-0421, RFC-0422, RFC-0424, RFC-0425 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/storage/resource.json |
| Related Catalog | catalog/storage-resource-model.md |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.0.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Security, Performance, Compatibility, Compliance, Runtime Independence, Acceptance Criteria, References, Compliance Matrix, Revision History |



