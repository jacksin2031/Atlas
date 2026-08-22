# ADR-0008: AI Provider Independence

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

Artificial Intelligence is one of the primary capabilities of Atlas.

Atlas relies on AI for:

- Workflow generation
- Workflow optimization
- Knowledge extraction
- Vision reasoning
- UI understanding
- Prompt execution
- Automation planning
- User assistance

The AI ecosystem evolves rapidly.

Providers frequently introduce:

- New APIs
- New pricing
- New capabilities
- Breaking API changes
- Model deprecations

Atlas must remain independent from any specific AI vendor.

---

# Problem Statement

Directly coupling Atlas to one provider introduces significant risks:

- Vendor lock-in
- API instability
- Pricing dependency
- Regional restrictions
- Internet availability
- Privacy concerns

Users should be free to choose the AI model that best meets their needs.

Atlas therefore requires a provider-independent AI architecture.

---

# Decision

Atlas SHALL implement an AI Provider Abstraction Layer.

All AI providers SHALL implement a common interface.

Core modules SHALL never communicate directly with provider-specific SDKs.

Provider switching SHALL require no changes to business logic.

---

# Design Principles

The AI architecture SHALL be:

- Provider-independent
- Extensible
- Offline-capable
- Privacy-first
- Configurable
- Testable
- Deterministic where possible

AI is a service consumed by Atlas—not the foundation of Atlas.

---

# Architecture

The AI subsystem SHALL consist of:

- AI Manager
- Provider Interface
- Provider Registry
- Prompt Engine
- Context Builder
- Memory Manager
- Response Validator
- Cache Manager

Only the AI Manager communicates with providers.

---

# Provider Interface

Every provider SHALL implement:

- Chat Completion
- Structured Output
- Streaming
- Embeddings (optional)
- Vision (optional)
- Tool Calling (optional)
- Function Calling (optional)
- Token Counting
- Health Check

Capabilities SHALL be declared explicitly.

---

# Supported Providers

The architecture SHALL support:

Cloud Providers

- OpenAI
- Anthropic Claude
- Google Gemini
- DeepSeek API
- Qwen API
- Mistral
- Groq

Local Providers

- Ollama
- LM Studio
- llama.cpp
- vLLM
- LocalAI

Enterprise Providers

- Azure OpenAI
- Self-hosted OpenAI-compatible APIs

New providers SHALL be installable without modifying the core system.

---

# Capability Detection

Providers SHALL declare supported capabilities.

Example:

- Text Generation
- Vision
- OCR Assistance
- Tool Calling
- JSON Output
- Streaming
- Embeddings
- Audio
- Image Generation

Atlas SHALL adapt automatically.

---

# Prompt Engine

Prompts SHALL be provider-independent.

Prompt templates SHALL reside under:

.ai/prompts/

Prompt templates SHALL avoid provider-specific syntax whenever possible.

Provider adapters MAY transform prompts before execution.

---

# Context Management

AI context SHALL include:

- Workflow
- User Settings
- Knowledge Packs
- Vision Results
- Runtime State
- Plugin Context

The Context Builder SHALL assemble context dynamically.

---

# Memory Management

AI memory SHALL be separated into:

- Session Memory
- Workspace Memory
- Project Memory
- Knowledge Pack Memory

Memory SHALL never depend on provider implementation.

---

# Structured Output

Whenever supported, providers SHALL return structured JSON.

Responses SHALL be validated using JSON Schema before execution.

Invalid outputs SHALL be rejected.

---

# Fallback Strategy

Atlas SHALL support automatic fallback.

Example:

Primary:

OpenAI GPT

↓

Fallback:

Claude

↓

Fallback:

Gemini

↓

Fallback:

Local Ollama

↓

User Notification

Workflow execution SHALL continue whenever possible.

---

# Offline Mode

Atlas SHALL support offline execution.

Offline mode SHALL use:

- Ollama
- llama.cpp
- LM Studio
- LocalAI

Core automation SHALL remain available without Internet access.

---

# Privacy

Users SHALL control:

- Local execution
- Cloud execution
- Data sharing
- Prompt logging

Atlas SHALL never upload user data without explicit consent.

---

# Security

API keys SHALL be encrypted.

Providers SHALL never access unrelated project files.

Sensitive information SHALL be masked before transmission when possible.

Prompt injection protection SHALL be implemented.

---

# Plugin Integration

Plugins MAY register additional providers.

Plugins SHALL NOT modify the AI Manager.

Provider plugins SHALL implement the Provider Interface.

---

# Workflow Integration

Workflow Nodes SHALL request AI services through the AI Manager.

Nodes SHALL NOT call provider SDKs directly.

---

# Knowledge Integration

Knowledge Packs SHALL enrich prompts.

Providers SHALL remain unaware of Knowledge Pack internals.

---

# Configuration

Users SHALL configure:

- Default Provider
- Preferred Models
- Temperature
- Context Size
- Max Tokens
- Timeout
- Retry Policy

Configuration SHALL be stored independently from provider SDKs.

---

# Performance

The AI subsystem SHALL support:

- Response Caching
- Prompt Caching
- Parallel Requests
- Streaming Responses
- Token Optimization

Large prompts SHOULD be compressed before transmission.

---

# Future Extensions

The architecture SHALL support:

- Multi-model orchestration
- Automatic model routing
- Cost-aware routing
- Latency-aware routing
- AI ensembles
- Agent collaboration
- On-device fine-tuned models

No architectural redesign should be required.

---

# Alternatives Considered

## Single Provider

Pros

Simple implementation.

Cons

Vendor lock-in.

Rejected.

---

## Provider-specific Architecture

Pros

Maximum feature utilization.

Cons

Impossible to maintain.

Rejected.

---

## Provider Abstraction Layer

Pros

Flexible.

Extensible.

Offline support.

Enterprise-ready.

Accepted.

---

# Consequences

## Positive

Freedom of provider choice.

Offline capability.

Lower migration cost.

Enterprise flexibility.

Improved privacy.

Future-proof architecture.

## Negative

Additional abstraction layer.

Capability differences between providers.

More testing required.

---

# Risks

Provider API changes.

Feature inconsistencies.

Model quality differences.

---

# Mitigations

Capability detection.

Versioned adapters.

Provider compatibility testing.

Automated integration tests.

---

# Implementation Notes

Implementation SHALL reside under:

packages/core/ai/

Suggested modules:

provider/

manager/

registry/

prompt/

memory/

cache/

validator/

router/

Each provider SHALL be isolated into its own module.

---

# Related ADRs

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0007 Knowledge Pack System

ADR-0010 IPC Architecture

ADR-0011 Vision Engine

ADR-0012 Contract-First Development

ADR-0013 Specification-Driven Development

---

# Related Specifications

specs/ai/

specs/runtime/

specs/workflow/

contracts/json/project.schema.json

---

# References

OpenAI API

Anthropic API

Google Gemini API

Ollama

llama.cpp

OpenAI-Compatible API Specification

Model Context Protocol (MCP)
