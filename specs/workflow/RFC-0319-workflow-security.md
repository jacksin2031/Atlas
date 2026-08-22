RFC: RFC-0319
Title: Workflow Security
Status: Proposed
Version: 1.1.0
Author: 
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Permission | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Capability | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Role | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Policy | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Sandbox | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Secret | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Encryption Key | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Access Control | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Authentication | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Authorization | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Threat Model | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Security Level | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0007 Runtime IPC Architecture
  - RFC-0008 Runtime Plugin Host
  - RFC-1001 Common Event Model
  - RFC-1003 Common Capability Model
  - RFC-1005 Common Manifest Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0307 Workflow Context
  - RFC-0308 Workflow Events
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0317 Workflow Validation
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0322 Workflow Extension
  - RFC-0323 Workflow Plugin Integration
  - RFC-0324 Workflow Storage
  - RFC-0327 Workflow IPC
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
  - ADR-0010 Security Architecture
Related JSON Schema:
  - schemas/workflow/permission.json
  - schemas/workflow/sandbox-policy.json
  - schemas/workflow/data-classification.json
Related Catalog:
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development

  - catalog/workflow-permissions.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the security requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0319 workflow security.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301 (Workflow Overview).

| Term | Definition | Source |
|---|---|---|
| Security | The set of controls, policies, and mechanisms that protect workflow definitions, execution state, and data from unauthorized access, modification, or destruction. | RFC-0301 |
| Permission | A granted authority allowing an actor to perform a specific operation on a workflow entity. | RFC-0301 |
| Capability | A declared ability or privilege that a workflow, node, or actor possesses. | RFC-0301 |
| Sandbox | An isolated execution environment that restricts what a workflow node can access or modify. | RFC-0301 |
| Authentication | The process of verifying the identity of an actor (user, system, or node). | This RFC |
| Authorization | The process of verifying that an authenticated actor has the required permissions for an operation. | This RFC |
| Least Privilege | The principle that every actor MUST operate with the minimum permissions necessary to accomplish its task. | This RFC |
| Data Classification | The categorization of workflow data by sensitivity level to determine appropriate protection measures. | This RFC |
| Audit Trail | An immutable, chronologically ordered record of security-relevant events. | This RFC |
| Secret | Encoded credential or sensitive value (API key, password, token) used by workflow nodes. | This RFC |
| Threat Model | A structured analysis of potential security threats to a workflow definition or execution. | This RFC |
| Security Boundary | A conceptual or physical partition that isolates trust domains within the workflow system. | This RFC |

---

## 2 Security Overview

The Workflow Security specification defines the security model for Atlas workflows. Security ensures that workflow execution respects permission constraints, data protection requirements, organizational policies, and the principle of least privilege.

This specification establishes the authoritative security contract for all workflow components. Every subsystem that participates in workflow execution MUST implement the security controls defined herein.

Key principles:

- Workflow execution MUST respect permission constraints enforced by the capability model.
- Nodes MUST operate within sandbox boundaries that restrict their access surface.
- Data MUST be protected at rest, in transit, and during processing.
- An immutable audit trail MUST record all security-relevant actions.
- The principle of least privilege MUST govern all permission grants.
- Secrets MUST never be transmitted in plaintext or logged in any form.

---

## 3 Security Controls

### 3.1 Required Controls

Every workflow implementation MUST enforce the following security controls:

| Control | Description | Enforcement Point | Mandatory |
|---|---|---|---|
| Authentication | Verify identity of workflow initiators, nodes, and actors | Workflow creation, node registration | YES |
| Authorization | Verify permissions for every workflow operation | Every operation | YES |
| Sandboxing | Isolate node execution from host and sibling nodes | Node execution | YES |
| Data Encryption | Encrypt data at rest and in transit | Storage, IPC channels | YES |
| Audit Logging | Record all security-relevant actions | All operations | YES |
| Resource Limits | Bound resource consumption per node to prevent DoS | Scheduling (RFC-0312) | YES |
| Input Validation | Validate all inputs before execution | Validation phase (RFC-0317) | YES |
| Output Sanitization | Sanitize all outputs before emission | Action completion | YES |
| Secret Management | Manage, rotate, and revoke workflow secrets | Runtime (RFC-0304) | YES |
| Threat Assessment | Evaluate threat models for new or modified workflows | Design-time | SHOULD |

### 3.2 Control Enforcement

Security controls MUST be enforced in the following order:

1. Authentication (identity verification)
2. Authorization (permission verification)
3. Sandboxing (environment isolation)
4. Input Validation (data integrity)
5. Execution (constrained by resource limits)
6. Output Sanitization (data protection)
7. Audit Logging (event recording)

If any control fails, the operation MUST be aborted and a security event MUST be emitted per RFC-0321.

---

## 4 Permission Model

### 4.1 Permission Types

| Permission | Description | Scope | Granularity |
|---|---|---|---|
| CREATE | Create workflow instances and definitions | Workflow | Instance-level |
| EXECUTE | Execute specific workflow nodes | Node | Node-type-level |
| READ | Read workflow state, context, and results | Workflow | Entity-level |
| WRITE | Modify workflow state and context | Workflow | Entity-level |
| DELETE | Delete workflow instances and definitions | Workflow | Entity-level |
| ADMIN | Administrative operations on the workflow system | System | Role-level |
| INVOKE | Invoke a specific action or trigger type | Action/Trigger | Type-level |
| MANAGE_SECRETS | Create, read, rotate, and revoke secrets | Secret | Secret-level |

### 4.2 Permission Assignment

Permissions MUST be assigned using a Role-Based Access Control (RBAC) model:

- Roles are collections of permissions.
- Actors (users, services, nodes) are assigned to one or more roles.
- Effective permissions for an actor are the union of all role permissions.
- No actor MAY inherit permissions beyond the union of their assigned roles.

### 4.3 Permission Inheritance

- Permissions are inherited from parent contexts downward.
- Child contexts CAN have more restrictive permissions (subtraction).
- Permissions CANNOT be elevated beyond the parent scope (no privilege escalation).
- Workflow-level permissions DO NOT grant node-level EXECUTE permissions unless explicitly declared.

### 4.4 Capability-Based Security

In addition to RBAC, workflow security uses a capability-based model:

- Each node declares the capabilities it requires in its manifest.
- The runtime (RFC-0304) grants capabilities only if the workflow's permission model permits.
- Capabilities are scoped to the workflow instance lifetime and are revoked upon termination.

---

## 5 Sandbox Model

### 5.1 Sandbox Boundaries

| Level | Boundary | Enforcement Mechanism | Isolation Guarantee |
|---|---|---|---|
| Workflow | Between workflow instances | Namespace isolation | Full |
| Node | Between sibling nodes | Capability restriction | Complete |
| Data | Between data flows | Encryption and access control | Partial |
| IPC | Between process boundaries | Authentication and message signing | Full |
| Extension | Between third-party extensions (RFC-0322) | Restricted capability set | Complete |

### 5.2 Sandbox Policies

- File system access IS restricted to declared resources per the manifest (RFC-1005).
- Network access IS controlled by security policy and MUST be explicitly declared.
- Environment variable access IS limited to declared secrets and configuration.
- System call access IS restricted per node type catalog (catalog/workflow-node-types.md).
- Memory access IS isolated between nodes; no shared mutable state without explicit declaration.

### 5.3 Sandbox Escape Prevention

Implementations MUST prevent sandbox escape through:

- Resource quota enforcement per RFC-0320.
- System call filtering or seccomp profiles.
- Network namespace isolation.
- Capability bounding sets.
- Mandatory access control (SELinux/AppArmor equivalent).

---

## 6 Data Protection

### 6.1 Encryption Requirements

| Data State | Encryption Algorithm | Key Management |
|---|---|---|
| At Rest | AES-256-GCM or ChaCha20-Poly1305 | Per-secret rotation |
| In Transit | TLS 1.3 or equivalent | Certificate validation |
| In Memory | Best effort (memory locking, zero-on-free) | Runtime-managed |
| Checkpoints (RFC-0315) | Same as at rest | Same as at rest |

### 6.2 Data Classification

| Classification | Description | Handling Requirements |
|---|---|---|
| Public | No sensitivity restrictions | No special handling |
| Internal | Organizational use only | Access logging required |
| Confidential | Sensitive business/personal data | Encryption at rest and transit required |
| Restricted | Highly sensitive (regulated data) | Strict access control, audit, encryption, retention policy |

### 6.3 Secret Management

- Secrets MUST be managed through the secret management system defined in RFC-0307 (Context).
- Secrets MUST be rotated at intervals defined by organizational policy (minimum: 90 days).
- Secrets MUST NEVER appear in logs, metrics, or error messages.
- Secret references in workflow definitions MUST use opaque identifiers, NOT plaintext values.

---

## 7 Audit Trail

### 7.1 Audited Events

| Event | Description | Severity | Retention |
|---|---|---|---|
| Workflow.Created | New workflow instance created | Info | Policy-defined |
| Workflow.Executed | Workflow node executed | Info | Policy-defined |
| Permission.Granted | Permission granted to actor | Warning | Policy-defined |
| Permission.Denied | Permission denied to actor | Error | Policy-defined |
| Sandbox.Breach | Sandbox boundary violation detected | Critical | Permanent |
| Data.Accessed | Sensitive data accessed | Warning | Policy-defined |
| Secret.Rotated | Secret rotation completed | Info | Policy-defined |
| Secret.Compromised | Secret compromise detected | Critical | Permanent |
| Workflow.Terminated | Workflow instance terminated | Info | Policy-defined |
| Extension.Loaded | Third-party extension loaded (RFC-0322) | Warning | Policy-defined |

### 7.2 Audit Log Properties

- Audit logs MUST be append-only and tamper-evident (cryptographic hash chain).
- Audit logs MUST include: timestamp, actor, action, resource, result, correlation ID.
- Audit logs MUST be queryable by all dimensions for compliance reporting (RFC-0330).
- Audit log retention periods MUST comply with applicable regulatory requirements.

---

## 8 Error Handling and Security

Security errors follow the error taxonomy defined in RFC-0314 (Workflow Error Handling):

- Security violations (unauthorized access, sandbox escape) MUST be treated as Fatal errors.
- Authentication failures MUST be retried with backoff per RFC-0313 (Parallelism).
- Authorization denials MUST be logged and reported to the observability system per RFC-0321.
- Secret rotation failures MUST trigger a workflow-level error per RFC-0315 (Recovery).

---

## 9 Layer Boundaries

### 9.1 Responsibilities

This specification IS responsible for:
- Defining the permission model (RBAC + capability-based).
- Specifying sandbox boundaries and isolation guarantees.
- Establishing data protection and encryption requirements.
- Defining the audit trail event taxonomy.
- Setting secret management policies.

### 9.2 Non-Responsibilities

This specification IS NOT responsible for:
- Implementing specific cryptographic algorithms (delegated to infrastructure).
- Managing user identities (delegated to identity providers).
- Executing workflow nodes (handled by Workflow Runtime, RFC-0304).
- Persisting audit logs (handled by Workflow Storage, RFC-0324).

### 9.3 Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational security concepts |
| RFC-0304 | Consumed | Workflow Runtime enforces security controls at execution |
| RFC-0307 | Consumed | Workflow Context provides secret management |
| RFC-0312 | Consumed | Workflow Scheduler enforces resource limits |
| RFC-0314 | Consumed | Workflow Error Handling defines security error taxonomy |
| RFC-0315 | Consumed | Workflow Recovery handles security incident recovery |
| RFC-0317 | Consumed | Workflow Validation verifies security constraints |
| RFC-0320 | Consumed | Workflow Performance defines resource limits |
| RFC-0321 | Consumed | Workflow Observability provides audit trail infrastructure |
| RFC-0322 | Consumed | Workflow Extension defines extension security model |
| RFC-0323 | Consumed | Workflow Plugin Integration defines plugin security |
| RFC-0324 | Consumed | Workflow Storage provides secure persistence |
| RFC-0327 | Consumed | Workflow IPC provides secure IPC channels |
| RFC-0330 | Consumed | Workflow Compliance provides compliance verification |

### 9.4 Consumers
- Workflow Runtime (RFC-0304): Enforces security controls during execution.
- Workflow Extension (RFC-0322): Inherits sandbox and permission model.
- Workflow Plugin Integration (RFC-0323): Plugin security model built on this specification.
- Workflow Compliance (RFC-0330): Uses security controls as compliance requirements.

### 9.5 Providers
- Permission Catalog (catalog/workflow-permissions.md): Provides the definitive permission taxonomy.
- Permission Schema (schemas/workflow/permission.json): Provides the permission format contract.

### 9.6 Forbidden Dependencies
- This specification MUST NOT depend on any platform-specific security framework (OAuth, Kerberos, etc.).
- This specification MUST NOT assume a particular identity provider.
- This specification MUST NOT prescribe specific cryptographic library implementations.

---

## 10 Performance

- Security control enforcement MUST add less than 1ms overhead per operation.
- Permission checks MUST complete within 100 microseconds.
- Audit log writes MUST be asynchronous with a maximum latency of 10ms.
- Encryption/decryption operations MUST NOT block workflow execution.

---

## 11 Compatibility

- Permission models MUST be backward compatible within a major version.
- New permission types MAY be added; existing permission types MUST NOT be removed or renamed.
- Audit log formats MUST be backward compatible within a major version.
- Encryption algorithm upgrades MUST support dual-mode operation during transition.

---

## 12 Compliance

- All security controls defined in Section 3 MUST be verifiable through the compliance model per RFC-0330.
- Security audit logs MUST be exportable in formats required by regulatory frameworks (SOX, GDPR, HIPAA, PCI-DSS).
- Compliance reports MUST include: permission assignments, audit event counts, security violation counts, secret rotation status.

---

## 13 Future Evolution

- **Zero-Trust Architecture**: Progressive adoption of zero-trust principles for all workflow communications.
- **Hardware-Enforced Isolation**: Support for SGX/TEE-based sandbox enforcement.
- **Quantum-Resistant Cryptography**: Migration path to post-quantum encryption algorithms.
- **Policy-as-Code**: Machine-readable security policies with automated compliance checking.
- **Cross-Domain Security**: Security model for cross-tenant and cross-organization workflow execution.

---

## 14 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

Security controls are defined as behavioral contracts, not implementation mechanisms.

---

## 15 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST enforce all ten security controls defined in Section 3.1. | Control enforcement test |
| AC-02 | The implementation MUST support eight permission types as defined in Section 4.1. | Permission enumeration test |
| AC-03 | The implementation MUST enforce five sandbox boundary levels as defined in Section 5.1. | Boundary isolation test |
| AC-04 | The implementation MUST support four data classification levels as defined in Section 6.2. | Classification test |
| AC-05 | The implementation MUST audit all ten event types defined in Section 7.1. | Event enumeration test |
| AC-06 | The implementation MUST prevent privilege escalation as defined in Section 4.3. | Privilege escalation test |
| AC-07 | The implementation MUST enforce tamper-evident audit logs as defined in Section 7.2. | Tamper detection test |
| AC-08 | The implementation MUST prevent secrets from appearing in logs or metrics. | Secret exposure test |
| AC-09 | Security control overhead MUST NOT exceed 1ms per operation. | Performance test |
| AC-10 | All security controls MUST be verifiable through the compliance model (RFC-0330). | Compliance verification test |

---

## 16 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (execution security) |
| RFC-0304 | Workflow Runtime (security enforcement at execution) |
| RFC-0307 | Workflow Context (secret management) |
| RFC-0312 | Workflow Scheduler (resource limit enforcement) |
| RFC-0313 | Workflow Parallelism (parallel security isolation) |
| RFC-0314 | Workflow Error Handling (security error taxonomy) |
| RFC-0315 | Workflow Recovery (security incident recovery) |
| RFC-0317 | Workflow Validation (security constraint validation) |
| RFC-0320 | Workflow Performance (resource limits and DoS prevention) |
| RFC-0321 | Workflow Observability (audit trail infrastructure) |
| RFC-0322 | Workflow Extension (extension security model) |
| RFC-0323 | Workflow Plugin Integration (plugin security) |
| RFC-0324 | Workflow Storage (secure persistence) |
| RFC-0327 | Workflow IPC (secure communication channels) |
| RFC-0329 | Workflow Compatibility (security model backward compatibility) |
| RFC-0330 | Workflow Compliance (security compliance verification) |
| RFC-0007 | Runtime IPC Architecture (IPC security foundation) |
| RFC-0008 | Runtime Plugin Host (plugin security foundation) |
| ADR-0012 | Contract-First Specification-Driven Development |
| ADR-0010 | Security Architecture |
| schemas/workflow/permission.json | Permission JSON Schema |
| schemas/workflow/sandbox-policy.json | Sandbox Policy JSON Schema |
| schemas/workflow/data-classification.json | Data Classification JSON Schema |
| catalog/workflow-permissions.md | Permission Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0319 (this document), RFC-0330 (Compliance), RFC-0322 (Extension Security) |
---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |
