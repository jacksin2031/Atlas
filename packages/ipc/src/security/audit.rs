//! Audit trail for security events.

use std::collections::VecDeque;
use std::sync::Arc;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

/// Types of security events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SecurityEventType {
    AuthenticationSuccess,
    AuthenticationFailure,
    AuthorizationDenied,
    TrustBoundaryViolation,
    ReplayAttempt,
    TamperingDetected,
    PermissionEscalation,
    SessionCreated,
    SessionTerminated,
    ChannelCreated,
    ChannelClosed,
    EndpointRegistered,
    EndpointDeregistered,
    MessageValidated,
    MessageRejected,
    Custom { description: String },
}

/// A single audit log entry.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEntry {
    pub timestamp: DateTime<Utc>,
    pub event_type: SecurityEventType,
    pub principal: String,
    pub resource: String,
    pub details: String,
    pub result: AuditResult,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuditResult {
    Success,
    Failure,
    Warning,
}

/// Audit trail - circular buffer of security events.
#[derive(Clone)]
pub struct AuditTrail {
    entries: Arc<std::sync::Mutex<VecDeque<AuditEntry>>>,
    max_entries: usize,
}

impl AuditTrail {
    pub fn new(max_entries: usize) -> Self {
        Self {
            entries: Arc::new(std::sync::Mutex::new(VecDeque::with_capacity(max_entries))),
            max_entries,
        }
    }

    pub fn record(
        &self,
        event_type: SecurityEventType,
        principal: impl Into<String>,
        resource: impl Into<String>,
        details: impl Into<String>,
        result: AuditResult,
    ) {
        let mut entries = self.entries.lock().unwrap();
        entries.push_back(AuditEntry {
            timestamp: Utc::now(),
            event_type,
            principal: principal.into(),
            resource: resource.into(),
            details: details.into(),
            result,
        });
        while entries.len() > self.max_entries {
            entries.pop_front();
        }
    }

    pub fn recent(&self, count: usize) -> Vec<AuditEntry> {
        let entries = self.entries.lock().unwrap();
        entries.iter().rev().take(count).cloned().collect()
    }

    pub fn entries_list(&self) -> Vec<AuditEntry> {
        let entries = self.entries.lock().unwrap();
        entries.iter().cloned().collect()
    }

    pub fn clear(&self) {
        let mut entries = self.entries.lock().unwrap();
        entries.clear();
    }

    pub fn count(&self) -> usize {
        let entries = self.entries.lock().unwrap();
        entries.len()
    }
}

impl Default for AuditTrail {
    fn default() -> Self {
        Self::new(100000)
    }
}
