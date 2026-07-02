# ADR-0012: Contract-First & Specification-Driven Development

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

Supersedes:
None

Superseded By:
None

---

# Context

Atlas is designed to be a long-lived, enterprise-grade, AI-assisted automation platform.

The project is expected to evolve over many years, with contributions from:

- Human developers
- AI coding assistants
- Plugin authors
- Community maintainers
- Enterprise teams

To ensure architectural consistency, reproducibility, and maintainability, Atlas adopts a Contract-First and Specification-Driven Development methodology.

Implementation SHALL always follow specifications and contracts rather than ad hoc prompts or spontaneous coding.

---

# Problem Statement

Prompt-driven development introduces several risks:

- Inconsistent architecture
- Hallucinated implementations
- Hidden assumptions
- Breaking API changes
- Tight coupling
- Missing documentation
- Difficult reviews
- Non-reproducible results

Atlas requires a deterministic engineering workflow where implementation is derived from approved specifications.

---

# Decision

Atlas SHALL adopt Contract-First Development.

Every feature SHALL be defined by specifications and contracts before implementation begins.

Implementation SHALL be considered invalid if no corresponding specification or contract exists.

---

# Development Lifecycle

Every feature SHALL follow this sequence:

Vision

↓

Architecture

↓

Specification

↓

Contract

↓

Implementation Plan

↓

Implementation

↓

Testing

↓

Review

↓

Documentation

↓

Release

Skipping any mandatory stage is prohibited.

---

# Specification Principles

Specifications SHALL define:

- Purpose
- Scope
- Functional Requirements
- Non-functional Requirements
- Inputs
- Outputs
- Constraints
- Error Conditions
- Performance Targets
- Security Requirements

Specifications SHALL avoid implementation details where possible.

---

# Contract Principles

Contracts SHALL define:

- Input Schema
- Output Schema
- Event Definitions
- API Interfaces
- IPC Interfaces
- Plugin Interfaces
- Version
- Compatibility Rules

Contracts SHALL remain technology-independent.

---

# Contract Types

Atlas SHALL support:

- JSON Schema
- IPC Contracts
- Plugin Contracts
- Runtime Contracts
- Workflow Contracts
- Vision Contracts
- AI Contracts
- Storage Contracts

Every public interface SHALL have an associated contract.

---

# Specification Ownership

Each specification SHALL have:

Owner

Version

Status

Review History

Related ADRs

Acceptance Criteria

Specifications SHALL be reviewed before implementation.

---

# AI Development Rules

AI-generated code SHALL:

Read related specifications first.

Read related contracts.

Validate architecture boundaries.

Generate implementation from specifications.

Never invent undocumented APIs.

Never modify contracts automatically.

---

# Human Development Rules

Human contributors SHALL:

Review specifications before coding.

Avoid bypassing contracts.

Submit architecture changes through ADRs.

Keep implementation synchronized with specifications.

---

# Architecture Changes

Architectural modifications SHALL require:

ADR proposal

Specification updates

Contract updates

Implementation updates

Documentation updates

Approval from maintainers

---

# Versioning

Specifications SHALL use semantic versioning.

Breaking specification changes SHALL require:

Major version increment

Migration strategy

Compatibility documentation

---

# Traceability

Every implementation SHALL reference:

Related Issue

Related ADR

Related Specification

Related Contract

Related Tests

Traceability SHALL be maintained throughout the project lifecycle.

---

# Validation

Before implementation begins:

Specification validation SHALL pass.

Contract validation SHALL pass.

Architecture review SHALL pass.

Implementation SHALL not begin otherwise.

---

# Documentation

Every feature SHALL include:

Specification

Architecture diagrams (if applicable)

Examples

Known limitations

Migration notes (if applicable)

Documentation SHALL evolve alongside implementation.

---

# Testing

Tests SHALL be derived from specifications.

Acceptance criteria SHALL originate from specifications rather than implementation details.

Regression tests SHALL be created for resolved defects.

---

# Plugin Development

Plugins SHALL implement published contracts.

Plugins SHALL never rely on undocumented internal behavior.

Plugin compatibility SHALL be verified against contract versions.

---

# Workflow Development

Workflow nodes SHALL be described by contracts.

Execution behavior SHALL follow specifications.

Runtime SHALL validate workflows before execution.

---

# AI Workflow Generation

AI-generated workflows SHALL:

Validate against workflow.schema.json.

Reference supported node types.

Avoid unsupported actions.

Produce deterministic outputs.

---

# Contract Validation

Contracts SHALL be machine-readable.

Validation SHALL occur:

During development

During CI

During plugin loading

During workflow import

Invalid contracts SHALL be rejected.

---

# Code Generation

Code generators MAY consume:

Specifications

Contracts

Schemas

ADRs

Generated code SHALL remain traceable to source specifications.

---

# Review Process

Pull Requests SHALL verify:

Specification compliance.

Contract compliance.

Architecture compliance.

Security compliance.

Performance compliance.

Documentation completeness.

---

# Continuous Integration

CI SHALL validate:

JSON Schemas

Contract compatibility

API changes

Documentation links

Specification references

Code formatting

Static analysis

Tests

Build integrity

---

# Future Extensions

The development model SHALL support:

Automatic code generation

Specification linting

AI planning

AI review

Architecture verification

Contract evolution

Distributed development

No redesign shall be required.

---

# Alternatives Considered

## Prompt-Driven Development

Pros

Fast.

Cons

Unpredictable.

Non-repeatable.

Architecture drift.

Rejected.

---

## Code-First Development

Pros

Simple.

Cons

Documentation lag.

Architecture inconsistency.

Rejected.

---

## Contract-First Development

Pros

Deterministic.

Maintainable.

AI-friendly.

Enterprise-ready.

Accepted.

---

# Consequences

## Positive

Consistent architecture.

Reproducible implementations.

Improved AI collaboration.

Simplified reviews.

Clear documentation.

Reduced maintenance costs.

Enterprise readiness.

## Negative

Higher upfront planning effort.

Additional documentation requirements.

Learning curve for contributors.

---

# Risks

Specification drift.

Outdated contracts.

Over-documentation.

Delayed implementation.

---

# Mitigations

Automated validation.

CI enforcement.

Architecture reviews.

Regular specification audits.

---

# Implementation Notes

Specifications SHALL reside under:

specs/

Contracts SHALL reside under:

contracts/

ADRs SHALL reside under:

docs/adr/

Engineering standards SHALL reside under:

.ai/

No implementation SHALL bypass these directories.

---

# Related ADRs

ADR-0001 Repository Governance

ADR-0002 Monorepo Architecture

ADR-0003 Technology Stack

ADR-0004 Module Boundaries

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0007 Knowledge Pack System

ADR-0008 AI Provider Independence

ADR-0009 AI Routing & Model Orchestration

ADR-0010 IPC & Runtime Architecture

ADR-0011 Vision Engine Architecture

ADR-0013 Workspace Architecture

ADR-0014 Project Manifest

---

# Related Specifications

specs/

contracts/

docs/adr/

.ai/

---

# References

JSON Schema Specification

OpenAPI Specification

Semantic Versioning 2.0

Architecture Decision Records

Domain-Driven Design

Clean Architecture

Model Context Protocol (MCP)

Specification by Example
