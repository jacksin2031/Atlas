//! Metrics integration — message counts, latency, queue sizes, errors.

pub mod recorders;
pub mod service;

pub use recorders::*;
pub use service::*;
