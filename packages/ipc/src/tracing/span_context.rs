//! Distributed tracing for IPC messages.
//!
//! Provides SpanContext with trace_id, span_id, and parent_span_id.
//! The router auto-propagates trace context on every hop.

use uuid::Uuid;
use serde::{Deserialize, Serialize};

/// A unique identifier — either a trace_id or span_id.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct TraceId(pub String);

impl TraceId {
    pub fn new() -> Self {
        Self(Uuid::new_v4().to_string())
    }
}

impl Default for TraceId {
    fn default() -> Self { Self::new() }
}

impl core::fmt::Display for TraceId {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// A unique span identifier.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct SpanId(pub String);

impl SpanId {
    pub fn new() -> Self {
        Self(Uuid::new_v4().to_string())
    }
}

impl Default for SpanId {
    fn default() -> Self { Self::new() }
}

impl core::fmt::Display for SpanId {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// Propagatable tracing context attached to a message.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpanContext {
    /// Root trace identifier.
    pub trace_id: TraceId,
    /// Current span identifier.
    pub span_id: SpanId,
    /// Parent span identifier, if this span is nested.
    pub parent_span_id: Option<SpanId>,
    /// Sampling decision.
    pub sampled: bool,
}

impl SpanContext {
    /// Create a new root span context.
    pub fn new_root() -> Self {
        Self {
            trace_id: TraceId::new(),
            span_id: SpanId::new(),
            parent_span_id: None,
            sampled: true,
        }
    }

    /// Create a child span from a parent context.
    pub fn child(&self) -> Self {
        Self {
            trace_id: self.trace_id.clone(),
            span_id: SpanId::new(),
            parent_span_id: Some(self.span_id.clone()),
            sampled: self.sampled,
        }
    }

    /// Extract an existing span context from trace/span strings.
    pub fn extract(trace_id: impl Into<String>, span_id: impl Into<String>, parent_span_id: Option<impl Into<String>>) -> Self {
        Self {
            trace_id: TraceId(trace_id.into()),
            span_id: SpanId(span_id.into()),
            parent_span_id: parent_span_id.map(|p| SpanId(p.into())),
            sampled: true,
        }
    }

    /// Check if this context is sampling.
    pub fn is_sampled(&self) -> bool {
        self.sampled
    }
}

impl Default for SpanContext {
    fn default() -> Self { Self::new_root() }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_root() {
        let ctx = SpanContext::new_root();
        assert!(ctx.parent_span_id.is_none());
        assert!(ctx.is_sampled());
    }

    #[test]
    fn test_child_span() {
        let root = SpanContext::new_root();
        let child = root.child();
        assert_eq!(child.trace_id, root.trace_id);
        assert_ne!(child.span_id, root.span_id);
        assert_eq!(child.parent_span_id, Some(root.span_id.clone()));
    }

    #[test]
    fn test_nested_child() {
        let root = SpanContext::new_root();
        let child1 = root.child();
        let child2 = child1.child();
        assert_eq!(child2.trace_id, root.trace_id);
        assert_eq!(child2.parent_span_id, Some(child1.span_id));
    }

    #[test]
    fn test_extract() {
        let ctx = SpanContext::extract("trace-1", "span-1", Some("parent-1"));
        assert_eq!(ctx.trace_id.0, "trace-1");
        assert_eq!(ctx.span_id.0, "span-1");
        assert_eq!(ctx.parent_span_id.unwrap().0, "parent-1");
    }

    #[test]
    fn test_trace_id_display() {
        let tid = TraceId::new();
        let s = format!("{}", tid);
        assert!(!s.is_empty());
    }

    #[test]
    fn test_span_id_display() {
        let sid = SpanId::new();
        let s = format!("{}", sid);
        assert!(!s.is_empty());
    }
}