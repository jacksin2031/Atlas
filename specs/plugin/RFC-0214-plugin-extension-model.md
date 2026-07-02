# RFC-0214: Plugin Extension Model

RFC: RFC-0214
Title: Plugin Extension Model
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0202 Plugin Manifest
  - RFC-0206 Plugin Capability
  - RFC-0209 Plugin API
Related RFC:
  - RFC-0203 Plugin Lifecycle
  - RFC-0205 Plugin Registry
  - RFC-0210 Plugin Events
Related ADR:
  - ADR-0014 Extension Point Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the extension points, custom services, custom workflow nodes, custom UI, custom commands, custom providers, custom AI adapters, custom vision processors, custom storage providers, custom IPC providers, future extension model, extension lifecycle, registration, validation, and compatibility requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Extension Philosophy](#4-extension-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Extension Points](#9-extension-points)
10. [Custom Services](#10-custom-services)
11. [Custom Workflow Nodes](#11-custom-workflow-nodes)
12. [Custom UI](#12-custom-ui)
13. [Custom Commands](#13-custom-commands)
14. [Custom Providers](#14-custom-providers)
15. [Custom AI Adapters](#15-custom-ai-adapters)
16. [Custom Vision Processors](#16-custom-vision-processors)
17. [Custom Storage Providers](#17-custom-storage-providers)
18. [Custom IPC Providers](#18-custom-ipc-providers)
19. [Future Extension Model](#19-future-extension-model)
20. [Extension Lifecycle](#20-extension-lifecycle)
21. [Registration](#21-registration)
22. [Validation](#22-validation)
23. [Compatibility](#23-compatibility)
24. [Performance Budgets](#24-performance-budgets)
25. [Glossary](#25-glossary)
26. [Acceptance Criteria](#26-acceptance-criteria)
27. [Cross References](#27-cross-references)
28. [References](#28-references)
29. [Revision History](#29-revision-history)
30. [Future Evolution](#30-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Extension Points**: Define standardized points where plugins can contribute functionality.
2. **Custom Services**: Allow plugins to provide reusable service implementations.
3. **Custom Workflow Nodes**: Enable plugins to add discrete steps to workflow executions.
4. **Custom UI**: Permit plugins to supply visual elements for the user interface.
5. **Custom Commands**: Support plugins to register callable commands.
6. **Custom Providers**: Allow plugins to supply data, resources, or connectivity.
7. **Custom AI Adapters**: Enable integration of AI models and inference services.
8. **Custom Vision Processors**: Support visual analysis and image processing contributions.
9. **Custom Storage Providers**: Allow persistent data storage implementations.
10. **Custom IPC Providers**: Enable inter-process communication implementations.
11. **Future Extensibility**: Ensure the extension model can evolve without breaking existing extensions.
12. **Extension Lifecycle**: Define registration, activation, and deactivation procedures.
13. **Registration**: Provide a standardized registration mechanism.
14. **Validation**: Ensure extensions meet contractual obligations.
15. **Compatibility**: Maintain backward compatibility across extension versions.

---



## 4 Extension Philosophy

Extensions in the Atlas Platform follow these principles:

- Extensions contribute functionality through well-defined contracts.
- Extensions are isolated from the core platform.
- Extensions MUST NOT modify core platform behavior.
- Extensions are discoverable through the registry.
- Extensions are versioned independently of the platform.
- Extension points are stable; new extension points MAY be added.
- Extension contracts are backward-compatible within major version boundaries.

---


## 6 Boundaries

Extensions are bounded by:

- **Contract Boundary**: Extensions MUST implement all methods defined in their extension point contract.
- **Isolation Boundary**: Extensions MUST NOT share mutable state with other extensions unless explicitly designed for it.
- **Scope Boundary**: Extensions are scoped to the plugin that implements them.
- **Security Boundary**: Extensions are subject to the same security policies as the host plugin.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
classDiagram
    class ExtensionRegistrar {
        +register(extension)
        +unregister(extensionId)
        +lookup(extensionPoint)
        +listAll()
    }
    class CapabilityManager {
        +resolve(capabilityId)
        +advertise(capability)
    }
    class ExtensionPoint {
        +string id
        +string contract
        +List~Extension~ implementations
    }
    class CustomService {
        +initialize()
        +execute(context)
        +shutdown()
    }
    class CustomWorkflowNode {
        +execute(input)
        +getErrorHandling()
        +getRetryPolicy()
    }
    class CustomUIComponent {
        +render(context)
        +handleEvent(event)
    }
    class CustomCommand {
        +execute(args)
        +getHelpText()
    }
    class CustomProvider {
        +connect()
        +getData()
        +disconnect()
    }
    class CustomAIAdapter {
        +infer(input)
        +getModelInfo()
    }
    class CustomVisionProcessor {
        +process(image)
        +getAnnotationSchema()
    }
    class CustomStorageProvider {
        +store(key, data)
        +retrieve(key)
        +delete(key)
    }
    class CustomIPCProvider {
        +sendMessage(target, message)
        +receive()
    }
    ExtensionRegistrar --> ExtensionPoint : manages
    ExtensionPoint o-- CustomService
    ExtensionPoint o-- CustomWorkflowNode
    ExtensionPoint o-- CustomUIComponent
    ExtensionPoint o-- CustomCommand
    ExtensionPoint o-- CustomProvider
    ExtensionPoint o-- CustomAIAdapter
    ExtensionPoint o-- CustomVisionProcessor
    ExtensionPoint o-- CustomStorageProvider
    ExtensionPoint o-- CustomIPCProvider
    ExtensionRegistrar --> CapabilityManager : coordinates

---

4. When multiple plugins implement the same extension point category, the PEXT-EVENT-HANDLER execution order MUST be determined by the priority field in the manifest, with lower numeric values executing first.
5. Extension point implementations MUST be discoverable through the PIF-CAPABILITY-MANAGER after the plugin reaches the PSTATE-ACTIVE state.

---


## 11 Custom Workflow Nodes

Custom workflow nodes add discrete steps to workflow execution graphs:

1. Workflow nodes MUST define clear input and output schemas.
2. Workflow nodes MUST implement error handling and retry semantics.
3. Workflow nodes MUST support cancellation through the lifecycle manager.
4. Workflow nodes MUST be idempotent where possible.
5. Workflow nodes MUST emit events at each execution phase.
6. Workflow nodes MUST support dependency injection for upstream node outputs.
7. Workflow nodes MUST define their execution timeout.
8. Workflow nodes MUST be composable: outputs of one node MAY feed into inputs of another.

---


## 13 Custom Commands

Custom commands register callable operations accessible through the CLI or API:

1. Commands MUST define their name, arguments, flags, and help text.
2. Commands MUST return structured output.
3. Commands MUST validate their inputs before execution.
4. Commands MUST support help text generation.
5. Commands MUST be discoverable through the command registry.
6. Commands MUST respect the plugin trust level for privileged operations.
7. Commands MUST emit audit events for security-relevant operations.
8. Commands MUST support subcommands through hierarchical naming.

---


## 15 Custom AI Adapters

Custom AI adapters integrate artificial intelligence models or inference services:

1. AI adapters MUST define the model interface including input and output schemas.
2. AI adapters MUST support parameter controls including temperature and top-p.
3. AI adapters MUST implement rate limiting to prevent resource exhaustion.
4. AI adapters MUST define model information including version and capabilities.
5. AI adapters MUST handle inference failures gracefully with retry logic.
6. AI adapters MUST be configurable through the plugin configuration interface.
7. AI adapters MUST emit events for inference requests and completions.
8. AI adapters MUST support model switching through the capability manager.

---


## 17 Custom Storage Providers

Custom storage providers manage persistent data storage operations:

1. Storage providers MUST implement CRUD operations with defined semantics.
2. Storage providers MUST support query capabilities for data retrieval.
3. Storage providers MUST define transaction semantics including isolation levels.
4. Storage providers MUST implement data retention policies.
5. Storage providers MUST support encryption for sensitive data.
6. Storage providers MUST be configurable through the plugin configuration interface.
7. Storage providers MUST emit events for data modification operations.
8. Storage providers MUST support backup and restore operations.

---


## 19 Future Extension Model

The extension model MUST support future extension types without requiring specification changes:

1. New extension point categories MAY be added through catalog updates.
2. New extension point implementations MUST conform to the registration and validation rules.
3. Future extension types MUST be backward-compatible with existing consumers.
4. Extension point contracts MUST be versioned independently of the plugin version.
5. The extension registrar MUST support dynamic extension point registration.
6. Extension point discovery MUST support filtering by version and capability.
7. The extension model MUST support composite extensions that implement multiple extension points.
8. Extension point evolution MUST follow the manifest evolution rules defined in RFC-0212.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 21 Registration

Extension registration rules:

1. Extensions MUST be registered before the plugin reaches PSTATE-ACTIVE.
2. Registration MUST include the extension point identifier, implementation reference, and priority.
3. Registration MUST be idempotent: registering the same extension twice MUST NOT create duplicates.
4. Registration MUST validate the extension implementation against the extension point contract.
5. Registration MUST fail if the extension point is not in the approved catalog.
6. Registration MUST update the capability manager with the extension information.
7. Registration MUST emit PEVT-CAPABILITY-ADDED events.
8. Registration MUST be logged for audit purposes.

---


## 23 Compatibility

Extension compatibility rules:

1. Extension contracts MUST be backward-compatible within major version boundaries.
2. New methods MAY be added to extension contracts in minor versions.
3. Existing methods MUST NOT be removed or have their signatures changed in minor versions.
4. Extension implementations MUST be compatible with the contract version declared in the manifest.
5. Version incompatibilities MUST be detected during registration validation.
6. Deprecated extension methods MUST continue to function until the sunset date.
7. Extension compatibility MUST be queryable through the registry.
8. Compatibility checks MUST use the PIF-VERSION-COMPATIBILITY interface.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 25 Glossary

| Term | Definition |
|---|---|
| Extension Point | A predefined location where plugins can contribute functionality. |
| Extension Registrar | The component that manages extension registration and lookup. |
| Extension Contract | The interface definition that an extension implementation MUST fulfill. |
| Capability Manager | The component that coordinates extension-to-capability mappings. |
| Hot-Reload | The ability to replace an extension at runtime without restarting the plugin. |
| Composite Extension | An extension that implements multiple extension point categories. |

---

- **Expected Result**: Only one registration exists.

#### AC-0214-006
- **Requirement**: Extensions MUST be unregistered during the PSTATE-DEACTIVATING phase.
- **Verification**: Deactivate a plugin and check extension registration.
- **Expected Result**: Extensions are unregistered.

#### AC-0214-007
- **Requirement**: Extension implementations MUST be thread-safe for concurrent access.
- **Verification**: Access an extension from multiple threads concurrently.
- **Expected Result**: No data corruption or race conditions occur.

#### AC-0214-008
- **Requirement**: Extensions MUST NOT hold persistent locks across lifecycle transitions.
- **Verification**: Hold a lock during a lifecycle transition and check for deadlocks.
- **Expected Result**: No deadlock occurs; lock is released.

#### AC-0214-009
- **Requirement**: Extensions MUST support graceful shutdown without data corruption.
- **Verification**: Shut down a plugin with active extensions and check data integrity.
- **Expected Result**: Data is intact after shutdown.

#### AC-0214-010
- **Requirement**: The extension architecture MUST support at least 15 extension point categories.
- **Verification**: Register extensions for all 15 categories.
- **Expected Result**: All registrations succeed.

### Extension Points (AC-0214-011 to AC-0214-020)

#### AC-0214-011
- **Requirement**: Every extension point in the catalog MUST have a unique PEXT-* identifier.
- **Verification**: Check all identifiers in the catalog.
- **Expected Result**: All identifiers are unique.

#### AC-0214-012
- **Requirement**: A plugin MUST declare every extension point it implements in its manifest.
- **Verification**: Implement an extension point without declaring it in the manifest.
- **Expected Result**: Registration is rejected.

#### AC-0214-013
- **Requirement**: A plugin MUST implement all methods defined for each registered extension point.
- **Verification**: Register an extension that omits a contract method.
- **Expected Result**: Registration is rejected.

#### AC-0214-014
- **Requirement**: A plugin MUST NOT implement more than one extension point of the same category serving the identical consumer role.
- **Verification**: Register two extensions of the same category for the same role.
- **Expected Result**: Second registration is rejected.

#### AC-0214-015
- **Requirement**: PEXT-EVENT-HANDLER execution order MUST be determined by the priority field.
- **Verification**: Register two event handlers with different priorities and trigger an event.
- **Expected Result**: Lower priority value executes first.

#### AC-0214-016
- **Requirement**: Extension point implementations MUST be discoverable after the plugin reaches PSTATE-ACTIVE.
- **Verification**: Query extensions before and after plugin activation.
- **Expected Result**: Extensions are only discoverable after activation.

#### AC-0214-017
- **Requirement**: All 15 extension point categories MUST be supported.
- **Verification**: Register one extension for each category.
- **Expected Result**: All 15 registrations succeed.

#### AC-0214-018
- **Requirement**: Extension point contracts MUST be versioned independently of the plugin version.
- **Verification**: Update a plugin version without changing the extension contract version.
- **Expected Result**: Contract version remains unchanged.

#### AC-0214-019
- **Requirement**: Extension points MUST be queryable by category and implementation type.
- **Verification**: Query extension points by each dimension.
- **Expected Result**: Correct results are returned.

#### AC-0214-020
- **Requirement**: Extension point catalogs MUST be immutable once published.
- **Verification**: Attempt to modify a published extension point.
- **Expected Result**: Modification is rejected.

### Custom Services (AC-0214-021 to AC-0214-026)

#### AC-0214-021
- **Requirement**: Custom services MUST define a clear interface contract with documented methods.
- **Verification**: Inspect a custom service implementation for interface documentation.
- **Expected Result**: Interface is documented and complete.

#### AC-0214-022
- **Requirement**: Custom services MUST support initialization and shutdown lifecycle hooks.
- **Verification**: Call initialization and shutdown hooks on a custom service.
- **Expected Result**: Hooks are called and service transitions states correctly.

#### AC-0214-023
- **Requirement**: Custom services MUST be replaceable at runtime to support hot-reload scenarios.
- **Verification**: Replace a running custom service.
- **Expected Result**: Replacement completes without disrupting consumers.

#### AC-0214-024
- **Requirement**: Custom services MUST report health status through the health event system.
- **Verification**: Check health events from a custom service.
- **Expected Result**: Health events are emitted.

#### AC-0214-025
- **Requirement**: Custom services MUST be configurable through the plugin configuration interface.
- **Verification**: Modify a custom service configuration.
- **Expected Result**: Configuration change is applied.

#### AC-0214-026
- **Requirement**: Custom services MUST NOT depend on plugin-specific state that changes across lifecycle transitions.
- **Verification**: Check service dependencies for lifecycle-sensitive state.
- **Expected Result**: No lifecycle-sensitive dependencies found.

### Custom Workflow Nodes (AC-0214-027 to AC-0214-032)

#### AC-0214-027
- **Requirement**: Custom workflow nodes MUST define clear input and output schemas.
- **Verification**: Inspect a workflow node for input and output schema definitions.
- **Expected Result**: Schemas are present and complete.

#### AC-0214-028
- **Requirement**: Custom workflow nodes MUST implement error handling and retry semantics.
- **Verification**: Trigger an error in a workflow node and check error handling.
- **Expected Result**: Error is handled according to the defined policy.

#### AC-0214-029
- **Requirement**: Custom workflow nodes MUST support cancellation through the lifecycle manager.
- **Verification**: Cancel a running workflow node.
- **Expected Result**: Node cancels gracefully.

#### AC-0214-030
- **Requirement**: Custom workflow nodes MUST be idempotent where possible.
- **Verification**: Execute the same workflow node multiple times with the same input.
- **Expected Result**: Outputs are identical across executions.

#### AC-0214-031
- **Requirement**: Custom workflow nodes MUST emit events at each execution phase.
- **Verification**: Execute a workflow node and check emitted events.
- **Expected Result**: Events are emitted for each phase.

#### AC-0214-032
- **Requirement**: Custom workflow nodes MUST define their execution timeout.
- **Verification**: Check a workflow node configuration for timeout definition.
- **Expected Result**: Timeout is defined.

### Custom UI (AC-0214-033 to AC-0214-038)

#### AC-0214-033
- **Requirement**: Custom UI components MUST define their rendering contract and data binding interface.
- **Verification**: Inspect a UI component for rendering contract and data binding.
- **Expected Result**: Both are defined.

#### AC-0214-034
- **Requirement**: Custom UI components MUST support accessibility requirements.
- **Verification**: Check a UI component for accessibility attributes.
- **Expected Result**: Accessibility attributes are present.

#### AC-0214-035
- **Requirement**: Custom UI components MUST NOT block the main rendering thread.
- **Verification**: Measure rendering thread responsiveness during UI component execution.
- **Expected Result**: Rendering thread is not blocked.

#### AC-0214-036
- **Requirement**: Custom UI components MUST handle resize and layout changes gracefully.
- **Verification**: Resize the UI and check component behavior.
- **Expected Result**: Component adapts without errors.

#### AC-0214-037
- **Requirement**: Custom UI components MUST support localization.
- **Verification**: Switch the UI locale and check component text.
- **Expected Result**: Text is localized.

#### AC-0214-038
- **Requirement**: Custom UI components MUST release resources on component destruction.
- **Verification**: Destroy a UI component and check resource usage.
- **Expected Result**: Resources are released.

### Custom Commands (AC-0214-039 to AC-0214-044)

#### AC-0214-039
- **Requirement**: Custom commands MUST define their name, arguments, flags, and help text.
- **Verification**: Inspect a command registration for all required fields.
- **Expected Result**: All fields are present.

#### AC-0214-040
- **Requirement**: Custom commands MUST validate their inputs before execution.
- **Verification**: Execute a command with invalid inputs.
- **Expected Result**: Input validation fails and execution is blocked.

#### AC-0214-041
- **Requirement**: Custom commands MUST return structured output.
- **Verification**: Execute a command and check output format.
- **Expected Result**: Output is structured.

#### AC-0214-042
- **Requirement**: Custom commands MUST respect the plugin trust level for privileged operations.
- **Verification**: Execute a privileged command from a low-trust plugin.
- **Expected Result**: Command is blocked.

#### AC-0214-043
- **Requirement**: Custom commands MUST emit audit events for security-relevant operations.
- **Verification**: Execute a security-relevant command and check audit events.
- **Expected Result**: Audit event is emitted.

#### AC-0214-044
- **Requirement**: Custom commands MUST support subcommands through hierarchical naming.
- **Verification**: Register and execute a subcommand.
- **Expected Result**: Subcommand is executed correctly.

### Custom Providers (AC-0214-045 to AC-0214-050)

#### AC-0214-045
- **Requirement**: Custom providers MUST define connection parameters and data schemas.
- **Verification**: Inspect a provider for connection parameters and data schema.
- **Expected Result**: Both are defined.

#### AC-0214-046
- **Requirement**: Custom providers MUST handle connection failures gracefully.
- **Verification**: Simulate a connection failure.
- **Expected Result**: Provider recovers or reports failure without crashing.

#### AC-0214-047
- **Requirement**: Custom providers MUST support authentication through the security gate.
- **Verification**: Connect a provider with authentication.
- **Expected Result**: Authentication is performed through the security gate.

#### AC-0214-048
- **Requirement**: Custom providers MUST emit health events when connection status changes.
- **Verification**: Change provider connection status and check events.
- **Expected Result**: Health event is emitted.

#### AC-0214-049
- **Requirement**: Custom providers MUST support graceful shutdown without data loss.
- **Verification**: Shut down a provider with pending data.
- **Expected Result**: Pending data is persisted.

#### AC-0214-050
- **Requirement**: Custom providers MUST define their data availability guarantees.
- **Verification**: Inspect a provider for availability guarantees.
- **Expected Result**: Guarantees are defined.

### Custom AI/Vision/Storage/IPC (AC-0214-051 to AC-0214-060)

#### AC-0214-051
- **Requirement**: Custom AI adapters MUST define the model interface including input and output schemas.
- **Verification**: Inspect an AI adapter for interface documentation.
- **Expected Result**: Interface is documented.

#### AC-0214-052
- **Requirement**: Custom AI adapters MUST implement rate limiting to prevent resource exhaustion.
- **Verification**: Send rapid inference requests and check rate limiting.
- **Expected Result**: Requests are rate-limited.

#### AC-0214-053
- **Requirement**: Custom vision processors MUST define input format expectations.
- **Verification**: Inspect a vision processor for input format documentation.
- **Expected Result**: Input format is documented.

#### AC-0214-054
- **Requirement**: Custom vision processors MUST handle large images through chunking or downsampling.
- **Verification**: Process a large image and check handling.
- **Expected Result**: Image is processed without memory overflow.

#### AC-0214-055
- **Requirement**: Custom storage providers MUST implement CRUD operations with defined semantics.
- **Verification**: Perform CRUD operations on a storage provider.
- **Expected Result**: Operations complete with defined semantics.

#### AC-0214-056
- **Requirement**: Custom storage providers MUST support encryption for sensitive data.
- **Verification**: Store sensitive data and check encryption.
- **Expected Result**: Data is encrypted.

#### AC-0214-057
- **Requirement**: Custom IPC providers MUST define message formats and transport protocols.
- **Verification**: Inspect an IPC provider for format and protocol documentation.
- **Expected Result**: Both are documented.

#### AC-0214-058
- **Requirement**: Custom IPC providers MUST support connection management including reconnection.
- **Verification**: Disconnect and reconnect an IPC provider.
- **Expected Result**: Reconnection succeeds.

#### AC-0214-059
- **Requirement**: Custom AI adapters MUST support model switching through the capability manager.
- **Verification**: Switch the model used by an AI adapter.
- **Expected Result**: Switch completes through the capability manager.

#### AC-0214-060
- **Requirement**: Custom vision processors MUST support batch processing for efficiency.
- **Verification**: Process multiple images in batch mode.
- **Expected Result**: Batch processing completes efficiently.

### Lifecycle (AC-0214-061 to AC-0214-066)

#### AC-0214-061
- **Requirement**: Extensions MUST be registered during the PSTATE-INITIALIZING phase.
- **Verification**: Attempt to register an extension during PSTATE-RUNNING.
- **Expected Result**: Registration is delayed until PSTATE-INITIALIZING.

#### AC-0214-062
- **Requirement**: Extensions MUST be unregistered during the PSTATE-DEACTIVATING phase.
- **Verification**: Check extension registration after deactivation.
- **Expected Result**: Extensions are unregistered.

#### AC-0214-063
- **Requirement**: Extension registration MUST emit PEVT-CAPABILITY-ADDED events.
- **Verification**: Register an extension and check emitted events.
- **Expected Result**: Capability added event is emitted.

#### AC-0214-064
- **Requirement**: Extension unregistration MUST emit PEVT-CAPABILITY-REMOVED events.
- **Verification**: Deactivate a plugin with extensions and check emitted events.
- **Expected Result**: Capability removed event is emitted.

#### AC-0214-065
- **Requirement**: Extension lifecycle transitions MUST be atomic with respect to observable behavior.
- **Verification**: Query extension state during a lifecycle transition.
- **Expected Result**: No partial state is observable.

#### AC-0214-066
- **Requirement**: Extension observability layers MUST record every lifecycle transition with a timestamp.
- **Verification**: Check observability logs for extension transitions.
- **Expected Result**: All transitions are recorded with timestamps.

### Registration/Validation (AC-0214-067 to AC-0214-072)

#### AC-0214-067
- **Requirement**: Extension registration MUST include the extension point identifier, implementation reference, and priority.
- **Verification**: Register an extension without one of these fields.
- **Expected Result**: Registration is rejected.

#### AC-0214-068
- **Requirement**: Registration MUST validate the extension implementation against the extension point contract.
- **Verification**: Register an extension that does not match its contract.
- **Expected Result**: Registration is rejected.

#### AC-0214-069
- **Requirement**: Registration MUST fail if the extension point is not in the approved catalog.
- **Verification**: Register an extension with a non-catalog extension point.
- **Expected Result**: Registration is rejected.

#### AC-0214-070
- **Requirement**: Registration MUST update the capability manager with the extension information.
- **Verification**: Register an extension and query the capability manager.
- **Expected Result**: Capability manager reflects the registration.

#### AC-0214-071
- **Requirement**: Extension validation MUST occur during the PSTATE-INITIALIZING phase.
- **Verification**: Attempt extension validation during PSTATE-RUNNING.
- **Expected Result**: Validation is deferred to PSTATE-INITIALIZING.

#### AC-0214-072
- **Requirement**: Validation failures MUST emit PEVT-MANIFEST-INVALID events.
- **Verification**: Trigger a validation failure and check events.
- **Expected Result**: Manifest invalid event is emitted.

### Compatibility (AC-0214-073 to AC-0214-075)

#### AC-0214-073
- **Requirement**: Extension contracts MUST be backward-compatible within major version boundaries.
- **Verification**: Check contract changes across minor versions.
- **Expected Result**: Changes are backward-compatible.

#### AC-0214-074
- **Requirement**: Deprecated extension methods MUST continue to function until the sunset date.
- **Verification**: Call a deprecated extension method before sunset.
- **Expected Result**: Method functions normally.

#### AC-0214-075
- **Requirement**: Extension compatibility MUST be queryable through the registry.
- **Verification**: Query extension compatibility through the registry.
- **Expected Result**: Compatibility information is returned.

### Performance (AC-0214-076 to AC-0214-078)

#### AC-0214-076
- **Requirement**: Extension registration MUST complete within 10 milliseconds per extension.
- **Verification**: Register 1,000 extensions and measure time per extension.
- **Expected Result**: Average registration time is at or below 10 milliseconds.

#### AC-0214-077
- **Requirement**: Extension lookup through the capability manager MUST complete within 1 millisecond.
- **Verification**: Perform 10,000 extension lookups.
- **Expected Result**: Average lookup time is at or below 1 millisecond.

#### AC-0214-078
- **Requirement**: Extension contract validation MUST complete within 100 milliseconds.
- **Verification**: Validate 100 extension contracts.
- **Expected Result**: Validation completes within 100 milliseconds.

### Security (AC-0214-079 to AC-0214-080)

#### AC-0214-079
- **Requirement**: Extension implementations MUST be subject to the same security policies as the host plugin.
- **Verification**: Apply a security policy that restricts extension behavior.
- **Expected Result**: Policy is enforced on the extension.

#### AC-0214-080
- **Requirement**: Extension registration MUST be logged for audit purposes.
- **Verification**: Register an extension and check audit logs.
- **Expected Result**: Registration is logged.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |



## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 28 References

1. RFC 2119: Key Words for Use in RFCs to Indicate Requirement Levels
2. Extension Point Design Pattern: Gamma et al., Design Patterns, Elements of Reusable Object-Oriented Software

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 30 Future Evolution

1. Support for dynamically registered extension points.
2. Extension composition patterns for combining multiple extension implementations.
3. Extension performance profiling and optimization recommendations.
4. Extension sandboxing profiles for untrusted third-party extensions.
5. Extension marketplace integration for public extension distribution.

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All plugin contracts are defined as abstract behavioral interfaces.

---




---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |