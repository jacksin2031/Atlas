---
id: ATLAS-PLUGINSPEC-CATALOG-SVLIFE
title: Plugin Service Lifecycle Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Service Lifecycle Catalog

## 1. Purpose

Documents the lifecycle states and transitions for services registered by plugins.

## 2. Service Lifecycle States

| State       | Description                              | Transitions To                          |
|-------------|------------------------------------------|-----------------------------------------|
| Creating    | Service factory is being invoked         | Ready, Error                            |
| Ready       | Service is registered, not yet started   | Running, Error                          |
| Running     | Service is actively processing requests  | Draining, Error                         |
| Draining    | Service stopping, draining in-flight req | Disposed, Error                         |
| Disposed    | Service resources fully released         | (terminal)                              |
| Error       | Service encountered a fatal error        | Disposed (auto), Recovering (manual)    |
| Recovering  | Service attempting to recover from error | Running, Disposed                       |

## 3. State Transition Rules

1. Creating -> Ready: Factory succeeded.
2. Creating -> Error: Factory threw exception.
3. Ready -> Running: Plugin started, service activated.
4. Ready -> Error: Registration error detected.
5. Running -> Draining: Plugin stopping or service update requested.
6. Running -> Error: Fatal error during operation.
7. Draining -> Disposed: All in-flight requests completed or timed out.
8. Draining -> Error: Error during drain.
9. Error -> Disposed: Error is unrecoverable.
10. Error -> Recovering: Manual recovery initiated.
11. Recovering -> Running: Recovery succeeded.
12. Recovering -> Disposed: Recovery failed.

## 4. State Machine Diagram

```
Creating -> Ready -> Running -> Draining -> Disposed
   |         |        |           |
   v         v        v           v
 Error -> Recovering -> Running
```

## 5. Cross-References

- RFC-0215 Plugin Service Model
- RFC-0203 Plugin Lifecycle
