# Layer Rules

> **Purpose**: Define layer boundaries and what each layer owns.
> **Reference**: architecture-rules.md for full architectural constraints.

---

## Layer Architecture

`
┌─────────────────────────────────────────┐
│  L5: Application / UI                  │  ← apps/, UI packages
│  Depends on: L4 (via IPC/contracts)     │
├─────────────────────────────────────────┤
│  L4: Subsystem / Feature               │  ← workflow/, plugin/, vision/
│  Depends on: L3 (via contracts)         │
├─────────────────────────────────────────┤
│  L3: Runtime Services                  │  ← runtime/, scheduler/, eventbus/
│  Depends on: L2                         │
├─────────────────────────────────────────┤
│  L2: Shared Types / Common             │  ← common/, error types
│  Depends on: L1                         │
├─────────────────────────────────────────┤
│  L1: Contracts / Interfaces            │  ← contracts/
│  Depends on: nothing                    │
└─────────────────────────────────────────┘
`

## Layer Ownership

| Layer | Owns | Cannot Own |
|-------|------|-----------|
| L1: Contracts | Trait definitions, interface specs | Implementations |
| L2: Common | Shared types, error enums, state enums | Business logic |
| L3: Runtime | Service implementations, lifecycle, scheduling | UI, workflow logic |
| L4: Subsystems | Feature-specific logic | Runtime internals |
| L5: Application | User-facing surfaces | Business logic, state management |

## Layer Boundary Rules

1. **No upward imports**: A lower layer never imports a higher layer.
2. **Interface abstraction**: Higher layers depend on lower layer interfaces, not implementations.
3. **No cross-layer shortcuts**: L5 cannot call L2 directly. Must go through L3/L4.
4. **IPC as boundary**: Cross-process communication is the hard boundary between layers.

## Forbidden Cross-Layer Patterns

| Pattern | Why Forbidden | Correct Approach |
|---------|--------------|-----------------|
| UI → Runtime internals | Breaks encapsulation | Use IPC channels |
| Workflow → Scheduler internals | Tight coupling | Use SchedulerController trait |
| Plugin → Runtime state | Isolation violation | Use event bus or IPC |
| Vision → Storage direct | Bypasses contracts | Use StorageContract trait |
| Any layer → Global state | Untestable | Dependency injection |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
