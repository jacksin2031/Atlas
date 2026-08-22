# ADR-0005: Plugin Architecture

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

---

# Context

Atlas aims to become an extensible automation platform.

Users should be able to install, update, and remove functionality without modifying the core application.

---

# Problem Statement

Embedding all functionality inside the core application reduces flexibility and limits community contributions.

---

# Decision

Atlas adopts a Plugin-First Architecture.

Core capabilities SHOULD be implemented as plugins whenever practical.

The core platform SHALL provide:

- Plugin Loader
- Plugin Sandbox
- Plugin API
- Permission System
- Lifecycle Manager
- Marketplace Integration

---

# Design Principles

- Loose coupling
- Stable APIs
- Independent deployment
- Security isolation
- Version compatibility

---

# Plugin Lifecycle

Install

↓

Validate

↓

Load

↓

Initialize

↓

Execute

↓

Suspend

↓

Unload

↓

Remove

---

# Alternatives Considered

Built-in modules only

Pros

Simple architecture

Cons

No extensibility

Rejected.

Dynamic scripting only

Pros

Easy customization

Cons

Lower security

Rejected.

---

# Consequences

Positive

- Community ecosystem
- Marketplace support
- Independent releases
- Easier maintenance

Negative

- Plugin compatibility management
- Version negotiation

---

# Risks

Malicious plugins.

---

# Mitigations

Permission system.

Sandbox.

Digital signatures.

Plugin manifests.

---

# Implementation Notes

Every plugin MUST provide:

plugin.json

Version

Permissions

Dependencies

Entry Point

Compatibility Range

---

# Related ADRs

ADR-0003

ADR-0007

ADR-0012

ADR-0015

---

# Related Specifications

specs/plugin/

specs/marketplace/

---

# References

VSCode Extension API

JetBrains Plugins

Obsidian Plugin System
