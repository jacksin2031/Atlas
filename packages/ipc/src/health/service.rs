//! IPC health service - exposes health states for the IPC runtime.

use serde::{Deserialize, Serialize};

/// IPC health states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
pub enum IpcHealthState {
    #[default]
    Healthy,
    Busy,
    Disconnected,
    Recovering,
    Failed,
}

impl IpcHealthState {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Healthy => "healthy",
            Self::Busy => "busy",
            Self::Disconnected => "disconnected",
            Self::Recovering => "recovering",
            Self::Failed => "failed",
        }
    }

    pub fn is_healthy(&self) -> bool {
        matches!(self, Self::Healthy)
    }
}

/// Aggregate health status for the IPC subsystem.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IpcHealthStatus {
    pub state: IpcHealthState,
    pub router_healthy: bool,
    pub channels_healthy: bool,
    pub sessions_healthy: bool,
    pub endpoints_healthy: bool,
    pub last_check_epoch: u64,
    pub details: String,
}

impl IpcHealthStatus {
    pub fn new() -> Self {
        Self {
            state: IpcHealthState::Healthy,
            router_healthy: true,
            channels_healthy: true,
            sessions_healthy: true,
            endpoints_healthy: true,
            last_check_epoch: 0,
            details: String::new(),
        }
    }

    pub fn mark_router_unhealthy(&mut self) {
        self.router_healthy = false;
        self.state = IpcHealthState::Failed;
        self.details = "Router unhealthy".into();
    }

    pub fn mark_all_healthy(&mut self) {
        self.router_healthy = true;
        self.channels_healthy = true;
        self.sessions_healthy = true;
        self.endpoints_healthy = true;
        self.state = IpcHealthState::Healthy;
        self.details = String::new();
    }

    pub fn is_healthy(&self) -> bool {
        self.state.is_healthy()
            && self.router_healthy
            && self.channels_healthy
            && self.sessions_healthy
            && self.endpoints_healthy
    }
}

impl Default for IpcHealthStatus {
    fn default() -> Self {
        Self::new()
    }
}

/// Health check service for the IPC runtime.
pub struct IpcHealthService {
    status: std::sync::Mutex<IpcHealthStatus>,
}

impl IpcHealthService {
    pub fn new() -> Self {
        Self {
            status: std::sync::Mutex::new(IpcHealthStatus::new()),
        }
    }

    pub fn get_status(&self) -> IpcHealthStatus {
        let status = self.status.lock().unwrap();
        status.clone()
    }

    pub fn update_status<F>(&self, f: F)
    where
        F: FnOnce(&mut IpcHealthStatus),
    {
        let mut status = self.status.lock().unwrap();
        f(&mut status);
    }
}

impl Default for IpcHealthService {
    fn default() -> Self {
        Self::new()
    }
}
