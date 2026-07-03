//! Plugin configuration (RFC-0222).
//!
//! Plugins receive an **immutable** configuration. Configuration MUST be
//! validated before initialization, and becomes immutable (frozen) after the
//! plugin reaches the `Started` state (RFC-0222 §4, Plugin Runtime scope).
//!
//! [`PluginConfig`] uses interior mutability so it can be shared via dependency
//! injection while still enforcing the freeze rule through `&self` accessors.

use crate::error::ConfigError;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashSet;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;

/// Immutable, validated plugin configuration.
pub struct PluginConfig {
    values: Mutex<serde_json::Map<String, Value>>,
    required_keys: HashSet<String>,
    frozen: AtomicBool,
}

impl PluginConfig {
    /// Create a new configuration from a JSON object map.
    pub fn new(values: serde_json::Map<String, Value>) -> Self {
        Self { values: Mutex::new(values), required_keys: HashSet::new(), frozen: AtomicBool::new(false) }
    }

    /// Create a configuration declaring `required_keys` that must be present.
    pub fn with_required(values: serde_json::Map<String, Value>, required_keys: Vec<String>) -> Self {
        Self {
            values: Mutex::new(values),
            required_keys: required_keys.into_iter().collect(),
            frozen: AtomicBool::new(false),
        }
    }

    /// Validate that all required keys are present and values are non-null.
    /// MUST be called before initialization (RFC-0222 §12).
    pub fn validate(&self) -> Result<(), ConfigError> {
        let values = self.values.lock().expect("plugin config mutex poisoned");
        for key in &self.required_keys {
            match values.get(key) {
                None => return Err(ConfigError::MissingKey(key.clone())),
                Some(Value::Null) => return Err(ConfigError::InvalidValue {
                    key: key.clone(),
                    value: "null".to_string(),
                }),
                _ => {}
            }
        }
        Ok(())
    }

    /// Freeze the configuration so further mutations are rejected.
    /// Called after the plugin reaches `Started` (RFC-0222 §4).
    pub fn freeze(&self) {
        self.frozen.store(true, Ordering::Release);
    }

    /// Whether the configuration is frozen (immutable).
    pub fn is_frozen(&self) -> bool {
        self.frozen.load(Ordering::Acquire)
    }

    /// Get a configuration value. Returns a clone (immutable access).
    pub fn get(&self, key: &str) -> Option<Value> {
        self.values.lock().expect("plugin config mutex poisoned").get(key).cloned()
    }

    /// Set a configuration value. Rejected once frozen.
    pub fn set(&self, key: &str, value: Value) -> Result<(), ConfigError> {
        if self.is_frozen() {
            return Err(ConfigError::Frozen);
        }
        self.values.lock().expect("plugin config mutex poisoned").insert(key.to_string(), value);
        Ok(())
    }

    /// The number of configuration entries.
    pub fn len(&self) -> usize {
        self.values.lock().expect("plugin config mutex poisoned").len()
    }

    /// Whether the configuration contains no entries.
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    /// Serialize the configuration to a JSON object.
    pub fn to_json(&self) -> Value {
        Value::Object(self.values.lock().expect("plugin config mutex poisoned").clone())
    }
}

/// A serializable snapshot of plugin configuration (for export/import, §16).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PluginConfigSnapshot {
    pub values: serde_json::Map<String, Value>,
    pub required_keys: Vec<String>,
}

impl PluginConfig {
    /// Export an immutable snapshot of the configuration.
    pub fn snapshot(&self) -> PluginConfigSnapshot {
        PluginConfigSnapshot {
            values: self.values.lock().expect("plugin config mutex poisoned").clone(),
            required_keys: self.required_keys.iter().cloned().collect(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn map() -> serde_json::Map<String, Value> {
        let mut m = serde_json::Map::new();
        m.insert("key".to_string(), json!("value"));
        m
    }

    #[test]
    fn test_get_and_set() {
        let cfg = PluginConfig::new(map());
        assert_eq!(cfg.get("key"), Some(json!("value")));
        assert!(cfg.get("missing").is_none());
        cfg.set("new", json!(42)).unwrap();
        assert_eq!(cfg.get("new"), Some(json!(42)));
    }

    #[test]
    fn test_freeze_blocks_mutation() {
        let cfg = PluginConfig::new(map());
        assert!(!cfg.is_frozen());
        cfg.freeze();
        assert!(cfg.is_frozen());
        assert!(matches!(cfg.set("x", json!(1)).unwrap_err(), ConfigError::Frozen));
    }

    #[test]
    fn test_validate_missing_required_key() {
        let cfg = PluginConfig::with_required(map(), vec!["missing".to_string()]);
        assert!(matches!(cfg.validate().unwrap_err(), ConfigError::MissingKey(_)));
    }

    #[test]
    fn test_validate_null_required_key() {
        let mut m = map();
        m.insert("k".to_string(), Value::Null);
        let cfg = PluginConfig::with_required(m, vec!["k".to_string()]);
        assert!(matches!(cfg.validate().unwrap_err(), ConfigError::InvalidValue { .. }));
    }

    #[test]
    fn test_validate_passes() {
        let cfg = PluginConfig::with_required(map(), vec!["key".to_string()]);
        assert!(cfg.validate().is_ok());
    }

    #[test]
    fn test_snapshot() {
        let cfg = PluginConfig::with_required(map(), vec!["key".to_string()]);
        let snap = cfg.snapshot();
        assert_eq!(snap.values.get("key"), Some(&json!("value")));
        assert_eq!(snap.required_keys, vec!["key".to_string()]);
    }

    #[test]
    fn test_len_and_is_empty() {
        let empty = PluginConfig::new(serde_json::Map::new());
        assert!(empty.is_empty());
        let cfg = PluginConfig::new(map());
        assert_eq!(cfg.len(), 1);
    }

    #[test]
    fn test_to_json() {
        let cfg = PluginConfig::new(map());
        let v = cfg.to_json();
        assert!(v.is_object());
    }
}

