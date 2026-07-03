//! Message metadata — routing, tracing, and extension fields.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use super::priority::MessagePriority;

/// Additional metadata attached to a message envelope.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MessageMetadata {
    /// Message priority (overrides header default).
    pub priority: MessagePriority,
    /// Channel identifier the message is routed through.
    pub channel_id: Option<String>,
    /// Trace ID for distributed tracing.
    pub trace_id: Option<String>,
    /// Span ID for distributed tracing.
    pub span_id: Option<String>,
    /// Sequence number for ordering guarantees.
    pub sequence_number: Option<u64>,
    /// Hop count (incremented at each routing hop).
    pub hop_count: u32,
    /// Arbitrary extension key-value pairs.
    pub extensions: HashMap<String, String>,
}

impl MessageMetadata {
    /// Create new metadata with sensible defaults.
    pub fn new() -> Self {
        Self {
            priority: MessagePriority::default(),
            channel_id: None,
            trace_id: None,
            span_id: None,
            sequence_number: None,
            hop_count: 0,
            extensions: HashMap::new(),
        }
    }

    /// Set the priority.
    pub fn with_priority(mut self, priority: MessagePriority) -> Self {
        self.priority = priority;
        self
    }

    /// Set the channel ID.
    pub fn with_channel(mut self, channel_id: impl Into<String>) -> Self {
        self.channel_id = Some(channel_id.into());
        self
    }

    /// Set the trace ID.
    pub fn with_trace(mut self, trace_id: impl Into<String>) -> Self {
        self.trace_id = Some(trace_id.into());
        self
    }

    /// Set the span ID.
    pub fn with_span(mut self, span_id: impl Into<String>) -> Self {
        self.span_id = Some(span_id.into());
        self
    }

    /// Set the sequence number.
    pub fn with_sequence(mut self, seq: u64) -> Self {
        self.sequence_number = Some(seq);
        self
    }

    /// Increment the hop count.
    pub fn increment_hop(&mut self) {
        self.hop_count += 1;
    }

    /// Add an extension field.
    pub fn insert_extension(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.extensions.insert(key.into(), value.into());
        self
    }

    /// Get an extension value.
    pub fn get_extension(&self, key: &str) -> Option<&str> {
        self.extensions.get(key).map(|s| s.as_str())
    }
}

impl Default for MessageMetadata {
    fn default() -> Self {
        Self::new()
    }
}
