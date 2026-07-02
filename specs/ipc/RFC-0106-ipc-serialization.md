# RFC-0106: IPC Serialization

RFC: RFC-0106
Title: IPC Serialization
Status: Accepted
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0101 IPC Overview
  - RFC-0102 IPC Message Model
  - RFC-0103 IPC Transport
Required By:
  - RFC-0104 IPC Routing
  - RFC-0105 IPC Channel
Supersedes: None
Superseded By: None
Category: IPC
Layer: Data
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010 IPC Architecture
  - ADR-0012 Contract-First Specification
Constitution References:
  - Section 3.5 IPC Isolation
Related RFCs:
  - RFC-0107 Security
  - RFC-0111 Error Model
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the IPC subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| IPC | Inter-Process Communication; the unified messaging fabric enabling cross-process data exchange. | Glossary |
| Channel | A bidirectional or unidirectional communication pathway between two endpoints. | Glossary |
| Transport | The underlying mechanism by which messages are delivered between processes. | Glossary |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | Glossary |

---
This specification is Normative. Every Atlas IPC implementation MUST conform to the serialization abstractions, schema validation rules, version compatibility policies, binary and structured format requirements, compression and fragmentation protocols, type system guarantees, and encoding norms defined herein. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and all active ADRs.

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
4. [Serialization Abstraction](#4-serialization-abstraction)
5. [Schema Validation](#5-schema-validation)
6. [Schema Evolution](#6-schema-evolution)
7. [Version Compatibility](#7-version-compatibility)
8. [Binary Model](#8-binary-model)
9. [Structured Model](#9-structured-model)
10. [Compression](#10-compression)
11. [Fragmentation](#11-fragmentation)
12. [Large Payload Handling](#12-large-payload-handling)
13. [Validation Pipeline](#13-validation-pipeline)
14. [Performance](#14-performance)
15. [Serialization Profiles](#15-serialization-profiles)
16. [Schema Registry](#16-schema-registry)
17. [Type System](#17-type-system)
18. [Encoding](#18-encoding)
19. [Mermaid Diagrams](#19-mermaid-diagrams)
20. [Glossary](#20-glossary)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [References](#22-references)
23. [Changelog](#23-changelog)

---


## 2 Goals

- **Format Independence**: The serialization layer MUST abstract the choice of encoding format. Producers and consumers MAY negotiate format independently, and the transport layer MUST remain oblivious to the serialization format used.
- **Schema Enforcement**: Every payload MUST be validated against a registered schema before transmission and upon receipt. Invalid payloads MUST be rejected without reaching application logic.
- **Backward and Forward Compatibility**: Schema evolution MUST preserve compatibility across major version boundaries. Older consumers MUST ignore fields they do not recognize; newer producers MUST include fields older consumers understand.
- **Deterministic Output**: Identical structured data serialized under the same schema and profile MUST produce byte-identical output, enabling content-addressable caching and integrity verification.
- **Performance Predictability**: Serialization and deserialization MUST operate within bounded latency budgets. The specification defines profiles that trade off size for speed, each with documented performance characteristics.
- **Type Safety Across Boundaries**: The Atlas type system MUST provide strong, cross-platform type guarantees. No implicit type coercion MAY occur without explicit schema declaration.

---

- RFC-0220 Plugin IPC (consumes IPC channel model)
- RFC-0327 Workflow IPC (consumes IPC routing model)


## 4 Serialization Abstraction

### 4.1 The Serialization Layer Interface
The serialization layer sits logically between the application data model and the transport framing layer. It exposes a uniform interface with two operations:

- **Serialize**: Transform a structured data object into a sequence of bytes suitable for transport.
- **Deserialize**: Transform a received byte sequence into a structured data object conforming to the target schema.

Both operations accept a profile parameter that selects the serialization strategy (see Section 15). The transport layer MUST receive only the output byte sequence and MUST NOT inspect or modify it.

### 4.2 Format Negotiation
Before exchanging payloads, communicating endpoints MUST negotiate the serialization format through the channel handshake protocol defined in RFC-0105. If negotiation fails, both endpoints MUST fall back to the default format (structured text representation). The negotiated format MUST be recorded in the channel metadata and re-validated on reconnect.

### 4.3 Format Selection Rules
An endpoint MUST select a serialization format based on the following priority:

1. Channel-level capability advertisement.
2. Schema registry format preferences.
3. Profile constraints (binary formats are preferred in the maximum profile; structured formats are preferred in the lightweight profile).
4. Explicit format override in the message header.

### 4.4 Format Agnosticism
The serialization layer MUST NOT depend on any single format being available. Implementations MUST support at minimum the binary model (Section 8) and the structured model (Section 9). Additional formats MAY be registered through the schema registry extension point.

---



---


  - Field ID (positive integer, unique within schema).
  - Field name (string).
  - Field type (from the type system, Section 17).
  - Cardinality (single, array, map).
  - Required flag (boolean).
  - Default value (optional).
  - Constraints (range, length, pattern, enum).
- Index definitions for common query patterns.

### 8.4 Binary Type Tag Encoding
Each primitive type in the binary model is assigned a single-byte tag:

| Tag | Type | Size |
|---|---|---|
| 0x00 | Null | 0 bytes |
| 0x01 | Bool | 1 byte |
| 0x02 | Int8 | 1 byte |
| 0x03 | Int16 | 2 bytes (little-endian) |
| 0x04 | Int32 | 4 bytes (little-endian) |
| 0x05 | Int64 | 8 bytes (little-endian) |
| 0x06 | UInt8 | 1 byte |
| 0x07 | UInt16 | 2 bytes (little-endian) |
| 0x08 | UInt32 | 4 bytes (little-endian) |
| 0x09 | UInt64 | 8 bytes (little-endian) |
| 0x0A | Float32 | 4 bytes (IEEE 754) |
| 0x0B | Float64 | 8 bytes (IEEE 754) |
| 0x0C | String | Variable (length-prefixed UTF-8) |
| 0x0D | Bytes | Variable (length-prefixed raw) |
| 0x0E | Array | Variable (count-prefixed elements) |
| 0x0F | Map | Variable (count-prefixed key-value pairs) |
| 0x10 | Timestamp | 8 bytes (Unix epoch nanoseconds) |
| 0x11 | UUID | 16 bytes (big-endian) |

---

- Establishing the boundaries between IPC layers.


## 10 Compression

### 10.1 Compression Algorithms
The serialization layer supports the following compression algorithms:

| Algorithm | Characteristics | Minimum Size Overhead |
|---|---|---|
| None | No compression applied | N/A |
| LZ4 | Fast compression and decompression, moderate ratio | 16 bytes |
| Zstandard | Tunable compression level, good ratio | 18 bytes |
| Brotli | High ratio, slower compression | 24 bytes |

Implementations MUST support LZ4 as the minimum compression algorithm. Zstandard and Brotli MUST be supported when the maximum serialization profile is selected.

### 10.2 Compression Levels
When using Zstandard or Brotli, the compression level is configurable:

- **Fast**: Level 1-3. Optimized for throughput. Compression ratio is 60 to 70 percent of uncompressed size.
- **Balanced**: Level 4-7. Balanced throughput and ratio. Compression ratio is 50 to 60 percentercent of uncompressed size.
- **Maximum**: Level 8-12. Optimized for ratio. Compression ratio is 40 to 50 percent of uncompressed size.

The default compression level is Balanced. Compression level selection MUST NOT affect decompression correctness; any compressed payload MUST be decompressible regardless of the level at which it was produced.

### 10.3 Compression Tradeoffs
The following tradeoff matrix summarizes the impact of compression algorithm and level selection:

| Algorithm | Compress Speed | Decompress Speed | Ratio | Memory Usage |
|---|---|---|---|---|
| None | N/A | N/A | 1.0x | Minimal |
| LZ4 (Fast) | Very Fast | Very Fast | 2.5x | Low |
| LZ4 (Balanced) | Fast | Very Fast | 3.0x | Low |
| Zstd (Fast) | Fast | Fast | 4.0x | Medium |
| Zstd (Balanced) | Medium | Fast | 5.5x | Medium |
| Zstd (Max) | Slow | Fast | 7.0x | High |
| Brotli (Balanced) | Slow | Medium | 8.0x | High |

Compression SHOULD be applied when the payload exceeds 1 KB. Compression of smaller payloads MAY produce larger output due to overhead and SHOULD be avoided for payloads under 256 bytes.

### 10.4 Compression Flags
The message header includes a compression flag that indicates whether the payload is compressed and which algorithm was used:

- Flag value 0x00: No compression.
- Flag value 0x01: LZ4 compressed.
- Flag value 0x02: Zstandard compressed.
- Flag value 0x03: Brotli compressed.

The receiver MUST verify the compression flag matches the advertised algorithm. A mismatch MUST cause a DeserializationError.

---


|---|---|---|
| Streaming threshold | 1 MB | 1 GB |
| Maximum chunk size | 64 KB | 4 MB |
| Maximum total payload | 1 GB | 10 GB |
| Maximum out-of-band references | 16 | 256 |
| Out-of-band retrieval timeout | 30 s | 300 s |

Exceeding any limit MUST produce a PayloadTooLargeError.

---

### 13.3 Incremental Validation
For streaming payloads, the validation pipeline MAY interleave deserialization and validation. As each chunk arrives, it is validated against the schema before the next chunk is requested. This reduces peak memory usage for large payloads at the cost of slightly increased validation latency.

---

| Operation | Budget | Measurement Context |
|---|---|---|
| Schema lookup | 0.01 ms | From local cache |
| Schema lookup (miss) | 0.50 ms | From remote registry |
| Structural validation | 0.05 ms | 10-field schema |
| Constraint validation | 0.02 ms | Per-constraint check |
| Serialization | See Section 14.1 | Per-profile |
| Deserialization | See Section 14.1 | Per-profile |
| Compression (per MB) | 0.50 ms | LZ4, balanced |
| Decompression (per MB) | 0.20 ms | LZ4 |
| Fragmentation | 0.01 ms | Per fragment |
| Reassembly | 0.02 ms | Per message |
| Checksum computation | 0.005 ms | Per MB |

Latency budgets are measured at p99 over a 60-second sustained load. Budgets are inclusive of any necessary memory allocation but exclusive of transport queuing and network propagation delays.

---

- **Compression**: Zstandard (balanced level) or Brotli.
- **Validation**: Full validation with pattern matching enforcement.
- **Fragmentation**: Supported with strict reassembly.
- **Type Coercion**: None allowed. All types must match exactly.
- **Use Case**: Financial data, audit logs, and other integrity-critical communications.

#### 15.1.4 Maximum Profile
The maximum profile optimizes for throughput and bandwidth efficiency at the cost of implementation complexity.

- **Formats**: Binary model only.
- **Compression**: Zstandard (maximum level) or Brotli (balanced level).
- **Validation**: Full validation with incremental streaming validation.
- **Fragmentation**: Supported with aggressive retransmission.
- **Type Coercion**: None allowed. Schema-strict enforcement.
- **Streaming**: Mandatory for payloads over 1 MB.
- **Use Case**: High-throughput telemetry, bulk data transfers, and bandwidth-constrained channels.

### 15.2 Profile Selection
Endpoints MUST advertise their supported profiles during channel negotiation. Communication between endpoints MUST use the highest common profile. If no common profile exists, the channel handshake MUST fail with ProfileMismatch.

### 15.3 Profile Constraints
The following table summarizes the constraints imposed by each profile:

| Constraint | Lightweight | Balanced | Robust | Maximum |
|---|---|---|---|---|
| Binary format | No | Yes | Yes | Yes |
| Compression | No | Yes | Yes | Yes |
| Fragmentation | No | Yes | Yes | Yes |
| Exact type match | No | No | Yes | Yes |
| Pattern validation | No | Yes | Yes | Yes |
| Streaming | No | Optional | Yes | Yes |
| Deterministic output | No | Yes | Yes | Yes |
| Schema registry required | No | Yes | Yes | Yes |

---

The schema registry MUST provide eventual consistency across all replicas. Schema updates propagate to all replicas within 100 ms under normal conditions. During network partitions, replicas MAY serve stale schema versions, but MUST NOT serve versions that conflict with the registered version history. Conflicting versions MUST be resolved through the registries conflict resolution protocol, which prioritizes the version with the highest timestamp.

---

### 17.2 Type Coercion
Type coercion is the automatic conversion of a value from one type to another during deserialization. The following coercion rules apply:

- **Numeric Widening**: int8 to int16, int16 to int32, int32 to int64, uint8 to uint16, uint16 to uint32, uint32 to uint64, float32 to float64. These coercions are lossless and MAY be applied in the lightweight and balanced profiles.
- **Integer to Float**: int32 to float32, int64 to float64. These coercions are lossy (precision may be lost) and MUST NOT be applied automatically. They require explicit schema declaration.
- **String to Numeric**: Conversion from string to any numeric type is NEVER allowed automatically. It requires explicit schema declaration and is restricted to the lightweight profile.
- **All Other Coercions**: All other type coercions are prohibited unless explicitly declared in the schema and permitted by the active profile.

In the robust and maximum profiles, automatic type coercion is disabled entirely. All types must match the schema declaration exactly.

### 17.3 Type Safety Guarantees
The type system provides the following safety guarantees:

- **No Implicit Lossy Conversion**: No type conversion that may lose data is performed implicitly.
- **Bounds Enforcement**: Numeric types enforce their declared bounds at all times. Values outside bounds produce a ValidationError.
- **Null Safety**: null is a distinct type from all other types. A field declared as non-nullable MUST NOT accept null values. Nullable fields are declared with a nullable modifier.
- **Enum Exhaustiveness**: When a field is declared as an enum, deserialization rejects any value not present in the enum definition, unless the enum is declared as extensible (which permits unknown values in the lightweight and balanced profiles only).
- **Array Element Type**: All elements in an array MUST conform to the declared element type. Mixed-type arrays are not permitted.
- **Map Key Uniqueness**: Map keys MUST be unique within their scope. Duplicate keys produce a ValidationError.

---


## 19 Mermaid Diagrams

### 19.1 Serialization Pipeline

`mermaid`
flowchart TD
    A[Application Data Object] --> B[Pre-Send Validation]
    B -->|Valid| C[Schema Lookup]
    B -->|Invalid| D[ValidationError]
    C --> E[Profile Selection]
    E --> F{Binary or Structured?}
    F -->|Binary| G[Binary Serialization]
    F -->|Structured| H[Structured Serialization]
    G --> I[Compression]
    H --> I
    I --> J{Payload Exceeds MTU?}
    J -->|Yes| K[Fragmentation]
    J -->|No| L[Checksum]
    K --> L
    L --> M[Transport Frame]
    M --> N[Transmit]
    O[Receive] --> P[De-fragmentation]
    P --> Q[Decompression]
    Q --> R[Checksum Verify]
    R --> S[Schema Lookup]
    S --> T{Binary or Structured?}
    T -->|Binary| U[Binary Deserialization]
    T -->|Structured| V[Structured Deserialization]
    U --> W[Post-Receive Validation]
    V --> W
    W -->|Valid| X[Application Data Object]
    W -->|Invalid| Y[ValidationError]
`

### 19.2 Schema Evolution Timeline

`mermaid`
flowchart LR
    A[v1.0 Schema Registered] --> B[v1.1 Schema Additive Change New Optional Field]
    B --> C[v1.2 Schema Additive Change New Enum Value]
    C --> D[v2.0 Schema Breaking Change Field Type Widened]
    D --> E[v2.1 Schema Additive Change New Required Field with Default]
    E --> F[v3.0 Schema Breaking Change Field Removed Tombstone Created]

    A -.->|Compatible| G[Old Consumer Processes v1.x]
    B -.->|Compatible| G
    C -.->|Compatible| G
    D -.->|Negotiate| H[New Consumer Processes v2.x]
    E -.->|Compatible| H
    F -.->|Grace Period| I[Migration Window Dual-Write Active]
`

### 19.3 Fragmentation and Reassembly

`mermaid`
sequenceDiagram
    participant Sender
    participant Serializer
    participant Fragmenter
    participant Transport
    participant Reassembler
    participant Receiver

    Sender->>Serializer: Payload 10 MB
    Serializer->>Fragmenter: Serialized bytes
    Fragmenter->>Fragmenter: Split into 160 fragments
    Fragmenter->>Transport: Fragment 0 seq 0 of 160
    Fragmenter->>Transport: Fragment 1 seq 1 of 160
    Fragmenter->>Transport: Fragment 2 seq 2 of 160
    Transport->>Reassembler: Fragment 0
    Transport->>Reassembler: Fragment 2
    Transport->>Reassembler: Fragment 1
    Reassembler->>Reassembler: Buffer out-of-order
    Reassembler->>Receiver: Reassembled payload
    Receiver->>Receiver: Checksum verify
    Receiver->>Sender: Acknowledgment
`

### 19.4 Type System Hierarchy

`mermaid`
classDiagram
    class Type {
        <<abstract>>
        +String name
        +Bool nullable
        +Validate() ValidationResult
    }
    class PrimitiveType {
        <<abstract>>
        +GetSize() Integer
    }
    class CompositeType {
        <<abstract>>
        +GetElementTypes() Type[]
    }
    class ScalarType {
        <<abstract>>
    }
    class NullType
    class BoolType
    class IntegerType {
        +Int bits
        +Bool signed
    }
    class FloatingPointType {
        +Int bits
    }
    class StringType
    class BytesType
    class TimestampType
    class UuidType
    class ArrayType {
        +Type elementType
        +Int maxLength
    }
    class MapType {
        +Type keyType
        +Type valueType
    }
    class ObjectType {
        +SchemaRef schema
        +Map fields
    }
    class EnumType {
        +String[] values
        +Bool extensible
    }
    class OneOfType {
        +Type[] alternatives
    }

    Type <|-- PrimitiveType
    Type <|-- CompositeType
    PrimitiveType <|-- ScalarType
    ScalarType <|-- NullType
    ScalarType <|-- BoolType
    ScalarType <|-- IntegerType
    ScalarType <|-- FloatingPointType
    ScalarType <|-- StringType
    ScalarType <|-- BytesType
    ScalarType <|-- TimestampType
    ScalarType <|-- UuidType
    CompositeType <|-- ArrayType
    CompositeType <|-- MapType
    CompositeType <|-- ObjectType
    CompositeType <|-- EnumType
    CompositeType <|-- OneOfType
`

---


## 21 Acceptance Criteria

### AC-601
- **Requirement**: Every serialized payload MUST be validated against a registered schema before transmission.
- **Verification**: Attempt to serialize a data object with a missing required field.
- **Expected Result**: Serialization is rejected with ValidationError; no bytes are transmitted.

### AC-602
- **Requirement**: Every received payload MUST be validated against its schema after deserialization.
- **Verification**: Send a structurally valid but constraint-violating payload (e.g., string exceeding max length).
- **Expected Result**: Receiver rejects the payload with ValidationError; application logic is not invoked.

### AC-603
- **Requirement**: Binary serialization MUST produce deterministic output for identical inputs.
- **Verification**: Serialize the same data object twice under the same schema and profile; compare byte sequences.
- **Expected Result**: The two byte sequences are byte-identical.

### AC-604
- **Requirement**: Structured serialization MUST produce deterministic output for identical inputs.
- **Verification**: Serialize the same data object twice under the same schema; compare output strings.
- **Expected Result**: The two output strings are identical, including field ordering.

### AC-605
- **Requirement**: Schema evolution MUST maintain backward compatibility for additive changes.
- **Verification**: Register a new schema version with an optional field; send a message using the new schema to a consumer with the old schema.
- **Expected Result**: The old consumer successfully deserializes the message, ignoring the unknown field.

### AC-606
- **Requirement**: Schema evolution MUST maintain forward compatibility for additive changes.
- **Verification**: Send a message using an old schema to a consumer with a newer schema that includes additional required fields with defaults.
- **Expected Result**: The new consumer successfully deserializes the message, using default values for the new fields.

### AC-607
- **Requirement**: Major version changes MUST NOT be compatible without negotiation.
- **Verification**: Connect a producer with schema v2.0 to a consumer that only supports v1.x.
- **Expected Result**: Connection is rejected with SchemaVersionMismatch unless negotiation succeeds.

### AC-608
- **Requirement**: Type coercion MUST be disabled in the robust and maximum profiles.
- **Verification**: Send a payload with an int32 field containing a value that requires int64 in the robust profile.
- **Expected Result**: Deserialization fails with ValidationError; no implicit widening occurs.

### AC-609
- **Requirement**: All string fields MUST be valid UTF-8.
- **Verification**: Send a payload containing a string field with invalid UTF-8 byte sequences.
- **Expected Result**: Deserialization fails with ValidationError.

### AC-610
- **Requirement**: Numeric types MUST enforce their declared bounds.
- **Verification**: Send a uint8 field with value 256.
- **Expected Result**: Deserialization fails with ValidationError; value exceeds declared range.

### AC-611
- **Requirement**: Compression MUST be applied when the payload exceeds 1 KB and the profile mandates it.
- **Verification**: Serialize a 2 KB payload under the robust profile with compression enabled.
- **Expected Result**: The transmitted byte sequence is smaller than the uncompressed equivalent.

### AC-612
- **Requirement**: Decompression MUST succeed for any valid compressed payload regardless of compression level.
- **Verification**: Compress a payload at the maximum level and decompress with a fast-level decoder.
- **Expected Result**: Decompression succeeds and produces the original uncompressed bytes.

### AC-613
- **Requirement**: Fragmentation MUST occur when a payload exceeds the channel MTU.
- **Verification**: Serialize a payload larger than the channel MTU.
- **Expected Result**: The payload is split into multiple fragments, each not exceeding the MTU.

### AC-614
- **Requirement**: Reassembly MUST tolerate out-of-order fragment arrival.
- **Verification**: Transmit fragments in reverse order and verify reassembly.
- **Expected Result**: The reassembled payload is identical to the original.

### AC-615
- **Requirement**: Missing fragments MUST trigger a reassembly timeout and rejection.
- **Verification**: Transmit all fragments except one and wait for the timeout period.
- **Expected Result**: The receiver discards all buffered fragments and returns FragmentTimeoutError after the timeout.

### AC-616
- **Requirement**: Streaming serialization MUST begin transmitting bytes before the full payload is assembled.
- **Verification**: Stream a 10 MB payload and measure time to first byte on the wire versus time to full assembly.
- **Expected Result**: First byte is transmitted before the full payload is assembled.

### AC-617
- **Requirement**: Out-of-band references MUST include a content hash for integrity verification.
- **Verification**: Create an out-of-band reference and verify the content hash matches the referenced data.
- **Expected Result**: Hash verification succeeds for correct data and fails for tampered data.

### AC-618
- **Requirement**: The schema registry MUST store schema documents immutably.
- **Verification**: Register a schema, then attempt to modify it in place.
- **Expected Result**: Modification is rejected; a new version must be registered.

### AC-619
- **Requirement**: Schema resolution MUST succeed within 0.5 ms from a remote registry on a cache miss.
- **Verification**: Measure the latency of resolving a schema from a remote registry under normal load.
- **Expected Result**: Latency is less than or equal to 0.5 ms for 99 percent of requests.

### AC-620
- **Requirement**: Local schema cache MUST be refreshed at least once per TTL interval.
- **Verification**: Configure a 5-minute TTL and observe cache refresh behavior over 10 minutes.
- **Expected Result**: The cache is refreshed at least twice within the 10-minute window.

### AC-621
- **Requirement**: The binary model MUST include a CRC32 checksum covering all preceding bytes.
- **Verification**: Serialize a message and verify the checksum field matches the computed CRC32.
- **Expected Result**: Checksum matches.

### AC-622
- **Requirement**: Tampering with serialized bytes MUST be detectable via checksum verification.
- **Verification**: Flip a bit in the middle of a serialized payload and attempt deserialization.
- **Expected Result**: Checksum verification fails; deserialization is rejected.

### AC-623
- **Requirement**: Enum fields MUST reject values not declared in the enum definition (non-extensible enums).
- **Verification**: Send a message with an enum field containing an undeclared value.
- **Expected Result**: Deserialization fails with ValidationError.

### AC-624
- **Requirement**: Array elements MUST all conform to the declared element type.
- **Verification**: Send an array containing elements of mixed types where the schema declares a single element type.
- **Expected Result**: Deserialization fails with ValidationError at the first non-conforming element.

### AC-625
- **Requirement**: Map keys MUST be unique within their scope.
- **Verification**: Send a map with duplicate keys.
- **Expected Result**: Deserialization fails with ValidationError.

### AC-626
- **Requirement**: Null values MUST be distinguishable from absent fields.
- **Verification**: Send a message where a nullable field is explicitly null versus a message where the field is omitted.
- **Expected Result**: The deserialized objects differ: one has a null value, the other has the field absent.

### AC-627
- **Requirement**: Timestamps MUST be encoded as nanosecond-precision Unix epoch values.
- **Verification**: Serialize a timestamp and verify the binary representation matches the expected nanosecond value.
- **Expected Result**: The decoded timestamp matches the original value with nanosecond precision.

### AC-628
- **Requirement**: UUIDs MUST be encoded as 16-byte big-endian sequences in the binary model.
- **Verification**: Serialize a UUID and inspect the binary representation.
- **Expected Result**: The 16 bytes match the canonical big-endian UUID representation.

### AC-629
- **Requirement**: The serialization layer MUST remain independent of the transport layer.
- **Verification**: Swap the transport from channel-based to broadcast-based without modifying serialization code.
- **Expected Result**: Serialization operates identically; no transport-specific logic is present in the serialization layer.

### AC-630
- **Requirement**: Pre-send validation MUST not be skipped for untrusted senders.
- **Verification**: Disable pre-send validation for a sender and transmit a malformed message.
- **Expected Result**: The receiver post-receive validation catches the malformation and rejects the message.

### AC-631
- **Requirement**: Post-receive validation MUST always be performed, regardless of pre-send validation status.
- **Verification**: Trust a sender that skips pre-send validation and send a maliciously crafted message.
- **Expected Result**: The receiver post-receive validation rejects the message before application logic is reached.

### AC-632
- **Requirement**: Incremental validation MUST produce the same results as full validation.
- **Verification**: Validate a 10 MB payload incrementally and then validate the same payload in full; compare results.
- **Expected Result**: Both validation approaches produce identical results.

### AC-633
- **Requirement**: Serialization throughput MUST meet the lightweight profile target of 100 MB/s on the reference platform.
- **Verification**: Run a sustained serialization benchmark with 10 KB payloads under the lightweight profile.
- **Expected Result**: Measured throughput is greater than or equal to 100 MB/s.

### AC-634
- **Requirement**: Deserialization throughput MUST meet the balanced profile target of 100 MB/s on the reference platform.
- **Verification**: Run a sustained deserialization benchmark with 10 KB payloads under the balanced profile.
- **Expected Result**: Measured throughput is greater than or equal to 100 MB/s.

### AC-635
- **Requirement**: Serialization p99 latency MUST not exceed the profile-defined budget.
- **Verification**: Run a 60-second serialization benchmark and measure p99 latency.
- **Expected Result**: p99 latency is within the budget defined in Section 14.3 for the active profile.

### AC-636
- **Requirement**: Schema deprecation MUST include a removal date at least 12 months from the announcement.
- **Verification**: Deprecate a schema and inspect the deprecation metadata.
- **Expected Result**: The removal date is at least 12 months after the announcement date.

### AC-637
- **Requirement**: Deprecated fields MUST produce deprecation warnings in the message metadata.
- **Verification**: Send a message containing a deprecated field and inspect the metadata.
- **Expected Result**: The message metadata includes a deprecation_warning flag.

### AC-638
- **Requirement**: After the removal date, deprecated fields MUST be rejected by validators.
- **Verification**: Send a message containing a field removed after its deprecation grace period.
- **Expected Result**: Validation fails with ValidationError.

### AC-639
- **Requirement**: Schema registry MUST support both pull and push distribution mechanisms.
- **Verification**: Subscribe to schema updates via push and verify that updates are delivered within 100 ms.
- **Expected Result**: Schema updates are received within the 100 ms propagation window.

### AC-640
- **Requirement**: Schema registry replicas MUST achieve eventual consistency within 100 ms.
- **Verification**: Write a schema to one replica and read from another replica within 100 ms.
- **Expected Result**: The read replica returns the newly written schema.

### AC-641
- **Requirement**: The magic bytes prefix in the binary model MUST uniquely identify the format version.
- **Verification**: Inspect the first four bytes of a serialized binary payload.
- **Expected Result**: The magic bytes match the declared binary format version.

### AC-642
- **Requirement**: Field IDs in the binary model MUST be positive integers.
- **Verification**: Inspect the schema definition for field ID values.
- **Expected Result**: All field IDs are positive integers greater than zero.

### AC-643
- **Requirement**: The structured model MUST reject duplicate field names at the same nesting level.
- **Verification**: Construct a structured payload with duplicate field names at the same level.
- **Expected Result**: Deserialization fails with ValidationError.

### AC-644
- **Requirement**: Maximum nesting depth MUST be enforced at 32 levels by default.
- **Verification**: Construct a payload with 33 levels of nested objects.
- **Expected Result**: Deserialization fails with ValidationError.

### AC-645
- **Requirement**: Compression overhead MUST not exceed the algorithm-defined minimum for empty payloads.
- **Verification**: Compress an empty payload and measure the output size.
- **Expected Result**: Output size equals or is less than the algorithm-defined overhead.

### AC-646
- **Requirement**: Fragment checksums MUST cover only the fragment data, not the fragment header.
- **Verification**: Compute the fragment checksum independently and compare with the stored value.
- **Expected Result**: Checksums match when computed over fragment data only.

### AC-647
- **Requirement**: The type system MUST support at least all types listed in Section 17.1.
- **Verification**: Register a schema using every declared type and serialize and deserialize a value of each type.
- **Expected Result**: All types serialize and deserialize correctly.

### AC-648
- **Requirement**: Type coercion for numeric widening MUST be lossless.
- **Verification**: Serialize an int64 maximum value, deserialize as int32-widened, and compare.
- **Expected Result**: The value is preserved exactly without overflow or truncation.

### AC-649
- **Requirement**: NaN and Infinity floating-point values MUST be preserved through serialization.
- **Verification**: Serialize a float64 field with NaN and Infinity values and deserialize.
- **Expected Result**: The deserialized values are NaN and Infinity respectively.

### AC-650
- **Requirement**: Timestamps outside the supported range (1678-2262) MUST be rejected.
- **Verification**: Attempt to serialize a timestamp representing the year 1600.
- **Expected Result**: Serialization fails with ValidationError.

### AC-651
- **Requirement**: Endianness conversion MUST be transparent to the application layer.
- **Verification**: Serialize on a little-endian system and deserialize on a big-endian system (simulated).
- **Expected Result**: The deserialized values match the original values without application-level intervention.

### AC-652
- **Requirement**: The serialization profile selection MUST use the highest common profile.
- **Verification**: Endpoint A supports lightweight and balanced; Endpoint B supports balanced and robust.
- **Expected Result**: The negotiated profile is balanced (the highest common profile).

### AC-653
- **Requirement**: Profile mismatch during channel negotiation MUST cause handshake failure.
- **Verification**: Endpoint A supports only lightweight; Endpoint B supports only maximum.
- **Expected Result**: Channel handshake fails with ProfileMismatch.

### AC-654
- **Requirement**: Schema version metadata MUST include creation, modification, and deprecation timestamps.
- **Verification**: Register a schema and inspect its metadata in the registry.
- **Expected Result**: All three timestamps are present and correctly formatted.

### AC-655
- **Requirement**: The validation pipeline MUST halt on the first error and report the specific failing rule.
- **Verification**: Send a payload violating both a required field rule and a type rule.
- **Expected Result**: The error report identifies the first violated rule; subsequent violations are not reported.

---

- Operating system scheduling.


## 23 Changelog

- **1.0.0** (2026-06-30): Initial release. Defined the complete IPC serialization specification including serialization abstraction, schema validation, schema evolution, version compatibility, binary and structured models, compression, fragmentation, large payload handling, validation pipeline, performance targets, serialization profiles, schema registry, type system, encoding norms, Mermaid diagrams, glossary, and 55 acceptance criteria.


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

All IPC contracts are defined as abstract behavioral interfaces.

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

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Accepted | 2026-06-30 | Atlas Team | Initial publication |
| 1.1.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






