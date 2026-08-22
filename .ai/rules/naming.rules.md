# Naming Rules

> **Purpose**: Standardize naming across all modules and languages.
> **Reference**: coding-standard.md for full style guidelines.

---

## General Principles

1. **Self-documenting**: Names must reveal intent without reading implementation.
2. **Consistent**: Same concept = same name everywhere.
3. **No abbreviations**: event_handler not evt_hndlr.
4. **No type suffixes**: UserService not UserServiceStruct.

---

## Language-Specific Rules

### Rust

| Element | Convention | Example |
|---------|-----------|---------|
| Module | snake_case | event_bus, service_registry |
| Type | PascalCase | RuntimeState, EventBusImpl |
| Function | snake_case | 	ransition_to, esolve_dependencies |
| Constant | SCREAMING_SNAKE_CASE | MAX_RETRIES, DEFAULT_TIMEOUT_MS |
| Trait | PascalCase or -er suffix | ServiceContract, HealthChecker |
| Macro | snake_case | define_service! |
| Type param | PascalCase, single letter or descriptive | T, ServiceId, EventPayload |
| File | snake_case | lifecycle_manager.rs |

### TypeScript

| Element | Convention | Example |
|---------|-----------|---------|
| Module/Package | kebab-case | event-bus, service-registry |
| Type/Interface | PascalCase | RuntimeState, EventBusConfig |
| Function/Method | camelCase | 	ransitionTo, esolveDependencies |
| Constant | UPPER_SNAKE_CASE | MAX_RETRIES, DEFAULT_TIMEOUT_MS |
| Variable | camelCase | eventBus, serviceRegistry |
| Class | PascalCase | LifecycleManager |
| Enum | PascalCase | RuntimeState, EventPriority |
| File | kebab-case | lifecycle-manager.ts |
| Private member | _prefix | _internalState |

---

## Domain-Specific Naming

| Concept | Naming Pattern | Examples |
|---------|---------------|----------|
| State | {Entity}State | RuntimeState, ServiceState, SchedulerState |
| Error | {Domain}Error | StateTransitionError, CircularDependencyError |
| Handler | {Event}Handler | EventHandler, LifecycleHandler |
| Manager | {Domain}Manager | LifecycleManager, ServiceManager |
| Controller | {Domain}Controller | SchedulerController, EventBusController |
| Contract | {Domain}Contract | ServiceContract, LifecycleContract |
| Config | {Domain}Config | RuntimeConfig, SchedulerConfig |
| Builder | {Entity}Builder | EventBuilder, ManifestBuilder |

---

## Forbidden Names

| Forbidden | Why | Alternative |
|-----------|-----|-------------|
| data, info, esult | Too generic | event_data, health_info, 	ransition_result |
| 	emp, 	mp | Hides purpose | 	emporary_token, 	mp_directory |
| handle | Unclear what it handles | subscription_handle, 	ask_handle |
| manager (alone) | Too vague | lifecycle_manager, config_manager |
| util / helper | Catch-all anti-pattern | Extract specific module |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
