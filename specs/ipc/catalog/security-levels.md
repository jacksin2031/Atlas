# RFC-IPC-CAT-SEC: IPC Security Level Catalog

RFC: IPC-CAT-SEC
Title: IPC Security Level Catalog
Status: Accepted
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0101 IPC Overview
  - RFC-0107 IPC Security
  - RFC-0109 IPC Lifecycle
Required By:
  - All RFCs in the IPC subsystem (RFC-0101 through RFC-0112)
  - RFC-0007 Runtime IPC
Supersedes: None
Superseded By: None
Category: IPC
Layer: Security
Normative: YES
Audience: Systems Engineers, Security Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.5 (IPC Isolation)
Related RFCs:
  - RFC-0101 IPC Overview
  - RFC-0107 IPC Security
  - RFC-0109 IPC Lifecycle
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status
This specification is Normative. Every Atlas process that participates in Inter-Process Communication MUST declare its Security Level at startup and MUST enforce all access restrictions defined herein. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Defense-in-Depth Model](#2-defense-in-depth-model)
3. [Security Level Registry](#3-security-level-registry)
4. [Security Level Rules](#4-security-level-rules)
5. [Security Level Escalation](#5-security-level-escalation)
6. [Security Level De-escalation](#6-security-level-de-escalation)
7. [Cross-Level Communication Matrix](#7-cross-level-communication-matrix)
8. [Security Level Assignment](#8-security-level-assignment)
9. [Security Level Enforcement](#9-security-level-enforcement)
10. [Cross-Level Communication Constraints](#10-cross-level-communication-constraints)
11. [Security Level Audit Requirements](#11-security-level-audit-requirements)
12. [Compliance Checklist](#12-compliance-checklist)
13. [Acceptance Criteria](#13-acceptance-criteria)
14. [References](#14-references)
15. [Changelog](#15-changelog)
16. [Glossary](#16-glossary)
17. [Compatibility](#17-compatibility)

---

## 1 Introduction

The Atlas platform comprises independent processes running in separate memory contexts. The IPC Security Level Catalog defines the authoritative classification of every process within the Atlas workspace boundary into one of five discrete Security Levels (L0 through L4). Each level imposes distinct requirements on authentication, encryption, audit logging, and cross-level communication permissions.

Every Atlas process MUST know its assigned Security Level at all times. The Security Level determines what channels a process MAY open, what messages it MAY send or receive, and what data it MAY access through IPC. The Security Level is not a runtime property that a process may arbitrarily modify; it is a declarative invariant established at process startup and enforced by the IPC Dispatcher.

The Security Level Catalog serves as the foundational reference for all security decisions within the IPC subsystem. RFC-0107 (IPC Security) builds upon these levels to define authentication mechanisms, encryption requirements, and audit obligations. The catalog itself is transport-independent: it specifies what security properties MUST hold, not how they are implemented.

### 1.1 Purpose

This catalog exists to provide a single, authoritative reference that answers the following questions for every Atlas process:

- What Security Level am I operating at?
- What am I permitted to communicate with?
- What authentication, encryption, and audit requirements apply to my level?
- Can I escalate to a higher level, and under what conditions?
- Must I de-escalate, and when?

By centralizing these answers in a single document, the catalog eliminates ambiguity and ensures consistent security enforcement across all IPC implementations.

### 1.2 Rationale

Without a formal Security Level taxonomy, IPC security becomes ad hoc: processes negotiate capabilities at runtime, security policies are duplicated across subsystems, and privilege boundaries erode through incremental concessions. The five-tier model defined herein provides a finite, well-ordered set of security levels that map directly to the principle of least privilege and the defense-in-depth paradigm.

Each level represents a distinct trust boundary. Higher levels impose stricter requirements but grant access to more sensitive data and capabilities. Lower levels are intentionally restricted to minimize the blast radius of any single process compromise.

### 1.3 Scope

This specification governs all IPC communication within the Atlas workspace boundary, including:

- Core runtime service-to-service communication.
- Plugin-to-runtime message exchanges.
- External service integrations traversing the IPC boundary.
- Administrative control channels and diagnostic interfaces.
- Event bus subscriptions and publications.

This specification does not govern:

- OS-level process isolation primitives.
- Physical network security.
- Application-layer business logic validation.
- User interface access controls.

---

## 2 Defense-in-Depth Model

The Atlas IPC Security Level Catalog implements a defense-in-depth model comprising four independent layers of protection:

1. **Authentication Layer**: Every process MUST prove its identity before establishing an IPC channel. The strength of authentication is proportional to the Security Level of the target channel.
2. **Authorization Layer**: Even authenticated processes are subject to access controls determined by their Security Level. A process MAY only communicate with levels equal to or lower than its own, subject to the constraints in Section 7.
3. **Encryption Layer**: Confidential data transmitted over IPC channels MUST be encrypted. The encryption requirements escalate with Security Level, from no encryption at L0 to always-encrypted end-to-end channels at L4.
4. **Audit Layer**: Every IPC event MUST be logged with sufficient detail to enable forensic reconstruction. Audit depth increases with Security Level, culminating in an immutable audit chain at L4.

These four layers operate independently. Compromise of one layer MUST NOT result in total system breach. For example, if authentication is bypassed, authorization controls MUST still prevent unauthorized access. If encryption is compromised, audit logs MUST still capture the security event for forensic analysis.

The defense-in-depth model ensures that the Security Level Catalog remains robust even under partial system compromise. Each layer provides a fallback when a lower layer fails.

---

## 3 Security Level Registry

The following table defines the complete set of Security Levels. Every level is permanent and SHALL NOT be removed, renamed, or reordered without a formal ADR submission and approval by the Core Architecture Board.

| Level | ID | Name | Description | Allowed To Communicate With | Authentication Required | Encryption Required | Audit Required |
|---|---|---|---|---|---|---|---|
| L0 | PUBLIC | Public | No authentication, no encryption. Intended for diagnostic, health-check, and status channels that expose no sensitive data. | L0, L1, L2, L3, L4 | No | No | No |
| L1 | INTERNAL | Internal | Valid process token required. Intended for standard service-to-service communication within the Atlas platform. | L1, L2, L3, L4 | Yes (token) | No | Yes (event only) |
| L2 | TRUSTED | Trusted | Verified process identity via certificate. Intended for channels carrying structured operational data. | L2, L3, L4 | Yes (certificate) | Yes (in-transit) | Yes (all events) |
| L3 | PRIVILEGED | Privileged | Elevated privileges, sandboxed. Intended for administrative operations and privileged data access. | L3, L4 | Yes (mutual TLS) | Yes (end-to-end) | Yes (all events + integrity) |
| L4 | CORE | Core Runtime | Highest privilege, trust root. Intended exclusively for the core runtime bootstrap, key management, and trust-anchor operations. | L4 only | Yes (hardware-backed) | Yes (always encrypted) | Yes (immutable audit chain) |

### 3.1 Level Descriptions

#### L0 -- PUBLIC
Public-level channels expose no sensitive data and require no authentication. L0 is the least restrictive level and is suitable for health checks, liveness probes, and public status endpoints. Processes operating at L0 MUST NOT transmit any data that could be used to infer platform topology, internal state, or user information.

#### L1 -- INTERNAL
Internal-level channels require a valid process token issued by the Security Manager. L1 is the default level for standard service-to-service communication. Tokens provide basic identity assurance but do not guarantee the full integrity of the calling process. L1 channels MAY carry operational data but MUST NOT carry credentials, secrets, or user-identifiable information.

#### L2 -- TRUSTED
Trusted-level channels require certificate-based identity verification. The calling process MUST present a valid certificate signed by the Atlas root CA. L2 channels carry structured operational data including configuration updates, state transitions, and telemetry. All L2 traffic MUST be encrypted in transit.

#### L3 -- PRIVILEGED
Privileged-level channels require mutual TLS authentication. Both the caller and the callee MUST present valid certificates. L3 channels carry administrative commands, elevated configuration changes, and privileged data. All communication is encrypted end-to-end, and every event MUST include integrity verification.

#### L4 -- CORE
Core-level channels are the most restrictive. Only processes operating at L4 MAY communicate with other L4 processes. L4 is reserved for the core runtime bootstrap sequence, cryptographic key management, trust-anchor operations, and security-critical state transitions. All L4 communication is always encrypted, and every event is recorded in an immutable audit chain.

---

## 4 Security Level Rules

Every Security Level imposes specific permissions and restrictions. The rules below define what a process MAY and MUST NOT do at each level.

### 4.1 L0 -- PUBLIC Rules

A process operating at L0:

- MAY communicate with any Security Level (L0 through L4).
- MUST NOT require authentication from any party.
- MUST NOT require encryption of its own messages.
- MUST NOT log or audit its communications.
- MUST NOT transmit any data beyond health status, liveness, or public diagnostics.
- MUST NOT open channels to L4 processes.
- SHOULD NOT initiate connections to L2 or higher; L0 processes SHOULD be passive recipients only.
- MUST NOT attempt to escalate its Security Level.

### 4.2 L1 -- INTERNAL Rules

A process operating at L1:

- MAY communicate with L1, L2, L3, and L4 processes.
- MUST present a valid process token when initiating communication with L1 or higher.
- MAY communicate with L0 without a token.
- MUST NOT require encryption of its outbound messages to L0 or L1 peers.
- MUST log all IPC events to the audit log.
- MUST NOT transmit credentials, secrets, or user-identifiable information.
- MUST NOT open channels directly to L4 processes.
- SHOULD NOT initiate connections to L3 or higher without explicit authorization from the Security Manager.
- MUST NOT escalate its Security Level without de-escalating first.

### 4.3 L2 -- TRUSTED Rules

A process operating at L2:

- MAY communicate with L2, L3, and L4 processes.
- MUST present a valid certificate signed by the Atlas root CA when initiating communication.
- MUST encrypt all outbound traffic using in-transit encryption.
- MUST log all IPC events with full details.
- MAY transmit structured operational data including configuration and telemetry.
- MUST NOT transmit cryptographic keys or secrets without end-to-end encryption.
- MUST NOT open channels directly to L4 processes.
- MUST enforce certificate revocation checks before establishing connections.
- SHOULD NOT initiate connections to L3 or higher without mutual TLS negotiation.
- MUST NOT escalate its Security Level without explicit re-authentication.

### 4.4 L3 -- PRIVILEGED Rules

A process operating at L3:

- MAY communicate with L3 and L4 processes.
- MUST perform mutual TLS authentication with every peer.
- MUST encrypt all outbound traffic end-to-end.
- MUST log all IPC events with integrity verification.
- MAY transmit administrative commands and privileged data.
- MUST verify the integrity of every received message using cryptographic signatures.
- MUST NOT open channels to L0, L1, or L2 processes from an L3 session.
- MUST enforce certificate rotation at the configured interval.
- MUST NOT escalate its Security Level; L3 is the maximum level for non-core processes.
- MUST de-escalate to L2 immediately upon detecting any integrity violation.

### 4.5 L4 -- CORE Rules

A process operating at L4:

- MAY communicate with L4 processes only.
- MUST authenticate every peer using hardware-backed credentials.
- MUST encrypt all communication; no L4 channel MAY operate without encryption.
- MUST maintain an immutable audit chain for every IPC event.
- MAY perform trust-anchor operations including key generation, rotation, and revocation.
- MUST verify the integrity of every message using hardware-backed signatures.
- MUST NOT communicate with any process operating below L4.
- MUST NOT accept connections from processes that do not present hardware-backed credentials.
- MUST NOT escalate its Security Level; L4 is the maximum Security Level.
- MUST enforce strict session isolation: L4 sessions MUST NOT share state with lower-level sessions.

---

## 5 Security Level Escalation

A process operating at a lower Security Level MAY escalate to a higher level only under the following conditions:

### 5.1 Escalation Conditions

Escalation from level N to level N+1 is permitted only when:

1. The target level N+1 channel requires higher authentication than the current level provides.
2. The Security Manager has issued an escalation authorization token.
3. The calling process presents valid credentials for the target level.
4. The escalation is initiated by the calling process, not imposed by the callee.
5. An audit record of the escalation event is created before the escalation takes effect.

### 5.2 Escalation Restrictions

- A process MUST NOT escalate directly from L0 to L3, or from L0 or L1 to L4. Escalation MUST proceed through each intermediate level sequentially.
- A process operating at L3 MUST NOT escalate to L4. L4 is reserved exclusively for core runtime processes.
- An escalation authorization token is valid for a single escalation event only. It MUST NOT be cached or reused.
- The Security Manager MUST revoke the escalation authorization token immediately after use.
- A process MUST NOT hold an escalated Security Level for more than the configured maximum duration. If the process continues operating at the escalated level beyond the maximum duration, it MUST de-escalate.

### 5.3 Escalation Procedure

When a process initiates an escalation, the following procedure MUST be followed:

1. The process requests an escalation authorization token from the Security Manager.
2. The Security Manager validates the request, checks the process credentials, and issues a short-lived token.
3. The process presents the token and the target-level credentials to the IPC Dispatcher.
4. The IPC Dispatcher verifies the token and credentials, creates an audit record, and updates the process effective Security Level.
5. The process begins operating at the escalated level.

### 5.4 Escalation Matrix

| From | To | Allowed | Conditions |
|---|---|---|---|
| L0 | L1 | Yes | Valid token from Security Manager |
| L1 | L2 | Yes | Valid certificate from Atlas root CA |
| L2 | L3 | Yes | Mutual TLS credentials and escalation token |
| L3 | L4 | No | Reserved for core runtime processes only |
| L0 | L2 | No | Sequential escalation required |
| L0 | L3 | No | Sequential escalation required |
| L0 | L4 | No | Sequential escalation required |
| L1 | L3 | No | Sequential escalation required |
| L1 | L4 | No | Sequential escalation required |
| L2 | L4 | No | Sequential escalation required |

---

## 6 Security Level De-escalation

A process MUST de-escalate its Security Level under the following conditions:

### 6.1 Mandatory De-escalation Triggers

A process MUST de-escalate immediately when:

1. Its authentication credentials expire or are revoked.
2. An integrity violation is detected in any received message.
3. The Security Manager issues a de-escalation directive.
4. The process detects a security anomaly in its own execution context.
5. The process transitions from an escalated state to a non-escalated state.

### 6.2 De-escalation Procedure

When a mandatory de-escalation trigger fires, the following procedure MUST be followed:

1. The process ceases all outbound communication at the current Security Level.
2. The process creates an audit record documenting the de-escalation event, including the trigger cause.
3. The process transitions to the next lower Security Level or to L0 if no lower level is available.
4. The process re-authenticates at the new Security Level before resuming communication.
5. If the process was operating at L0, it MUST NOT resume communication until re-initialized.

### 6.3 De-escalation from Escalated States

When a process de-escalates from an escalated state (as described in Section 5), the following additional rules apply:

- The escalation authorization token MUST be destroyed immediately.
- Any state acquired during the escalated session MUST NOT be carried over to the lower level.
- An audit record MUST be created for both the de-escalation and the destruction of the escalation token.

### 6.4 Graceful vs. Forced De-escalation

- **Graceful de-escalation** occurs when the process initiates de-escalation voluntarily (e.g., credential expiration). The process completes all pending operations before transitioning.
- **Forced de-escalation** occurs when a security anomaly or Security Manager directive triggers immediate de-escalation. The process MUST halt all operations and transition immediately, potentially discarding in-flight messages.

---

## 7 Cross-Level Communication Matrix

The following matrix defines which Security Levels MAY communicate with which other levels. A "Yes" entry indicates that communication is permitted subject to the authentication and encryption requirements of the target level. A "No" entry indicates that communication is prohibited.

| From \\ To | L0 | L1 | L2 | L3 | L4 |
|---|---|---|---|---|---|
| L0 | Yes | Yes | No | No | No |
| L1 | Yes | Yes | Yes | No | No |
| L2 | Yes | Yes | Yes | Yes | No |
| L3 | Yes | Yes | Yes | Yes | Yes |
| L4 | Yes | Yes | Yes | Yes | Yes |

### 7.1 Matrix Interpretation Rules

- Communication is directional. A "Yes" in the cell (From=L1, To=L2) means L1 processes MAY initiate communication with L2 processes. It does NOT imply that L2 processes MAY initiate communication with L1 processes (though that is separately permitted by the L2 row).
- The diagonal entries (L0 to L0, L1 to L1, etc.) indicate same-level communication, which is always permitted.
- The L4 column shows that L4 processes MAY communicate with all levels, but L4 processes are constrained by Section 4.5 to only open channels to L4 peers in practice.
- The L0 row shows that L0 processes may communicate with all levels, but are restricted by Section 4.1 from opening channels to L4.

### 7.2 Downward Communication

A higher-level process MAY communicate with any lower-level process, subject to the lower level own requirements. For example, an L3 process MAY send messages to an L0 process, but the L0 process is not required to authenticate the sender.

### 7.3 Upward Communication

A lower-level process MAY communicate with a higher-level process only if it satisfies the higher level authentication and encryption requirements. For example, an L1 process MAY communicate with an L2 process only if it presents a valid certificate.

---

## 8 Security Level Assignment

Every process MUST be assigned a Security Level at startup. The assignment is performed by the IPC Dispatcher based on the process declared level and verified credentials.

### 8.1 Declaration

At startup, every process MUST declare its intended Security Level to the IPC Dispatcher. The declaration includes:

- The intended Security Level (L0 through L4).
- The process identifier.
- The authentication credentials appropriate for the declared level.
- The list of channels the process intends to open.

### 8.2 Verification

The IPC Dispatcher verifies the declaration against the following rules:

- A process declaring L0 MUST NOT present authentication credentials.
- A process declaring L1 MUST present a valid process token.
- A process declaring L2 MUST present a valid certificate signed by the Atlas root CA.
- A process declaring L3 MUST present mutual TLS credentials.
- A process declaring L4 MUST present hardware-backed credentials.

If verification fails, the IPC Dispatcher rejects the declaration and terminates the process IPC participation.

### 8.3 Assignment Invariants

- A process MUST NOT change its declared Security Level after successful assignment, except through the escalation and de-escalation procedures defined in Sections 5 and 6.
- The IPC Dispatcher MUST enforce the declared Security Level for the entire lifetime of the process.
- If a process credentials are revoked, the IPC Dispatcher MUST force de-escalation as defined in Section 6.

### 8.4 Default Assignment

If a process does not declare a Security Level at startup, the IPC Dispatcher assigns it L0 by default. A default-assigned L0 process MAY NOT open channels to L2 or higher.

---

## 9 Security Level Enforcement

Security Level enforcement occurs at multiple points in the IPC stack to ensure defense-in-depth.

### 9.1 Enforcement Points

| Enforcement Point | Location | Responsibility |
|---|---|---|
| Connection Establishment | IPC Dispatcher | Verifies the Security Level of both the caller and the callee before accepting the connection. |
| Channel Opening | IPC Dispatcher | Validates that the requested channel Security Level is accessible from the caller current level. |
| Message Transmission | Transport Layer | Applies encryption requirements based on the Security Level of the channel. |
| Message Reception | Transport Layer | Verifies authentication and decryption requirements before delivering the message to the application. |
| Audit Logging | Observability Layer | Records every IPC event at the granularity required by the Security Level. |

### 9.2 Enforcement Guarantees

- The IPC Dispatcher MUST reject any connection attempt that violates the Cross-Level Communication Matrix (Section 7).
- The Transport Layer MUST enforce encryption requirements based on the Security Level. Channels requiring encryption MUST NOT transmit plaintext.
- The Observability Layer MUST enforce audit requirements based on the Security Level. Events requiring audit logging MUST NOT be silently dropped.

### 9.3 Enforcement Failures

If any enforcement point detects a violation:

1. The violating message or connection is immediately terminated.
2. An audit record is created documenting the violation.
3. The offending process is de-escalated to L0 or terminated, depending on the severity of the violation.
4. The Security Manager is notified of the violation.
