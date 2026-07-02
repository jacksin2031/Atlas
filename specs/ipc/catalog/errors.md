# RFC-IPC-CAT-ERR: IPC Error Code Catalog

RFC: IPC-CAT-ERR
Title: IPC Error Code Catalog
Status: Accepted
Version: 1.0.0
Category: IPC
Layer: Error Handling
Normative: YES
Authors: Atlas Team
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0007 Runtime IPC Architecture
  - RFC-0101 IPC Transport Layer
  - RFC-0107 IPC Security Framework
  - RFC-0108 IPC Routing Protocol
  - RFC-0111 IPC Serialization Schema
Required By:
  - All RFCs within the IPC subsystem
Supersedes: None
Superseded By: None
Audience: Systems Engineers, Security Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.5 (IPC Isolation)
Related RFCs:
  - RFC-0007 Runtime IPC Architecture
  - RFC-0101 IPC Transport Layer
  - RFC-0107 IPC Security Framework
  - RFC-0108 IPC Routing Protocol
  - RFC-0111 IPC Serialization Schema
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

This specification is Normative. Every RFC within the Atlas IPC subsystem MUST reference the error codes defined in this catalog by their assigned Error Code ID (e.g., `IPC-1001`) instead of using free-text descriptions. Any IPC error handling implementation that emits, logs, or propagates an error MUST map it to exactly one entry in this catalog. Deviations from this catalog MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Error Code Registry](#2-error-code-registry)
3. [Error Code Ranges](#3-error-code-ranges)
4. [Error Severity Levels](#4-error-severity-levels)
5. [Error Recovery Procedures](#5-error-recovery-procedures)
6. [Cross-References](#6-cross-references)
7. [Glossary](#7-glossary)
8. [Revision History](#8-revision-history)

---

## 1 Introduction

The Atlas IPC subsystem coordinates communication between independent processes within the Atlas runtime boundary. Every IPC interaction — including connection establishment, message transmission, routing resolution, serialization, and security enforcement — is subject to failure conditions that must be communicated to callers in a consistent, machine-parseable, and human-readable manner.

This catalog establishes a fixed set of Error Code IDs, each mapped to a specific failure condition within the IPC subsystem. The catalog serves three purposes:

1. **Uniqueness**: Every IPC error condition has exactly one canonical Error Code ID. No two entries in this catalog share the same ID.
2. **Referencability**: Every RFC within the IPC subsystem MUST cite the appropriate Error Code ID when describing error conditions, rather than relying on free-text error descriptions.
3. **Stability**: Error Code IDs are immutable once assigned. An Error Code ID MUST NOT be reassigned, deprecated, or repurposed across any version of the Atlas specification.

### 1.1 Usage Rules

- Every IPC implementation MUST emit the Error Code ID defined in this catalog for each error condition it encounters.
- Error Code IDs are globally unique within the Atlas specification. They are not scoped to individual RFCs.
- When an RFC describes an error condition, it MUST reference the corresponding Error Code ID and MUST NOT redefine or extend the error's meaning.
- Implementations MAY log additional diagnostic context alongside the Error Code ID, but the ID itself is the authoritative identifier.
- New error conditions MUST NOT introduce ad-hoc error codes. They MUST be submitted through the ADR process for catalog extension.

---

## 2 Error Code Registry

The following table defines every standard IPC error code. Each row is normative and binding on all IPC implementations.

| Error Code | Category | Name | Retryable | Severity | Description |
|---|---|---|---|---|---|
| IPC-1001 | Transport | Connection Timeout | Yes | Warning | The connection attempt exceeded the maximum allowed duration |
| IPC-1002 | Security | Authentication Failed | No | Critical | The process failed cryptographic authentication |
| IPC-1003 | Routing | Invalid Route | No | Error | No valid route exists for the target destination |
| IPC-1004 | Serialization | Serialization Failed | Yes | Error | The payload could not be encoded or decoded |
| IPC-1005 | Channel | Channel Closed | No | Error | The target channel is not available or has been closed |
| IPC-1006 | Transport | Connection Lost | Yes | Warning | The transport connection was unexpectedly terminated |
| IPC-1007 | Security | Authorization Denied | No | Critical | The process lacks required permissions for this operation |
| IPC-1008 | Routing | Route Expired | Yes | Warning | The dynamic route entry has exceeded its validity period |
| IPC-1009 | Message | Invalid Message Format | No | Error | The message envelope does not conform to the schema |
| IPC-1010 | Transport | Connection Refused | No | Error | The target process rejected the connection |
| IPC-1011 | Security | Token Expired | Yes | Warning | The authentication token has exceeded its validity period |
| IPC-1012 | Serialization | Schema Mismatch | Yes | Error | The message schema version is incompatible |
| IPC-1013 | Routing | Ambiguous Route | Yes | Warning | Multiple valid routes exist; selection requires additional criteria |
| IPC-1014 | Channel | Channel Full | Yes | Warning | The channel message queue has reached capacity |
| IPC-1015 | Transport | Max Retries Exceeded | No | Critical | The maximum retry count has been reached |
| IPC-1016 | Security | Replay Detected | No | Critical | A replay attack was detected on this connection |
| IPC-1017 | Message | Message Expired | No | Warning | The message TTL has elapsed before delivery |
| IPC-1018 | Serialization | Payload Too Large | No | Error | The message payload exceeds the maximum allowed size |
| IPC-1019 | Routing | Dead Letter | No | Error | The message has been moved to the dead letter queue |
| IPC-1020 | Transport | Backpressure Active | Yes | Warning | The transport is applying backpressure due to congestion |
| IPC-1021 | Security | Spoofing Detected | No | Critical | Source or destination spoofing was detected |
| IPC-1022 | Channel | Channel Permission Violation | No | Critical | Unauthorized access attempt to a restricted channel |
| IPC-1023 | Message | Duplicate Message | No | Info | A duplicate message was detected and deduplicated |
| IPC-1024 | Transport | Circuit Breaker Open | Yes | Warning | The circuit breaker is open; requests are being rejected |
| IPC-1025 | Security | Certificate Revoked | No | Critical | The authentication certificate has been revoked |
| IPC-1026 | Routing | Route Not Found | No | Error | No static or dynamic route matches the destination |
| IPC-1027 | Serialization | Encoding Unsupported | No | Error | The requested encoding format is not supported |
| IPC-1028 | Channel | Channel Not Registered | No | Error | The target channel has not been registered |
| IPC-1029 | Message | Sequence Gap Detected | Yes | Warning | A gap in the message sequence was detected |
| IPC-1030 | Transport | Heartbeat Missed | Yes | Warning | Consecutive heartbeats were not received |

### 2.1 Registry Semantics

Each column in the Error Code Registry carries the following normative meaning:

- **Error Code**: The canonical, immutable identifier for this error condition. All references MUST use this exact form (e.g., `IPC-1001`).
- **Category**: The functional domain within the IPC subsystem to which this error belongs. Categories are Transport, Security, Routing, Serialization, Channel, and Message.
- **Name**: A human-readable label for the error condition. Names are informative only; the Error Code is the authoritative identifier.
- **Retryable**: Indicates whether the caller MAY automatically retry the operation that produced this error. `Yes` means automatic retry is permissible; `No` means the caller MUST NOT retry without explicit remediation.
- **Severity**: The classification of the error's operational impact, as defined in Section 4.
- **Description**: A normative statement of the condition that triggers this error. Implementations MUST emit this error code when the described condition is met.

---

## 3 Error Code Ranges

Error Code IDs are allocated within fixed ranges per category. These ranges are reserved and MUST NOT be crossed.

| Category | Range | Allocated Codes | Notes |
|---|---|---|---|
| Transport | 1001–1030 | IPC-1001, IPC-1006, IPC-1010, IPC-1015, IPC-1020, IPC-1024, IPC-1030 | Covers connection lifecycle, congestion control, and fault tolerance |
| Security | Reserved subset | IPC-1002, IPC-1007, IPC-1011, IPC-1016, IPC-1021, IPC-1025 | Covers authentication, authorization, token management, and threat detection |
| Routing | Reserved subset | IPC-1003, IPC-1008, IPC-1013, IPC-1019, IPC-1026 | Covers route resolution, expiration, ambiguity, and dead lettering |
| Serialization | Reserved subset | IPC-1004, IPC-1012, IPC-1018, IPC-1027 | Covers encoding, schema compatibility, payload sizing, and format support |
| Channel | Reserved subset | IPC-1005, IPC-1014, IPC-1022, IPC-1028 | Covers channel availability, capacity, permission enforcement, and registration |
| Message | Reserved subset | IPC-1009, IPC-1017, IPC-1023, IPC-1029 | Covers message format, TTL, deduplication, and sequence integrity |

### 3.1 Allocation Rules

- Error Code IDs within a category MUST fall within the designated range for that category.
- The Transport range (1001–1030) encompasses all categories; individual category subsets are reserved as shown above.
- No Error Code ID MAY be shared across categories.
- Future allocations within a category MUST use the lowest unallocated ID within that category's reserved subset.
- Gaps within a category's reserved subset are reserved for future use and MUST NOT be reassigned to other categories.

---

## 4 Error Severity Levels

Every error code in this catalog is assigned one of four severity levels. Severity determines logging, alerting, and escalation behavior.

| Severity | Level | Definition | Logging Requirement | Alert Requirement |
|---|---|---|---|---|
| Info | 1 | An informational event that does not indicate failure but is worth recording for audit purposes | Logged | No alert required |
| Warning | 2 | A recoverable condition that may require attention but does not halt operations | Logged with warning level | Alert if sustained beyond threshold |
| Error | 3 | A non-recoverable failure that prevents the requested operation from completing | Logged with error level | Alert immediately |
| Critical | 4 | A severe failure that compromises system integrity, security, or availability | Logged with critical level | Alert immediately and escalate |

### 4.1 Severity Assignment Rules

- **Info** severity is assigned exclusively to non-disruptive conditions (e.g., IPC-1023 Duplicate Message).
- **Warning** severity is assigned to transient or recoverable conditions that do not compromise system integrity (e.g., IPC-1001 Connection Timeout, IPC-1020 Backpressure Active).
- **Error** severity is assigned to conditions that prevent successful completion of an operation but do not indicate a security breach (e.g., IPC-1003 Invalid Route, IPC-1018 Payload Too Large).
- **Critical** severity is assigned to conditions that indicate security breaches, authentication failures, or unrecoverable systemic faults (e.g., IPC-1002 Authentication Failed, IPC-1016 Replay Detected).

### 4.2 Severity Enforcement

- Every IPC implementation MUST classify each emitted error according to the severity level assigned in the Error Code Registry.
- Implementations MUST NOT downgrade a Critical error to a lower severity level.
- Implementations MUST NOT elevate an Info error to a higher severity level.
- Alerting systems MUST enforce the alerting requirements specified in the table above.

---

## 5 Error Recovery Procedures

This section defines the normative recovery behavior for each error code. Recovery procedures are categorized as Automatic, Manual, or None.

### 5.1 Recovery Categories

| Recovery Type | Definition | Applicable Errors |
|---|---|---|
| Automatic | The system or caller MAY retry the operation without external intervention | Errors where Retryable = Yes |
| Manual | Remediation requires operator action or external configuration change | Errors where Retryable = No, except Critical |
| None | The operation is irrecoverable and must be abandoned | Critical errors where Retryable = No |

### 5.2 Per-Error Recovery Procedures

| Error Code | Retryable | Recovery Type | Procedure |
|---|---|---|---|
| IPC-1001 | Yes | Automatic | Wait for the retry interval and reattempt the connection. If the error persists beyond the configured retry budget, escalate to IPC-1015. |
| IPC-1002 | No | None | Terminate the connection. Log the failure at Critical severity. No automatic recovery is permitted. |
| IPC-1003 | No | Manual | Review the routing configuration and correct the route definition. Re-attempt only after configuration is verified. |
| IPC-1004 | Yes | Automatic | Reattempt serialization with the same payload. If the error persists, inspect the payload for corruption. |
| IPC-1005 | No | None | The channel is closed; no recovery is possible. The caller MUST establish a new channel or use an alternative destination. |
| IPC-1006 | Yes | Automatic | Re-establish the transport connection. If reconnection fails repeatedly, escalate to IPC-1015. |
| IPC-1007 | No | Manual | The caller MUST obtain the required permissions from the Security Manager. Re-attempt only after authorization is granted. |
| IPC-1008 | Yes | Automatic | Refresh the routing table and re-resolve the route. If no new route is found, escalate to IPC-1026. |
| IPC-1009 | No | None | The message is malformed and irrecoverable. Discard the message and log at Error severity. |
| IPC-1010 | No | None | The target process actively refused the connection. No retry is permitted. Investigate the target process status. |
| IPC-1011 | Yes | Automatic | Refresh the authentication token via the Security Manager and re-attempt the operation. |
| IPC-1012 | Yes | Automatic | Negotiate the schema version with the peer. If negotiation fails, abort the exchange. |
| IPC-1013 | Yes | Automatic | Apply additional selection criteria (e.g., load, latency) to disambiguate the route. |
| IPC-1014 | Yes | Automatic | Queue the message and retry after the backpressure window elapses. |
| IPC-1015 | No | None | The retry budget is exhausted. The operation MUST be abandoned and escalated at Critical severity. |
| IPC-1016 | No | None | Terminate the connection immediately. Log at Critical severity. Initiate a security incident response. |
| IPC-1017 | No | None | Discard the expired message. No retry is permitted. |
| IPC-1018 | No | None | Reject the oversized payload. The caller MUST compress or split the payload before re-attempting. |
| IPC-1019 | No | None | The message resides in the dead letter queue. Recovery requires manual inspection and remediation. |
| IPC-1020 | Yes | Automatic | Wait for the backpressure window to elapse and retry. Monitor congestion metrics to determine clearance. |
| IPC-1021 | No | None | Terminate the connection immediately. Log at Critical severity. Initiate a security incident response. |
| IPC-1022 | No | None | Deny the access request. Log at Critical severity. No recovery is permitted. |
| IPC-1023 | No | Info | Deduplicate the message silently. Log at Info severity. No recovery action is required. |
| IPC-1024 | Yes | Automatic | Wait for the circuit breaker to reset. Retry only after the breaker transitions to the half-open state. |
| IPC-1025 | No | Manual | Obtain a replacement certificate from the certificate authority. Re-authenticate with the new certificate. |
| IPC-1026 | No | Manual | Review and update the routing table. Re-attempt only after a valid route is configured. |
| IPC-1027 | No | None | The encoding format is unsupported. The caller MUST select a supported encoding format. |
| IPC-1028 | No | None | Register the target channel before attempting communication. Re-attempt only after registration is confirmed. |
| IPC-1029 | Yes | Automatic | Request the missing sequence from the sender and resume processing. |
| IPC-1030 | Yes | Automatic | Re-establish the heartbeat monitoring. If heartbeats do not resume, escalate to IPC-1006. |

### 5.3 Escalation Rules

- An error that triggers an Automatic recovery procedure MUST escalate to a higher-severity error if the recovery attempt itself produces a different error code.
- Escalation chains are defined as follows:
  - IPC-1001 (Connection Timeout) → IPC-1015 (Max Retries Exceeded)
  - IPC-1006 (Connection Lost) → IPC-1015 (Max Retries Exceeded)
  - IPC-1008 (Route Expired) → IPC-1026 (Route Not Found)
  - IPC-1030 (Heartbeat Missed) → IPC-1006 (Connection Lost)

---

## 6 Cross-References

This catalog is referenced by the following IPC subsystem RFCs. Each RFC cites error codes from this catalog in its normative prose.

| RFC | Title | Referenced Error Codes |
|---|---|---|
| RFC-0101 | IPC Transport Layer | IPC-1001, IPC-1006, IPC-1010, IPC-1015, IPC-1020, IPC-1024, IPC-1030 |
| RFC-0107 | IPC Security Framework | IPC-1002, IPC-1007, IPC-1011, IPC-1016, IPC-1021, IPC-1025 |
| RFC-108 | IPC Routing Protocol | IPC-1003, IPC-1008, IPC-1013, IPC-1019, IPC-1026 |
| RFC-0111 | IPC Serialization Schema | IPC-1004, IPC-1012, IPC-1018, IPC-1027 |
| RFC-0007 | Runtime IPC Architecture | All error codes in this catalog |

### 6.1 Reference Rules

- Every RFC within the IPC subsystem that defines error conditions MUST cite the Error Code ID from this catalog.
- RFCs MUST NOT define new error codes outside this catalog.
- RFCs MAY refine the description of an error code by adding contextual details, but MUST NOT contradict the normative description in this catalog.

---

## 7 Glossary

| Term | Definition |
|---|---|
| **Automatic Recovery** | A recovery procedure that the system or caller can execute without external intervention, typically involving a retry after a backoff period. |
| **Backpressure** | A congestion control mechanism whereby a transport or channel slows or halts incoming requests when its processing capacity is saturated. |
| **Circuit Breaker** | A fault-tolerance pattern that temporarily halts requests to a failing service, allowing it time to recover before resuming. |
| **Dead Letter Queue** | A storage location for messages that could not be delivered or processed successfully, awaiting manual inspection. |
| **Error Code ID** | The canonical, immutable identifier for an IPC error condition (e.g., `IPC-1001`). |
| **Heartbeat** | A periodic signal sent by a transport to confirm that a connection is alive. |
| **Manual Recovery** | A recovery procedure that requires operator intervention or external configuration changes. |
| **Replay Attack** | A malicious interception and retransmission of a valid authentication exchange to impersonate a legitimate process. |
| **Retryable** | A property of an error code indicating whether the caller is permitted to automatically retry the failed operation. |
| **Schema Mismatch** | A condition where the message schema version used by the sender is incompatible with the schema version expected by the receiver. |
| **Severity Level** | A classification (Info, Warning, Error, Critical) that determines logging, alerting, and escalation behavior for an error. |
| **Spoofing** | A condition where the apparent source or destination identity of a message has been falsified. |
| **Token** | A cryptographically signed credential issued by the Security Manager that authenticates a process for IPC communication. |
| **Transport** | The physical or logical communication medium through which IPC messages are exchanged (e.g., named pipes, TCP sockets, Unix sockets). |

---

## 8 Revision History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 1.0.0 | 2026-06-30 | Atlas Team | Initial release. Defined 30 error codes across six categories (Transport, Security, Routing, Serialization, Channel, Message). Established severity levels, recovery procedures, escalation rules, and cross-references to RFC-0101, RFC-0107, RFC-0108, and RFC-0111. |

---

## 9 Compatibility

- Compatible with Spec Version 1.x.
- Error Code IDs are immutable and forward-compatible across all 1.x minor versions.
- New error codes MAY be added in subsequent minor versions within the reserved ranges defined in Section 3.
- Removal or reassignment of any existing Error Code ID is prohibited across all 1.x versions.

---

*End of specification.*
