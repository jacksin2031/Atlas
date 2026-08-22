# ADR-0007: Knowledge Pack System

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

Atlas aims to automate not only applications but also user knowledge.

Traditional automation systems require users to manually build every workflow from scratch.

Atlas introduces a reusable Knowledge Pack System that encapsulates domain-specific expertise into versioned, distributable packages.

Examples include:

- Minecraft Automation
- Genshin Impact Automation
- Photoshop Assistant
- Microsoft Excel Assistant
- Chrome Browser Automation
- Blender Workflow
- Unity Editor Assistant

Knowledge Packs transform Atlas from an automation tool into an extensible knowledge platform.

---

# Problem Statement

Without a standardized knowledge system:

- AI cannot understand application-specific behaviors.
- Workflow generation becomes inconsistent.
- Community contributions become fragmented.
- Marketplace distribution becomes unreliable.
- Every user must repeatedly teach Atlas identical knowledge.

Atlas therefore requires a portable, versioned, and extensible knowledge representation.

---

# Decision

Atlas SHALL introduce a first-class Knowledge Pack System.

Knowledge Packs SHALL be treated as independent platform assets.

Knowledge Packs SHALL contain structured information rather than executable business logic.

Knowledge Packs SHALL be installable, removable, upgradeable, and shareable.

---

# Design Principles

The Knowledge Pack System SHALL follow these principles:

- Modular
- Versioned
- Portable
- AI-friendly
- Human-readable
- Marketplace-compatible
- Offline-capable
- Language-independent

Knowledge SHALL be separated from implementation.

---

# Knowledge Pack Architecture

Each Knowledge Pack SHALL contain:

- Metadata
- Manifest
- Localization
- Domain Knowledge
- Templates
- AI Prompts
- OCR Models (optional)
- Image Templates (optional)
- Object Detection Models (optional)
- Workflow Templates
- Examples
- Documentation

Knowledge Packs SHALL NOT contain executable platform code.

---

# Manifest

Every Knowledge Pack SHALL provide a manifest.

Example:

{
    "id": "minecraft",
    "name": "Minecraft Knowledge Pack",
    "version": "1.0.0",
    "author": "Atlas Community",
    "license": "MIT",
    "compatibility": ">=1.0.0",
    "language": [
        "en",
        "zh-CN",
        "zh-TW",
        "ja"
    ]
}

---

# Knowledge Structure

Knowledge SHALL be categorized.

Examples:

- UI Elements
- Menus
- Windows
- Objects
- Controls
- OCR Keywords
- Common Tasks
- Workflows
- Best Practices
- AI Prompt Templates
- Error Recovery Rules

Knowledge SHALL remain independent from specific AI providers.

---

# Localization

Knowledge Packs SHALL support multiple languages.

All user-facing content SHALL be localized.

Internal identifiers SHALL remain language-neutral.

Example:

Button Identifier

save_button

Translations

English

Save

Traditional Chinese

儲存

Japanese

保存

---

# AI Integration

AI SHALL use Knowledge Packs as contextual information.

Knowledge Packs SHALL provide:

- Prompt Fragments
- Task Definitions
- Domain Vocabulary
- UI Semantics
- Action Sequences

AI providers SHALL NOT modify installed Knowledge Packs directly.

Customized knowledge SHALL be stored separately.

---

# Workflow Integration

Knowledge Packs MAY include reusable workflow templates.

Examples:

Auto Fishing

Inventory Sorting

NPC Conversation

Photoshop Export

Excel Formatting

These workflows SHALL remain editable by users.

---

# Vision Integration

Knowledge Packs MAY include:

OCR dictionaries

Template Matching Images

Object Detection Labels

UI Anchors

Color Profiles

Vision resources SHALL be optional.

---

# Plugin Integration

Plugins MAY depend on Knowledge Packs.

Knowledge Packs SHALL NOT depend on plugins.

Dependency direction SHALL always be:

Platform

↓

Plugin

↓

Knowledge Pack

---

# Marketplace Integration

Knowledge Packs SHALL be distributable through the Atlas Marketplace.

Marketplace SHALL support:

- Installation
- Upgrade
- Version history
- Ratings
- Reviews
- Digital signatures
- Dependency checking

---

# User Customization

Users SHALL be able to create customized Knowledge Packs.

Customized packs SHALL override base knowledge without modifying upstream packages.

Priority:

User Pack

↓

Workspace Pack

↓

Installed Pack

↓

Built-in Pack

This ensures updates never overwrite user modifications.

---

# Storage

Knowledge Packs SHALL remain self-contained.

Suggested directory structure:

knowledge-pack/

manifest.json

knowledge/

templates/

translations/

vision/

workflows/

assets/

README.md

LICENSE

---

# Security Considerations

Knowledge Packs SHALL NOT execute arbitrary code.

Executable logic SHALL remain inside plugins.

Imported Knowledge Packs SHALL be validated before installation.

Marketplace SHALL verify package signatures.

---

# Performance Considerations

Knowledge Packs SHALL support:

Lazy loading

Incremental indexing

Search caching

Memory optimization

Unused packs SHOULD remain unloaded.

---

# Future Extensions

The architecture SHALL support:

Cloud synchronization

Enterprise knowledge repositories

Collaborative editing

AI-generated knowledge

Automatic UI learning

Semantic search

Vector embeddings

Knowledge inheritance

Version branching

No architectural redesign should be required.

---

# Alternatives Considered

## Hardcoded Knowledge

Pros

Simple implementation.

Cons

Impossible to maintain.

Rejected.

---

## Plugin-only Knowledge

Pros

Simple architecture.

Cons

Knowledge coupled with executable code.

Rejected.

---

## External Database

Pros

Centralized storage.

Cons

Requires network access.

Not suitable for offline usage.

Rejected.

---

## Independent Knowledge Packs

Pros

Modular

Portable

AI-friendly

Marketplace-ready

Offline

Versioned

Accepted.

---

# Consequences

## Positive

Reusable domain knowledge.

Community contributions.

Marketplace ecosystem.

AI becomes more accurate.

Language localization.

Offline support.

Reusable workflow generation.

## Negative

Package version management.

Localization maintenance.

Knowledge synchronization.

---

# Risks

Outdated knowledge.

Conflicting packages.

Duplicate information.

Large package size.

---

# Mitigations

Versioning.

Digital signatures.

Dependency validation.

Conflict detection.

Marketplace moderation.

---

# Implementation Notes

Knowledge Pack runtime SHALL be implemented under:

packages/knowledge/

Suggested modules:

loader/

registry/

resolver/

search/

cache/

validator/

translator/

serializer/

No application logic SHALL exist inside Knowledge Packs.

---

# Related ADRs

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0008 AI Provider Independence

ADR-0012 Contract-First Development

ADR-0013 Specification-Driven Development

ADR-0021 Marketplace Philosophy

---

# Related Specifications

specs/knowledge/

specs/workflow/

specs/vision/

contracts/json/knowledge.schema.json

---

# References

Visual Studio Code Extensions

JetBrains Plugins

Unity Packages

Node-RED

n8n

Unreal Engine Content Packs

Hugging Face Model Hub
