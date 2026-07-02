# RFC-0208: Plugin Sandbox

RFC: Rfc 0209 Plugin Api
Title: Plugin API
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0013 Runtime Contracts
  - RFC-0201 Plugin Overview
  - RFC-0205 Plugin Registry
  - RFC-0210 Plugin Events
Related RFC:
  - RFC-0206 Plugin Capability
  - RFC-0214 Plugin Extension Model
Related ADR:
  - ADR-0012 Contract-First Specification
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
This specification is Normative. Every Atlas implementation MUST conform to the sandbox architecture, isolation boundaries, execution constraints, resource quotas, filesystem isolation, memory/CPU/GPU limits, IPC restrictions, runtime interaction controls, recovery procedures, and sandbox lifecycle requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---



## Layer Boundaries

### Responsibilities

This specification IS responsible for:

- Defining the architectural contract for this domain.
- Specifying behavioral requirements that all implementations MUST satisfy.
- Establishing extension points and their contracts.

### Non-Responsibilities

This specification IS NOT responsible for:

- Implementation details (see related RFCs for implementation guidance).
- Runtime platform specifics.
- User-facing UI behavior.

### Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview — foundational runtime architecture |

### Consumers

- See related RFCs for consumer listings.

### Providers

- This specification provides domain-specific contracts and behavioral models.

### Forbidden Dependencies

- This specification MUST NOT depend on any specific programming language.
- This specification MUST NOT depend on any specific storage backend.
- This specification MUST NOT depend on any specific operating system.
## Table of Contents
1. [Introduction]
2. [Goals]
3. [Non-Goals]
4. [Sandbox Philosophy]
5. [Ownership]
6. [Boundaries]
7. [Runtime Invariants]
8. [Architecture]
9. [Sandbox Architecture]
10. [Execution Isolation]
11. [Resource Quotas]
12. [Filesystem Isolation]
13. [Memory Limits]
14. [CPU Limits]
15. [GPU Limits]
16. [IPC Restrictions]
17. [Runtime Interaction]
18. [Recovery]
19. [Sandbox Lifecycle]
20. [Performance Budgets]
21. [Glossary]
22. [Acceptance Criteria]
23. [Cross References]
24. [References]
25. [Revision History]
26. [Future Evolution]
---

## 1 Introduction

The Plugin API specification defines the application programming interfaces through which plugins interact with the Atlas Platform. It covers API contracts, extension interfaces, service access, event subscriptions, configuration, context, service discovery, API versioning, compatibility, validation, and deprecation policies.

---

## 2 Goals
1. **API Contracts**:  All plugin-platform interactions occur through versioned, schema-validated API contracts.
2. **Extension Interfaces**:  Plugins interact with the platform through well-defined extension interfaces.
3. **Service Access**:  Plugins access runtime services through a standardized service discovery mechanism.
4. **Event Subscriptions**:  Plugins subscribe to and publish events through the Event Bus.
5. **Configuration**:  Plugins receive configuration through a standardized configuration interface.
6. **Context**:  Plugins receive execution context including variables, metrics, and state.
7. **Service Discovery**:  Plugins discover available services through the Service Registry.
8. **API Versioning**:  All APIs follow semantic versioning with backward compatibility guarantees.
9. **Compatibility**:  APIs maintain backward compatibility within major version boundaries.
10. **Deprecation**:  Deprecated APIs are announced and supported for at least two major versions.

---

## 3 Non-Goals
- **API Implementation**: How APIs are implemented is outside this specification.
- **Client SDK Development**: SDK development for plugin authors is outside this specification.
- **API Documentation Generation**: Documentation generation tools are outside this specification.

---

## 4 API Philosophy
1. **Contract-First**: All APIs are defined by contracts before implementation.
2. **Versioned**: All APIs are versioned using semantic versioning.
3. **Backward Compatible**: New versions MUST maintain backward compatibility within major version.
4. **Declarative**: API usage is declared in the plugin manifest.
5. **Validated**: All API calls are validated against registered schemas.
6. **Auditable**: All API interactions are logged for audit purposes.

---

## 5 Ownership
- **The Platform MUST own**: API schema definitions, version management, deprecation policy, compatibility matrix, validation engine.
- **Plugin Authors MUST own**: API usage within declared contracts, error handling, configuration correctness.

---

## 6 Boundaries
- **API Provider MAY communicate with**: Plugin Registry (RFC-0205), Event Bus (RFC-0210), Capability Manager (RFC-0206), Service Registry (RFC-0003).
- **API Provider MUST NOT communicate with**: Plugin extension logic directly, External networks directly.

---

## 7 Runtime Invariants
- **INV-API-01**: All API calls MUST be validated against registered schemas.
- **INV-API-02**: API version mismatches MUST prevent communication.
- **INV-API-03**: Deprecated APIs MUST continue functioning for the deprecation period.
- **INV-API-04**: API interactions MUST be auditable.
- **INV-API-05**: Service discovery MUST return accurate, current service information.
- **INV-API-06**: API context MUST be isolated between plugins.

---

## 8 Architecture
`mermaid
graph TD
    subgraph API Provider
        SchemaValidator[Schema Validator]
        ServiceRegistry[Service Registry Client]
        EventSubs[Event Subscription Manager]
        ConfigMgr[Configuration Manager]
        ContextMgr[Context Manager]
        VersionChecker[Version Checker]
        DeprecationTracker[Deprecation Tracker]
        APIGateway[API Gateway]
    end
    subgraph External Systems
        Registry[Plugin Registry RFC-0205]
        EventBus[Event Bus RFC-0210]
        CapReg[Capability Registry RFC-0206]
        ServiceReg[Service Registry RFC-0003]
    end
    SchemaValidator --> Registry
    ServiceRegistry --> ServiceReg
    EventSubs --> EventBus
    ConfigMgr --> Registry
    ContextMgr --> Registry
    VersionChecker --> Registry
    DeprecationTracker --> Registry
    APIGateway --> ServiceReg
    APIGateway --> EventBus
    APIGateway --> Registry
`

---

## 9 API Contracts
All plugin-platform interactions occur through versioned API contracts.
- **Contract Declaration**: APIs are declared in the plugin manifest.
- **Schema Validation**: Every API call is validated against the registered schema.
- **Version Negotiation**: API versions are negotiated at connection time.
- **Error Handling**: API errors follow the common error model (RFC-1006).

## 10 Extension Interfaces
Plugins interact with the platform through extension interfaces.
- **Service Interface**: Standard interface for runtime service access.
- **Event Interface**: Standard interface for event subscription and publishing.
- **Configuration Interface**: Standard interface for reading plugin configuration.
- **Context Interface**: Standard interface for receiving execution context.

## 11 Service Access
- **Discovery**: Plugins discover services through the Service Registry (RFC-0003).
- **Authentication**: Service access requires valid authentication tokens.
- **Authorization**: Service access is authorized based on declared permissions.
- **Rate Limiting**: Service calls are rate-limited per plugin.

## 12 Event Subscriptions
- **Subscription**: Plugins subscribe to event channels declared in the manifest.
- **Publication**: Plugins publish events through the Event Bus (RFC-0210).
- **Filtering**: Plugins MAY filter events by category, priority, and source.
- **Ordering**: Events are delivered in order within a channel.

## 13 Configuration
- **Declaration**: Configuration is declared in the plugin manifest.
- **Validation**: Configuration is validated against the declared schema.
- **Update**: Configuration updates trigger a configuration change event.
- **Isolation**: Plugin configuration is isolated from other plugins.

## 14 Context
- **Execution Context**: Plugins receive execution context including variables and metrics.
- **Transaction Context**: Plugins participate in platform transactions.
- **Correlation ID**: Every context includes a correlation ID for tracing.
- **Trace ID**: Every context includes a trace ID for distributed tracing.

## 15 Service Discovery
- **Registry Query**: Plugins query the Service Registry for available services.
- **Capability Check**: Plugins verify service capabilities before use.
- **Health Check**: Plugins monitor service health through the Event Bus.
- **Failover**: Service failures trigger automatic failover to alternate services.

## 16 API Versioning
- **Semantic Versioning**: All APIs follow semantic versioning (RFC-0212).
- **Major Version**: Breaking changes. New major version required.
- **Minor Version**: Additive, backward-compatible changes.
- **Patch Version**: Bug fixes and non-functional improvements.
- **Version Negotiation**: Clients and servers negotiate compatible versions.

## 17 Compatibility
- **Backward Compatibility**: New API versions MUST support old clients within major version.
- **Forward Compatibility**: Old API versions MAY support new clients where possible.
- **Compatibility Matrix**: Defined in RFC-0212.

## 18 Validation
- **Schema Validation**: All API calls are validated against registered schemas.
- **Type Checking**: Parameter types are validated at call time.
- **Range Checking**: Numeric parameters are validated against declared ranges.
- **Format Checking**: String parameters are validated against declared formats.

## 19 Deprecation
- **Announcement**: Deprecated APIs are announced through the Event Bus.
- **Support Period**: Deprecated APIs are supported for at least two major versions.
- **Migration Path**: Migration guidance is provided for deprecated APIs.
- **Removal**: Deprecated APIs are removed after the support period expires.

## 20 Performance Budgets
| Metric | Target Budget |
|---|---|
| API Call Validation | 0.1 ms |
| Service Discovery | 1 ms |
| Event Subscription | 10 ms |
| Configuration Read | 0.01 ms |
| Context Creation | 0.1 ms |
| Version Negotiation | 5 ms |
---

## 21 Acceptance Criteria

### API Contracts
#### AC-0209-001
- **Requirement**: All API calls MUST be validated against registered schemas.
- **Verification**: Send invalid API call.
- **Expected Result**: Call is rejected.
#### AC-0209-002
- **Requirement**: API version mismatches MUST prevent communication.
- **Verification**: Connect incompatible versions.
- **Expected Result**: Connection rejected.
#### AC-0209-003
- **Requirement**: API errors MUST follow the common error model (RFC-1006).
- **Verification**: Generate API error and check format.
- **Expected Result**: Error conforms to RFC-1006.
#### AC-0209-004
- **Requirement**: Every API call MUST include a correlation ID.
- **Verification**: Make API call and check metadata.
- **Expected Result**: Correlation ID is present.
#### AC-0209-005
- **Requirement**: Every API call MUST include a trace ID.
- **Verification**: Make API call and check metadata.
- **Expected Result**: Trace ID is present.

### Extension Interfaces
#### AC-0209-006
- **Requirement**: Service interface MUST provide standard runtime service access.
- **Verification**: Invoke service through interface.
- **Expected Result**: Service is accessible.
#### AC-0209-007
- **Requirement**: Event interface MUST support subscription and publishing.
- **Verification**: Subscribe and publish events.
- **Expected Result**: Operations succeed.
#### AC-0209-008
- **Requirement**: Configuration interface MUST support reading plugin configuration.
- **Verification**: Read configuration through interface.
- **Expected Result**: Configuration is returned.
#### AC-0209-009
- **Requirement**: Context interface MUST provide execution context variables.
- **Verification**: Access context variables.
- **Expected Result**: Variables are accessible.

### Service Access
#### AC-0209-010
- **Requirement**: Plugins MUST discover services through the Service Registry.
- **Verification**: Query service registry.
- **Expected Result**: Services are discovered.
#### AC-0209-011
- **Requirement**: Service access MUST require valid authentication tokens.
- **Verification**: Access service without token.
- **Expected Result**: Access denied.
#### AC-0209-012
- **Requirement**: Service access MUST be authorized based on declared permissions.
- **Verification**: Access service without permission.
- **Expected Result**: Access denied.
#### AC-0209-013
- **Requirement**: Service calls MUST be rate-limited per plugin.
- **Verification**: Exceed rate limit.
- **Expected Result**: Calls are throttled.

### Event Subscriptions
#### AC-0209-014
- **Requirement**: Plugins MUST subscribe to event channels declared in the manifest.
- **Verification**: Subscribe to undeclared channel.
- **Expected Result**: Subscription rejected.
#### AC-0209-015
- **Requirement**: Plugins MUST publish events through the Event Bus.
- **Verification**: Publish event and check bus.
- **Expected Result**: Event is published.
#### AC-0209-016
- **Requirement**: Plugins MAY filter events by category, priority, and source.
- **Verification**: Apply event filters.
- **Expected Result**: Events are filtered.
#### AC-0209-017
- **Requirement**: Events MUST be delivered in order within a channel.
- **Verification**: Publish unordered events.
- **Expected Result**: Events are ordered.

### Configuration
#### AC-0209-018
- **Requirement**: Configuration MUST be declared in the plugin manifest.
- **Verification**: Check manifest for config declaration.
- **Expected Result**: Config is declared.
#### AC-0209-019
- **Requirement**: Configuration MUST be validated against the declared schema.
- **Verification**: Submit invalid configuration.
- **Expected Result**: Validation fails.
#### AC-0209-020
- **Requirement**: Configuration updates MUST trigger a configuration change event.
- **Verification**: Update configuration and check events.
- **Expected Result**: Event is produced.
#### AC-0209-021
- **Requirement**: Plugin configuration MUST be isolated from other plugins.
- **Verification**: Attempt cross-plugin config access.
- **Expected Result**: Access denied.

### Context
#### AC-0209-022
- **Requirement**: Plugins MUST receive execution context including variables and metrics.
- **Verification**: Check context on plugin start.
- **Expected Result**: Context is provided.
#### AC-0209-023
- **Requirement**: Plugins MUST participate in platform transactions.
- **Verification**: Start transaction in plugin.
- **Expected Result**: Transaction participates.
#### AC-0209-024
- **Requirement**: Every context MUST include a correlation ID.
- **Verification**: Inspect context.
- **Expected Result**: Correlation ID is present.
#### AC-0209-025
- **Requirement**: Every context MUST include a trace ID.
- **Verification**: Inspect context.
- **Expected Result**: Trace ID is present.

### Service Discovery
#### AC-0209-026
- **Requirement**: Plugins MUST query the Service Registry for available services.
- **Verification**: Query service registry.
- **Expected Result**: Services are returned.
#### AC-0209-027
- **Requirement**: Plugins MUST verify service capabilities before use.
- **Verification**: Check capability verification.
- **Expected Result**: Capabilities are verified.
#### AC-0209-028
- **Requirement**: Plugins MUST monitor service health through the Event Bus.
- **Verification**: Check health monitoring.
- **Expected Result**: Health events are received.
#### AC-0209-029
- **Requirement**: Service failures MUST trigger automatic failover to alternate services.
- **Verification**: Fail a service.
- **Expected Result**: Failover occurs.

### API Versioning
#### AC-0209-030
- **Requirement**: All APIs MUST follow semantic versioning.
- **Verification**: Check API version format.
- **Expected Result**: Versions follow SemVer.
#### AC-0209-031
- **Requirement**: Major version changes MUST indicate breaking changes.
- **Verification**: Inspect version change documentation.
- **Expected Result**: Breaking changes are documented.
#### AC-0209-032
- **Requirement**: Minor version changes MUST be backward-compatible.
- **Verification**: Add feature in minor version.
- **Expected Result**: Existing clients work.
#### AC-0209-033
- **Requirement**: Patch version changes MUST be freely mixable.
- **Verification**: Mix patch versions.
- **Expected Result**: Compatibility is maintained.
#### AC-0209-034
- **Requirement**: Clients and servers MUST negotiate compatible versions.
- **Verification**: Connect mismatched versions.
- **Expected Result**: Negotiation succeeds or fails gracefully.

### Compatibility
#### AC-0209-035
- **Requirement**: New API versions MUST support old clients within major version.
- **Verification**: Deploy new API version with old client.
- **Expected Result**: Old client works.
#### AC-0209-036
- **Requirement**: Deprecated APIs MUST continue functioning for the deprecation period.
- **Verification**: Use deprecated API during deprecation.
- **Expected Result**: API functions.
#### AC-0209-037
- **Requirement**: Migration guidance MUST be provided for deprecated APIs.
- **Verification**: Check deprecation announcement.
- **Expected Result**: Migration guide is included.
#### AC-0209-038
- **Requirement**: Deprecated APIs MUST be removed after the support period expires.
- **Verification**: Use deprecated API after expiration.
- **Expected Result**: API is removed.

### Validation
#### AC-0209-039
- **Requirement**: All API calls MUST be validated against registered schemas.
- **Verification**: Send malformed API call.
- **Expected Result**: Call is rejected.
#### AC-0209-040
- **Requirement**: Parameter types MUST be validated at call time.
- **Verification**: Send wrong type parameter.
- **Expected Result**: Validation fails.
#### AC-0209-041
- **Requirement**: Numeric parameters MUST be validated against declared ranges.
- **Verification**: Send out-of-range number.
- **Expected Result**: Validation fails.
#### AC-0209-042
- **Requirement**: String parameters MUST be validated against declared formats.
- **Verification**: Send malformed string.
- **Expected Result**: Validation fails.

### Architecture
#### AC-0209-043
- **Requirement**: The architecture MUST be illustrated with a Mermaid graph TD diagram.
- **Verification**: Inspect Section 8.
- **Expected Result**: Diagram is present.
#### AC-0209-044
- **Requirement**: The API provider MUST define at least six runtime invariants.
- **Verification**: Count invariants in Section 7.
- **Expected Result**: Six invariants are defined.
#### AC-0209-045
- **Requirement**: The specification MUST define at least eight goals.
- **Verification**: Count goals in Section 2.
- **Expected Result**: Eight goals are defined.
#### AC-0209-046
- **Requirement**: The specification MUST define at least three non-goals.
- **Verification**: Count non-goals in Section 3.
- **Expected Result**: Three non-goals are defined.
#### AC-0209-047
- **Requirement**: The specification MUST define at least six API philosophy principles.
- **Verification**: Count principles in Section 4.
- **Expected Result**: Six principles are defined.

### Performance
#### AC-0209-048
- **Requirement**: API call validation MUST complete within 0.1 ms.
- **Verification**: Benchmark API validation.
- **Expected Result**: Validation completes within 0.1 ms.
#### AC-0209-049
- **Requirement**: Service discovery MUST complete within 1 ms.
- **Verification**: Benchmark service discovery.
- **Expected Result**: Discovery completes within 1 ms.
#### AC-0209-050
- **Requirement**: Event subscription MUST complete within 10 ms.
- **Verification**: Benchmark event subscription.
- **Expected Result**: Subscription completes within 10 ms.
#### AC-0209-051
- **Requirement**: Configuration read MUST complete within 0.01 ms.
- **Verification**: Benchmark configuration read.
- **Expected Result**: Read completes within 0.01 ms.
#### AC-0209-052
- **Requirement**: Version negotiation MUST complete within 5 ms.
- **Verification**: Benchmark version negotiation.
- **Expected Result**: Negotiation completes within 5 ms.

### Consistency
#### AC-0209-053
- **Requirement**: The API model MUST be consistent with RFC-0201.
- **Verification**: Compare API definitions between RFC-0201 and RFC-0209.
- **Expected Result**: Definitions are consistent.
#### AC-0209-054
- **Requirement**: The API model MUST be consistent with RFC-0206 capability model.
- **Verification**: Compare capability access between RFC-0206 and RFC-0209.
- **Expected Result**: Access is consistent.
#### AC-0209-055
- **Requirement**: The API model MUST be consistent with RFC-0210 event model.
- **Verification**: Compare event interfaces between RFC-0210 and RFC-0209.
- **Expected Result**: Interfaces are consistent.
#### AC-0209-056
- **Requirement**: The API model MUST be consistent with RFC-0212 versioning model.
- **Verification**: Compare versioning between RFC-0212 and RFC-0209.
- **Expected Result**: Versioning is consistent.
#### AC-0209-057
- **Requirement**: The API model MUST reference catalog/interfaces.md for interface IDs.
- **Verification**: Check interface references.
- **Expected Result**: All interfaces reference PIF-* IDs.

### Edge Cases
#### AC-0209-058
- **Requirement**: The API MUST handle zero-service registries gracefully.
- **Verification**: Query registry with no services.
- **Expected Result**: Empty result returned.
#### AC-0209-059
- **Requirement**: The API MUST handle API version changes at runtime.
- **Verification**: Change API version during operation.
- **Expected Result**: Version change is handled.
#### AC-0209-060
- **Requirement**: The API MUST handle concurrent API calls from multiple plugins.
- **Verification**: Make concurrent API calls.
- **Expected Result**: Calls are serialized safely.
#### AC-0209-061
- **Requirement**: The API MUST handle network disconnection during API calls.
- **Verification**: Disconnect network during API call.
- **Expected Result**: Call fails gracefully.
#### AC-0209-062
- **Requirement**: The API MUST handle configuration schema changes.
- **Verification**: Change configuration schema.
- **Expected Result**: Schema change is handled.

### Security
#### AC-0209-063
- **Requirement**: API interactions MUST be auditable.
- **Verification**: Make API call and check audit log.
- **Expected Result**: Call is logged.
#### AC-0209-064
- **Requirement**: API tokens MUST expire after configured intervals.
- **Verification**: Check token expiration.
- **Expected Result**: Tokens expire.
#### AC-0209-065
- **Requirement**: API rate limiting MUST prevent abuse.
- **Verification**: Exceed rate limits.
- **Expected Result**: Calls are throttled.
#### AC-0209-066
- **Requirement**: API context MUST be isolated between plugins.
- **Verification**: Attempt cross-plugin context access.
- **Expected Result**: Access denied.
#### AC-0209-067
- **Requirement**: API schemas MUST prevent injection attacks.
- **Verification**: Send injection payload.
- **Expected Result**: Payload is rejected.
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





---

## References

| Reference | Description |
|---|---|
| RFC-0201 | Plugin Overview |
| RFC-0206 | Plugin Capability |
| RFC-0220 | Plugin IPC |
| Glossary | Atlas Master Glossary |

---


| Category | Value |
|---|---|
| Related RFC | RFC-0201, RFC-0206, RFC-0220 |
| Related ADR | ADR-0012 |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-06-30 | Atlas Team | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Fixed duplicate Layer Boundaries sections, added References, Compliance Matrix, Revision History |



