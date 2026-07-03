//! Serialization abstraction — RFC-0106.
//!
//! Defines the `Serializer` trait and reference implementations for JSON,
//! binary, and structured serialization.  No platform-specific libraries
//! are used; all implementations rely only on `serde` + `serde_json`.

pub mod serializer;
pub mod json_serializer;
pub mod binary_serializer;
pub mod structured_serializer;
pub mod factory;

pub use serializer::*;
pub use json_serializer::*;
pub use binary_serializer::*;
pub use structured_serializer::*;
pub use factory::*;
