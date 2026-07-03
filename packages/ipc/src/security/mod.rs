//! Security layer — RFC-0107.
//!
//! Permission validation, authentication abstraction, trust boundaries,
//! origin validation, message integrity, replay protection, and audit.

pub mod permissions;
pub mod authentication;
pub mod trust_boundaries;
pub mod origin_validation;
pub mod message_validation;
pub mod replay_protection;
pub mod authorization;
pub mod audit;

pub use permissions::*;
pub use authentication::*;
pub use trust_boundaries::*;
pub use origin_validation::*;
pub use message_validation::*;
pub use replay_protection::*;
pub use authorization::*;
pub use audit::*;
