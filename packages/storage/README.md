# packages/storage

## Purpose

The Atlas Storage Foundation — abstract storage provider registry and
lifecycle state machines. This crate exposes **abstract providers and
registries only**; it contains **no database-specific logic**.

Implemented components:

- **`ProviderRegistryImpl`** — concrete `ProviderRegistry` implementation that
  discovers, registers, activates, and deactivates storage providers; enforces
  the provider lifecycle state machine (RFC-0403 §5); and performs
  capability-based provider selection (RFC-0403 §6.2 / §7).
- **`ProviderLifecycleManager`** — enforces the provider state machine
  (RFC-0403 §5.2–§5.3) with legal-transition validation.
- **`ResourceManager`** — enforces the resource lifecycle state machine
  (RFC-0404 §8) with atomic, legal-transition validation.

Concrete backends implement the `StorageProvider` trait (defined in
`atlas-contracts`); this crate provides only the platform-side registry and
lifecycle enforcement. No global mutable state is used — all state is held
behind `Mutex`es inside owned instances shared via dependency injection.

## Ownership

Storage team

## Dependencies

- `packages/contracts` (storage provider/registry traits)
- `packages/common` (re-exported storage types)

## Related RFCs

- RFC-0401 (Storage Overview)
- RFC-0402 (Storage Architecture)
- RFC-0403 (Storage Provider)
- RFC-0404 (Storage Lifecycle)

## Testing

Integration tests in `tests/storage_tests.rs` exercise the registry,
provider lifecycle, and resource lifecycle using an in-memory mock provider.
Run with `cargo test -p atlas-storage`.
