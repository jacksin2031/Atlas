# ADR-0009: AI Routing & Model Orchestration

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

Atlas is designed to support multiple AI providers, local language models, enterprise deployments, and future AI capabilities.

Modern AI systems differ significantly in:

- Cost
- Latency
- Accuracy
- Context length
- Vision capability
- Function calling
- Structured outputs
- Offline availability

No single model performs optimally across every workload.

Atlas therefore requires an intelligent routing system capable of selecting the most appropriate model for each task.

---

# Problem Statement

If every request is always sent to a single AI model:

- Costs increase unnecessarily.
- Latency becomes unpredictable.
- Local execution is ignored.
- Large-context tasks waste resources.
- Specialized models cannot be utilized.
- Offline mode becomes impossible.

Atlas must automatically select the optimal model while remaining transparent to users.

---

# Decision

Atlas SHALL implement an AI Routing & Model Orchestration subsystem.

All AI requests SHALL pass through the AI Router.

The router SHALL determine:

- Provider
- Model
- Execution Mode
- Retry Strategy
- Fallback Strategy

Business logic SHALL never communicate directly with AI providers.

---

# Design Principles

The routing system SHALL be:

- Provider-independent
- Deterministic
- Extensible
- Observable
- Configurable
- Offline-capable
- Cost-aware
- Performance-aware

Routing SHALL remain transparent to users unless explicitly configured.

---

# Architecture

The orchestration subsystem SHALL consist of:

- AI Router
- Capability Registry
- Cost Analyzer
- Latency Monitor
- Health Monitor
- Policy Engine
- Load Balancer
- Fallback Manager
- Retry Manager
- Execution Queue

Only the AI Router may dispatch AI requests.

---

# Routing Policies

The router SHALL support multiple routing strategies.

Examples include:

- Capability-based Routing
- Cost-based Routing
- Latency-based Routing
- Privacy-based Routing
- Local-first Routing
- User-defined Routing
- Workspace Routing
- Enterprise Policies

Policies SHALL be configurable.

---

# Capability Routing

Each model SHALL declare supported capabilities.

Examples:

- Chat
- Vision
- OCR
- Code Generation
- Function Calling
- JSON Output
- Embeddings
- Audio
- Translation
- Long Context

Unsupported requests SHALL never be dispatched to incompatible models.

---

# Cost Optimization

The router SHALL minimize operational cost whenever practical.

Example:

Simple Translation

↓

Local Llama

Large Architecture Design

↓

GPT-5

Vision OCR

↓

Gemini Vision

Workflow Optimization

↓

Claude

Cost SHALL be considered alongside quality requirements.

---

# Local-first Execution

Users MAY enable Local-first Mode.

When enabled:

1. Local Models
2. Enterprise Models
3. Cloud Providers

Cloud execution SHALL occur only when necessary.

---

# Privacy Routing

Sensitive requests MAY be restricted.

Examples:

Passwords

Financial Data

Medical Records

Enterprise Source Code

Such requests SHALL only execute on approved providers.

---

# Health Monitoring

Each provider SHALL expose:

- Availability
- Response Time
- Error Rate
- Queue Length

Unhealthy providers SHALL be temporarily removed from routing decisions.

---

# Retry Strategy

Retries SHALL support:

- Same Provider Retry
- Alternate Provider Retry
- Local Fallback
- Manual Confirmation

Infinite retry loops SHALL be prohibited.

---

# Fallback Strategy

Example:

Primary

GPT-5

↓

Claude

↓

Gemini

↓

DeepSeek

↓

Ollama

↓

User Notification

Workflow execution SHALL continue whenever possible.

---

# Load Balancing

When multiple equivalent models exist, requests SHALL be distributed using configurable strategies.

Supported algorithms:

- Round Robin
- Least Latency
- Weighted Routing
- Cost Priority
- Health Score

---

# Context Optimization

Before dispatching requests, the router MAY:

- Compress prompts
- Remove duplicated context
- Cache reusable prompts
- Inject Knowledge Packs
- Trim conversation history

---

# Caching

Atlas SHALL cache:

- Prompt Templates
- Embeddings
- OCR Results
- Workflow Analysis
- Repeated Responses

Cache SHALL use configurable expiration policies.

---

# Streaming

The orchestration layer SHALL support streaming outputs.

UI SHALL receive incremental updates.

Streaming SHALL be provider-independent.

---

# Workflow Integration

Workflow Nodes SHALL submit AI tasks to the AI Router.

Nodes SHALL never choose providers directly.

---

# Knowledge Integration

Knowledge Packs SHALL enrich routing context.

The router MAY select specialized models based on detected domains.

Example:

Photoshop Pack

↓

Vision Model

Minecraft Pack

↓

Reasoning Model

Excel Pack

↓

Structured Output Model

---

# Plugin Integration

Plugins MAY register routing policies.

Plugins SHALL NOT bypass the router.

Custom routers SHALL implement the Routing Interface.

---

# Configuration

Users SHALL configure:

- Preferred Providers
- Maximum Cost
- Maximum Latency
- Local-first
- Privacy Mode
- Offline Mode
- Preferred Models
- Retry Count

Configuration SHALL remain provider-independent.

---

# Performance Considerations

The router SHALL support:

- Parallel dispatch
- Request batching
- Dynamic scheduling
- Queue prioritization
- Model warm-up
- Adaptive caching

Routing overhead SHALL remain minimal.

---

# Future Extensions

The architecture SHALL support:

- Multi-agent collaboration
- Ensemble reasoning
- Automatic benchmarking
- Reinforcement routing
- Self-learning routing
- Federated AI execution
- Distributed inference

No architectural redesign should be required.

---

# Alternatives Considered

## Fixed Provider

Pros

Simple implementation.

Cons

No flexibility.

Rejected.

---

## User-selected Provider

Pros

Simple UI.

Cons

Poor automation.

Rejected.

---

## Intelligent AI Router

Pros

Automatic optimization.

Provider independence.

Offline capability.

Enterprise-ready.

Accepted.

---

# Consequences

## Positive

Reduced AI cost.

Lower latency.

Improved privacy.

Offline support.

Automatic provider selection.

Better scalability.

Future-proof architecture.

## Negative

Higher implementation complexity.

Additional monitoring required.

More configuration options.

---

# Risks

Incorrect routing decisions.

Capability mismatches.

Provider failures.

Routing policy conflicts.

---

# Mitigations

Capability validation.

Continuous benchmarking.

Health monitoring.

Fallback routing.

User override support.

---

# Implementation Notes

Implementation SHALL reside under:

packages/core/router/

Suggested modules:

router/

scheduler/

registry/

policies/

fallback/

retry/

health/

metrics/

cache/

dispatcher/

All routing logic SHALL remain isolated from provider implementations.

---

# Related ADRs

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0007 Knowledge Pack System

ADR-0008 AI Provider Independence

ADR-0010 IPC Architecture

ADR-0011 Vision Engine

ADR-0012 Contract-First Development

---

# Related Specifications

specs/ai/

specs/runtime/

specs/workflow/

specs/project/

---

# References

OpenAI API

Anthropic API

Google Gemini API

Ollama

llama.cpp

vLLM

LangChain Router

Haystack

Microsoft Semantic Kernel

OpenAI-Compatible API Specification
