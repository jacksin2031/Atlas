# RFC-0323: Workflow Plugin Integration

# RFC-0323: Workflow Plugin Integration
'''
## Header
'''
```
RFC: RFC-0323
Title: Workflow Plugin Integration
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
Related JSON Schema: workflow-resource-types.md
Related Catalog: workflow-resource-types.md
```
'''

## Abstract

This RFC defines the plugin integration framework for Atlas Workflow, specifying how third-party and community plugins are discovered, loaded, validated, and executed within the workflow runtime. The plugin system provides a secure, versioned, and isolated mechanism for extending workflow capabilities beyond the built-in functionality, while maintaining system stability and security.

## Status

This is a Proposed specification. Implementation feedback is encouraged before final adoption.

## Motivation

Atlas Workflow serves diverse deployment scenarios requiring integration with a wide variety of external systems, custom logic, and domain-specific workflows. A plugin integration framework enables:

- Community-contributed connectors and nodes for popular services
- Vendor-specific plugins for proprietary systems
- Custom workflow logic packaged as distributable plugins
- Version-controlled plugin updates without core engine changes
- Secure plugin execution with proper isolation boundaries

Without a formal plugin system, organizations resort to embedding custom code directly in the core engine, creating upgrade incompatibilities and security risks.

## Scope

This RFC covers:

- Plugin package format and structure
- Plugin discovery and registration mechanisms
- Plugin loading, validation, and initialization
- Plugin execution isolation and security
- Plugin version management and upgrade paths
- Plugin dependency resolution
- Plugin lifecycle management within the workflow runtime
- Plugin testing and certification requirements

This RFC does NOT cover:

- Plugin marketplace or distribution platform (future RFC)
- Plugin authoring SDK details (covered by RFC-0322 Extension Points)
- Plugin monetization or licensing (future RFC)
- Plugin store review process (operational concern)

## Terminology

The following terms are defined per RFC-0301 (Workflow Overview) and extended for plugins:

| Term | Definition |
| --- | --- |
| Plugin | A distributable package containing one or more extension point implementations |
| Plugin Package | A versioned, signed archive containing plugin code, metadata, and dependencies |
| Plugin Manifest | A declarative file within the plugin package describing capabilities, dependencies, and permissions |
| Plugin Registry | A centralized or distributed store of available plugins with version information |
| Plugin Loader | Component responsible for loading plugin packages into the workflow runtime |
| Plugin Sandbox | Isolated execution environment for plugin code |
| Plugin Version | Semantic version of a plugin package |
| Plugin Dependency | A required plugin or core component that another plugin relies upon |
| Plugin Capability | A named feature exposed by a plugin (e.g., connector:aws-s3, action:custom-script) |
| Plugin Signature | Cryptographic signature verifying plugin package integrity and origin |
| Plugin Certificate | X.509 certificate used for plugin signing |
| Plugin Trust Chain | The chain of certificates from plugin certificate to root CA |
| Plugin Upgrade | The process of replacing a plugin version with a newer version |
| Plugin Rollback | The process of reverting a plugin to a previous version |
| Plugin Quarantine | Temporary isolation of a plugin suspected of malicious behavior |
| Plugin Health Check | Periodic verification that a plugin is functioning correctly |

## Requirements

### Requirement 1: Plugin Package Format

The implementation MUST define and enforce a standard plugin package format.

The implementation MUST:

- Package plugins as versioned archives containing:
  - plugin.json — Plugin manifest with metadata, capabilities, dependencies, and permissions
  - src/ — Plugin source code or compiled binaries
  - schema/ — JSON Schema definitions for plugin configuration
  - docs/ — Plugin documentation and usage examples
  - 	ests/ — Plugin test suite (for certified plugins)
- Require every plugin manifest to include:
  - 
ame (unique identifier, dot-separated namespace)
  - ersion (semantic version)
  - description (human-readable description)
  - capabilities (list of extension point implementations)
  - dependencies (list of required plugins and minimum versions)
  - permissions (list of required resource access grants)
  - uthor (plugin author or organization)
  - license (plugin license identifier)
  - signature (cryptographic signature of package contents)
- Enforce semantic versioning for plugin releases
- Support plugin packages in both compiled (binary) and interpreted (source) forms

The implementation SHOULD:

- Support plugin package compression (gzip, zstd)
- Provide a plugin package builder CLI tool
- Support plugin package bundling of multiple related capabilities

The implementation MAY:

- Support plugin package streaming installation from remote registries

#### Plugin Package Structure

`mermaid
graph TB
    subgraph Plugin Package
        PJ[plugin.json]
        SRC[src/]
        SCH[schema/]
        DOC[docs/]
        TST[tests/]
        SIG[signature.sig]
    end

    subgraph Capabilities
        C1[Connector: aws-s3]
        C2[Action: custom-script]
        C3[Trigger: webhook]
    end

    PJ --> C1
    PJ --> C2
    PJ --> C3
    SRC --> C1
    SRC --> C2
    SRC --> C3
    SCH --> PJ
`

### Requirement 2: Plugin Discovery and Registration

The implementation MUST provide mechanisms for discovering and registering plugins.

The implementation MUST:

- Scan configured plugin directories for available plugin packages
- Parse plugin manifests to extract capabilities and dependencies
- Register discovered plugins with the Extension Registry (RFC-0322)
- Resolve plugin dependencies before loading
- Detect and report dependency conflicts
- Support both local and remote plugin registries
- Maintain a plugin cache of available versions

The implementation SHOULD:

- Support automatic plugin discovery from environment variables or configuration
- Provide a plugin listing API for operational tooling
- Support plugin version pinning per workflow definition

The implementation MAY:

- Support automatic plugin updates from registered registries

#### Plugin Discovery Flow

`mermaid
sequenceDiagram
    participant Core
    participant Scanner
    participant Resolver
    participant Registry
    participant PluginStore

    Core->>Scanner: DiscoverPlugins(directory_paths)
    Scanner->>PluginStore: ReadPackage(plugin_path)
    PluginStore-->>Scanner: PluginArchive
    Scanner->>Scanner: ParseManifest(plugin.json)
    Scanner->>Resolver: ResolveDependencies(deps)
    Resolver->>PluginStore: LookupDependency(dep_name, dep_version)
    PluginStore-->>Resolver: DependencyFound
    Resolver-->>Scanner: ResolutionResult
    Scanner->>Registry: RegisterPlugin(plugin_info)
    Registry-->>Core: DiscoveryComplete
`

### Requirement 3: Plugin Loading and Validation

The implementation MUST validate plugin packages before loading them into the runtime.

The implementation MUST:

- Verify plugin package signature against trusted certificate authorities
- Validate plugin manifest schema against the plugin manifest JSON Schema
- Check plugin compatibility with the current engine version
- Verify that all required permissions are granted
- Resolve and validate all plugin dependencies
- Load plugin code into an isolated sandbox environment
- Initialize plugins in the correct dependency order
- Report validation errors with specific details (which check failed and why)

The implementation MUST NOT:

- Load plugins with invalid or expired signatures
- Load plugins with unresolved or conflicting dependencies
- Load plugins requesting permissions not granted in the manifest
- Load plugins incompatible with the engine version

The implementation SHOULD:

- Provide a plugin validation report with pass/fail status for each check
- Support dry-run validation without loading the plugin
- Cache validated plugin checksums to speed up subsequent loads

### Requirement 4: Plugin Execution Isolation

The implementation MUST isolate plugin execution from the core engine and other plugins.

The implementation MUST:

- Execute each plugin in an isolated sandbox (process, container, or VM)
- Restrict plugin access to declared permissions only
- Enforce resource limits per plugin (CPU, memory, network, file I/O)
- Prevent plugins from accessing other plugins memory space
- Implement plugin crash containment (plugin crash MUST NOT affect core engine)
- Log all plugin resource access attempts for audit (RFC-0321)

The implementation SHOULD:

- Support adjustable isolation levels based on plugin trust tier
- Provide plugin resource usage metrics
- Implement plugin restart on failure with configurable retry policy

The implementation MAY:

- Support multiple isolation tiers (strict, moderate, relaxed) based on plugin certification level

#### Plugin Isolation Model

`mermaid
graph TB
    subgraph Core Engine
        CE[Core Runtime]
        ER[Extension Registry]
        OBS[Observability]
    end

    subgraph Plugin Sandbox 1
        P1[Plugin A]
        P1A[Action: custom-http]
        P1T[Trigger: webhook]
    end

    subgraph Plugin Sandbox 2
        P2[Plugin B]
        P2A[Action: db-query]
        P2C[Connector: postgres]
    end

    subgraph Plugin Sandbox 3
        P3[Plugin C]
        P3A[Node: ml-inference]
        P3C[Connector: ai-api]
    end

    CE --> ER
    CE --> OBS
    ER --> P1
    ER --> P2
    ER --> P3
    P1 -.sandbox.-> P1A
    P1 -.sandbox.-> P1T
    P2 -.sandbox.-> P2A
    P2 -.sandbox.-> P2C
    P3 -.sandbox.-> P3A
    P3 -.sandbox.-> P3C
`

### Requirement 5: Plugin Version Management

The implementation MUST support plugin version lifecycle management.

The implementation MUST:

- Support multiple plugin versions installed simultaneously (for rollback)
- Enforce plugin version compatibility with the engine version
- Provide plugin upgrade procedure that preserves workflow state
- Support plugin rollback to previous version on upgrade failure
- Track plugin version history with timestamps and change reasons
- Prevent loading of deprecated plugin versions after grace period

The implementation SHOULD:

- Support canary plugin upgrades for risk mitigation
- Provide plugin version comparison reports (what changed between versions)
- Notify operators of upcoming plugin version deprecations

The implementation MAY:

- Support automatic plugin version downgrade on detected compatibility issues

### Requirement 6: Plugin Security Model

The implementation MUST enforce a security model for plugin execution.

The implementation MUST:

- Implement a permission-based access control model for plugins
- Require explicit permission grants for each plugin capability:
  - Network access (outbound, inbound, specific hosts/ports)
  - File system access (read, write, specific paths)
  - Environment variable access (listed variables only)
  - Process execution (whitelisted commands)
  - Memory allocation (limits per plugin)
- Validate plugin code against known malicious patterns during loading
- Quarantine plugins exhibiting anomalous behavior (excessive resource usage, unauthorized access attempts)
- Support plugin revocation without engine restart

The implementation SHOULD:

- Provide a security audit log for all plugin actions
- Support plugin permission scanning during CI/CD
- Implement plugin sandbox escape detection

## Layer Boundaries

### Plugin Layer Responsibilities
- Define and enforce plugin package format and manifest schema
- Discover, validate, and load plugins into the runtime
- Manage plugin lifecycle (install, upgrade, rollback, uninstall)
- Enforce plugin isolation and security boundaries
- Resolve plugin dependencies and version compatibility
- Provide plugin testing and certification infrastructure

### Plugin Layer Non-Responsibilities
- Plugin content development (plugin author responsibility)
- Plugin distribution and marketplace operations
- Plugin pricing and licensing enforcement
- Plugin user authentication (identity management)
- Plugin runtime monitoring (observability layer)

### Dependencies
- Depends on: RFC-0304 (Workflow Runtime), RFC-0322 (Extension Points)
- Depends on: RFC-0312 (Scheduler), RFC-0321 (Observability)
- Provides to: Extension Registry, Workflow Executor
- Consumers: Workflow operator, plugin developer, security auditor
- Providers: Plugin loader, plugin validator, plugin registry

### Forbidden Dependencies
- Plugins MUST NOT depend on core engine internals
- The plugin loader MUST NOT grant permissions not declared in the manifest
- The plugin layer MUST NOT bypass sandbox isolation under any circumstances
- Plugins MUST NOT communicate with other plugins directly (must route through core engine)

## Future Evolution

- **v1.1**: Add plugin dependency graph visualization for conflict analysis
- **v1.2**: Introduce plugin performance profiling and bottleneck detection
- **v1.3**: Add plugin A/B testing framework for gradual rollout
- **v2.0**: Support for plugin marketplace integration with automated distribution
- **v2.0**: Add plugin sandbox hardening (seccomp profiles, AppArmor, SELinux)

## Runtime Independence

This specification is runtime-independent. The plugin system MUST NOT assume:

- Any specific programming language for plugin implementation
- Any specific runtime environment (Electron, Tauri, browser, server)
- Any specific database backend
- Any specific operating system
- Any specific GPU or graphics acceleration
- Any specific threading model

Plugin communication with the core engine MUST use language-neutral protocols (gRPC, HTTP/JSON, or equivalent).


#### Plugin Upgrade and Rollback Flow

`mermaid
sequenceDiagram
    participant Admin
    participant CLI
    participant Loader
    participant Validator
    participant Registry
    participant Sandbox
    participant Backup

    Admin->>CLI: plugin upgrade plugin-name v2.0
    CLI->>Loader: DownloadPackage(plugin-name, v2.0)
    Loader->>Validator: ValidateSignature(package)
    Validator-->>Loader: Valid
    Loader->>Validator: ValidateDependencies(v2.0)
    Validator-->>Loader: Resolved
    Loader->>Backup: CreateSnapshot(plugin-name)
    Backup-->>Loader: SnapshotReady
    Loader->>Registry: Deactivate(plugin-name, v1.0)
    Registry-->>Loader: Deactivated
    Loader->>Sandbox: Initialize(plugin-name, v2.0)
    Sandbox-->>Loader: Ready
    Loader->>Registry: Activate(plugin-name, v2.0)
    Registry-->>Admin: Upgrade Complete

    alt Upgrade Failure
        Loader->>Backup: RestoreSnapshot(plugin-name)
        Backup-->>Loader: Restored
        Loader->>Registry: Activate(plugin-name, v1.0)
        Registry-->>Admin: Rolled Back to v1.0
    end

`
## Acceptance Criteria

1. The implementation MUST enforce the plugin package format defined in Requirement 1.
2. The implementation MUST discover plugins from configured directories and register them with the Extension Registry.
3. The implementation MUST validate plugin signatures, manifests, and dependencies before loading.
4. The implementation MUST isolate plugin execution in a sandbox with enforced resource limits.
5. The implementation MUST support multiple plugin versions simultaneously for rollback capability.
6. The implementation MUST enforce the permission-based access control model for all plugins.
7. The implementation MUST prevent plugin crashes from affecting the core engine.
8. The implementation MUST log all plugin lifecycle events and resource access attempts.
9. The implementation MUST support plugin upgrade and rollback procedures.
10. The implementation MUST reject plugins with invalid signatures or unresolved dependencies.

## References

| Type | Reference | Description |
| --- | --- | --- |
| Related RFC | RFC-0301 | Workflow Overview (Terminology source) |
| Related RFC | RFC-0304 | Workflow Runtime |
| Related RFC | RFC-0312 | Scheduler |
| Related RFC | RFC-0315 | Recovery |
| Related RFC | RFC-0316 | Debugging |
| Related RFC | RFC-0321 | Observability |
| Related RFC | RFC-0322 | Extension Points |
| Related RFC | RFC-0324 | Storage |
| Related RFC | RFC-1003 | Common Capability Model |
| Related ADR | ADR-0012 | Plugin Architecture Decision |
| Related JSON Schema | workflow-resource-types.md | Plugin resource type schema |
| Related Catalog | workflow-resource-types.md | Catalog entry for plugin resources |
| See Also | OSGi Spec | Plugin module system reference |
| See Also | NPM Security | Plugin supply chain security reference |
