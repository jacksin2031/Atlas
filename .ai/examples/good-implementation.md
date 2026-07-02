# Example: Good Implementation

> **Purpose**: Template for implementations that pass review on first submission.
> **Reference**: coding-standard.md, engineering.md for full guidelines.

---

## Implementation Checklist

Before submitting any implementation:

### Structure
- [ ] Interfaces defined before implementations (contracts/ first)
- [ ] Shared types in packages/common/
- [ ] Module-level single responsibility
- [ ] No cross-module coupling beyond dependency graph
- [ ] No circular dependencies

### Code Quality
- [ ] No TODO comments
- [ ] No placeholder implementations
- [ ] No dead code
- [ ] No unused imports
- [ ] No global mutable state
- [ ] No static mutable state
- [ ] No service locator pattern
- [ ] Dependency injection used throughout
- [ ] All public functions have tests

### Testing
- [ ] Unit tests for every public function
- [ ] Lifecycle tests for state machines
- [ ] Failure tests for error paths
- [ ] Integration tests for cross-module flows
- [ ] All tests pass locally

### Conformance
- [ ] Follows governing RFC exactly
- [ ] Naming follows coding-standard.md
- [ ] Performance within RFC budgets
- [ ] Security standards met
- [ ] No forbidden imports

---

## Example: Good Module Structure

`
packages/runtime/src/lifecycle/
├── mod.rs          # FSM implementation + exports
├── state.rs        # RuntimeState enum
├── transition.rs   # TransitionGuard + validation
├── error.rs        # StateTransitionError types
├── event.rs        # Lifecycle event definitions
└── test.rs         # Module tests
`

Each file has:
- Clear module-level doc comment
- Public API documented
- Tests in the same file or dedicated test module
- No hidden coupling to other modules

---

## Example: Good Function

`ust
/// Transitions the runtime to the target state.
///
/// # Arguments
/// * 	arget — The state to transition to.
///
/// # Errors
/// Returns StateTransitionError if:
/// - The current state cannot transition to 	arget
/// - The transition would violate an invariant
///
/// # Panics
/// Never panics. All errors are returned.
pub fn transition(&mut self, target: RuntimeState) -> Result<(), StateTransitionError> {
    self.validate_transition(&target)?;
    let old_state = self.state.clone();
    self.state = target.clone();
    self.publish_transition_event(&old_state, &target)?;
    Ok(())
}
`

Good functions have:
- Doc comment with description, arguments, errors, panics
- Clear return type
- Error handling that never panics
- Side effects documented

---

## Anti-Patterns to Avoid

| Anti-Pattern | Bad Example | Good Example |
|-------------|-------------|--------------|
| Global state | static mut CONFIG: Config | Config passed via constructor |
| Service locator | get_service("event_bus") | event_bus: Arc<dyn EventBus> in constructor |
| Silent failure | if err { return; } | eturn Err(Error::EventBus(err)) |
| Magic numbers | if queue.len() > 800 | if queue.len() > QUEUE_WATERMARK |
| God function | 500-line n main() | Split into small, testable functions |

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
