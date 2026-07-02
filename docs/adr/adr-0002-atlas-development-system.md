# ADR-0002: Adopt the Atlas Development System (ADS)

- **Status:** Accepted
- **Date:** 2026-06-28
- **Deciders:** Atlas Core Team
- **Supersedes:** None
- **Superseded by:** None

---

# Context

Atlas is intended to become an AI-native automation platform rather than a traditional desktop application.

The project is expected to be developed by:

- Human contributors
- ChatGPT
- Claude
- Gemini
- GitHub Copilot
- Future AI assistants
- Open-source contributors

Different AI models produce different coding styles, architectures, and implementation strategies.

Without a standardized development system, the project would gradually become inconsistent, difficult to maintain, and impossible to reproduce.

Atlas therefore requires a repository-contained development framework that defines how every feature is designed, implemented, reviewed, tested, and documented.

The development process must never depend on a specific AI model.

---

# Decision

Atlas officially adopts the **Atlas Development System (ADS)** as the mandatory development methodology.

ADS is the only approved software engineering process for this repository.

Every implementation must follow ADS.

Every contributor—human or AI—must follow the same workflow.

---

# ADS Layers

Atlas Development System consists of four primary layers.

## Layer 1 — Governance

Defines:

- Vision
- Mission
- Philosophy
- Long-term goals
- Decision making
- Repository governance

Primary files:

- constitution.md
- governance/

---

## Layer 2 — ADS

Defines how development is executed.

Includes:

- bootstrap
- operating system
- workflow
- AI behavior
- specification rules
- contracts

Purpose:

Every AI entering the repository must understand how to work before writing code.

---

## Layer 3 — Engineering Standards

Defines engineering practices.

Includes:

- Coding standards
- Architecture rules
- Review checklist
- Definition of Done
- Testing standards
- Security standards
- Performance standards

Purpose:

Ensure consistent implementation quality.

---

## Layer 4 — Specifications

Defines what the platform should become.

Examples:

- Runtime
- Recorder
- Vision Engine
- Workflow Engine
- Plugin System
- Storage
- IPC
- UI

Specifications always have higher priority than implementation.

---

# Development Lifecycle

Every feature follows the same lifecycle.

Vision

↓

Architecture

↓

Specification

↓

Contracts

↓

Implementation Plan

↓

Implementation

↓

Review

↓

Testing

↓

Documentation

↓

Release

No step may be skipped.

---

# Golden Rules

ADS introduces the following mandatory principles.

## Specification First

No feature begins implementation before specifications exist.

---

## Architecture Before Code

Architecture decisions always precede implementation.

---

## Reproducibility

Given the same specifications, different AI models should produce functionally equivalent implementations.

---

## Model Independence

Atlas must never depend on one AI provider.

All AI providers are considered interchangeable.

---

## Deterministic Development

Repository structure must remain stable.

Engineering decisions must be documented.

Unexpected architectural changes are prohibited.

---

# Responsibilities

ADS is responsible for:

- repository consistency
- implementation quality
- AI collaboration
- engineering workflow
- architecture protection
- documentation quality
- review process

ADS is NOT responsible for:

- product features
- UI design
- business decisions
- marketplace content

---

# Consequences

Positive:

- AI models become interchangeable.
- Contributors have predictable workflows.
- Documentation quality improves.
- Architecture remains consistent.
- Long-term maintenance becomes easier.

Negative:

- Initial setup requires additional documentation.
- Contributors must learn ADS before contributing.
- Early development speed may be slightly slower.

---

# Alternatives Considered

## No Development Framework

Rejected.

Reason:

Would result in inconsistent implementations.

---

## AI-specific prompts only

Rejected.

Reason:

Prompts are not architecture.

Architecture must exist independently of prompts.

---

## Traditional Coding Guidelines Only

Rejected.

Reason:

Coding standards alone do not define development workflows.

---

# Compliance

All future pull requests must comply with ADS.

Major architectural changes require:

- ADR
- Architecture Review
- Maintainer approval

Failure to comply with ADS may result in rejection of the pull request.

---

# References

- ADR-0001 Architecture Freeze
- constitution.md
- operating-system.md
- workflow.md
- specification-rules.md