//! IPC Message Model — RFC-0102.
//!
//! Defines the immutable message envelope, header, payload, metadata,
//! message types, priorities, and validation rules used throughout the
//! Atlas IPC runtime.

pub mod envelope;
pub mod header;
pub mod metadata;
pub mod payload;
pub mod priority;
pub mod types;
pub mod validation;

// Re-export all public types for convenient access.
pub use envelope::*;
pub use header::*;
pub use metadata::*;
pub use payload::*;
pub use priority::*;
pub use types::*;
pub use validation::*;
