# Atlas Implementation Roadmap

> **Sprint 1 — Runtime Foundation**  
> Status: Planning  
> Last Updated: 2026-07-02

---

## Purpose

This document is the **single source of truth** for AI agents implementing Project Atlas.  
Every agent MUST read this document before writing any code.  
It translates the RFC specifications into concrete implementation steps.

---

## Scope: Sprint 1 — Runtime Foundation

### In Scope

| Component | RFC Reference |
|-----------|---------------|
| Bootstrap | RFC-0001 §1, RFC-0010 §12 |
| Configuration Loading | RFC-0010 §9 |
| Manifest Loading | RFC-0010 §8–12 |
| Runtime Creation | RFC-0002 §8–9 |
| Service Registry | RFC-0003 §8, §10–15 |
| Dependency Resolution | RFC-0003 §11 |
| Event Bus | RFC-0005 §8–18 |
| Scheduler | RFC-0004 §8–18 |
| Runtime Lifecycle (FSM) | RFC-0002 §8–9, §38 |
| Health Monitor | RFC-0003 §16 |
| Graceful Shutdown | RFC-0002 §32–33 |

### Out of Scope (Do NOT implement)

- Workflow Engine
- Plugin Host
- Vision Engine
- AI Engine
- Marketplace
- Knowledge System
- Storage Backend (interfaces only)
- IPC Transport (interfaces only)
- UI

---

## Project Layout

`
Atlas/
├── .ai/                              # ADS governance (read-only)
├── specs/
│   ├── runtime/                      # RFC-0001 through RFC-0014 (read-only)
│   ├── common/                       # RFC-1001, RFC-1005 (read-only)
│   └── ...                           # other subsystems (read-only)
├── contracts/
│   ├── api/                          # Service interface definitions
│   ├── json/                         # JSON schema files
│   └── ipc/                          # IPC contract definitions
├── packages/
│   ├── runtime/                      # ← Sprint 1 target
│   │   ├── src/
│   │   │   ├── lib.rs                # Crate root
│   │   │   ├── bootstrap/            # Bootstrap coordinator
│   │   │   ├── lifecycle/            # FSM state machine
│   │   │   ├── registry/             # Service Registry
│   │   │   ├── dependency/           # Topological resolver
│   │   │   ├── eventbus/             # Event Bus
│   │   │   ├── scheduler/            # Task Scheduler
│   │   │   ├── health/               # Health Monitor
│   │   │   ├── config/               # Configuration loader
│   │   │   ├── manifest/             # Manifest parser/loader
│   │   │   ├── error/                # Error types
│   │   │   └── test_helpers/         # Test utilities
│   │   ├── tests/                    # Integration tests
│   │   └── Cargo.toml
│   ├── common/                       # Shared types
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── event.rs              # Common Event struct
│   │   │   ├── manifest.rs           # Common Manifest struct
│   │   │   ├── error.rs              # Shared error types
│   │   │   └── lifecycle.rs          # State enum
│   │   └── Cargo.toml
│   └── contracts/                    # Trait definitions
│       ├── src/
│       │   ├── lib.rs
│       │   ├── service.rs            # ServiceContract trait
│       │   ├── event_bus.rs          # EventBus trait
│       │   ├── scheduler.rs          # SchedulerController trait
│       │   ├── lifecycle.rs          # Lifecycle transitions
│       │   └── health.rs             # HealthChecker trait
│       └── Cargo.toml
├── configs/                          # Default config files
├── tests/                            # E2E tests
├── scripts/                          # Build/helper scripts
└── docs/
    └── adr/                          # Architecture Decision Records
`

---

## Implementation Order

**Always implement from interfaces inward:**

`
Phase 0: contracts/ (traits & interfaces)
    ↓
Phase 1: packages/common/ (shared types)
    ↓
Phase 2: packages/runtime/ (core services)
    ↓
Phase 3: integration tests
`

### Phase 0 — Contracts (Interfaces First)

Create trait definitions in packages/contracts/src/:

1. **service.rs** — ServiceContract trait
   - id() -> &str
   - 
ame() -> &str
   - dependencies() -> &[&str]
   - priority() -> u8
   - equired() -> bool
   - health_check() -> HealthStatus
   - initialize() -> Result<(), Error>
   - deinitialize() -> Result<(), Error>

2. **event_bus.rs** — EventBus trait
   - publish(channel: &Channel, event: &Event) -> Result<(), Error>
   - subscribe(pattern: &str, handler: Box<dyn EventHandler>) -> SubscriptionHandle
   - unsubscribe(handle: SubscriptionHandle) -> Result<(), Error>
   - get_stats() -> EventBusStats

3. **scheduler.rs** — SchedulerController trait
   - submit_task(task: TaskDefinition) -> TaskId
   - cancel_task(task_id: TaskId) -> Result<(), Error>
   - get_queue_depth() -> QueueDepth
   - get_worker_pool_status() -> WorkerPoolStatus
   - pause() -> Result<(), Error>
   - esume() -> Result<(), Error>

4. **lifecycle.rs** — State transition definitions
   - RuntimeState enum: Created, Initializing, Ready, Running, Paused, ShuttingDown, Failed, Terminated
   - StateTransitionError type
   - TransitionGuard trait for validating transitions

5. **health.rs** — HealthChecker trait
   - check() -> HealthStatus
   - interval() -> Duration

### Phase 1 — Common Types

Create shared types in packages/common/src/:

1. **event.rs** — Event struct per RFC-1001
   `ust
   pub struct Event {
       pub event_id: Uuid,
       pub name: String,        // e.g., "Runtime.Created"
       pub category: EventCategory,
       pub priority: EventPriority,
       pub correlation_id: Uuid,
       pub trace_id: Uuid,
       pub timestamp: u64,      // monotonic
       pub source: String,
       pub payload: serde_json::Value,
   }
   `

2. **manifest.rs** — Manifest struct per RFC-1005
   `ust
   pub struct Manifest {
       pub manifest_version: String,
       pub package_type: PackageType,
       pub name: String,
       pub version: SemVer,
       pub author: String,
       pub description: String,
       pub capabilities: Vec<Capability>,
       pub permissions: Vec<Permission>,
       pub dependencies: Vec<String>,
       pub resource_limits: Option<ResourceLimits>,
   }
   `

3. **error.rs** — Error hierarchy
   - AtlasError enum covering: Lifecycle, Service, Event, Scheduler, Manifest, Config, Health

4. **lifecycle.rs** — State enum
   - RuntimeState with all 8 states from RFC-0002

### Phase 2 — Runtime Package

#### 2.1 Bootstrap (ootstrap/)

**File:** packages/runtime/src/bootstrap/mod.rs

The bootstrap coordinator orchestrates the boot sequence:

1. Read manifest file from config path
2. Parse and validate against JSON schema
3. Register core services with Service Registry
4. Resolve dependencies (topological sort)
5. Initialize services in dependency order
6. Transition Runtime to Ready state
7. Publish BootCompleted event

#### 2.2 Lifecycle (lifecycle/)

**File:** packages/runtime/src/lifecycle/mod.rs

Implement the FSM from RFC-0002 §8:

`ust
pub struct LifecycleManager {
    state: RuntimeState,
    monotonic_clock: MonotonicClock,
    event_bus: Arc<dyn EventBus>,
    transition_log: Vec<StateTransition>,
}

impl LifecycleManager {
    pub fn transition(&mut self, target: RuntimeState) -> Result<(), StateTransitionError>;
    pub fn current_state(&self) -> &RuntimeState;
    pub fn can_transition(&self, target: &RuntimeState) -> bool;
}
`

Key rules:
- Use a whitelist of valid transitions (hardcoded from FSM diagram)
- Reject illegal transitions with StateTransitionError
- Publish lifecycle event on every transition
- Enforce monotonic timestamps
- Serialize state changes (single owner)

#### 2.3 Service Registry (egistry/)

**File:** packages/runtime/src/registry/mod.rs

`ust
pub struct ServiceRegistry {
    services: HashMap<String, RegisteredService>,
    init_order: Vec<String>,        // topological order
    health_intervals: HashMap<String, Duration>,
}

impl ServiceRegistry {
    pub fn register(service: Box<dyn ServiceContract>) -> Result<ServiceId, Error>;
    pub fn resolve_dependencies() -> Vec<ServiceId>;  // topological sort
    pub fn get(id: &str) -> Option<&RegisteredService>;
    pub fn all_services() -> Vec<&RegisteredService>;
    pub fn detect_cycles() -> Result<(), CircularDependencyError>;
}
`

Key rules:
- Detect circular dependencies during registration
- Resolve topological order (dependencies first)
- Thread-safe lookups
- Register core services: EventBus, Scheduler, HealthMonitor, ConfigLoader, ManifestLoader

#### 2.4 Dependency Resolution (dependency/)

**File:** packages/runtime/src/dependency/mod.rs

Implement topological sort using Kahn's algorithm:

`ust
pub fn resolve(service_graph: &[ServiceDependency]) -> Result<Vec<String>, CircularDependencyError>;
`

- Input: list of services with their dependency declarations
- Output: ordered list respecting dependency order
- Failure: CircularDependencyError if graph has cycles
- Budget: ≤ 100ms (RFC-0003 §19)

#### 2.5 Event Bus (eventbus/)

**File:** packages/runtime/src/eventbus/mod.rs

`ust
pub struct EventBusImpl {
    channels: HashMap<Channel, ChannelState>,
    subscribers: Vec<Subscription>,
    dlq: DeadLetterQueue,
    stats: EventBusStats,
    priority_queues: [VecDeque<Event>; 5],  // 5 priority levels
}
`

Key features:
- Priority-based dispatching (RFC-0005 §10)
- Wildcard channel matching (e.g., untime.*.error)
- Dead Letter Queue for undeliverable events (RFC-0005 §15)
- Backpressure at 80% queue capacity
- DLQ routing at 100% capacity
- Request-response correlation via correlation_id
- Validate all events against RFC-1001 schema before publishing

#### 2.6 Scheduler (scheduler/)

**File:** packages/runtime/src/scheduler/mod.rs

`ust
pub struct SchedulerImpl {
    task_queue: PriorityQueue<TaskDefinition>,
    worker_pool: WorkerPool,
    state: SchedulerState,
}
`

Key features:
- Priority-based task queue (RFC-0004 §10)
- Worker pool with isolation (RFC-0004 §11)
- Backpressure at 80% queue depth
- Task retries with exponential backoff (RFC-0004 §14)
- Task cancellation (RFC-0004 §14.2)
- Dispatch-only (does NOT execute task logic)

#### 2.7 Health Monitor (health/)

**File:** packages/runtime/src/health/mod.rs

`ust
pub struct HealthMonitor {
    watchers: HashMap<String, HealthWatcher>,
    event_bus: Arc<dyn EventBus>,
}
`

Key features:
- Periodic health checks per service (RFC-0003 §16)
- Default interval: 5000ms ±100ms tolerance
- Degraded → Disabled → Failed escalation path
- Publish health events to Event Bus
- Heartbeat monitoring for watchdog

#### 2.8 Configuration Loader (config/)

**File:** packages/runtime/src/config/mod.rs

- Read configuration from JSON/YAML file
- Validate required fields
- Provide typed accessors
- Hot-reload support (stub for now)

#### 2.9 Manifest Loader (manifest/)

**File:** packages/runtime/src/manifest/mod.rs

`ust
pub struct ManifestLoader {
    schema_validator: SchemaValidator,
}

impl ManifestLoader {
    pub fn load(path: &Path) -> Result<Manifest, Error>;
    pub fn validate(manifest: &Manifest) -> Result<(), ValidationError>;
    pub fn resolve_capabilities(manifest: &Manifest) -> Vec<Capability>;
}
`

Key features:
- Parse manifest file (RFC-0010 §12)
- Validate against JSON schema (RFC-0010 §16)
- Discover capabilities (RFC-0010 §10)
- Version negotiation (RFC-0010 §11)
- Apply fallback policies for missing capabilities (RFC-0010 §15)

#### 2.10 Error Types (error/)

**File:** packages/runtime/src/error/mod.rs

Define the error hierarchy per RFC-0011:

`ust
pub enum AtlasError {
    Lifecycle(StateTransitionError),
    Service(ServiceError),
    Event(EventBusError),
    Scheduler(SchedulerError),
    Manifest(ManifestError),
    Config(ConfigError),
    Health(HealthError),
    Dependency(CircularDependencyError),
}
`

### Phase 3 — Runtime Assembly

**File:** packages/runtime/src/lib.rs

Assemble the Runtime:

`ust
pub struct AtlasRuntime {
    lifecycle: LifecycleManager,
    registry: ServiceRegistry,
    event_bus: Arc<EventBusImpl>,
    scheduler: Arc<SchedulerImpl>,
    health_monitor: Arc<HealthMonitor>,
    config: ConfigLoader,
    manifest: ManifestLoader,
}

impl AtlasRuntime {
    pub fn bootstrap(config_path: &Path) -> Result<Self, Error>;
    pub fn activate(&mut self) -> Result<(), Error>;
    pub fn shutdown(&mut self) -> Result<(), Error>;
    pub fn health_status(&self) -> RuntimeHealth;
}
`

Boot sequence:
1. Load config
2. Load manifest
3. Register core services
4. Resolve dependencies
5. Initialize services in order
6. Transition to Ready
7. Publish Ready event

Activation:
1. Transition to Running
2. Start scheduler loop
3. Start health monitor
4. Publish Running event

Shutdown:
1. Transition to ShuttingDown
2. Pause scheduler
3. Deinitialize services in reverse order
4. Drain event bus
5. Transition to Terminated
6. Publish Terminated event

---

## Testing Strategy

### Unit Tests

Each module MUST have unit tests covering:

| Module | Test Focus |
|--------|-----------|
| Lifecycle | All legal/illegal transitions, monotonic time |
| Registry | Registration, lookup, duplicate detection |
| Dependency | Topological sort, cycle detection |
| EventBus | Priority ordering, wildcard matching, DLQ routing |
| Scheduler | Priority queue, cancellation, retry backoff |
| Health | Interval enforcement, degradation escalation |
| Config | Parse valid/invalid configs |
| Manifest | Parse/validate manifest, capability discovery |
| Error | Error conversion, display formatting |

### Lifecycle Tests

- Full boot sequence: Created → Initializing → Ready → Running
- Full shutdown: Running → ShuttingDown → Terminated
- Illegal transitions (pause from Created, resume from Terminated)
- Concurrent shutdown() calls (idempotency)

### Failure Tests

- Circular dependency detection
- Manifest validation failure
- Service health check failure → degradation → disable
- Event bus overflow → DLQ routing
- Scheduler queue overflow → backpressure

### Integration Tests

- Bootstrap → register → activate → shutdown flow
- Event publishing during lifecycle transitions
- Health monitor checking registered services
- Scheduler processing tasks during Running state

---

## Quality Gates

Before any code is merged, verify:

- [ ] Architecture follows RFC-0001, RFC-0002, RFC-0003
- [ ] Naming follows coding-standard.md
- [ ] Lifecycle follows RFC-0002 state machine
- [ ] Service contracts implemented per RFC-0003
- [ ] Dependency graph respected (no forbidden imports)
- [ ] No circular dependencies
- [ ] All tests passing
- [ ] No TODO comments
- [ ] No placeholder implementations
- [ ] No dead code

---

## Forbidden Patterns

- ❌ Global mutable state
- ❌ Service locator anti-pattern
- ❌ Static mutable state
- ❌ Hardcoded service references (use DI)
- ❌ Cross-module coupling (use traits/interfaces)
- ❌ Blocking the event bus thread
- ❌ Shared mutable state between workers

---

## Dependencies Between Phases

`
Phase 0 (contracts)
    ↓
Phase 1 (common types)
    ↓
Phase 2 (runtime services)
    ↓
Phase 3 (runtime assembly)
    ↓
Tests
`

Each phase depends only on phases below it.  
No upward dependencies allowed.

---

## Notes for AI Agents

1. **Read this document fully before starting.** Do not skip sections.
2. **Implement interfaces first.** Never implement a concrete type before its trait.
3. **Follow RFCs literally.** If an RFC says "MUST", it is mandatory.
4. **No guessing.** If a specification is ambiguous, stop and ask.
5. **Small commits.** Each logical unit gets its own commit.
6. **Tests are mandatory.** Every service needs unit + lifecycle + failure tests.
7. **No TODOs.** Ship complete code, not placeholders.
8. **Respect scope.** Do NOT implement Workflow, Plugin, Vision, AI, or Marketplace.
