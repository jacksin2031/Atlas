---
id: ATLAS-PLUGINSPEC-CATALOG-SVCTYPES
title: Plugin Service Types Catalog
version: \"1.0.0\"
status: active
language: independent
---

# Plugin Service Types Catalog

## 1. Purpose

This catalog defines the canonical set of service types that plugins can register with the Atlas runtime service registry. Each service type determines lifetime behavior, scope, and consumption patterns.

## 2. Stable ID Prefix

All service type identifiers use the prefix SVC-.

## 3. Complete Service Types Table

| Stable ID | Type Name  | Lifetime Behavior         | Scope              | Registration Pattern                          | Consumption Pattern                         | Example Use Case                  |
|-----------|------------|---------------------------|--------------------|-----------------------------------------------|---------------------------------------------|-----------------------------------|
| SVC-SGL   | Singleton  | One instance per runtime  | Global             | egister(ServiceDef) on init                | esolve(name) returns cached instance     | Configuration manager             |
| SVC-TRN   | Transient  | New instance per request  | Per-call           | egister(ServiceDef, Transient{})           | esolve(name) creates new instance        | HTTP client factory               |
| SVC-SCPD  | Scoped     | One instance per scope    | Workspace/Session  | egister(ServiceDef, Scoped{scope: ...})    | esolve(name, scope) returns scoped inst. | Per-workspace state manager       |
| SVC-SHD   | Shared     | Cross-plugin shared state | Global             | egister(ServiceDef, Shared{visibility: ...})| esolve(name) returns shared instance    | Shared cache, shared session data |
| SVC-LAZY  | Lazy       | Init on first access      | Per-instance       | egister(ServiceDef, Lazy{factory: ...})    | esolve(name) wraps in lazy proxy         | Heavy model loading               |
| SVC-PL    | Pool       | Object pool reuse         | Per-type           | egister(ServiceDef, Pool{min: N, max: M})  | cquire(name) / elease(obj)            | Database connections              |
| SVC-PRXY  | Proxy      | Remote service wrapper    | Per-connection     | egister(ServiceDef, Proxy{target: url})    | esolve(name) returns proxy stub          | Remote AI service adapter         |
| SVC-FBLL  | Fallback   | Graceful degradation chain| Per-type           | egister(ServiceDef, Fallback[{primary, secondary}]) | esolve(name) tries chain in order | Multi-provider AI adapter         |

## 4. Service Type Constraints

1. Singleton services MUST be registered before the plugin.ready event.
2. Transient services MUST be stateless; any state MUST be stored externally.
3. Scoped services MUST define a clear scope boundary (workspace or session).
4. Shared services MUST declare visibility: public (consumable by any plugin) or private (same-author only).
5. Lazy services MUST not execute the factory during registration.
6. Pool services MUST enforce min/max bounds; acquiring beyond max MUST block or return error.
7. Proxy services MUST implement circuit breaker pattern (see RFC-0220).
8. Fallback services MUST define a strict priority order; primary failure triggers secondary.

## 5. Service Resolution Algorithm

`
resolve(name, scope?) -> ServiceInstance
1. Lookup name in registry
2. If scope provided AND service is Scoped, verify scope match
3. If service is Lazy, invoke factory on first call
4. If service is Pool, acquire from pool (or create if below max)
5. If service is Proxy, establish connection if not connected
6. Return ServiceInstance
`

## 6. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- RFC-0215 Plugin Service Model
- RFC-0205 Plugin Registry
