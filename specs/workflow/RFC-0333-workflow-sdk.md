RFC: RFC-0333
Title: Workflow Extension SDK
Status: Proposed
Version: 1.0.0
Auth
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Node SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Trigger SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Action SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Condition SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Hook SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Debug SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Capability SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Marketplace SDK | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| SDK Interface | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Plugin Interface | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Extension API | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Developer Tool | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
or: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADS Version: 1.x.x
Spec Version: 1.x.x
Normative: YES
Depends On:
  - RFC-0301 Workflow Overview
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0309 Workflow Actions
  - RFC-0310 Workflow Conditions
  - RFC-0311 Workflow Triggers
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0322 Workflow Extension
  - RFC-0323 Workflow Plugin Integration
  - RFC-0324 Workflow Storage
  - RFC-0325 Workflow AI
  - RFC-0326 Workflow Vision
  - RFC-0327 Workflow IPC
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
  - RFC-0331 Workflow Testing
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/sdk-node.json
  - schemas/workflow/sdk-trigger.json
  - schemas/workflow/sdk-action.json
  - schemas/workflow/sdk-condition.json
  - schemas/workflow/sdk-hook.json
  - schemas/workflow/sdk-debug.json
  - schemas/workflow/sdk-capability.json
  - schemas/workflow/sdk-marketplace.json
Related Catalog:
  - catalog/workflow-extension-points.md
  - catalog/workflow-node-types.md
  - catalog/workflow-triggers.md
  - catalog/workflow-actions.md
  - catalog/workflow-conditions.md
  - catalog/workflow-hooks.md
  - catalog/workflow-debug-events.md
  - catalog/workflow-capabilities.md
Audience: Third-Party Developers
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Third-party developers MUST conform to the SDK interface contracts defined in this document.

---

## Authority
This RFC is the authoritative specification for the Workflow Extension SDK.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Node SDK | The interface contract for implementing custom workflow node types. | This RFC |
| Trigger SDK | The interface contract for implementing custom workflow trigger types. | This RFC |
| Action SDK | The interface contract for implementing custom workflow action types. | This RFC |
| Condition SDK | The interface contract for implementing custom workflow condition types. | This RFC |
| Hook SDK | The interface contract for implementing lifecycle hooks. | This RFC |
| Debug SDK | The interface contract for implementing custom debug operations. | This RFC |
| Capability SDK | The interface contract for declaring node capabilities. | This RFC |
| Marketplace SDK | The interface contract for publishing to the Atlas Marketplace. | This RFC |
| Extension Point | A defined location in the workflow system where third-party code can inject behavior. | RFC-0322 |
| Node Type | A registered classification of workflow nodes with defined inputs and outputs. | RFC-0309 |
| Trigger Type | A named category of trigger (e.g., Manual, Scheduled, Event-based) that determines execution initiation. | RFC-0311 | RFC-0311 |
| Action Type | A registered classification of workflow actions with defined operations. | RFC-0309 |
| Condition Type | A registered classification of workflow conditions with defined evaluation logic. | RFC-0310 |
| Lifecycle Hook | A callback invoked at specific workflow lifecycle stages. | RFC-0305 |
| Debug Operation | An action performed through the debugging interface for inspection or intervention. | RFC-0316 | RFC-0316 |
| Capability Declaration | A structured declaration of resources and permissions a node requires. | RFC-0319 |
| Package Manifest | A structured document describing the SDK extension for marketplace submission. | RFC-0323 |

## 2 SDK Overview

The Workflow Extension SDK specification defines the interfaces through which third-party developers extend the Atlas workflow system. The SDK provides eight distinct extension points, each with a standardized interface contract.

Key principles:

- Every SDK extension MUST implement its interface contract exactly.
- Every SDK extension MUST declare its capabilities in the manifest.
- Every SDK extension MUST operate within sandbox boundaries per RFC-0319.
- Every SDK extension MUST be testable per RFC-0331.
- Every SDK extension MUST be versioned per RFC-0318.
- Every SDK extension MUST be distributable through the marketplace per RFC-0323.

## 3 SDK Interfaces

### 3.1 Node SDK

The Node SDK enables custom workflow node types:

| Interface | Method | Description |
|---|---|---|
| egisterNodeType(id, schema) | Declare | Register a new node type with its input/output schema |
| execute(context, inputs) | Implement | Execute the node's work with given context and inputs |
| alidate(inputs) | Implement | Validate inputs before execution |
| getCapabilities() | Implement | Return declared capabilities for this node type |
| getMetadata() | Implement | Return node metadata (name, description, version) |

### 3.2 Trigger SDK

The Trigger SDK enables custom workflow triggers:

| Interface | Method | Description |
|---|---|---|
| egisterTriggerType(id, schema) | Declare | Register a new trigger type with its event schema |
| subscribe(eventSource, handler) | Implement | Subscribe to an event source |
| unsubscribe(eventSource) | Implement | Unsubscribe from an event source |
| alidateConfig(config) | Implement | Validate trigger configuration |
| getMetadata() | Implement | Return trigger metadata |

### 3.3 Action SDK

The Action SDK enables custom workflow actions:

| Interface | Method | Description |
|---|---|---|
| egisterActionType(id, schema) | Declare | Register a new action type |
| execute(actionParams) | Implement | Execute the action with given parameters |
| alidate(params) | Implement | Validate action parameters |
| getMetadata() | Implement | Return action metadata |

### 3.4 Condition SDK

The Condition SDK enables custom workflow conditions:

| Interface | Method | Description |
|---|---|---|
| egisterConditionType(id, schema) | Declare | Register a new condition type |
| evaluate(left, operator, right) | Implement | Evaluate the condition expression |
| alidateExpression(expr) | Implement | Validate the condition expression |
| getMetadata() | Implement | Return condition metadata |

### 3.5 Hook SDK

The Hook SDK enables lifecycle hooks:

| Interface | Method | Description |
|---|---|---|
| egisterHook(type, callback) | Declare | Register a hook for a lifecycle event |
| onWorkflowCreated(instanceId) | Implement | Called when a workflow instance is created |
| onNodeStarted(instanceId, nodeId) | Implement | Called when a node starts execution |
| onNodeCompleted(instanceId, nodeId, result) | Implement | Called when a node completes |
| onWorkflowCompleted(instanceId, result) | Implement | Called when a workflow completes |
| onWorkflowFailed(instanceId, error) | Implement | Called when a workflow fails |
| onCheckpointSaved(instanceId, checkpointId) | Implement | Called when a checkpoint is saved |

### 3.6 Debug SDK

The Debug SDK enables custom debug operations:

| Interface | Method | Description |
|---|---|---|
| egisterDebugger(id, operations) | Declare | Register a custom debugger |
| inspectNode(instanceId, nodeId) | Implement | Inspect a node's state |
| modifyVariable(instanceId, variableId, value) | Implement | Modify a variable value (write mode) |
| skipNode(instanceId, nodeId) | Implement | Skip a node execution |
| eplayNode(instanceId, nodeId) | Implement | Replay a node execution |
| getExecutionTrace(instanceId) | Implement | Get the full execution trace |

### 3.7 Capability SDK

The Capability SDK enables capability declarations:

| Interface | Method | Description |
|---|---|---|
| declareCapability(name, resource, quantity) | Declare | Declare a resource capability |
| declarePermission(scope, permission) | Declare | Declare a permission requirement |
| alidateCapability(capability) | Validate | Validate a capability declaration |
| esolveCapability(request) | Resolve | Resolve a capability request |

### 3.8 Marketplace SDK

The Marketplace SDK enables marketplace distribution:

| Interface | Method | Description |
|---|---|---|
| packageExtension(manifest, assets) | Package | Package an extension for distribution |
| signPackage(privateKey, package) | Sign | Cryptographically sign a package |
| submitToMarketplace(package, metadata) | Submit | Submit a package to the marketplace |
| getMarketplaceStatus(packageId) | Query | Query marketplace submission status |
| publishVersion(packageId, version) | Publish | Publish a new version |

## 4 Extension Lifecycle

### 4.1 Development Lifecycle

| Stage | Description | SDK Interface |
|---|---|---|
| Design | Define extension interface and manifest | Node SDK, Trigger SDK, etc. |
| Implement | Write extension logic | All SDK interfaces |
| Test | Run unit, integration, and replay tests | RFC-0331 test framework |
| Validate | Validate against RFC compliance | RFC-0317 validation |
| Package | Create distributable package | Marketplace SDK |
| Submit | Submit to marketplace | Marketplace SDK |
| Deploy | Install and activate | Marketplace SDK |
| Monitor | Observe extension health | Debug SDK, Observability |

### 4.2 Version Lifecycle

Extensions follow the same versioning model as workflow definitions (RFC-0318):

- MAJOR: Breaking interface changes
- MINOR: Backward-compatible additions
- PATCH: Backward-compatible fixes

## 5 Layer Boundaries

### 5.1 Responsibilities
This specification IS responsible for: defining eight SDK interface contracts, specifying the extension development lifecycle, establishing version management for extensions, and defining marketplace distribution interfaces.

### 5.2 Non-Responsibilities
This specification IS NOT responsible for: implementing SDK runtimes (delegated to RFC-0304), managing the marketplace (delegated to RFC-0501), or validating extension code (delegated to RFC-0317).

### 5.3 Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0303 | Consumed | Workflow Execution provides execution context |
| RFC-0304 | Consumed | Workflow Runtime provides hosting |
| RFC-0309 | Consumed | Workflow Actions provides action SDK contract |
| RFC-0310 | Consumed | Workflow Conditions provides condition SDK contract |
| RFC-0311 | Consumed | Workflow Triggers provides trigger SDK contract |
| RFC-0312 | Consumed | Workflow Scheduler provides scheduling interface |
| RFC-0314 | Consumed | Workflow Error Handling provides error interface |
| RFC-0315 | Consumed | Workflow Recovery provides recovery interface |
| RFC-0316 | Consumed | Workflow Debugging provides debug SDK contract |
| RFC-0317 | Consumed | Workflow Validation provides validation rules |
| RFC-0318 | Consumed | Workflow Versioning provides version management |
| RFC-0319 | Consumed | Workflow Security provides sandboxing |
| RFC-0320 | Consumed | Workflow Performance provides performance constraints |
| RFC-0321 | Consumed | Workflow Observability provides telemetry |
| RFC-0322 | Consumed | Workflow Extension provides extension points |
| RFC-0323 | Consumed | Workflow Plugin Integration provides plugin hosting |
| RFC-0324 | Consumed | Workflow Storage provides persistence |
| RFC-0325 | Consumed | Workflow AI provides AI node interface |
| RFC-0326 | Consumed | Workflow Vision provides vision node interface |
| RFC-0327 | Consumed | Workflow IPC provides communication interface |
| RFC-0328 | Consumed | Workflow Serialization provides encoding |
| RFC-0329 | Consumed | Workflow Compatibility provides version compatibility |
| RFC-0330 | Consumed | Workflow Compliance provides compliance verification |
| RFC-0331 | Consumed | Workflow Testing provides test framework |

### 5.4 Consumers
- Third-party developers: Use SDK interfaces to build extensions.
- Workflow Runtime (RFC-0304): Hosts SDK extensions.
- Marketplace (RFC-0501): Distributes SDK packages.

### 5.5 Providers
- Node SDK Schema (schemas/workflow/sdk-node.json): Provides node interface contract.
- Trigger SDK Schema (schemas/workflow/sdk-trigger.json): Provides trigger interface contract.
- Action SDK Schema (schemas/workflow/sdk-action.json): Provides action interface contract.
- Condition SDK Schema (schemas/workflow/sdk-condition.json): Provides condition interface contract.
- Hook SDK Schema (schemas/workflow/sdk-hook.json): Provides hook interface contract.
- Debug SDK Schema (schemas/workflow/sdk-debug.json): Provides debug interface contract.
- Capability SDK Schema (schemas/workflow/sdk-capability.json): Provides capability interface contract.
- Marketplace SDK Schema (schemas/workflow/sdk-marketplace.json): Provides marketplace interface contract.

### 5.6 Forbidden Dependencies
- This specification MUST NOT depend on any specific programming language SDK (npm, pip, Maven, etc.).
- This specification MUST NOT prescribe a particular IDE or development toolchain.

## 6 Security
- All SDK extensions MUST operate within sandbox boundaries per RFC-0319.
- SDK extensions MUST declare all required capabilities and permissions.
- Marketplace packages MUST be cryptographically signed.
- SDK extensions MUST NOT have access to secrets without explicit declaration.

## 7 Performance
- SDK interface calls MUST add less than 1ms overhead per invocation.
- Extension loading MUST complete within 500ms.
- Capability resolution MUST complete within 100ms.

## 8 Compatibility
- SDK interfaces MUST be backward compatible within a major version.
- Breaking SDK interface changes MUST require a new major version.
- Deprecated SDK interfaces MUST remain functional for at least two minor versions.

## 9 Compliance
- All SDK extensions MUST be testable per RFC-0331.
- SDK extension submissions MUST comply with marketplace policies per RFC-0330.
- SDK usage MUST be recorded in the audit trail per RFC-0321.

## 10 Future Evolution
- **SDK Code Generation**: Automatic SDK stub generation from interface definitions.
- **SDK Hot Reload**: Runtime SDK extension updates without restart.
- **SDK Playground**: Interactive development environment for SDK extensions.
- **SDK Analytics**: Usage analytics for SDK extensions in the marketplace.
- **Multi-Language SDK**: SDK interfaces available in multiple languages simultaneously.

## 11 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any SDK packaging format (npm, pip, Maven, Cargo, etc.)
- Any IDE or development toolchain

## 12 Acceptance Criteria

### 12.1 SDK Interfaces

| # | Criterion | Verification Method |
|---|---|---|

### 12.2 Extension Lifecycle

| # | Criterion | Verification Method |
|---|---|---|

### 12.3 Security and Performance

| # | Criterion | Verification Method |
|---|---|---|

## 13 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (extension execution context) |
| RFC-0304 | Workflow Runtime (extension hosting) |
| RFC-0309 | Workflow Actions (action SDK contract) |
| RFC-0310 | Workflow Conditions (condition SDK contract) |
| RFC-0311 | Workflow Triggers (trigger SDK contract) |
| RFC-0312 | Workflow Scheduler (scheduling interface) |
| RFC-0314 | Workflow Error Handling (error interface) |
| RFC-0315 | Workflow Recovery (recovery interface) |
| RFC-0316 | Workflow Debugging (debug SDK contract) |
| RFC-0317 | Workflow Validation (validation rules) |
| RFC-0318 | Workflow Versioning (version management) |
| RFC-0319 | Workflow Security (sandboxing) |
| RFC-0320 | Workflow Performance (performance constraints) |
| RFC-0321 | Workflow Observability (telemetry) |
| RFC-0322 | Workflow Extension (extension points) |
| RFC-0323 | Workflow Plugin Integration (plugin hosting) |
| RFC-0324 | Workflow Storage (persistence) |
| RFC-0325 | Workflow AI (AI node interface) |
| RFC-0326 | Workflow Vision (vision node interface) |
| RFC-0327 | Workflow IPC (communication interface) |
| RFC-0328 | Workflow Serialization (encoding) |
| RFC-0329 | Workflow Compatibility (version compatibility) |
| RFC-0330 | Workflow Compliance (compliance verification) |
| RFC-0331 | Workflow Testing (test framework) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/sdk-node.json | Node SDK JSON Schema |
| schemas/workflow/sdk-trigger.json | Trigger SDK JSON Schema |
| schemas/workflow/sdk-action.json | Action SDK JSON Schema |
| schemas/workflow/sdk-condition.json | Condition SDK JSON Schema |
| schemas/workflow/sdk-hook.json | Hook SDK JSON Schema |
| schemas/workflow/sdk-debug.json | Debug SDK JSON Schema |
| schemas/workflow/sdk-capability.json | Capability SDK JSON Schema |
| schemas/workflow/sdk-marketplace.json | Marketplace SDK JSON Schema |
| catalog/workflow-extension-points.md | Extension Points Catalog |
| catalog/workflow-node-types.md | Node Types Catalog |
| catalog/workflow-triggers.md | Triggers Catalog |
| catalog/workflow-actions.md | Actions Catalog |
| catalog/workflow-conditions.md | Conditions Catalog |
| catalog/workflow-hooks.md | Hooks Catalog |
| catalog/workflow-debug-events.md | Debug Events Catalog |
| catalog/workflow-capabilities.md | Capabilities Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0333 (this document), RFC-0331 (Testing), RFC-0332 (Migration) |

## 14 Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0301 through RFC-0332 (all Workflow RFCs) |
| Related ADR | ADR-0012 |
| Related JSON Schema | schemas/workflow/sdk-{node,trigger,action,condition,hook,debug,capability,marketplace}.json |
| Related Catalog | catalog/workflow-extension-points.md, catalog/workflow-node-types.md, catalog/workflow-triggers.md, catalog/workflow-actions.md, catalog/workflow-conditions.md, catalog/workflow-hooks.md, catalog/workflow-debug-events.md, catalog/workflow-capabilities.md |

## 15 Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |







