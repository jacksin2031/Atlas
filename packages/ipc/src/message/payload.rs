//! Message payload with typed support and schema versioning.

use serde::{Deserialize, Serialize};
use serde_json::Value;

/// Typed message payload with optional schema version.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MessagePayload {
    data: Value,
    /// Schema version for this payload (e.g. "v1", "v2.1.0").
    pub schema_version: Option<String>,
}

impl MessagePayload {
    pub fn new<T: Serialize>(value: T) -> Result<Self, PayloadError> {
        let data =
            serde_json::to_value(value).map_err(|e| PayloadError::Serialization(e.to_string()))?;
        Ok(Self {
            data,
            schema_version: None,
        })
    }

    pub fn empty() -> Self {
        Self {
            data: Value::Null,
            schema_version: None,
        }
    }

    pub fn from_value(value: Value) -> Self {
        Self {
            data: value,
            schema_version: None,
        }
    }

    pub fn from_str(json: &str) -> Result<Self, PayloadError> {
        let value =
            serde_json::from_str(json).map_err(|e| PayloadError::Deserialize(e.to_string()))?;
        Ok(Self {
            data: value,
            schema_version: None,
        })
    }

    pub fn with_schema_version(mut self, version: impl Into<String>) -> Self {
        self.schema_version = Some(version.into());
        self
    }

    /// Get the schema version, if set.
    pub fn schema_version(&self) -> Option<&str> {
        self.schema_version.as_deref()
    }

    pub fn as_value(&self) -> &Value {
        &self.data
    }

    pub fn into_value(self) -> Value {
        self.data
    }

    pub fn to_json(&self) -> Result<String, PayloadError> {
        serde_json::to_string(&self.data).map_err(|e| PayloadError::Serialization(e.to_string()))
    }

    pub fn as_str(&self) -> Option<&str> {
        self.data.as_str()
    }

    pub fn as_i64(&self) -> Option<i64> {
        self.data.as_i64()
    }

    pub fn as_bool(&self) -> Option<bool> {
        self.data.as_bool()
    }

    pub fn as_object(&self) -> Option<&serde_json::Map<String, Value>> {
        self.data.as_object()
    }

    pub fn as_array(&self) -> Option<&Vec<Value>> {
        self.data.as_array()
    }

    pub fn is_empty(&self) -> bool {
        matches!(&self.data, Value::Null)
    }

    pub fn deserialize<T: for<'de> Deserialize<'de>>(&self) -> Result<T, PayloadError> {
        serde_json::from_value(self.data.clone())
            .map_err(|e| PayloadError::Deserialize(e.to_string()))
    }
}

impl Default for MessagePayload {
    fn default() -> Self {
        Self::empty()
    }
}

impl From<Value> for MessagePayload {
    fn from(value: Value) -> Self {
        Self::from_value(value)
    }
}

impl From<&str> for MessagePayload {
    fn from(s: &str) -> Self {
        Self {
            data: Value::String(s.to_string()),
            schema_version: None,
        }
    }
}

impl From<String> for MessagePayload {
    fn from(s: String) -> Self {
        Self {
            data: Value::String(s),
            schema_version: None,
        }
    }
}

impl core::fmt::Display for MessagePayload {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.data)
    }
}

/// Errors for payload operations.
#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum PayloadError {
    #[error("serialization failed: {0}")]
    Serialization(String),
    #[error("deserialization failed: {0}")]
    Deserialize(String),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_schema_version() {
        let payload = MessagePayload::new(serde_json::json!({"key": "val"})).unwrap();
        assert!(payload.schema_version().is_none());
        let with_ver = payload.with_schema_version("v1.2.3");
        assert_eq!(with_ver.schema_version(), Some("v1.2.3"));
    }

    #[test]
    fn test_schema_version_empty() {
        let payload = MessagePayload::empty();
        assert!(payload.schema_version().is_none());
    }
}
