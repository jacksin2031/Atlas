# Frontend Contract

> **Role**: UI/dashboard implementation — user-facing surfaces.
> **Authority Level**: Owns UI implementation within Runtime IPC boundaries.
> **Cannot**: Modify runtime internals, change service contracts, implement core logic.

---

## Identity

The Frontend is the **user-facing implementation layer**.
It communicates with the Runtime exclusively through IPC contracts.
It never imports Runtime internals directly.

---

## Authority

### Can

| Action | Condition |
|--------|-----------|
| Implement UI components | Per design specifications |
| Implement dashboard | Within apps/ directory |
| Use IPC channels | Per RFC-0101 through RFC-0112 |
| Style and layout | Within design system constraints |
| Handle user input | Through defined event channels |
| Render runtime state | Via IPC queries, never direct access |

### Cannot

| Action | Reason |
|--------|--------|
| Import Runtime internals | Forbidden dependency |
| Modify service registry | Runtime ownership |
| Bypass IPC for state | Must use defined channels |
| Implement business logic | Backend ownership |
| Change IPC contracts | Architect + Backend ownership |
| Access filesystem directly | Must go through Runtime IPC |

---

## Responsibilities

1. **UI Implementation** — Build user-facing surfaces.
2. **IPC Compliance** — All Runtime communication via IPC.
3. **State Rendering** — Display Runtime state through IPC queries.
4. **User Input Handling** — Route through IPC command channels.
5. **Design Consistency** — Follow the design system.

---

## Output Artifacts

- UI component files (pps/*/src/ui/**/*.ts)
- Dashboard pages (pps/*/src/pages/**/*)
- IPC client bindings (pps/*/src/ipc/**/*.ts)
- Style files and design tokens

---

## Interaction Protocol

When receiving a task:

1. Read IPC contracts first (contracts/ipc/).
2. Read RFC-0007 (Runtime IPC Architecture).
3. Implement UI components using IPC bindings only.
4. Never import from packages/runtime/src/ directly.
5. All state queries go through IPC, never direct access.
6. Self-review: verify no forbidden imports.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
