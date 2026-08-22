RFC: RFC-0326

Title: Workflow Vision

Status: Proposed

Version: 1.0.0

Author: Atlas Specification Committee

Creat
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Roadmap Phase | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Milestone | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Technology Horizon | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Adoption Threshold | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Platform Maturity | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Ecosystem Readiness | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Strategic Initiative | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Technical Debt | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Innovation Area | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Market Fit | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
ed: 2026-07-01

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

  - RFC-0325 Workflow AI


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

  - schemas/workflow/vision-node.json

Related Catalog:

  - catalog/workflow-node-types.md

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Vision specification defines how workflows interact with the Atlas vision system. Vision nodes execute vision operations (frame capture, OCR, detection, segmentation) within the workflow graph.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0326 workflow vision.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 2 Vision Integration Overview



Key principles:



- Vision nodes execute vision operations (frame capture, OCR, detection, segmentation).

- Vision operations are bounded by resource constraints (GPU, memory).

- Vision results are propagated through the data flow model.

- Vision nodes support template matching and pattern recognition.



---



## 3 Integration Points



| Point | Description | RFC Reference |

|---|---|---|

| Vision Nodes | Nodes that perform vision operations | RFC-0201 |

| Frame Capture | Screen and window frame capture | RFC-0202 |

| Template Matching | Visual template matching | RFC-0203 |

| OCR | Optical character recognition | RFC-0204 |

| Object Detection | Object detection and segmentation | RFC-0205 |

| Video Processing | Video frame processing pipeline | RFC-0206 |



---



## 4 Vision Node Execution



### 4.1 Execution Flow



1. Vision node receives input parameters (screen region, template, etc.).

2. Vision operation is executed within the sandbox.

3. Vision results are stored in output variables.

4. Vision events are emitted for observability.



### 4.2 Resource Requirements



| Resource | Description |

|---|---|

| GPU | Accelerator for vision operations |

| Memory | Frame buffer storage |

| Display | Screen access for frame capture |



---



## 5 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | Six integration points MUST be defined. | Point enumeration test |

| AC-02 | Three vision resource types MUST be declared. | Resource test |



---



## 6 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview |

| RFC-0325 | Workflow AI |



---



## 5 Terminology



| Term | Definition | Source |

|---|---|---|

| Vision Node | A workflow node that executes vision operations (frame capture, OCR, detection, segmentation). | RFC-0301 |

| Frame Capture | The process of capturing a screen or window image for vision processing. | This RFC |

| OCR | Optical Character Recognition; extracting text from captured images. | This RFC |

| Object Detection | Identifying and locating objects within a captured frame. | This RFC |

| Segmentation | Partitioning a captured frame into semantic regions. | This RFC |

| Template | A reference image used for visual template matching. | This RFC |



## 6 Layer Boundaries



### 6.1 Responsibilities

This specification IS responsible for: defining vision node execution model, specifying vision operation types, establishing vision result propagation, and defining vision resource constraints.



### 6.2 Non-Responsibilities

This specification IS NOT responsible for: implementing vision algorithms (delegated to vision providers), managing display hardware (delegated to Runtime, RFC-0304), or providing vision-specific security beyond sandboxing (delegated to RFC-0319).



### 6.3 Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0312 | Consumed | Workflow Scheduler provides scheduling for vision nodes |

| RFC-0314 | Consumed | Workflow Error Handling provides vision error taxonomy |

| RFC-0315 | Consumed | Workflow Recovery provides vision recovery |

| RFC-0319 | Consumed | Workflow Security provides vision sandboxing |

| RFC-0320 | Consumed | Workflow Performance provides vision resource budgets |

| RFC-0322 | Consumed | Workflow Extension provides vision node extension |



### 6.4 Consumers

- Workflow Runtime (RFC-0304): Executes vision nodes.

- Workflow Scheduler (RFC-0312): Schedules vision node execution.

- Workflow Extension (RFC-0322): Extends vision node types.



### 6.5 Providers

- Vision Node Schema (schemas/workflow/vision-node.json): Provides the vision node format contract.



### 6.6 Forbidden Dependencies

- This specification MUST NOT assume GPU availability; CPU-only vision processing MUST be supported.

- This specification MUST NOT assume any specific display system (X11, Wayland, DirectShow, etc.).



## 7 Security

- Vision nodes MUST operate within sandbox boundaries per RFC-0319.

- Captured frames containing sensitive data MUST be encrypted per RFC-0319.

- Vision provider credentials MUST be managed as secrets per RFC-0307.



## 8 Performance

- Vision node execution MUST respect the budget constraints defined in RFC-0320.

- Frame capture latency MUST be bounded by configurable timeouts.

- OCR processing MUST complete within the node's execution budget.



## 9 Compatibility

- Vision provider interfaces MUST be versioned per RFC-0329.

- Frame format changes MUST be backward compatible within a major version.



## 10 Compliance

- Vision operations MUST comply with organizational data privacy policies per RFC-0330.

- Frame capture events MUST be logged in the audit trail per RFC-0321.



## 11 Future Evolution

- **Multi-Modal Vision**: Combining vision with audio and text in unified workflow nodes.

- **Edge Vision**: Distributed vision processing at the edge for low-latency operations.

- **Real-Time Vision**: Continuous vision processing for live video streams.

- **Vision Governance**: Automated compliance checking for vision data handling.



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

| RFC-0304 | Workflow Runtime (vision node execution) |

| RFC-0312 | Workflow Scheduler (vision scheduling) |

| RFC-0314 | Workflow Error Handling (vision errors) |

| RFC-0315 | Workflow Recovery (vision recovery) |

| RFC-0317 | Workflow Validation (vision input validation) |

| RFC-0319 | Workflow Security (vision sandboxing) |

| RFC-0320 | Workflow Performance (vision resource budgets) |

| RFC-0321 | Workflow Observability (vision telemetry) |

| RFC-0322 | Workflow Extension (vision node extension) |

| RFC-0324 | Workflow Storage (vision result persistence) |

| RFC-0329 | Workflow Compatibility (vision provider compatibility) |

| RFC-0330 | Workflow Compliance (vision governance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/vision-node.json | Vision Node JSON Schema |

| catalog/workflow-node-types.md | Node Type Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0326 (this document), RFC-0325 (AI), RFC-0322 (Extension) |
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
