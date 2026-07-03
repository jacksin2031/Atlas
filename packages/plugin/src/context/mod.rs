//! Plugin context (RFC-0209).
//!
//! [`PluginContext`] is the only handle a plugin receives to interact with the
//! platform. It provides a logger, metrics recorder, immutable configuration,
//! capability registry, event bus, health monitor, optional storage access,
//! and a service directory. No plugin may access Runtime internals directly
//! (RFC-0209 §6): every capability is exposed through this context.
//!
//! All members are shared via [`Arc`] trait objects so the context is [`Send`]
//! + [`Sync`] and constructed by the platform (the `PluginHost`).

use crate::capability::{CapabilityRegistry, PluginCapability, PluginId};
use crate::config::PluginConfig;
use crate::error::PluginError;
use crate::health::PluginHealthMonitor;
use atlas_contracts::{MetricsRecorder, StorageProvider};
use std::sync::Arc;
use std::sync::Mutex;

/// Logger contract provided to plugins (RFC-0209).
pub trait PluginLogger: Send + Sync {
    fn debug(&self, plugin_id: &str, msg: &str);
    fn info(&self, plugin_id: &str, msg: &str);
    fn warn(&self, plugin_id: &str, msg: &str);
    fn error(&self, plugin_id: &str, msg: &str);
}

/// A simple logger that writes to the platform tracing substrate.
pub struct TracingLogger;

impl PluginLogger for TracingLogger {
    fn debug(&self, plugin_id: &str, msg: &str) {
        tracing::debug!("[{plugin_id}] {msg}");
    }
    fn info(&self, plugin_id: &str, msg: &str) {
        tracing::info!("[{plugin_id}] {msg}");
    }
    fn warn(&self, plugin_id: &str, msg: &str) {
        tracing::warn!("[{plugin_id}] {msg}");
    }
    fn error(&self, plugin_id: &str, msg: &str) {
        tracing::error!("[{plugin_id}] {msg}");
    }
}

/// A logger that captures messages in memory — used for testing and diagnostics.
pub struct CapturingLogger {
    messages: Mutex<Vec<(String, String, String)>>,
}

impl CapturingLogger {
    pub fn new() -> Self {
        Self { messages: Mutex::new(Vec::new()) }
    }
    pub fn messages(&self) -> Vec<(String, String, String)> {
        self.messages.lock().expect("capturing logger mutex poisoned").clone()
    }
}

impl Default for CapturingLogger {
    fn default() -> Self {
        Self::new()
    }
}

impl PluginLogger for CapturingLogger {
    fn debug(&self, plugin_id: &str, msg: &str) {
        self.messages
            .lock()
            .expect("capturing logger mutex poisoned")
            .push(("debug".to_string(), plugin_id.to_string(), msg.to_string()));
    }
    fn info(&self, plugin_id: &str, msg: &str) {
        self.messages
            .lock()
            .expect("capturing logger mutex poisoned")
            .push(("info".to_string(), plugin_id.to_string(), msg.to_string()));
    }
    fn warn(&self, plugin_id: &str, msg: &str) {
        self.messages
            .lock()
            .expect("capturing logger mutex poisoned")
            .push(("warn".to_string(), plugin_id.to_string(), msg.to_string()));
    }
    fn error(&self, plugin_id: &str, msg: &str) {
        self.messages
            .lock()
            .expect("capturing logger mutex poisoned")
            .push(("error".to_string(), plugin_id.to_string(), msg.to_string()));
    }
}

/// Read-only service directory exposed to plugins (RFC-0209 §6).
///
/// Lets a plugin locate capability providers without direct access to the
/// registry internals.
pub trait PluginServiceDirectory: Send + Sync {
    /// Return the IDs of plugins providing `capability`.
    fn providers_of(&self, capability: &PluginCapability) -> Vec<String>;
    /// Return the IDs of all known plugins/services.
    fn service_ids(&self) -> Vec<String>;
}

/// A service directory backed by a [`CapabilityRegistry`].
pub struct CapabilityServiceDirectory {
    registry: Arc<dyn CapabilityRegistry>,
}

impl CapabilityServiceDirectory {
    pub fn new(registry: Arc<dyn CapabilityRegistry>) -> Self {
        Self { registry }
    }
}

impl PluginServiceDirectory for CapabilityServiceDirectory {
    fn providers_of(&self, capability: &PluginCapability) -> Vec<String> {
        self.registry.providers(capability)
    }
    fn service_ids(&self) -> Vec<String> {
        // Derive known plugin ids from all registered capabilities.
        let caps = self.registry.list_all();
        let mut ids: Vec<PluginId> = Vec::new();
        for cap in caps {
            for id in self.registry.providers(&cap) {
                if !ids.contains(&id) {
                    ids.push(id);
                }
            }
        }
        ids.sort();
        ids
    }
}

/// The handle a plugin receives to interact with the platform (RFC-0209).
///
/// Constructed by the `PluginHost` and passed to [`crate::contracts::Plugin::initialize`].
/// Every member is a shared, dependency-injected service — no Runtime internals
/// are reachable from a plugin.
pub struct PluginContext {
    /// The id of the plugin this context belongs to.
    pub plugin_id: String,
    pub logger: Arc<dyn PluginLogger>,
    pub metrics: Arc<dyn MetricsRecorder>,
    pub config: Arc<PluginConfig>,
    pub capabilities: Arc<dyn CapabilityRegistry>,
    pub event_bus: Arc<crate::events::PluginEventBusImpl>,
    pub health: Arc<dyn PluginHealthMonitor>,
    pub storage: Option<Arc<dyn StorageProvider>>,
    pub services: Arc<dyn PluginServiceDirectory>,
}

impl PluginContext {
    /// The plugin id this context is scoped to.
    pub fn plugin_id(&self) -> &str {
        &self.plugin_id
    }

    /// Builder for [`PluginContext`].
    pub fn builder(plugin_id: impl Into<String>) -> PluginContextBuilder {
        PluginContextBuilder::new(plugin_id)
    }
}

/// Builder for [`PluginContext`].
pub struct PluginContextBuilder {
    plugin_id: String,
    logger: Option<Arc<dyn PluginLogger>>,
    metrics: Option<Arc<dyn MetricsRecorder>>,
    config: Option<Arc<PluginConfig>>,
    capabilities: Option<Arc<dyn CapabilityRegistry>>,
    event_bus: Option<Arc<crate::events::PluginEventBusImpl>>,
    health: Option<Arc<dyn PluginHealthMonitor>>,
    storage: Option<Arc<dyn StorageProvider>>,
    services: Option<Arc<dyn PluginServiceDirectory>>,
}

impl PluginContextBuilder {
    pub fn new(plugin_id: impl Into<String>) -> Self {
        Self {
            plugin_id: plugin_id.into(),
            logger: None,
            metrics: None,
            config: None,
            capabilities: None,
            event_bus: None,
            health: None,
            storage: None,
            services: None,
        }
    }

    pub fn logger(mut self, logger: Arc<dyn PluginLogger>) -> Self {
        self.logger = Some(logger);
        self
    }
    pub fn metrics(mut self, metrics: Arc<dyn MetricsRecorder>) -> Self {
        self.metrics = Some(metrics);
        self
    }
    pub fn config(mut self, config: Arc<PluginConfig>) -> Self {
        self.config = Some(config);
        self
    }
    pub fn capabilities(mut self, capabilities: Arc<dyn CapabilityRegistry>) -> Self {
        self.capabilities = Some(capabilities);
        self
    }
    pub fn event_bus(mut self, event_bus: Arc<crate::events::PluginEventBusImpl>) -> Self {
        self.event_bus = Some(event_bus);
        self
    }
    pub fn health(mut self, health: Arc<dyn PluginHealthMonitor>) -> Self {
        self.health = Some(health);
        self
    }
    pub fn storage(mut self, storage: Arc<dyn StorageProvider>) -> Self {
        self.storage = Some(storage);
        self
    }
    pub fn services(mut self, services: Arc<dyn PluginServiceDirectory>) -> Self {
        self.services = Some(services);
        self
    }

    /// Build the context, supplying defaults for any unset services.
    pub fn build(self) -> Result<PluginContext, PluginError> {
        let capabilities = self
            .capabilities
            .unwrap_or_else(|| Arc::new(crate::capability::CapabilityRegistryImpl::new()));
        let event_bus = self
            .event_bus
            .unwrap_or_else(|| Arc::new(crate::events::PluginEventBusImpl::new()));
        Ok(PluginContext {
            plugin_id: self.plugin_id,
            logger: self.logger.unwrap_or_else(|| Arc::new(TracingLogger)),
            metrics: self.metrics.unwrap_or_else(|| Arc::new(NullMetrics)),
            config: self.config.unwrap_or_else(|| Arc::new(PluginConfig::new(serde_json::Map::new()))),
            capabilities,
            event_bus,
            health: self.health.unwrap_or_else(|| Arc::new(crate::health::PluginHealthServiceImpl::new())),
            storage: self.storage,
            services: self.services.unwrap_or_else(|| Arc::new(CapabilityServiceDirectory::new(Arc::new(
                crate::capability::CapabilityRegistryImpl::new(),
            )))),
        })
    }
}

/// A no-op metrics recorder used as a default context member.
struct NullMetrics;

impl MetricsRecorder for NullMetrics {
    fn register_counter(&self, _name: &str, _description: &str) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn register_gauge(&self, _name: &str, _description: &str) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn register_histogram(
        &self,
        _name: &str,
        _description: &str,
        _buckets: Vec<f64>,
    ) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn increment(&self, _name: &str, _by: u64) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn set_gauge(&self, _name: &str, _value: f64) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn observe(&self, _name: &str, _value: f64) -> Result<(), atlas_common::MetricsError> {
        Ok(())
    }
    fn snapshot(&self) -> Vec<atlas_common::MetricSnapshot> {
        Vec::new()
    }
    fn list_metrics(&self) -> Vec<atlas_common::MetricDescriptor> {
        Vec::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_capturing_logger() {
        let log = CapturingLogger::new();
        log.info("p1", "hello");
        log.warn("p1", "careful");
        let msgs = log.messages();
        assert_eq!(msgs.len(), 2);
        assert_eq!(msgs[0].0, "info");
        assert_eq!(msgs[1].0, "warn");
    }

    #[test]
    fn test_service_directory() {
        let reg = Arc::new(crate::capability::CapabilityRegistryImpl::new());
        reg.register(&"p1".to_string(), &[PluginCapability::Vision]).unwrap();
        reg.register(&"p2".to_string(), &[PluginCapability::OCR]).unwrap();
        let dir = CapabilityServiceDirectory::new(reg);
        assert_eq!(dir.providers_of(&PluginCapability::Vision), vec!["p1".to_string()]);
        let mut ids = dir.service_ids();
        ids.sort();
        assert_eq!(ids, vec!["p1".to_string(), "p2".to_string()]);
    }

    #[test]
    fn test_context_builder_defaults() {
        let ctx = PluginContext::builder("p1").build().unwrap();
        assert_eq!(ctx.plugin_id(), "p1");
        assert!(ctx.storage.is_none());
        // defaults are usable
        ctx.logger.info("p1", "works");
        assert!(ctx.config.is_empty());
    }

    #[test]
    fn test_context_builder_with_storage() {
        let cfg = Arc::new(PluginConfig::new(serde_json::Map::new()));
        let ctx = PluginContext::builder("p1").config(cfg).build().unwrap();
        assert_eq!(ctx.plugin_id, "p1");
    }
}




