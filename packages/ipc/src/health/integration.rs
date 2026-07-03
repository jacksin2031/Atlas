//! Integration with Runtime Health Service.

use super::service::{IpcHealthService, IpcHealthStatus};

/// Integrates IPC health with the runtime health service.
pub struct HealthIntegration {
    ipc_health: IpcHealthService,
}

impl HealthIntegration {
    pub fn new() -> Self {
        Self {
            ipc_health: IpcHealthService::new(),
        }
    }

    pub fn get_health(&self) -> IpcHealthStatus {
        self.ipc_health.get_status()
    }

    pub fn report_degradation(&self, reason: &str) {
        self.ipc_health.update_status(|status| {
            status.state = super::service::IpcHealthState::Busy;
            status.details = reason.into();
        });
    }

    pub fn report_recovery(&self) {
        self.ipc_health.update_status(|status| {
            status.state = super::service::IpcHealthState::Healthy;
            status.details = String::new();
        });
    }
}

impl Default for HealthIntegration {
    fn default() -> Self {
        Self::new()
    }
}
