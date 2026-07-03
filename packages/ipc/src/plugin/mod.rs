//! Plugin integration — ensures plugins communicate only through IPC abstractions.

pub mod integration;
pub mod bridge;

pub use integration::*;
pub use bridge::*;
