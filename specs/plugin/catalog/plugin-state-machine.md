---
id: ATLAS-PLUGINSPEC-CATALOG-PSM
title: Plugin State Machine Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin State Machine Catalog

## 1. Purpose

Documents the state machine for plugin lifecycle states.

## 2. Plugin States

| State       | Description                              | Transitions To                          |
|-------------|------------------------------------------|-----------------------------------------|
| Discovered  | Plugin found during discovery            | Loading, Ignored                        |
| Loading     | Plugin manifest being parsed             | Loaded, Error                           |
| Loaded      | Manifest parsed, dependencies resolved   | Ready, Error                            |
| Ready       | All dependencies satisfied, ready to start| Starting, Error                        |
| Starting    | Plugin init hooks executing              | Running, Error                          |
| Running     | Plugin is fully operational              | Stopping, Error                         |
| Stopping    | Plugin deactivation in progress          | Stopped, Error                          |
| Stopped     | Plugin deactivated, resources released   | Starting (reload), Uninstalled          |
| Uninstalling| Plugin removal in progress               | Uninstalled                             |
| Uninstalled | Plugin fully removed                     | (terminal)                              |
| Error       | Plugin encountered a fatal error         | Recovering, Uninstalled                 |
| Recovering  | Plugin attempting recovery               | Running, Uninstalled                    |

## 3. State Machine

```
Discovered -> Loading -> Loaded -> Ready -> Starting -> Running
                                                        |    |
                                                        v    v
                                                     Stopping <- Error
                                                        |        |
                                                        v        v
                                                      Stopped   Recovering
                                                        |         |
                                                        v         v
                                                   Uninstalling -> Uninstalled
```

## 4. Cross-References

- RFC-0203 Plugin Lifecycle
- RFC-0225 Plugin Hot Reload
