//! Health Monitor.

use atlas_common::HealthStatus;
use crate::eventbus::EventBusImpl;

pub struct HealthMonitor {
    health_map: std::collections::HashMap<String, HealthStatus>,
}

impl HealthMonitor {
    pub fn new(_event_bus: &EventBusImpl) -> Self {
        Self {
            health_map: std::collections::HashMap::new(),
        }
    }

    pub fn aggregate_health(&self) -> Vec<(String, HealthStatus)> {
        self.health_map
            .iter()
            .map(|(id, status)| (id.clone(), status.clone()))
            .collect()
    }

    pub fn service_health(&self, service_id: &str) -> Option<HealthStatus> {
        self.health_map.get(service_id).cloned()
    }

    pub fn record_health(&mut self, service_id: String, status: HealthStatus) {
        self.health_map.insert(service_id, status);
    }
}

