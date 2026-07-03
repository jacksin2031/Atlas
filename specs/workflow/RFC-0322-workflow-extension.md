# RFC-0322: Workflow Extension Points

# RFC-0322: Workflow Extension Points
'''
## Header
'''
```
RFC: RFC-0322
Title: Workflow Extension Points
Status: Proposed
Version: 1.0.0
Author: Atlas Specification Committee
Created: 2026-07-01
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
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0312 Scheduler
  - RFC-0315 Recovery
  - RFC-0316 Debugging
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1006 Common Error Model
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01
Related ADR: ADR-0012
Related JSON Schema: workflow-extension-points.md
Related Catalog: workflow-extension-points.md
```
'''

## Abstract

This RFC defines the extension point architecture for Atlas Workflow, enabling third-party developers to extend the workflow engine with custom nodes, triggers, actions, conditions, and scheduler plugins. The extension system provides a pluggable interface that maintains backward compatibility while allowing the workflow runtime to be customized without modifying core code.

## Status

This is a Proposed specification. Implementation feedback is encouraged before final adoption.

## Motivation

Atlas Workflow must support extensibility for diverse use cases without requiring modifications to the core engine. Organizations need to:

- Integrate with proprietary or internal systems not covered by built-in connectors
- Implement domain-specific workflow steps with custom logic
- Extend trigger mechanisms beyond the built-in event-based and cron-based triggers
- Add custom condition evaluators for business-rule-based branching
- Customize scheduling behavior for specialized workload management
- Maintain compatibility across workflow engine upgrades

Without a formal extension architecture, organizations face a fork-and-modify approach that creates maintenance burden and blocks upgrade paths.

## Scope

This RFC covers:

- Extension point interface definitions for nodes, triggers, actions, conditions, and schedulers
- Extension registration and lifecycle management
- Extension sandboxing and security model
- Extension API versioning and compatibility guarantees
- Third-party extension distribution and discovery
- Extension testing and validation framework

This RFC does NOT cover:

- Built-in node implementations (covered by RFC-0309 Actions)
- Built-in trigger implementations (covered by RFC-0311 Triggers)
- Built-in condition implementations (covered by RFC-0310 Conditions)
- Plugin binary format (covered by RFC-0323 Plugin Integration)
- Extension marketplace or store (future RFC)

## Terminology

The following terms are defined per RFC-0301 (Workflow Overview) and extended for extensions:

| Term | Definition |
| --- | --- |
| Extension Point | A well-defined interface that third-party code can implement to extend workflow behavior |
| Extension | A package containing one or more extension point implementations |
| Extension Registry | A lookup service that maps extension point identifiers to registered implementations |
| Extension Manifest | Metadata describing an extension package, including capabilities, dependencies, and version |
| Extension Loader | Component responsible for loading extension packages at runtime |
| Extension Sandbox | Isolated execution environment for untrusted extensions |
| Extension Context | Runtime information available to an extension during execution (workflow state, inputs, outputs) |
| Extension Lifecycle Hook | Callback invoked at specific points in extension lifetime (initialize, execute, teardown) |
| Extension Version | Semantic version of an extension package, used for compatibility checking |
| Extension Capability | A named feature that an extension provides (e.g., custom-node, custom-trigger) |
| Extension Dependency | A required extension or core component that another extension relies upon |
| Extension Interface | The contract between the core engine and an extension implementation |
| Extension Resolver | Component that resolves extension dependencies and determines load order |
| Extension Validator | Component that validates extension packages before loading |
| Extension Registry Entry | A single registration of an extension implementation for a specific extension point |

## Requirements

### Requirement 1: Extension Point Interfaces

The implementation MUST define extension point interfaces for all extensible workflow components.

The implementation MUST provide the following extension point interfaces:

**Custom Node Extension Point:**
- Interface: INodeExtension
- Methods: execute(context: ExtensionContext) -> NodeResult
- Lifecycle hooks: initialize(config: ExtensionConfig), shutdown()
- Input: workflow step inputs via ExtensionContext
- Output: NodeResult with status, outputs, and error information
- The interface MUST support synchronous and asynchronous execution modes

**Custom Trigger Extension Point:**
- Interface: ITriggerExtension
- Methods: 
egister(registry: TriggerRegistry), unregister()
- Lifecycle hooks: initialize(config: ExtensionConfig), start(), stop()
- Must be able to subscribe to external event sources
- Must be able to emit workflow trigger events
- The interface MUST support both polling and event-driven trigger models

**Custom Action Extension Point:**
- Interface: IActionExtension
- Methods: execute(context: ExtensionContext, params: ActionParameters) -> ActionResult
- Lifecycle hooks: initialize(config: ExtensionConfig), alidate(params: ActionParameters) -> ValidationResult
- Must be able to invoke external APIs, services, or systems
- Must support parameter validation and type coercion
- The interface MUST provide access to connector infrastructure

**Custom Condition Extension Point:**
- Interface: IConditionExtension
- Methods: evaluate(context: ExtensionContext, params: ConditionParameters) -> bool
- Lifecycle hooks: initialize(config: ExtensionConfig)
- Must receive workflow state and step inputs for evaluation
- Must return boolean result with optional diagnostic information
- The interface MUST support lazy evaluation for complex conditions

**Custom Scheduler Extension Point:**
- Interface: ISchedulerExtension
- Methods: schedule(workflow: WorkflowDefinition) -> ScheduledExecution, cancel(execution_id: str) -> bool
- Lifecycle hooks: initialize(config: ExtensionConfig), start(), stop()
- Must integrate with the core scheduler (RFC-0312)
- Must support custom scheduling policies (priority, affinity, constraints)
- The interface MUST provide visibility into scheduler queue state

The implementation SHOULD:

- Define extension point interfaces in a language-neutral IDL (Interface Definition Language)
- Provide stub generators for common languages (TypeScript, Python, Go, Rust)
- Document parameter types, return types, and error contracts for each interface method

### Requirement 2: Extension Registration

The implementation MUST provide a registration mechanism for extension point implementations.

The implementation MUST:

- Maintain an Extension Registry that maps extension point identifiers to registered implementations
- Support registration by extension manifest during initialization
- Support dynamic registration and deregistration at runtime
- Assign a unique extension ID to each registered extension implementation
- Enforce uniqueness of extension point + extension capability combinations
- Provide lookup methods: get(id), list(point_type), ind(capability)
- Support extension priority ordering for competing implementations

The implementation SHOULD:

- Support extension registration via configuration files
- Support extension registration via API calls from other extensions
- Provide extension registration events for lifecycle observers

The implementation MAY:

- Support hot-reloading of extensions without restarting the workflow engine
- Allow extensions to register themselves during initialization

#### Extension Registration Flow

`mermaid
sequenceDiagram
    participant Core
    participant Loader
    participant Validator
    participant Registry
    participant Extension

    Core->>Loader: LoadExtension(package_path)
    Loader->>Validator: ValidateManifest(manifest)
    Validator-->>Loader: ValidationResult
    Loader->>Extension: Initialize(config)
    Extension->>Registry: Register(point_id, impl)
    Registry-->>Extension: RegistrationConfirmed
    Extension->>Registry: RegisterCapability(capability)
    Registry-->>Core: ExtensionReady
`

### Requirement 3: Extension Lifecycle Management

The implementation MUST manage the lifecycle of all loaded extensions.

The implementation MUST:

- Call initialize(config) on extension load, before any other method
- Call start() on extension activation (scheduler extensions, trigger extensions)
- Call execute() or equivalent on extension activation (action, node, condition extensions)
- Call stop() on extension deactivation
- Call shutdown() on extension unload
- Ensure lifecycle hooks are called in the correct order
- Handle lifecycle hook failures gracefully without crashing the core engine
- Log lifecycle transitions for audit purposes (RFC-0321)

The implementation SHOULD:

- Support graceful shutdown with configurable timeout
- Implement health checks for active extensions
- Provide extension lifecycle metrics (load time, startup time, execution count)

The implementation MAY:

- Support extension version migration hooks for breaking changes

### Requirement 4: Extension Sandboxing and Security

The implementation MUST provide security boundaries for extension execution.

The implementation MUST:

- Isolate extension execution from the core engine memory space
- Restrict extension access to file system, network, and system resources via configurable policy
- Implement permission grants per extension, declared in the extension manifest
- Validate extension package integrity using cryptographic signatures
- Enforce extension resource limits (CPU, memory, execution time)
- Reject unsigned extensions in production environments (configurable for development)

The implementation SHOULD:

- Provide a default-deny security policy for extensions
- Support per-extension resource quotas
- Implement extension crash recovery (restart sandbox on failure)

The implementation MAY:

- Support multiple sandbox isolation levels (process, container, VM)
- Provide extension security audit logs

### Requirement 5: Extension API Versioning

The implementation MUST guarantee backward compatibility for extension APIs.

The implementation MUST:

- Use semantic versioning (SemVer) for extension interface versions
- Support at least the last two major extension interface versions simultaneously
- Reject extensions requesting unsupported interface versions at load time
- Provide deprecation warnings for interface versions entering deprecation cycle
- Document breaking changes in extension interface changelog

The implementation SHOULD:

- Provide migration guides for deprecated interface versions
- Support extension interface version negotiation during registration

### Requirement 6: Extension Testing Framework

The implementation MUST provide a testing framework for extension development.

The implementation MUST:

- Provide unit test harness for each extension point interface
- Provide integration test fixtures simulating workflow execution context
- Support mock objects for workflow engine, connectors, and external services
- Include test assertions for extension lifecycle compliance
- Provide test coverage reporting for extension code

The implementation SHOULD:

- Include extension validation in CI/CD pipeline
- Support extension contract testing against core engine interfaces

## Layer Boundaries

### Extension Layer Responsibilities
- Define and maintain extension point interfaces
- Manage extension registration, lifecycle, and discovery
- Enforce extension security boundaries and resource limits
- Provide extension testing framework and validation tools
- Handle extension API versioning and compatibility

### Extension Layer Non-Responsibilities
- Implement specific extension logic (extension author responsibility)
- Deploy or distribute extensions (packaging concern)
- Authenticate extension authors (identity management)
- Monitor extension runtime performance (observability layer)
- Define built-in workflow components (core engine)

### Dependencies
- Depends on: RFC-0304 (Workflow Runtime), RFC-0312 (Scheduler), RFC-0309 (Actions), RFC-0310 (Conditions), RFC-0311 (Triggers)
- Depends on: RFC-0321 (Observability), RFC-0323 (Plugin Integration)
- Provides to: None (extensions are consumed by core engine)
- Consumers: Third-party developers, internal extension teams
- Providers: Extension loader, extension validator, extension registry

### Forbidden Dependencies
- Extensions MUST NOT depend on internal core engine modules
- Extensions MUST NOT import the core engine package directly
- Extensions MUST NOT access the extension registry through internal APIs
- The extension layer MUST NOT depend on any specific extension implementation

## Future Evolution

- **v1.1**: Add extension marketplace integration for discovery and distribution
- **v1.2**: Support for extension composition (combining multiple extensions into composite extensions)
- **v1.3**: Add extension hot-reload with zero-downtime deployment
- **v2.0**: Support for extension version pinning per workflow definition
- **v2.0**: Add extension dependency graph analysis for conflict detection

## Runtime Independence

This specification is runtime-independent. The extension architecture MUST NOT assume:

- Any specific programming language for extension implementation
- Any specific runtime environment (Electron, Tauri, browser, server)
- Any specific database backend
- Any specific operating system
- Any specific GPU or graphics acceleration
- Any specific threading model

Extensions MUST communicate with the core engine through language-neutral interface contracts (IDL-generated stubs, gRPC, or equivalent).


#### Extension Interface Contract

`mermaid
classDiagram
    class INodeExtension {
        <<interface>>
        +execute(context) NodeResult
        +initialize(config) void
        +shutdown() void
    }

    class ITriggerExtension {
        <<interface>>
        +register(registry) void
        +unregister() void
        +initialize(config) void
        +start() void
        +stop() void
    }

    class IActionExtension {
        <<interface>>
        +execute(context, params) ActionResult
        +initialize(config) void
        +validate(params) ValidationResult
    }

    class IConditionExtension {
        <<interface>>
        +evaluate(context, params) bool
        +initialize(config) void
    }

    class ISchedulerExtension {
        <<interface>>
        +schedule(workflow) ScheduledExecution
        +cancel(execution_id) bool
        +initialize(config) void
        +start() void
        +stop() void
    }

    class ExtensionContext {
        +workflow_id: string
        +step_id: string
        +inputs: Map
        +outputs: Map
        +metadata: Map
    }

    class ExtensionConfig {
        +parameters: Map
        +credentials: SecretRef
        +timeout: Duration
    }

    INodeExtension --> ExtensionContext
    IActionExtension --> ExtensionContext
    IActionExtension --> ExtensionConfig
    IConditionExtension --> ExtensionContext
    ITriggerExtension --> ExtensionConfig
    ISchedulerExtension --> ExtensionConfig

`

#### Extension Version Compatibility

`mermaid
graph TB
    subgraph Engine v1.0
        EI1[Extension Interface v1.0]
    end

    subgraph Engine v1.1
        EI2[Extension Interface v1.0]
        EI3[Extension Interface v1.1]
    end

    subgraph Engine v2.0
        EI4[Extension Interface v1.0]
        EI5[Extension Interface v1.1]
        EI6[Extension Interface v2.0]
    end

    subgraph Extensions
        Ext1[Plugin A v1.0 - IF v1.0]
        Ext2[Plugin B v1.0 - IF v1.1]
        Ext3[Plugin C v1.0 - IF v2.0]
        Ext4[Plugin D v2.0 - IF v2.0]
    end

    EI1 --> Ext1
    EI2 --> Ext1
    EI3 --> Ext2
    EI4 --> Ext1
    EI5 --> Ext2
    EI6 --> Ext3
    EI6 --> Ext4

`
## Acceptance Criteria

1. The implementation MUST provide extension point interfaces for nodes, triggers, actions, conditions, and schedulers.
2. The implementation MUST register all extensions through the Extension Registry before they can be invoked.
3. The implementation MUST enforce extension lifecycle hooks in the correct order.
4. The implementation MUST isolate extension execution from the core engine memory space.
5. The implementation MUST validate extension package integrity before loading.
6. The implementation MUST reject extensions requesting unsupported interface versions.
7. The implementation MUST provide a testing framework with unit and integration test fixtures for each extension point.
8. The implementation MUST NOT allow extensions to access internal core engine modules.
9. The implementation MUST log all extension lifecycle transitions.
10. The implementation MUST support at least the last two major extension interface versions simultaneously.

## References

| Type | Reference | Description |
| --- | --- | --- |
| Related RFC | RFC-0301 | Workflow Overview (Terminology source) |
| Related RFC | RFC-0304 | Workflow Runtime |
| Related RFC | RFC-0309 | Actions |
| Related RFC | RFC-0310 | Conditions |
| Related RFC | RFC-0311 | Triggers |
| Related RFC | RFC-0312 | Scheduler |
| Related RFC | RFC-0315 | Recovery |
| Related RFC | RFC-0316 | Debugging |
| Related RFC | RFC-0321 | Observability |
| Related RFC | RFC-0323 | Plugin Integration |
| Related RFC | RFC-1003 | Common Capability Model |
| Related ADR | ADR-0012 | Extension Architecture Decision |
| Related JSON Schema | workflow-extension-points.md | Extension point configuration schema |
| Related Catalog | workflow-extension-points.md | Catalog entry for extension points |
| See Also | OSGi Spec | Extension module system reference |
| See Also | SemVer 2.0 | https://semver.org/ |
