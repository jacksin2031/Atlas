//! Runtime lifecycle state definitions.
//!
//! Re-exports from atlas-contracts for convenience.
//! See RFC-0002 §8 (Runtime State Machine).

pub use atlas_contracts::{RuntimeState, is_legal_transition, StateTransitionError, LEGAL_TRANSITIONS};
