RFC: RFC-0323
Title: Workflow Plugin Integration
Status: Proposed
Version: 1.1.0
Author: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADR References:
  - ADR-0012 Contract-First Specification-Driven Development`nRelated ADR: ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/performance-metric.json
  - schemas/workflow/sla-definition.json
Related Catalog:
  - catalog/workflow-metrics.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

---

---

## Authority

This RFC is the authoritative specification for the RFC 0323 workflow plugin integration.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.



This RFC is the authoritative specification for the RFC 0323 workflow plugin integration.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## Normative Status
This specification is normative. Every implementation MUST conform to the requirements defined herein.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Plugin | A self-contained unit of workflow functionality that extends the Atlas system. | RFC-0323 |
| Plugin Package | A distributable archive containing plugin code, manifest, and dependencies. | RFC-0323 |
| Plugin Discovery | The process of finding and registering available plugins. | RFC-0323 |
| Plugin Isolation | The enforcement of boundaries between plugins and the host system. | RFC-0323 |
| Plugin Lifecycle | The stages a plugin goes through from installation to uninstallation. | RFC-0323 |

## 2 Layer Boundaries

## 3 Security
- Plugins MUST operate within sandbox boundaries per RFC-0319.
- Plugin installation MUST require administrative permissions.
- Plugin communication MUST be authenticated and encrypted.

## 4 Performance
- Plugin loading MUST complete within 500ms.
- Plugin-to-plugin communication MUST add less than 1ms overhead.

## 5 Compatibility
- Plugin interfaces MUST be versioned per RFC-0329.
- Breaking plugin interface changes MUST require a new major version.

## 6 Compliance
- All plugin installations MUST be recorded in the audit trail per RFC-0321.

## 7 Future Evolution
- **Plugin Store Integration**: Direct plugin installation from a centralized marketplace.
- **Plugin Dependency Resolution**: Automatic resolution of plugin-to-plugin dependencies.
- **Plugin Hot Reload**: Runtime plugin updates without workflow restart.
- **Plugin Signature Verification**: Cryptographic verification of plugin authenticity.

## 8 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

## 9 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0304 | Workflow Runtime (plugin hosting) |
| RFC-0309 | Workflow Actions (action plugins) |
| RFC-0311 | Workflow Triggers (trigger plugins) |
| RFC-0312 | Workflow Scheduler (scheduler plugins) |
| RFC-0317 | Workflow Validation (plugin manifest validation) |
| RFC-0319 | Workflow Security (plugin sandboxing) |
| RFC-0320 | Workflow Performance (plugin performance) |
| RFC-0321 | Workflow Observability (plugin telemetry) |
| RFC-0322 | Workflow Extension (plugin extension integration) |
| RFC-0324 | Workflow Storage (plugin persistence) |
| RFC-0329 | Workflow Compatibility (plugin compatibility) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/plugin-package.json | Plugin Package JSON Schema |
| catalog/workflow-capabilities.md | Capabilities Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0323 (this document), RFC-0322 (Extension), RFC-0319 (Security) |
---


## 10 Plugin Architecture

This section defines the plugin integration architecture for the workflow system.

### 10.1 Plugin Package Structure

Every plugin package MUST conform to the following structure:

`
plugin-package/
├── manifest.json          # Required: Plugin manifest
├── README.md              # Recommended: Plugin documentation
├── plugins/               # Required: Plugin code directory
│   ├── <plugin-name>/     # Per-plugin subdirectory
│   │   ├── index.js       # Entry point (language-agnostic)
│   │   └── ...            # Plugin dependencies
├── schemas/               # Optional: Plugin-defined schemas
│   └── *.json
├── assets/                # Optional: Plugin resources
│   └── ...
└── .signature             # Optional: Cryptographic signature
`

The manifest MUST contain: 
ame, ersion, description, license, tlas_version, entry_point, permissions, extensions, dependencies, hooks.

### 10.2 Plugin Discovery Protocol

Plugins are discovered through the following protocol:

1. **Scan**: The runtime scans configured plugin directories for manifest.json files.
2. **Parse**: Each manifest is parsed and validated against the plugin package schema.
3. **Resolve**: Dependencies are resolved transitively. Circular dependencies are rejected.
4. **Validate**: Permission requirements are checked against the host's security policy.
5. **Register**: Valid plugins are registered with the extension point system (RFC-0322).
6. **Index**: Discovered plugins are indexed for the plugin catalog.

Discovery MUST complete within 5 seconds for a plugin with up to 50 transitive dependencies.

### 10.3 Plugin Isolation Model

Plugins operate within isolation boundaries defined by their declared permissions:

| Permission Class | File System | Network | Secrets | Environment |
|---|---|---|---|---|
| Read-Only | Read mounted volumes | Outbound deny | None | Read-only |
| Read-Write | Read/write mounted volumes | Outbound deny | None | Read-write |
| Network-Enabled | Read mounted volumes | Configurable outbound | Declared | Read-only |
| Full | Full access | Full access | All | Full |
| Kernel | Full access | Full access | All | Full |

Isolation is enforced at the runtime level. A plugin requesting permissions greater than its declared class MUST be rejected.

### 10.4 Plugin Lifecycle

The plugin lifecycle follows these states:

`
Discovered → Installed → Validated → Loaded → Active → (Paused → Stopped → Uninstalled)
                                       ↕
                                    Error → (Repairing → Loaded)
`

- **Discovered**: Manifest found, not yet processed.
- **Installed**: Package extracted and manifest parsed.
- **Validated**: Permissions and dependencies verified.
- **Loaded**: Code loaded into isolation boundary.
- **Active**: Plugin operational.
- **Paused**: Plugin suspended, not processing events.
- **Stopped**: Plugin unloaded from memory, package retained.
- **Uninstalled**: Package removed.
- **Error**: Plugin failed in any state.

Transitions from Error to Loaded MUST require explicit administrator action.

### 10.5 Plugin Communication Model

Plugins communicate through the following channels:

| Channel | Direction | Latency | Ordering | Use Case |
|---|---|---|---|---|
| Event Bus | Pub/Sub | < 10ms | Per-topic FIFO | Workflow events |
| RPC | Request/Reply | < 1ms | FIFO | Plugin-to-plugin |
| Shared State | Read/Write | < 100μs | None | Cache, counters |
| Hooks | Callback | < 1ms | Ordered | Lifecycle events |
| Stream | Push | < 5ms | Ordered | Telemetry, logs |

All inter-plugin communication MUST be mediated by the runtime. Direct memory access between plugins is forbidden.

### 10.6 Plugin Dependency Resolution

Plugin dependencies are resolved using a directed acyclic graph (DAG):

- Each plugin declares required plugins with minimum version constraints.
- Dependencies are resolved transitively.
- Circular dependencies are rejected during the Validated stage.
- Version conflicts are resolved by selecting the highest compatible version.
- Unresolvable dependencies cause plugin installation to fail.

### 10.7 Plugin Manifest Schema

The plugin manifest MUST conform to the following schema:

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | Yes | Plugin identifier (dot-notation) |
| version | semver | Yes | Plugin version |
| description | string | Yes | Human-readable description |
| license | string | Yes | SPDX license identifier |
| atlas_version | semver_range | Yes | Compatible Atlas versions |
| entry_point | string | Yes | Path to plugin code entry point |
| permissions | permission_class | Yes | Required permission class |
| extensions | extension_ref[] | No | Extension points provided |
| dependencies | dependency[] | No | Required plugins |
| hooks | hook_definition[] | No | Lifecycle hooks |
| metadata | object | No | Custom metadata |

### 10.8 Plugin Security Model

Plugins MUST adhere to the security model defined in RFC-0319:

- Plugins MUST declare their permission class in the manifest.
- The runtime MUST enforce declared permissions at runtime.
- Plugins requesting elevated permissions MUST undergo additional validation.
- Plugin code signatures MUST be verified if the plugin store requires signing.
- Plugin communication channels MUST be authenticated.
- Plugin data access MUST be audited per RFC-0321.

## 11 Acceptance Criteria

### 11.1 Plugin Package Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Every plugin package MUST contain a manifest.json with all ten (10) required fields from Section 10.7. | Schema test: Parse manifest of valid plugin → Verify all required fields present with correct types |
| AC-02 | Plugin discovery MUST scan configured directories and parse all manifest.json files found. | Discovery test: Place 5 valid plugins in scan directory → Verify all 5 discovered and registered |
| AC-03 | Circular plugin dependencies MUST be rejected during the Validated stage. | Cycle test: Create two plugins with mutual dependencies → Verify installation fails at Validated stage with cycle error |

### 11.2 Isolation Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-04 | Five (5) permission classes (Read-Only, Read-Write, Network-Enabled, Full, Kernel) MUST be supported. | Class enumeration test: Register plugins with each class → Verify each class enforces correct access boundaries |
| AC-05 | Plugins requesting permissions exceeding their declared class MUST be rejected. | Escalation test: Plugin manifest declares Read-Only but code attempts network access → Verify runtime blocks and logs violation |
| AC-06 | Direct memory access between plugins MUST be forbidden. | Memory isolation test: Plugin A attempts to read Plugin B's heap → Verify access denied |

### 11.3 Lifecycle Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-07 | Plugin lifecycle MUST follow the state machine: Discovered → Installed → Validated → Loaded → Active. | State test: Monitor plugin from discovery → Verify all five states traversed in order |
| AC-08 | Plugins in Error state MUST require explicit administrator action to return to Loaded. | Error recovery test: Induce error → Verify plugin stuck in Error → Call admin repair → Verify transition to Loaded |
| AC-09 | Plugin discovery MUST complete within 5 seconds for up to 50 transitive dependencies. | Timing test: Install plugin with 50 dependencies → Measure discovery time → Verify ≤ 5 seconds |

### 11.4 Communication Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-10 | All five communication channels (Event Bus, RPC, Shared State, Hooks, Stream) MUST be available. | Channel test: Exercise each channel between two plugins → Verify data transfer succeeds with expected latency |
| AC-11 | Inter-plugin communication MUST be mediated by the runtime. No direct plugin-to-plugin channels allowed. | Mediation test: Intercept all plugin network activity → Verify all communication passes through runtime mediation layer |## Revision History

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


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |