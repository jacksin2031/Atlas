# Plugin Extension Points Catalog

## 1. Purpose

This catalog defines the canonical set of extension point categories that plugins MAY implement to contribute functionality to the Atlas ecosystem. Each extension point specifies a contract that implementing plugins MUST fulfill and a discovery mechanism through which consumers MAY locate implementations.

## 2. Stable ID Prefix

All extension point identifiers use the prefix `PEXT-`. This prefix is reserved exclusively for plugin extension point definitions within the Atlas ecosystem.

## 3. Naming Convention

Extension point identifiers MUST conform to the pattern `PEXT-<CATEGORY>-<ROLE>` where `<CATEGORY>` denotes the functional domain and `<ROLE>` denotes the specific contribution type within that domain. Both segments MUST use uppercase ASCII letters and hyphens.

## 4. Canonical Extension Point Table

| Stable ID | Name | Contribution Type | Contract Scope |
|---|---|---|---|
| `PEXT-SERVICE` | Service | Provides a reusable service implementation | Defines service interface, lifecycle methods, configuration requirements, and availability guarantees. |
| `PEXT-WORKFLOW-NODE` | Workflow Node | Adds a discrete step to a workflow execution graph | Defines node inputs, outputs, execution behavior, error handling, and retry semantics. |
| `PEXT-UI-COMPONENT` | UI Component | Supplies a visual element rendered in the Atlas user interface | Defines component markup, styling requirements, data binding contracts, and accessibility obligations. |
| `PEXT-COMMAND` | Command | Registers a callable command accessible through the CLI or API | Defines command name, arguments, flags, help text, execution behavior, and output format. |
| `PEXT-PROVIDER` | Provider | Supplies data, resources, or connectivity to external systems | Defines connection parameters, data schema, refresh policies, and failure recovery behavior. |
| `PEXT-AI-ADAPTER` | AI Adapter | Integrates an artificial intelligence model or inference service | Defines model interface, input/output schemas, temperature and parameter controls, and rate limiting. |
| `PEXT-VISION-PROCESSOR` | Vision Processor | Performs visual analysis, recognition, or image processing | Defines input format expectations, output annotation schemas, processing pipelines, and accuracy guarantees. |
| `PEXT-STORAGE-PROVIDER` | Storage Provider | Manages persistent data storage operations | Defines CRUD operations, query capabilities, transaction semantics, data retention policies, and encryption requirements. |
| `PEXT-IPC-PROVIDER` | IPC Provider | Enables inter-process communication between plugin hosts and external processes | Defines message formats, transport protocols, serialization schemes, and security boundaries. |
| `PEXT-EVENT-HANDLER` | Event Handler | Responds to system or plugin events with custom logic | Defines subscribed event types, handler execution order, idempotency requirements, and error propagation. |
| `PEXT-MIDDLEWARE` | Middleware | Intercepts and transforms requests or events flowing through the pipeline | Defines intercept position, transformation logic, header injection, and filtering criteria. |
| `PEXT-HOOK` | Hook | Inserts custom logic at predefined lifecycle or operational junctures | Defines hook point, execution timing (before/after/skip), parameter access, and cancellation capabilities. |
| `PEXT-CONFIGURATOR` | Configurator | Provides a configuration interface or migration logic for plugin settings | Defines configuration schema, default values, migration paths, validation rules, and hot-reload support. |
| `PEXT-VALIDATOR` | Validator | Enforces business rules, schema constraints, or policy checks on data | Defines validation rules, error message formats, severity levels, and bypass conditions. |
| `PEXT-TRANSFORMER` | Transformer | Converts data between formats, schemas, or representations | Defines input schema, output schema, transformation logic, loss guarantees, and encoding requirements. |

## 5. Extension Point Registration Rules

1. A plugin MUST declare every extension point it implements in its manifest under the `extension_points` field.
2. A plugin MUST implement all methods and fulfill all contractual obligations defined for each registered extension point.
3. A plugin MUST NOT implement more than one extension point of the same category that serves the identical consumer role.
4. When multiple plugins implement the same extension point category, the `PEXT-EVENT-HANDLER` execution order MUST be determined by the `priority` field in the manifest, with lower numeric values executing first.
5. Extension point implementations MUST be discoverable through the `PIF-CAPABILITY-MANAGER` after the plugin reaches the `PSTATE-ACTIVE` state.

## 6. Extension Point Lifecycle Rules

1. Extension point implementations MUST be registered with the `PIF-EXTENSION-REGISTRAR` during the `PSTATE-INITIALIZING` phase.
2. Extension point implementations MUST be unregistered during the `PSTATE-DEACTIVATING` phase.
3. Extension point implementations MUST be thread-safe for concurrent access unless explicitly documented as single-threaded.
4. Extension point implementations MUST NOT hold persistent locks across lifecycle transitions.
5. Extension point implementations MUST support graceful shutdown without data corruption.

## 7. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin Manifest Specification: Defines the `extension_points` field schema.
- Atlas Plugin Capability Specification: Defines how extension points are discovered and resolved by consumers.

## 8. Usage Guidelines

Plugin authors SHOULD select the most specific extension point category that matches their contribution; generic `PEXT-SERVICE` implementations SHOULD be reserved for contributions that do not fit any other category. Consumers MUST query the `PIF-EXTENSION-REGISTRAR` for available implementations rather than assuming their presence. Extension point contracts MUST be versioned independently of the plugin version to enable partial upgrades. New extension point categories MUST be proposed through the catalog governance process before being adopted in production environments.
