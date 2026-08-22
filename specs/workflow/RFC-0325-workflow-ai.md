RFC: RFC-0325

Title: Workflow AI

Status: Proposed

Version: 1.0.0

Author: Atlas Specification Committee

Created: 
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| AI Agent | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| AI Node | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Model Invocation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Prompt | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Completion | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Embedding | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Vector Store | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Fine-Tuning | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Agent Loop | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Tool Use | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Function Calling | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Reasoning Step | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
2026-07-01

Depends On:

  - RFC-0001 Runtime Overview

  - RFC-0002 Runtime Lifecycle

  - RFC-0003 Runtime Service Model

  - RFC-0004 Runtime Scheduler

  - RFC-0005 Runtime Event Bus

  - RFC-0006 Runtime State Management

  - RFC-1001 Common Event Model

  - RFC-1002 Common State Model

  - RFC-1003 Common Capability Model

  - RFC-1004 Common Contract Model

  - RFC-1005 Common Manifest Model

  - RFC-1006 Common Error Model

Supersedes: None

Superseded By: None

Category: Workflow

Layer: Standard

Normative: YES

Audience: All Subsystem Teams

ADR References:

  - ADR-0012

Constitution References:

  - Section 1 (Workflow Philosophy)

Related RFCs:

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage


  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC

  - RFC-0328 Workflow Serialization

  - RFC-0329 Workflow Compatibility

  - RFC-0330 Workflow Compliance

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x



Related ADR:

  - ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema:

  - schemas/workflow/ai-node.json

Related Catalog:

  - catalog/workflow-node-types.md

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow AI specification defines how workflows interact with the Atlas AI system. AI nodes execute AI model inference or agent operations within the workflow graph.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0325 workflow ai.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 2 AI Integration Overview



Key principles:



- AI nodes execute AI model inference or agent operations.

- AI operations are bounded by execution budgets and timeouts.

- AI results are propagated through the data flow model.

- AI nodes support retry and recovery for transient failures.



---



## 3 Integration Points



| Point | Description | RFC Reference |

|---|---|---|

| AI Nodes | Nodes that perform AI inference | RFC-0301 |

| Provider Selection | AI provider selection through capability registry | RFC-0302 |

| Context Management | AI context and prompt management | RFC-0303 |

| Agent Coordination | Multi-agent coordination through workflow | RFC-0304 |

| Memory Integration | AI memory through storage nodes | RFC-0305 |

| Tool Calling | AI tool calling through action nodes | RFC-0307 |



---



## 4 AI Node Execution



### 4.1 Execution Flow



1. AI node receives input variables from upstream nodes.

2. AI provider is selected based on capability registry.

3. AI operation is executed within the sandbox.

4. AI results are stored in output variables.

5. AI events are emitted for observability.



### 4.2 Resource Requirements



| Resource | Description |

|---|---|

| Compute | CPU/GPU for inference |

| Memory | Context window storage |

| Network | Provider API connectivity |

| Budget | Token/operation limits |



---



## 5 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | Six integration points MUST be defined. | Point enumeration test |

| AC-02 | Five AI execution flow steps MUST be enforced. | Execution flow test |

| AC-03 | Four AI resource types MUST be declared. | Resource test |



---



## 6 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview |

| RFC-0323 | Workflow Plugin Integration |



---



## 5 Terminology



| Term | Definition | Source |

|---|---|---|

| AI Node | A workflow node that executes AI model inference or agent operations. | RFC-0301 |

| AI Provider | An external or internal service that provides AI model inference capabilities. | This RFC |

| Inference | The process of executing an AI model to produce predictions or completions. | This RFC |

| Agent | An autonomous or semi-autonomous AI entity that can execute workflow nodes. | This RFC |

| Context Window | The maximum amount of input data an AI model can process in a single inference. | This RFC |



## 6 Layer Boundaries



### 6.1 Responsibilities

This specification IS responsible for: defining AI node execution model, specifying AI provider selection, establishing AI operation boundaries, and defining AI result propagation.



### 6.2 Non-Responsibilities

This specification IS NOT responsible for: implementing AI models (delegated to AI providers), managing GPU resources (delegated to Runtime, RFC-0304), or providing AI-specific security beyond sandboxing (delegated to RFC-0319).



### 6.3 Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0312 | Consumed | Workflow Scheduler provides scheduling for AI nodes |

| RFC-0314 | Consumed | Workflow Error Handling provides AI error taxonomy |

| RFC-0315 | Consumed | Workflow Recovery provides AI recovery |

| RFC-0319 | Consumed | Workflow Security provides AI sandboxing |

| RFC-0320 | Consumed | Workflow Performance provides AI resource budgets |

| RFC-0322 | Consumed | Workflow Extension provides AI node extension |



### 6.4 Consumers

- Workflow Runtime (RFC-0304): Executes AI nodes.

- Workflow Scheduler (RFC-0312): Schedules AI node execution.

- Workflow Extension (RFC-0322): Extends AI node types.



### 6.5 Providers

- AI Node Schema (schemas/workflow/ai-node.json): Provides the AI node format contract.



### 6.6 Forbidden Dependencies

- This specification MUST NOT assume any specific AI framework (a machine learning framework, a machine learning framework, a standard model interchange format, etc.).

- This specification MUST NOT assume GPU availability; CPU-only inference MUST be supported.



## 7 Security

- AI nodes MUST operate within sandbox boundaries per RFC-0319.

- AI model inputs and outputs MUST be validated per RFC-0317.

- AI provider credentials MUST be managed as secrets per RFC-0307.



## 8 Performance

- AI node execution MUST respect the budget constraints defined in RFC-0320.

- AI inference timeouts MUST be configurable per node.

- AI result caching MAY be used to reduce redundant inference.



## 9 Compatibility

- AI provider interfaces MUST be versioned per RFC-0329.

- Model format changes MUST be backward compatible within a major version.



## 10 Compliance

- AI operations MUST comply with organizational AI usage policies per RFC-0330.

- AI inference results MUST be logged in the audit trail per RFC-0321.



## 11 Future Evolution

- **Multi-Agent Workflows**: Coordination of multiple AI agents within a single workflow.

- **Federated AI**: Distributed AI inference across multiple providers.

- **Real-Time AI**: Streaming AI inference for real-time workflow decisions.

- **AI Governance**: Automated compliance checking for AI model usage and bias.



## 12 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)

- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)

- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)

- Any operating system (Windows, Linux, macOS, etc.)

- Any hardware architecture (CPU, GPU, FPGA, etc.)

- Any threading model (single-threaded, multi-threaded, actor-based, etc.)



## 13 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (canonical terminology source) |

| RFC-0304 | Workflow Runtime (AI node execution) |

| RFC-0312 | Workflow Scheduler (AI scheduling) |

| RFC-0314 | Workflow Error Handling (AI errors) |

| RFC-0315 | Workflow Recovery (AI recovery) |

| RFC-0317 | Workflow Validation (AI input/output validation) |

| RFC-0319 | Workflow Security (AI sandboxing) |

| RFC-0320 | Workflow Performance (AI resource budgets) |

| RFC-0321 | Workflow Observability (AI telemetry) |

| RFC-0322 | Workflow Extension (AI node extension) |

| RFC-0324 | Workflow Storage (AI result persistence) |

| RFC-0329 | Workflow Compatibility (AI provider compatibility) |

| RFC-0330 | Workflow Compliance (AI governance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/ai-node.json | AI Node JSON Schema |

| catalog/workflow-node-types.md | Node Type Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0325 (this document), RFC-0326 (Vision), RFC-0322 (Extension) |
---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |
