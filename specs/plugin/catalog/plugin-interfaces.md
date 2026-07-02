# Plugin Interfaces Catalog

## 1. Purpose

This catalog defines the canonical set of plugin subsystem interfaces that govern the contract between the Atlas Plugin runtime and its internal components. Each interface represents a distinct responsibility boundary and MUST be implemented in full by any component claiming compliance.

## 2. Stable ID Prefix

All interface identifiers use the prefix `PIF-`. This prefix is reserved exclusively for plugin subsystem interface definitions within the Atlas ecosystem.

## 3. Naming Convention

Interface identifiers MUST conform to the pattern `PIF-<CATEGORY>-<ROLE>` where `<CATEGORY>` denotes the functional domain and `<ROLE>` denotes the specific responsibility within that domain. Both segments MUST use uppercase ASCII letters and hyphens.

## 4. Canonical Interface Table

| Stable ID | Name | Responsibility |
|---|---|---|
| `PIF-MANIFEST-VALIDATOR` | Manifest Validator | Validates plugin manifests against the schema specification, enforces structural constraints, verifies integrity hashes, and rejects manifests that violate policy rules. |
| `PIF-LOADER` | Loader | Resolves plugin binaries from registered sources, loads them into the execution environment, manages memory allocation for plugin instances, and handles unloading. |
| `PIF-REGISTRY` | Registry | Maintains the authoritative inventory of all known plugins, records plugin metadata, supports query operations, and persists state across restarts. |
| `PIF-LIFECYCLE-MANAGER` | Lifecycle Manager | Orchestrates state transitions across all plugin instances, enforces the state machine rules, coordinates startup and shutdown sequences, and handles error recovery. |
| `PIF-CAPABILITY-MANAGER` | Capability Manager | Registers, discovers, and resolves plugin capabilities; maintains capability-to-consumer mappings; enforces capability access controls. |
| `PIF-SECURITY-GATE` | Security Gate | Enforces security policies at plugin load time and runtime, validates trust levels, applies sandbox boundaries, and blocks unauthorized operations. |
| `PIF-SANDBOX-MANAGER` | Sandbox Manager | Creates and manages execution sandboxes for untrusted plugins, enforces resource quotas, isolates file system and network access, and monitors sandbox violations. |
| `PIF-DEPENDENCY-RESOLVER` | Dependency Resolver | Computes dependency graphs, detects cycles, resolves version constraints, evaluates compatibility matrices, and determines safe load orders. |
| `PIF-EVENT-BUS` | Event Bus | Routes lifecycle events, capability events, and plugin-to-plugin communication events; guarantees delivery semantics as specified by the event contract. |
| `PIF-API-PROVIDER` | API Provider | Exposes the plugin subsystem API to external consumers; manages API versioning; enforces rate limits and authentication for API access. |
| `PIF-EXTENSION-REGISTRAR` | Extension Registrar | Manages the registration, lookup, and lifecycle of extension point implementations; coordinates extension activation and deactivation. |
| `PIF-MARKETPLACE-CLIENT` | Marketplace Client | Communicates with external marketplace services; handles plugin discovery, download, update checks, and license verification through marketplace endpoints. |
| `PIF-OBSERVABILITY` | Observability | Collects, aggregates, and exports telemetry data including metrics, logs, and traces; provides health check endpoints and diagnostic information. |
| `PIF-VERSION-COMPATIBILITY` | Version Compatibility | Evaluates version constraints between plugins and the runtime; determines forward and backward compatibility; enforces compatibility matrix policies. |

## 5. Interface Compliance Requirements

Any component implementing a registered interface MUST satisfy the following requirements:

1. An implementation MUST expose all methods defined in the interface contract without omission.
2. An implementation MUST handle all error conditions specified in the interface contract and MUST NOT suppress errors silently.
3. An implementation MUST be thread-safe or MUST explicitly document its concurrency model and enforce appropriate synchronization.
4. An implementation MUST NOT introduce side effects beyond those specified in the interface contract.
5. An implementation MUST log all error conditions at the appropriate severity level through the observability layer.
6. An implementation MUST support graceful degradation or explicit failure when underlying dependencies are unavailable.

## 6. Interface Composition Rules

1. The `PIF-LIFECYCLE-MANAGER` MUST depend on `PIF-REGISTRY` for state persistence and on `PIF-EVENT-BUS` for broadcasting transitions.
2. The `PIF-LOADER` MUST invoke `PIF-MANIFEST-VALIDATOR` before loading any plugin binary.
3. The `PIF-SECURITY-GATE` MUST be consulted by `PIF-LOADER` before loading any plugin into memory.
4. The `PIF-DEPENDENCY-RESOLVER` MUST be invoked by `PIF-LIFECYCLE-MANAGER` before initiating any activation sequence.
5. The `PIF-SANDBOX-MANAGER` MUST be invoked by `PIF-SECURITY-GATE` when enforcing sandbox boundaries for plugins at or below the enterprise-approved trust level.
6. The `PIF-CAPABILITY-MANAGER` MUST coordinate with `PIF-EXTENSION-REGISTRAR` when activating or deactivating extension point implementations.
7. The `PIF-VERSION-COMPATIBILITY` MUST be consulted by `PIF-DEPENDENCY-RESOLVER` when evaluating version constraints.

## 7. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin Manifest Specification: Defines the schema that `PIF-MANIFEST-VALIDATOR` enforces.
- Atlas Plugin Lifecycle Specification: Defines the state transitions coordinated by `PIF-LIFECYCLE-MANAGER`.
- Atlas Plugin Trust Model: Defines the trust evaluation performed by `PIF-SECURITY-GATE`.

## 8. Usage Guidelines

Plugin runtime implementations MUST register each interface implementation with the `PIF-REGISTRY` before beginning any lifecycle operations. Components MUST acquire interface references through the registry rather than through direct instantiation. Interface implementations MUST be replaceable at runtime to support hot-reload scenarios. Any new interface MUST receive a unique stable ID and MUST be documented in this catalog before being used in production.
