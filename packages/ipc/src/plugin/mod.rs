//! Plugin integration — ensures plugins communicate only through IPC abstractions.

pub mod bridge;
pub mod integration;

pub use bridge::*;
pub use integration::*;
