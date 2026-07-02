---
id: ATLAS-STORAGE-CATALOG-SCHEMA
title: Storage Schema Definitions Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Schema Definitions Catalog

## 1. Purpose

This catalog defines the canonical schema structure types and field data types used by the Atlas Storage subsystem for resource validation and evolution.

## 2. Schema Type Catalog

| Schema Type ID | Name | Description | Supported Operations | RFC Reference |
|---|---|---|---|---|
| SCHEMA-DOC | Document | Flexible key-value structure with nested objects. | CRUD, query, scan | RFC-0405 |
| SCHEMA-HIER | Hierarchical | Tree-structured data with parent-child relationships. | CRUD, traverse | RFC-0405 |
| SCHEMA-GRAPH | Graph | Node-edge structure with relationship queries. | CRUD, traverse, match | RFC-0405 |
| SCHEMA-REL | Relational | Tabular data with column definitions and constraints. | CRUD, join, aggregate | RFC-0405 |
| SCHEMA-TEMP | Temporal | Time-series data with timestamp-based indexing. | CRUD, range query | RFC-0405 |
| SCHEMA-SPATIAL | Spatial | Geospatial data with coordinate-based queries. | CRUD, proximity search | RFC-0405 |

## 3. Field Data Type Catalog

| Field Type ID | Name | Description | Valid Operations | Nullable |
|---|---|---|---|---|
| FT-STRING | String | Variable-length text. | Read, write, scan | Yes |
| FT-INTEGER | Integer | Signed 64-bit whole number. | Read, write, query | Yes |
| FT-FLOAT | Float | IEEE 754 double-precision number. | Read, write, query | Yes |
| FT-BOOLEAN | Boolean | True or false value. | Read, write | No |
| FT-TIMESTAMP | Timestamp | ISO 8601 datetime value. | Read, write, query | Yes |
| FT-UUID | UUID | 128-bit universally unique identifier. | Read, write | No |
| FT-BINARY | Binary | Raw byte sequence. | Read, write | Yes |
| FT-ARRAY | Array | Ordered list of homogeneous elements. | Read, write | Yes |
| FT-OBJECT | Object | Nested key-value structure. | Read, write | Yes |
| FT-ENUM | Enum | Value from a predefined set. | Read, write | No |
| FT-RANGE | Range | Numeric range with lower and upper bounds. | Read, write, query | Yes |
| FT-COMPOSITE | Composite | Structured type with multiple named fields. | Read, write | Yes |

## 4. Schema Evolution Compatibility Rules

| Change Type | Direction | Compatibility | Description |
|---|---|---|---|
| Add Field | Forward | Compatible | New field added with default value. |
| Remove Field | Backward | Compatible | Field removed; readers using old schema ignore missing data. |
| Rename Field | Bidirectional | Breaking | Field name change requires migration. |
| Change Type | Forward | Breaking | Field type change requires data transformation. |
| Make Required | Backward | Breaking | Previously nullable field becomes required. |
| Add Constraint | Forward | Compatible | New constraint on existing field. |
| Remove Constraint | Backward | Compatible | Existing constraint removed. |
| Add Nested Field | Forward | Compatible | Field added to nested object. |
| Remove Nested Field | Backward | Compatible | Nested field removed. |

## 5. Validation Rules

1. Every schema type identifier MUST match the regex ^SCHEMA-[A-Z]+$.
2. Every field type identifier MUST match the regex ^FT-[A-Z]+$.
3. Schema definitions MUST declare at least one field.
4. Schema evolution MUST follow the compatibility rules in Section 4.
5. Breaking changes MUST be accompanied by a migration plan per RFC-0408.
6. Field names MUST use camelCase and match the regex ^[a-z][a-zA-Z0-9]*$.
7. Default values MUST be compatible with the field type.
