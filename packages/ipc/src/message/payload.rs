//! Message payload with typed support.

use serde::{Deserialize, Serialize};
use serde_json::Value;

/// Typed message payload.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MessagePayload {
    data: Value,
}

impl MessagePayload {
    pub fn new<T: Serialize>(value: T) -> Result<Self, PayloadError> {
        let data = serde_json::to_value(value).map_err(|e| PayloadError::Serialization(e.to_string()))?;
        Ok(Self { data })
    }

    pub fn empty() -> Self {
        Self { data: Value::Null }
    }

    pub fn from_value(value: Value) -> Self {
        Self { data: value }
    }

    pub fn from_str(json: &str) -> Result<Self, PayloadError> {
        let value = serde_json::from_str(json).map_err(|e| PayloadError::Deserialize(e.to_string()))?;
        Ok(Self { data: value })
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
        serde_json::from_value(self.data.clone()).map_err(|e| PayloadError::Deserialize(e.to_string()))
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
        Self { data: Value::String(s.to_string()) }
    }
}

impl From<String> for MessagePayload {
    fn from(s: String) -> Self {
        Self { data: Value::String(s) }
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
