---
title: Workflow Operators Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Operators Reference

## Overview

This document defines the operator reference for the Atlas Development System (ADS) workflow engine. Operators are atomic comparison and membership predicates used by condition entities to evaluate boolean expressions. Operators are the building blocks of all conditional logic in the workflow graph.

Operators MUST be pure functions of their operands. They MUST NOT produce side effects. Operator semantics are defined at the abstract entity level; implementations MUST preserve these semantics regardless of the underlying evaluation engine.

## Operator Taxonomy

The workflow engine defines fifteen operators organized into three groups: comparison, membership, and null-state operators.

### Comparison Operators

Comparison operators evaluate relational predicates between two operands.

| Operator | Symbol | Operand Types | Result Type | Associativity |
|----------|--------|--------------|-------------|--------------|
| Equal | `==` | Any comparable type | Boolean | Symmetric |
| NotEqual | `!=` | Any comparable type | Boolean | Symmetric |
| LessThan | `<` | Numeric, Temporal, Ordinal | Boolean | Non-symmetric |
| GreaterThan | `>` | Numeric, Temporal, Ordinal | Boolean | Non-symmetric |
| LessThanOrEqual | `<=` | Numeric, Temporal, Ordinal | Boolean | Non-symmetric |
| GreaterThanOrEqual | `>=` | Numeric, Temporal, Ordinal | Boolean | Non-symmetric |

#### Equal

Tests whether two operands have equivalent values.

| Property | Value |
|----------|-------|
| Semantics | Returns true if and only if left and right operands represent the same logical value |
| Type Coercion | Numeric types are coerced to a common type before comparison |
| Null Handling | Two null operands evaluate to true; a null and a non-null evaluate to false |
| Container Comparison | Arrays and objects are compared element-wise or field-wise in canonical order |
| Transitivity | If A equals B and B equals C, then A equals C |

#### NotEqual

Tests whether two operands have different values.

| Property | Value |
|----------|-------|
| Semantics | Returns true if and only if left and right operands do NOT represent the same logical value |
| Type Coercion | Same as Equal |
| Null Handling | Two null operands evaluate to false; a null and a non-null evaluate to true |
| Container Comparison | Arrays and objects differ if any corresponding element or field differs |
| Transitivity | Not transitive by definition |

#### LessThan

Tests whether the left operand is strictly less than the right operand.

| Property | Value |
|----------|-------|
| Semantics | Returns true if left < right under the natural ordering of the operand type |
| Numeric | Standard numeric ordering (signed, unsigned as declared) |
| Temporal | Chronological ordering; earlier times are less than later times |
| Ordinal | Lexicographic or enumerated ordering |
| Null Handling | Comparison with null returns false |
| Type Requirement | Both operands MUST be of a comparable type |

#### GreaterThan

Tests whether the left operand is strictly greater than the right operand.

| Property | Value |
|----------|-------|
| Semantics | Returns true if left > right under the natural ordering of the operand type |
| Relationship | Logically equivalent to `NOT(LessThanOrEqual)` |
| Null Handling | Comparison with null returns false |
| Type Requirement | Both operands MUST be of a comparable type |

#### LessThanOrEqual

Tests whether the left operand is less than or equal to the right operand.

| Property | Value |
|----------|-------|
| Semantics | Returns true if left <= right under the natural ordering of the operand type |
| Relationship | Logically equivalent to `LessThan OR Equal` |
| Null Handling | Comparison with null returns false |
| Type Requirement | Both operands MUST be of a comparable type |

#### GreaterThanOrEqual

Tests whether the left operand is greater than or equal to the right operand.

| Property | Value |
|----------|-------|
| Semantics | Returns true if left >= right under the natural ordering of the operand type |
| Relationship | Logically equivalent to `GreaterThan OR Equal` |
| Null Handling | Comparison with null returns false |
| Type Requirement | Both operands MUST be of a comparable type |

### Membership Operators

Membership operators test whether an operand belongs to a collection, matches a pattern, or falls within a range.

| Operator | Symbol | Operand Types | Result Type |
|----------|--------|--------------|-------------|
| Contains | `contains` | Container, Element | Boolean |
| StartsWith | `startsWith` | String, String | Boolean |
| EndsWith | `endsWith` | String, String | Boolean |
| Matches | `matches` | String, Pattern | Boolean |
| In | `in` | Element, Set | Boolean |
| Between | `between` | Numeric/Temporal, Range | Boolean |

#### Contains

Tests whether a container entity includes a specified element.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left operand (container) includes the right operand (element) |
| Array | Checks for element presence in the array |
| Object | Checks for key presence in the object |
| String | Checks for substring presence |
| Null Handling | Container is null: returns false. Element is null: returns true if container accepts null |

#### StartsWith

Tests whether a string begins with a specified prefix.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left string begins with the right string as a prefix |
| Case Sensitivity | Case-sensitive by default; configurable via condition metadata |
| Empty Prefix | An empty right operand always returns true |
| Null Handling | Null left or right operand returns false |

#### EndsWith

Tests whether a string ends with a specified suffix.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left string ends with the right string as a suffix |
| Case Sensitivity | Case-sensitive by default; configurable via condition metadata |
| Empty Suffix | An empty right operand always returns true |
| Null Handling | Null left or right operand returns false |

#### Matches

Tests whether a string matches a pattern.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left string satisfies the pattern defined by the right operand |
| Pattern Language | Regular-expression-like syntax with workflow-specific extensions |
| Anchoring | Patterns are anchored to the full string by default |
| Flags | Case-insensitive and multiline flags are configurable via condition metadata |
| Null Handling | Null left or right operand returns false |
| Invalid Pattern | If the right operand is not a valid pattern, evaluation returns false with a warning |

#### In

Tests whether an element is a member of a set.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left operand is an element of the right operand set |
| Set Representation | Sets are represented as arrays or entity references to set collections |
| Membership Criteria | Uses Equal operator semantics for membership determination |
| Null Handling | Null left operand returns false. Null right operand returns false |
| Performance | Set lookup is O(n) for arrays; O(log n) for sorted sets; O(1) for hash-based sets |

#### Between

Tests whether a value falls within an inclusive range.

| Property | Value |
|----------|-------|
| Semantics | Returns true if left >= range.lower AND left <= range.upper |
| Range Representation | The right operand is a two-element array [lower, upper] |
| Ordering | Lower bound MUST be less than or equal to upper bound; otherwise, evaluation returns false |
| Null Handling | Null left operand returns false. Null range bounds return false |
| Type | Supports numeric and temporal types |

### Null-State Operators

Null-state operators test the existence or absence of values.

| Operator | Symbol | Operand Types | Result Type |
|----------|--------|--------------|-------------|
| Exists | `exists` | Any | Boolean |
| IsNull | `isNull` | Any | Boolean |
| IsNotNull | `isNotNull` | Any | Boolean |

#### Exists

Tests whether an entity reference resolves to a non-null value.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left operand entity reference resolves to a value that is not null |
| Resolution | Entity resolution follows the context hierarchy per `workflow-context.md` |
| Dereferencing | If the entity reference points to a container, existence of the container is tested, not its contents |
| Null Handling | Null entity reference returns false |

#### IsNull

Tests whether an entity reference resolves to a null value.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left operand entity reference resolves to null |
| Definition of Null | Null includes: absent entity reference, explicitly null value, and empty container where emptiness is defined as null-equivalent |
| Relationship | Logically equivalent to `NOT(Exists)` |
| Null Handling | Always returns true when the operand is null |

#### IsNotNull

Tests whether an entity reference resolves to a non-null value.

| Property | Value |
|----------|-------|
| Semantics | Returns true if the left operand entity reference resolves to a non-null value |
| Relationship | Logically equivalent to `Exists` |
| Null Handling | Always returns false when the operand is null |

## Operator Type Requirements

Each operator has specific type requirements that MUST be satisfied at evaluation time. Violations result in a TypeMismatch error per `workflow-errors.md`.

| Operator | Left Operand Type | Right Operand Type |
|----------|------------------|-------------------|
| Equal | Any comparable | Same as left, or coercible |
| NotEqual | Any comparable | Same as left, or coercible |
| LessThan | Numeric, Temporal, Ordinal | Same as left |
| GreaterThan | Numeric, Temporal, Ordinal | Same as left |
| LessThanOrEqual | Numeric, Temporal, Ordinal | Same as left |
| GreaterThanOrEqual | Numeric, Temporal, Ordinal | Same as left |
| Contains | Container (Array, Object, String) | Element compatible with container |
| StartsWith | String | String |
| EndsWith | String | String |
| Matches | String | String (pattern) |
| In | Element | Set (Array of compatible elements) |
| Between | Numeric, Temporal | Range [Numeric, Numeric] or [Temporal, Temporal] |
| Exists | Any entity reference | N/A |
| IsNull | Any entity reference | N/A |
| IsNotNull | Any entity reference | N/A |

## Operator Precedence

When multiple operators appear in a single expression, the following precedence rules apply (highest to lowest):

1. `Exists`, `IsNull`, `IsNotNull` (unary null-state)
2. `Between` (range membership)
3. `In`, `Contains` (set membership)
4. `Matches`, `StartsWith`, `EndsWith` (string pattern)
5. `LessThan`, `LessThanOrEqual`, `GreaterThan`, `GreaterThanOrEqual` (relational)
6. `Equal`, `NotEqual` (equality)
7. `AND` (logical conjunction)
8. `OR` (logical disjunction)
9. `NOT` (logical negation, unary)

Parentheses MAY override precedence. Expressions within parentheses are evaluated before the enclosing expression.

## Operator Evaluation

Operator evaluation follows these principles:

1. **Determinism**: Given identical operands, an operator ALWAYS produces the same result.
2. **Short-circuit**: In logical compositions, operators evaluate left-to-right with short-circuit semantics.
3. **Type Safety**: Operators reject type mismatches with a defined error per `workflow-errors.md`.
4. **Null Safety**: Operators handle null operands gracefully; no operator throws an unhandled exception on null.
5. **Performance**: Operators are optimized for the common case; pathological inputs MAY degrade performance.
