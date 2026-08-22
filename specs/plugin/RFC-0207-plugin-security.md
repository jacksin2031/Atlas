# RFC-0207: Plugin Security

RFC: RFC-0207
Title: Plugin Security
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0008 Runtime Plugin Host
  - RFC-0107 IPC Security
  - RFC-0201 Plugin Overview
  - RFC-0205 Plugin Registry
  - RFC-0208 Plugin Sandbox
  - RFC-1006 Common Error Model
Related RFC:
  - RFC-0202 Plugin Manifest
  - RFC-0206 Plugin Capability
  - RFC-0210 Plugin Events
Related ADR:
  - ADR-0005 Plugin Architecture
  - ADR-0012 Contract-First Specification
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the plugin trust model, authentication, authorization, permission system, least privilege enforcement, filesystem boundaries, network boundaries, IPC permissions, workflow permissions, AI permissions, threat model, audit logging, security events, and tamper detection requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, ADR-0012, and RFC-0201.

---

## Table of Contents
- 1. [Introduction]
- 2. [Goals]
- 3. [Non-Goals]
- 4. [Security Philosophy]
- 5. [Ownership]
- 6. [Boundaries]
- 7. [Runtime Invariants]
- 8. [Architecture]
- 9. [Trust Model]
- 10. [Authentication]
- 11. [Authorization]
- 12. [Permission System]
- 13. [Least Privilege]
- 14. [Filesystem Boundaries]
- 15. [Network Boundaries]
- 16. [IPC Permissions]
- 17. [Workflow Permissions]
- 18. [AI Permissions]
- 19. [Threat Model]
- 20. [Audit Logging]
- 21. [Security Events]
- 22. [Tamper Detection]
- 23. [Performance Budgets]
- 24. [Glossary]
- 25. [Acceptance Criteria]
- 26. [Cross References]
- 27. [References]
- 28. [Revision History]
- 29. [Future Evolution]---

## 2 Goals
1. **Zero-Trust Execution**: Every plugin is untrusted by default. No implicit permissions exist.
2. **Defense in Depth**: Multiple independent security controls operate at every boundary.
3. **Least Privilege**: Plugins operate with minimum permissions required for their function.
4. **Complete Auditability**: Every security event is logged immutably.
5. **Threat Mitigation**: Security controls address all six STRIDE threat categories.
6. **Tamper Resistance**: Plugin integrity is verified continuously.
7. **Permission Granularity**: Permissions are granular enough to restrict access precisely.
8. **Cross-Subsystem Security**: Security policies extend to IPC, Workflow, and AI interactions.

---



## 4 Security Philosophy
1. **Zero-Trust by Default**: No plugin is trusted without verification.
2. **Explicit Authorization**: Every access requires explicit authorization.
3. **Minimal Exposure**: Plugins expose the minimum interface necessary.
4. **Continuous Verification**: Security is verified at every interaction, not just at initialization.
5. **Fail Secure**: Security failures result in denial, not graceful degradation.
6. **Immutable Audit**: Security audit logs are tamper-resistant.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 6 Boundaries
- **Security Manager MAY communicate with**:
  - Plugin Registry (RFC-0205) for trust level queries
  - Plugin Sandbox Manager (RFC-0208) for boundary enforcement
  - IPC Security Layer (RFC-0107) for IPC permissions
  - Event Bus (RFC-0210) for security events
  - Observability subsystem for audit logs
- **Security Manager MUST NOT communicate with**:
  - Plugin extension logic directly
  - External networks directly

---


## 8 Architecture
`mermaid
graph TD
    subgraph Security Manager
        TrustEvaluator[Trust Evaluator]
        Authenticator[Authenticator]
        AuthorizationEngine[Authorization Engine]
        PermissionMapper[Permission Mapper]
        BoundaryEnforcer[Boundary Enforcer]
        TamperDetector[Tamper Detector]
        AuditLogger[Audit Logger]
        ThreatAnalyzer[Threat Analyzer]
    end
    subgraph External Systems
        Registry[Plugin Registry RFC-0205]
        Sandbox[Sandbox Manager RFC-0208]
        IPCSecurity[IPC Security RFC-0107]
        EventBus[Event Bus RFC-0210]
        Observability[Observability Subsystem]
    end
    TrustEvaluator --> Registry
    Authenticator --> TrustEvaluator
    AuthorizationEngine --> PermissionMapper
    PermissionMapper --> BoundaryEnforcer
    BoundaryEnforcer --> Sandbox
    TamperDetector --> AuditLogger
    AuditLogger --> Observability
    ThreatAnalyzer --> AuditLogger
    AuthorizationEngine --> IPCSecurity
`
---

- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 10 Authentication
- **Manifest Signature**: Plugins MUST present a valid digital signature in their manifest.
- **Trust Chain**: Signatures are verified against a trust chain rooted in the platform certificate.
- **Token-Based Session**: Authenticated plugins receive session tokens for IPC communication.
- **Token Rotation**: Session tokens are rotated at configurable intervals.
- **Revocation**: Compromised plugin signatures are revoked through the trust chain.

---


## 12 Permission System
- **Permission IDs**: All permissions use PERM-* IDs from catalog/permissions.md.
- **Permission Declaration**: Permissions are declared in the plugin manifest.
- **Permission Enforcement**: The Boundary Enforcer enforces permissions at every access point.
- **Permission Revocation**: Permissions MAY be revoked at runtime for security violations.
- **Permission Audit**: All permission grants and revocations are audit-logged.

---


## 14 Filesystem Boundaries
- **Sandbox Namespace**: Plugins have access only to their sandbox file system namespace.
- **Read Access**: Plugins MAY read from declared resource directories.
- **Write Access**: Plugins MAY write only to declared output directories.
- **Cross-Plugin Access**: Plugins MUST NOT access other plugin file systems.
- **Host File System**: Plugins MUST NOT access the host file system directly.
- **Temporary Storage**: Plugins MAY use temporary storage within their sandbox.

---


## 16 IPC Permissions
- **Channel Access**: Plugins may only access IPC channels declared in their manifest.
- **Message Validation**: All IPC messages are validated against schemas.
- **Rate Limiting**: IPC message rates are limited per plugin.
- **Direction Control**: IPC channels are unidirectional or bidirectional as declared.
- **Security Level Enforcement**: IPC security levels (RFC-0107) are enforced.

---


## 18 AI Permissions
- **Model Access**: AI plugins may only access declared AI models.
- **Inference Limits**: AI inference is subject to declared resource quotas.
- **Data Privacy**: AI plugin input data is isolated from other plugins.
- **Output Validation**: AI plugin outputs are validated against declared schemas.
- **Resource Isolation**: AI model loading is isolated per plugin.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Audit Logging
- **Logged Events**: Installation, activation, permission requests, security violations, suspensions, trust level changes.
- **Log Immutability**: Audit logs are append-only and tamper-resistant.
- **Log Retention**: Logs are retained for a minimum of 365 days.
- **Log Access**: Audit logs are accessible only to authorized administrators.
- **Log Export**: Logs MAY be exported to external SIEM systems.

---



## 22 Tamper Detection
- **Load-Time Verification**: Plugin integrity is verified at load time.
- **Periodic Verification**: Plugin integrity is verified at configurable intervals.
- **Hash Comparison**: Current hash is compared against the manifest integrity hash.
- **Tamper Response**: Detected tampering triggers immediate sandbox suspension and audit logging.
- **Recovery**: Tampered plugins are quarantined and reported to the administrator.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 24 Glossary
| Term | Definition |
|---|---|
| Trust Model | Classification of plugin security posture. |
| Authentication | Verification of plugin identity. |
| Authorization | Granting of access permissions. |
| Least Privilege | Operating with minimum required permissions. |
| STRIDE | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. |
| Audit Log | Immutable record of security events. |
| Tamper Detection | Identification of unauthorized modifications. |
---

#### AC-0207-006
- **Requirement**: Plugins MUST present a valid digital signature in their manifest.
- **Verification**: Submit a manifest without a signature.
- **Expected Result**: Authentication fails.

#### AC-0207-007
- **Requirement**: Signatures MUST be verified against a trust chain.
- **Verification**: Submit a manifest with an invalid signature.
- **Expected Result**: Verification fails.

#### AC-0207-008
- **Requirement**: Compromised signatures MUST be revocable.
- **Verification**: Revoke a signature and attempt plugin load.
- **Expected Result**: Load is rejected.

#### AC-0207-009
- **Requirement**: Authorization MUST be capability-based.
- **Verification**: Check authorization logic against RFC-0206.
- **Expected Result**: Authorization uses declared capabilities.

#### AC-0207-010
- **Requirement**: Permissions MUST map to PERM-* IDs from catalog.
- **Verification**: Inspect permission mapping table.
- **Expected Result**: All capabilities map to valid PERM-* IDs.

#### AC-0207-011
- **Requirement**: Trust level MUST affect authorization scope.
- **Verification**: Compare authorization for different trust levels.
- **Expected Result**: Higher trust grants broader access.

#### AC-0207-012
- **Requirement**: Deny by default MUST be enforced.
- **Verification**: Attempt access without explicit authorization.
- **Expected Result**: Access is denied.

#### AC-0207-013
- **Requirement**: All permissions MUST use PERM-* IDs from catalog/permissions.md.
- **Verification**: Check permission declarations against catalog.
- **Expected Result**: All permissions match catalog IDs.

#### AC-0207-014
- **Requirement**: Permissions MUST be declared in the manifest.
- **Verification**: Inspect manifest schema for permission field.
- **Expected Result**: Permission field is required.

#### AC-0207-015
- **Requirement**: Permission revocation MUST be possible at runtime.
- **Verification**: Revoke a permission during plugin execution.
- **Expected Result**: Permission is revoked immediately.

#### AC-0207-016
- **Requirement**: Permission grants MUST be audit-logged.
- **Verification**: Grant a permission and check audit log.
- **Expected Result**: Grant event is logged.

#### AC-0207-017
- **Requirement**: Plugins MUST operate with minimum declared permissions.
- **Verification**: Inspect permission enforcement.
- **Expected Result**: Only declared permissions are granted.

#### AC-0207-018
- **Requirement**: Unused permissions MUST be detectable.
- **Verification**: Run a plugin with unused permissions.
- **Expected Result**: Unused permissions are reported.

#### AC-0207-019
- **Requirement**: Privilege escalation MUST be prevented.
- **Verification**: Attempt to increase permissions beyond declared.
- **Expected Result**: Escalation is blocked.

#### AC-0207-020
- **Requirement**: Plugins MUST NOT access host file system directly.
- **Verification**: Attempt host file access from plugin.
- **Expected Result**: Access is denied.

#### AC-0207-021
- **Requirement**: Plugins MUST NOT access other plugin file systems.
- **Verification**: Attempt cross-plugin file access.
- **Expected Result**: Access is denied.

#### AC-0207-022
- **Requirement**: Volume mounts MUST be declared in manifest.
- **Verification**: Mount a volume without declaration.
- **Expected Result**: Mount is rejected.

#### AC-0207-023
- **Requirement**: Plugins MUST only connect to declared outbound endpoints.
- **Verification**: Connect to undeclared endpoint.
- **Expected Result**: Connection is blocked.

#### AC-0207-024
- **Requirement**: Plugins MUST NOT accept undeclared inbound connections.
- **Verification**: Attempt inbound connection without declaration.
- **Expected Result**: Connection is rejected.

#### AC-0207-025
- **Requirement**: All outbound traffic MUST use encrypted channels.
- **Verification**: Inspect network traffic from plugin.
- **Expected Result**: Traffic is encrypted.

#### AC-0207-026
- **Requirement**: Plugins may only access declared IPC channels.
- **Verification**: Access undeclared IPC channel.
- **Expected Result**: Access is denied.

#### AC-0207-027
- **Requirement**: IPC messages MUST be validated against schemas.
- **Verification**: Send malformed IPC message.
- **Expected Result**: Message is rejected.

#### AC-0207-028
- **Requirement**: IPC security levels (RFC-0107) MUST be enforced.
- **Verification**: Attempt cross-level IPC.
- **Expected Result**: Connection is rejected.

#### AC-0207-029
- **Requirement**: All six STRIDE categories MUST be addressed.
- **Verification**: Check threat model table for all categories.
- **Expected Result**: All six categories have mitigations.

#### AC-0207-030
- **Requirement**: Spoofing MUST be mitigated by signature verification.
- **Verification**: Inspect spoofing mitigation.
- **Expected Result**: Signature verification is defined.

#### AC-0207-031
- **Requirement**: Tampering MUST be mitigated by integrity verification.
- **Verification**: Inspect tampering mitigation.
- **Expected Result**: Integrity hash verification is defined.

#### AC-0207-032
- **Requirement**: Repudiation MUST be mitigated by audit logging.
- **Verification**: Inspect repudiation mitigation.
- **Expected Result**: Immutable audit logging is defined.

#### AC-0207-033
- **Requirement**: Information Disclosure MUST be mitigated by sandbox isolation.
- **Verification**: Inspect information disclosure mitigation.
- **Expected Result**: Sandbox isolation is defined.

#### AC-0207-034
- **Requirement**: Denial of Service MUST be mitigated by resource quotas.
- **Verification**: Inspect DoS mitigation.
- **Expected Result**: Resource quotas are defined.

#### AC-0207-035
- **Requirement**: Elevation of Privilege MUST be mitigated by least privilege.
- **Verification**: Inspect privilege escalation mitigation.
- **Expected Result**: Least privilege enforcement is defined.

#### AC-0207-036
- **Requirement**: All security events MUST be audit-logged.
- **Verification**: Trigger security events and check logs.
- **Expected Result**: All events are logged.

#### AC-0207-037
- **Requirement**: Audit logs MUST be append-only and tamper-resistant.
- **Verification**: Attempt to modify audit log.
- **Expected Result**: Modification is rejected.

#### AC-0207-038
- **Requirement**: Logs MUST be retained for at least 365 days.
- **Verification**: Check retention policy.
- **Expected Result**: Retention is 365 days or more.

#### AC-0207-039
- **Requirement**: Log access MUST be restricted to authorized administrators.
- **Verification**: Attempt log access without admin privileges.
- **Expected Result**: Access is denied.

#### AC-0207-040
- **Requirement**: PEVT-SECURITY-VIOLATION MUST be produced on permission violation.
- **Verification**: Violate a permission and check events.
- **Expected Result**: Event is produced.

#### AC-0207-041
- **Requirement**: PEVT-TRUST-LEVEL-CHANGE MUST be produced on trust level change.
- **Verification**: Change trust level and check events.
- **Expected Result**: Event is produced.

#### AC-0207-042
- **Requirement**: PEVT-INTEGRITY-FAIL MUST be produced on integrity failure.
- **Verification**: Tamper with manifest and check events.
- **Expected Result**: Event is produced.

#### AC-0207-043
- **Requirement**: Plugin integrity MUST be verified at load time.
- **Verification**: Load a plugin and check integrity verification.
- **Expected Result**: Integrity is verified.

#### AC-0207-044
- **Requirement**: Plugin integrity MUST be verified periodically during execution.
- **Verification**: Check periodic verification configuration.
- **Expected Result**: Periodic verification is configured.

#### AC-0207-045
- **Requirement**: Detected tampering MUST trigger sandbox suspension.
- **Verification**: Simulate tampering detection.
- **Expected Result**: Sandbox is suspended.

#### AC-0207-046
- **Requirement**: Tampered plugins MUST be quarantined.
- **Verification**: Check quarantine procedure.
- **Expected Result**: Plugin is quarantined.

#### AC-0207-047
- **Requirement**: Every plugin MUST start with zero permissions.
- **Verification**: Load a new plugin and check permissions.
- **Expected Result**: Zero permissions are granted.

#### AC-0207-048
- **Requirement**: Every resource access MUST be authorized before execution.
- **Verification**: Check authorization before resource access.
- **Expected Result**: Authorization is enforced.

#### AC-0207-049
- **Requirement**: Security violations MUST trigger immediate sandbox suspension.
- **Verification**: Trigger a security violation.
- **Expected Result**: Sandbox is suspended.

#### AC-0207-050
- **Requirement**: Trust level escalation MUST require administrative approval.
- **Verification**: Attempt trust escalation without approval.
- **Expected Result**: Escalation is rejected.

#### AC-0207-051
- **Requirement**: The architecture MUST be illustrated with a Mermaid graph TD diagram.
- **Verification**: Inspect Section 8.
- **Expected Result**: A graph TD diagram is present.

#### AC-0207-052
- **Requirement**: The security manager MUST define at least six runtime invariants.
- **Verification**: Count invariants in Section 7.
- **Expected Result**: Six invariants are defined.

#### AC-0207-053
- **Requirement**: The specification MUST define at least eight goals.
- **Verification**: Count goals in Section 2.
- **Expected Result**: Eight goals are defined.

#### AC-0207-054
- **Requirement**: The specification MUST define at least three non-goals.
- **Verification**: Count non-goals in Section 3.
- **Expected Result**: Three non-goals are defined.

#### AC-0207-055
- **Requirement**: Signature verification MUST complete within 50 ms.
- **Verification**: Benchmark signature verification.
- **Expected Result**: Verification completes within 50 ms.

#### AC-0207-056
- **Requirement**: Permission check MUST complete within 0.05 ms.
- **Verification**: Benchmark permission check.
- **Expected Result**: Check completes within 0.05 ms.

#### AC-0207-057
- **Requirement**: Trust level evaluation MUST complete within 0.01 ms.
- **Verification**: Benchmark trust level evaluation.
- **Expected Result**: Evaluation completes within 0.01 ms.

#### AC-0207-058
- **Requirement**: Tamper detection check MUST complete within 5 ms.
- **Verification**: Benchmark tamper detection.
- **Expected Result**: Check completes within 5 ms.

#### AC-0207-059
- **Requirement**: The security model MUST be consistent with RFC-0201 security principles.
- **Verification**: Compare Section 18 of RFC-0201 with RFC-0207.
- **Expected Result**: Principles are consistent.

#### AC-0207-060
- **Requirement**: The security model MUST be consistent with RFC-0107 IPC security.
- **Verification**: Compare IPC permission sections.
- **Expected Result**: IPC permissions are consistent.

#### AC-0207-061
- **Requirement**: The security model MUST reference catalog/permissions.md for permission IDs.
- **Verification**: Check permission references.
- **Expected Result**: All permissions reference PERM-* IDs.

#### AC-0207-062
- **Requirement**: The security model MUST reference catalog/trust-levels.md for trust levels.
- **Verification**: Check trust level references.
- **Expected Result**: All trust levels reference TRUST-LEVEL-* IDs.

#### AC-0207-063
- **Requirement**: The security model MUST reference catalog/plugin-events.md for event IDs.
- **Verification**: Check event references.
- **Expected Result**: All events reference PEVT-* IDs.


---



## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 27 References
1. **RFC-0008**: Runtime Plugin Host
2. **RFC-0107**: IPC Security
3. **RFC-0201**: Plugin Overview
4. **RFC-0202**: Plugin Manifest
5. **RFC-0205**: Plugin Registry
6. **RFC-0208**: Plugin Sandbox
7. **RFC-0210**: Plugin Events
8. **RFC-1006**: Common Error Model
9. **ADR-0005**: Plugin Architecture
10. **ADR-0012**: Contract-First Specification
11. **glossary.md**: Unified Atlas Glossary

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 29 Future Evolution
- **Zero-Knowledge Proofs**: Future versions MAY define zero-knowledge proof mechanisms for privacy-preserving plugin authentication.
- **Automated Threat Analysis**: Future versions MAY define automated STRIDE threat analysis for plugin manifests.
- **Security Scorecard**: Future versions MAY define a standardized security scorecard for plugin trust assessment.
- **Runtime Behavioral Analysis**: Future versions MAY define behavioral analysis for detecting anomalous plugin activity.
- **Plugin Security Certification**: Future versions MAY define a formal security certification process for enterprise plugins.
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

All plugin contracts are defined as abstract behavioral interfaces.

---




---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |