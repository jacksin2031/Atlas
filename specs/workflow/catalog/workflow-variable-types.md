---
title: Workflow Variable Types Taxonomy
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Variable Types Taxonomy

## Overview

This document defines the variable type taxonomy for the Atlas Development System (ADS) workflow engine. Variables are the fundamental data carriers within workflow contexts. The variable type system provides a unified abstraction for all data representations used in workflow execution, including inputs, outputs, computed values, and system metadata.

Variable types are abstract entities. Concrete serialization and transmission formats are implementation-defined, but the type semantics, coercion rules, and validation behavior described herein are normative.

## Nine Variable Types

The workflow engine defines nine primitive and composite variable types. Each type has distinct semantics, serialization behavior, and coercion rules.

| Type | Category | Mutable | Comparable | Serializable |
|------|----------|---------|-----------|-------------|
| String | Text | NO | YES | YES |
| Integer | Numeric | NO | YES | YES |
| Float | Numeric | NO | YES | YES |
| Boolean | Logical | NO | YES | YES |
| Array | Composite | YES | NO | YES |
| Object | Composite | YES | NO | YES |
| Binary | Raw | NO | NO | YES |
| Timestamp | Temporal | NO | YES | YES |
| UUID | Identifier | NO | YES | YES |

## Detailed Variable Type Definitions

### String

A sequence of Unicode characters representing text data.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | String | The character sequence |
| `encoding` | Enum | `UTF-8`, `UTF-16`, or `ASCII` |
| `length` | Integer | Number of characters |
| `max_length` | Integer | Declared maximum length |

**Constraints:**
- Strings are immutable once created.
- Maximum length is enforced per the manifest's string size policy.
- Empty strings are valid and distinct from null.

**Coercion Rules:**
- Integer to String: Decimal representation of the integer value.
- Float to String: Decimal representation with configurable precision.
- Boolean to String: `true` or `false`.
- Array to String: Elements joined by comma separator.
- Object to String: JSON canonical serialization.
- Timestamp to String: ISO 8601 formatted representation.
- UUID to String: Hyphenated hexadecimal representation.
- Binary to String: Base64 encoded representation.

### Integer

A whole number value with arbitrary precision within the manifest's declared range.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Integer | The numeric value |
| `min` | Integer | Minimum allowed value |
| `max` | Integer | Maximum allowed value |
| `signed` | Boolean | Whether negative values are permitted |

**Constraints:**
- Integers are immutable once created.
- Range validation is enforced at assignment time.
- Overflow produces a Type error per `workflow-errors.md`.

**Coercion Rules:**
- Float to Integer: Truncated toward zero.
- String to Integer: Parsed decimal representation; whitespace is trimmed.
- Boolean to Integer: `true` becomes 1; `false` becomes 0.
- Timestamp to Integer: Unix epoch seconds.
- UUID to Integer: Not coercible (permanent error).

### Float

A floating-point number value with configurable precision.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Float | The numeric value |
| `precision` | Enum | `single`, `double`, or `decimal` |
| `min` | Float | Minimum allowed value |
| `max` | Float | Maximum allowed value |
| `NaN_handling` | Enum | `error`, `zero`, or `preserve` |

**Constraints:**
- Floats are immutable once created.
- NaN and Infinity values are handled per the declared policy.
- Precision loss during coercion is documented in the variable metadata.

**Coercion Rules:**
- Integer to Float: Exact representation if within float range; otherwise rounded.
- String to Float: Parsed decimal or scientific notation; locale-independent.
- Boolean to Float: `true` becomes 1.0; `false` becomes 0.0.
- Timestamp to Float: Unix epoch seconds as a floating-point value.
- UUID to Float: Not coercible (permanent error).

### Boolean

A binary logical value representing truth or falsity.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Boolean | `true` or `false` |
| `default` | Boolean | Default value when undefined |

**Constraints:**
- Booleans are immutable once created.
- Undefined booleans resolve to the declared default.
- Null booleans are distinct from false.

**Coercion Rules:**
- String to Boolean: `true`, `yes`, `1`, `on` coerce to true; `false`, `no`, `0`, `off` coerce to false. Other values produce a Type error.
- Integer to Boolean: 0 coerces to false; all other values coerce to true.
- Float to Boolean: 0.0 coerces to false; all other values coerce to true.
- Array to Boolean: Empty array coerces to false; non-empty coerces to true.
- Object to Boolean: Empty object coerces to false; non-empty coerces to true.
- Timestamp to Boolean: Not coercible (permanent error).
- UUID to Boolean: Not coercible (permanent error).
- Binary to Boolean: Not coercible (permanent error).

### Array

An ordered collection of elements of a single declared type.

| Attribute | Type | Description |
|-----------|------|-------------|
| `elements` | Array | The collection of elements |
| `element_type` | Enum | Declared type of all elements |
| `length` | Integer | Number of elements |
| `max_length` | Integer | Maximum allowed elements |
| `ordered` | Boolean | Whether element order is significant |

**Constraints:**
- Arrays are mutable; elements MAY be added or removed.
- All elements MUST conform to the declared element type.
- Maximum length is enforced per the manifest's array size policy.
- Null arrays are distinct from empty arrays.

**Coercion Rules:**
- String to Array: Split by delimiter; each substring becomes an element.
- Object to Array: Values extracted in canonical key order.
- Binary to Array: Decoded into byte elements.
- Scalar to Array: Single element array containing the scalar value.

### Object

A keyed collection of name-value pairs with a declared schema.

| Attribute | Type | Description |
|-----------|------|-------------|
| `fields` | Object | The key-value pairs |
| `schema` | Object | Declared field types and constraints |
| `required_fields` | Array | Fields that must be present |
| `nullable_fields` | Array | Fields that may be null |

**Constraints:**
- Objects are mutable; fields MAY be added, modified, or removed.
- Field types MUST conform to the declared schema.
- Required fields MUST be present for the object to be valid.
- Null objects are distinct from empty objects.

**Coercion Rules:**
- Array to Object: Elements paired with generated keys (0, 1, 2, ...).
- String to Object: Parsed as structured text (e.g., key=value pairs).
- Binary to Object: Decoded and parsed per the declared format.
- Scalar to Object: Single field with key `_value` containing the scalar.

### Binary

An opaque sequence of bytes with no inherent structure.

| Attribute | Type | Description |
|-----------|------|-------------|
| `data` | Binary | The byte sequence |
| `encoding` | Enum | `raw`, `base64`, or `hex` |
| `length` | Integer | Number of bytes |
| `max_length` | Integer | Maximum allowed bytes |

**Constraints:**
- Binary values are immutable once created.
- Maximum length is enforced per the manifest's binary size policy.
- Binary values are transmitted and stored with the declared encoding.
- Null binary values are distinct from empty binary values.

**Coercion Rules:**
- String to Binary: Decoded from base64 or hex encoding.
- Array to Binary: Elements concatenated as bytes.
- Object to Binary: Serialized per the declared schema.
- Scalar to Binary: Converted to byte representation.

### Timestamp

A point in time represented as an absolute instant.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Timestamp | The time instant |
| `timezone` | String | IANA timezone identifier |
| `precision` | Enum | `second`, `millisecond`, or `microsecond` |
| `monotonic` | Boolean | Whether the timestamp is monotonic |

**Constraints:**
- Timestamps are immutable once created.
- Comparison and arithmetic operations use the declared precision.
- Monotonic timestamps are unaffected by wall-clock adjustments.
- Null timestamps are distinct from epoch-zero timestamps.

**Coercion Rules:**
- String to Timestamp: Parsed as ISO 8601 or Unix epoch.
- Integer to Timestamp: Interpreted as Unix epoch seconds or milliseconds based on precision.
- Float to Timestamp: Interpreted as Unix epoch with fractional seconds.
- Duration to Timestamp: Added to the reference timestamp to produce a new timestamp.

### UUID

A universally unique identifier following the standard UUID format.

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | UUID | The 128-bit identifier |
| `version` | Integer | UUID version (1-5) |
| `namespace` | String | Namespace for version 3 and 5 |
| `generated` | Boolean | Whether the UUID was generated by the engine |

**Constraints:**
- UUIDs are immutable once created.
- Version compatibility is enforced for UUIDs exchanged between systems.
- Null UUIDs are distinct from zero UUIDs.

**Coercion Rules:**
- String to UUID: Parsed from hyphenated or compact hexadecimal representation.
- Binary to UUID: First 16 bytes interpreted as a UUID.
- Timestamp to UUID: Version 1 UUID generated from the timestamp.
- All other types: Not coercible (permanent error).

## Type Coercion Rules

Type coercion is the automatic conversion of a variable from one type to another. The following rules govern coercion:

### Coercion Direction

1. Coercion is unidirectional; the source type is converted to the target type.
2. Bidirectional coercion is achieved by applying coercion in both directions.
3. Cyclic coercion chains are prohibited; the coercion graph MUST be acyclic.

### Coercion Safety

| Safety Level | Description | Examples |
|-------------|-------------|----------|
| Safe | Lossless coercion; no data is discarded | Integer to Float, Boolean to Integer |
| Partial | Lossy coercion; some precision may be discarded | Float to Integer, String to Integer |
| Unsafe | Coercion may fail; requires explicit opt-in | Binary to Object, String to UUID |
| Prohibited | Coercion is never permitted | UUID to Float, Timestamp to Boolean |

### Coercion Errors

Unsafe or prohibited coercions produce a TypeMismatch error per `workflow-errors.md`. Safe and partial coercions always succeed.

## Type Validation

Variables are validated against their declared types at assignment time.

| Validation Check | Description | Failure Behavior |
|-----------------|-------------|-----------------|
| Type match | Variable value must match declared type | TypeMismatch error |
| Range check | Numeric values must be within declared range | RangeViolation error |
| Length check | String, Array, and Binary lengths must be within limits | LengthViolation error |
| Schema check | Object fields must conform to declared schema | SchemaViolation error |
| Nullability | Null values must be permitted for the variable | NullViolation error |
| Uniqueness | UUID variables must be unique within scope | UniquenessViolation error |

## Type Serialization

Variables are serialized for storage, transmission, and persistence.

| Format | Supported Types | Schema Versioning |
|--------|----------------|-------------------|
| Canonical JSON | String, Integer, Float, Boolean, Array, Object | Forward and backward compatible |
| Binary | Binary, Timestamp, UUID | Fixed-length encoding |
| Text | String, Timestamp | Human-readable representation |
| Protocol | All types | Version-tagged messages |

Serialization preserves type information; deserialization reconstructs the exact original type.
