//! Event types for the IPC event bus bridge.

use serde::{Deserialize, Serialize};

/// Types of events that flow through the IPC event bus.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum IpcEventType {
    Runtime(RuntimeEvent),
    Plugin(PluginEvent),
    Workflow(WorkflowEvent),
    System(SystemEvent),
    External(ExternalEvent),
}

/// Epoch-based timestamp.
type EpochTime = u64;

/// Runtime events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RuntimeEvent {
    pub event_kind: RuntimeEventKind,
    pub timestamp_epoch: EpochTime,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RuntimeEventKind {
    Started,
    Stopped,
    Paused,
    Resumed,
    ConfigChanged,
    ServiceRegistered,
    ServiceDeregistered,
}

/// Plugin events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PluginEvent {
    pub plugin_id: String,
    pub event_kind: PluginEventKind,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PluginEventKind {
    Loaded,
    Unloaded,
    Error,
    HealthCheck,
    MessageReceived,
}

/// Workflow events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct WorkflowEvent {
    pub workflow_id: String,
    pub event_kind: WorkflowEventKind,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum WorkflowEventKind {
    Started,
    Completed,
    Failed,
    Paused,
    Resumed,
    StateChanged,
}

/// System events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SystemEvent {
    pub event_kind: SystemEventKind,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SystemEventKind {
    HealthCheck,
    MetricsSnapshot,
    ConfigReload,
    SecurityAlert,
}

/// External events.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExternalEvent {
    pub source: String,
    pub event_kind: String,
    pub data: serde_json::Value,
}
