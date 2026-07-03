//! IPC Message Model — RFC-0102.
//!
//! Defines the immutable message envelope, header, payload, metadata,
//! message types, priorities, and validation rules used throughout the
//! Atlas IPC runtime.

pub mod types;
pub mod priority;
pub mod header;
pub mod payload;
pub mod metadata;
pub mod envelope;
pub mod validation;

// Re-export all public types for convenient access.
pub use types::*;
pub use priority::*;
pub use header::*;
pub use payload::*;
pub use metadata::*;
pub use envelope::*;
pub use validation::*;
