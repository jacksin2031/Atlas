//! Event bus bridge — integrates IPC with the Runtime Event Bus.

pub mod bridge;
pub mod events;
pub mod publisher;
pub mod subscriber;

pub use bridge::*;
pub use events::*;
pub use publisher::*;
pub use subscriber::*;
