RFC: RFC-0322
Title: Workflow Extension
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

This RFC is the authoritative specification for the RFC 0322 workflow extension.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.



This RFC is the authoritative specification for the RFC 0322 workflow extension.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## Normative Status
This specification is normative. Every implementation MUST conform to the requirements defined herein.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Extension Point | A defined location in the workflow system where third-party code can inject behavior. | RFC-0322 |
| Extension Registration | The process of making an extension available to the workflow system. | RFC-0322 |
| Extension Interface | The contract between the workflow system and an extension. | RFC-0322 |
| Node Type Extension | An extension that registers a new workflow node type. | RFC-0322 |
| Trigger Extension | An extension that registers a new workflow trigger type. | RFC-0322 |
| Action Extension | An extension that registers a new workflow action type. | RFC-0322 |
| Condition Extension | An extension that registers a new workflow condition type. | RFC-0322 |
| Scheduler Extension | An extension that registers a new workflow scheduler policy. | RFC-0322 |

## 2 Layer Boundaries

## 3 Security
- Extensions MUST operate within sandbox boundaries per RFC-0319.
- Extension registration MUST be authorized per the permission model.
- Extensions MUST NOT have access to secrets without explicit declaration.

## 4 Performance
- Extension registration MUST complete within 100ms.
- Extension loading MUST NOT block workflow execution.

## 5 Compatibility
- Extension interfaces MUST be versioned and backward compatible within a major version.
- Breaking extension interface changes MUST require a new extension point registration.

## 6 Compliance
- All extension registrations MUST be recorded in the audit trail per RFC-0321.

## 7 Future Evolution
- **Hot-Swappable Extensions**: Runtime extension replacement without workflow restart.
- **Extension Marketplace**: Centralized extension discovery and installation.
- **Extension Sandboxing Profiles**: Pre-defined security profiles for common extension types.
- **Extension Dependency Resolution**: Automatic resolution of extension-to-extension dependencies.

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
| RFC-0304 | Workflow Runtime (extension hosting) |
| RFC-0309 | Workflow Actions (action extensions) |
| RFC-0310 | Workflow Conditions (condition extensions) |
| RFC-0311 | Workflow Triggers (trigger extensions) |
| RFC-0312 | Workflow Scheduler (scheduler extensions) |
| RFC-0317 | Workflow Validation (extension validation) |
| RFC-0319 | Workflow Security (extension sandboxing) |
| RFC-0320 | Workflow Performance (extension performance) |
| RFC-0321 | Workflow Observability (extension telemetry) |
| RFC-0323 | Workflow Plugin Integration (plugin hosting) |
| RFC-0329 | Workflow Compatibility (extension compatibility) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/extension-registration.json | Extension Registration JSON Schema |
| catalog/workflow-extension-points.md | Extension Points Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0322 (this document), RFC-0323 (Plugin Integration), RFC-0319 (Security) |
---


## 10 Extension Point Model

This section defines the extension point architecture that enables third-party extensibility.

### 10.1 Extension Point Registry

The extension point registry is the authoritative catalog of all available extension points. Each extension point has:

| Field | Type | Required | Description |
|---|---|---|---|
| id | string | Yes | Unique extension point identifier (dot-notation: domain.name) |
| name | string | Yes | Human-readable name |
| version | semver | Yes | Extension point API version |
| type | enum | Yes | Category of extension point |
| interface | schema_ref | Yes | JSON Schema for the extension interface |
| lifecycle | enum | Yes | Lifecycle model |
| security_level | enum | Yes | Required security clearance |
| stability | enum | Yes | API stability guarantee |
| metadata | object | No | Additional extension point attributes |

Valid extension point types: {Node, Trigger, Action, Condition, Scheduler, Hook, Middleware, Validator, Serializer, Deserializer, Transformer, Formatter}.

Valid lifecycle models: {Singleton, PerWorkflow, PerExecution, PerNode, PerEvent}.

Valid security levels: {Unrestricted, SandboxRequired, AdminOnly, Kernel}.

Valid stability guarantees: {Experimental, Beta, Stable, Deprecated}.

### 10.2 Extension Registration Protocol

Extensions MUST register through the following protocol:

1. **Discovery**: The runtime scans registered extension point IDs and validates the extension declares at least one supported point.
2. **Validation**: The extension interface is validated against the extension point schema. Validation errors reject registration.
3. **Authorization**: The extension's security level is compared against the caller's clearance level. Mismatch rejects registration.
4. **Loading**: The extension is loaded into the appropriate lifecycle scope.
5. **Activation**: The extension's activate hook is called. Failure deactivates and unloads the extension.
6. **Ready**: The extension is registered and available for workflow use.

Registration MUST complete within 100ms for SandboxRequired and below. AdminOnly extensions MAY take up to 5 seconds.

### 10.3 Extension Interface Contract

Every extension MUST implement the interface defined by its extension point. The interface contract includes:

- **Input schema**: Validated against the extension point's input definition. Invalid input returns a validation error.
- **Output schema**: Extension output MUST conform to the extension point's output definition.
- **Error contract**: Extensions MUST use standardized error codes from RFC-0314. Custom errors MUST include category, code, message, and context.
- **Timeout contract**: Extensions MUST respect the timeout declared in the extension point. Exceeding timeout triggers a TimeoutError.
- **Idempotency contract**: Extensions declaring idempotent behavior MUST produce identical results for identical inputs.

### 10.4 Extension Versioning

Extension points follow semantic versioning with the following compatibility rules:

| Version Change | Allowed Modifications | Breaking Change |
|---|---|---|
| Major | Remove extension points, change interface structure | Yes |
| Minor | Add new extension points, add optional fields | No |
| Patch | Fix bugs, improve documentation | No |

Extensions MUST declare the minimum extension point major version they require. An extension with major version N MUST work with extension point major version N and N-1.

### 10.5 Extension Lifecycle States

Each extension instance transitions through the following states:

`
Installing → Validating → Loading → Activating → Active → (Deactivating → Uninstalling → Uninstalled)
                                      ↕
                                   Error → (Retrying → Loading)
`

- **Installing**: Extension package received, not yet validated.
- **Validating**: Extension interface validated against schema.
- **Loading**: Extension code/resources loaded into memory.
- **Activating**: Extension activate hook called.
- **Active**: Extension is operational and available.
- **Deactivating**: Extension deactivate hook called, refusing new work.
- **Uninstalling**: Extension resources released.
- **Uninstalled**: Extension fully removed.
- **Error**: Extension failed in any state. Error state extensions MUST be unloadable.

### 10.6 Extension Isolation Model

Extensions MUST operate within isolation boundaries appropriate to their security level:

| Security Level | Memory Isolation | Network Isolation | File System Access | Secret Access |
|---|---|---|---|---|
| Unrestricted | Process boundary | None | Full | Declared secrets |
| SandboxRequired | Virtual machine / container | Egress filtering | Mounted volumes only | None |
| AdminOnly | Process boundary | Egress filtering | Full | All secrets |
| Kernel | In-process | None | Full | All secrets |

The runtime MUST enforce isolation boundaries. Violations MUST be treated as fatal errors.

## 11 Acceptance Criteria

### 11.1 Extension Point Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The extension point registry MUST contain all twelve (12) extension point types enumerated in Section 10.1. | Type enumeration test: Query registry → Verify all twelve types present with valid id, name, version, and interface fields |
| AC-02 | Extension registration MUST follow the six-step protocol: Discovery → Validation → Authorization → Loading → Activation → Ready. | Protocol test: Register extension with debug logging → Verify all six steps execute in order, no step skipped |
| AC-03 | Invalid extension interfaces MUST be rejected during the Validation step with a schema error. | Validation test: Submit extension with invalid interface → Verify rejection during Validation step with error containing schema violation details |
| AC-04 | Extensions MUST declare a security level from {Unrestricted, SandboxRequired, AdminOnly, Kernel}. | Security level test: Register five extensions with each level → Verify each extension's security level is correctly recorded |

### 11.2 Lifecycle Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-05 | Every extension MUST traverse the state machine: Installing → Validating → Loading → Activating → Active. | State machine test: Monitor extension lifecycle → Verify state transitions match prescribed sequence |
| AC-06 | Extensions in Error state MUST be unloadable. | Error unload test: Induce error in extension → Call unload → Verify extension removed successfully |
| AC-07 | Extension registration MUST complete within 100ms for SandboxRequired or below, 5 seconds for AdminOnly. | Timing test: Register 10 SandboxRequired extensions → Measure total time → Verify ≤ 1 second (10 × 100ms); Register AdminOnly → Verify ≤ 5 seconds |

### 11.3 Versioning Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-08 | Minor version additions (new extension points, optional fields) MUST NOT break existing extensions. | Backward compatibility test: Add new extension point via minor version bump → Verify existing extensions continue operating |
| AC-09 | Major version changes MUST require extensions to declare the new minimum major version. | Major version test: Bump extension point major version → Verify existing extensions with lower declared version are flagged incompatible |

### 11.4 Isolation Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-10 | SandboxRequired extensions MUST NOT access resources outside their mounted volumes. | Isolation test: SandboxRequired extension attempts file access outside mounts → Verify access denied |
| AC-11 | Extension isolation violations MUST be treated as fatal errors. | Violation test: Force extension to breach isolation boundary → Verify runtime terminates extension and logs fatal error |## Revision History

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