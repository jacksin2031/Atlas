//! Serializer factory — creates serializers by format name.

use super::binary_serializer::BinarySerializer;
use super::json_serializer::JsonSerializer;
use super::serializer::{SerializationError, Serializer};
use super::structured_serializer::StructuredSerializer;

/// The supported serialization formats.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SerializerFormat {
    Json,
    Binary,
    Structured,
}

impl SerializerFormat {
    /// Convert from a string name.
    pub fn from_name(name: &str) -> Result<Self, SerializationError> {
        match name {
            "json" => Ok(Self::Json),
            "binary" => Ok(Self::Binary),
            "structured" => Ok(Self::Structured),
            _ => Err(SerializationError::UnsupportedMessageType(name.to_string())),
        }
    }

    /// Convert to a format name string.
    pub fn name(&self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::Binary => "binary",
            Self::Structured => "structured",
        }
    }
}

impl Default for SerializerFormat {
    fn default() -> Self {
        Self::Json
    }
}

/// Factory for creating serializers.
#[derive(Debug, Clone, Default)]
pub struct SerializerFactory;

impl SerializerFactory {
    /// Create a new serializer instance for the given format.
    pub fn create(&self, format: SerializerFormat) -> Box<dyn Serializer> {
        match format {
            SerializerFormat::Json => Box::new(JsonSerializer::new()),
            SerializerFormat::Binary => Box::new(BinarySerializer::new()),
            SerializerFormat::Structured => Box::new(StructuredSerializer::new()),
        }
    }

    /// Create a serializer by format name string.
    pub fn create_by_name(&self, name: &str) -> Result<Box<dyn Serializer>, SerializationError> {
        let format = SerializerFormat::from_name(name)?;
        Ok(self.create(format))
    }

    /// Create the default serializer (JSON).
    pub fn create_default(&self) -> Box<dyn Serializer> {
        self.create(SerializerFormat::default())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_factory_creates_json() {
        let factory = SerializerFactory::default();
        let ser = factory.create(SerializerFormat::Json);
        assert_eq!(ser.format_name(), "json");
    }

    #[test]
    fn test_factory_creates_binary() {
        let factory = SerializerFactory::default();
        let ser = factory.create(SerializerFormat::Binary);
        assert_eq!(ser.format_name(), "binary");
    }

    #[test]
    fn test_factory_creates_structured() {
        let factory = SerializerFactory::default();
        let ser = factory.create(SerializerFormat::Structured);
        assert_eq!(ser.format_name(), "structured");
    }

    #[test]
    fn test_factory_by_name() {
        let factory = SerializerFactory::default();
        let json_ser = factory.create_by_name("json").unwrap();
        assert_eq!(json_ser.format_name(), "json");

        let bin_ser = factory.create_by_name("binary").unwrap();
        assert_eq!(bin_ser.format_name(), "binary");

        let structured_ser = factory.create_by_name("structured").unwrap();
        assert_eq!(structured_ser.format_name(), "structured");

        assert!(factory.create_by_name("unknown").is_err());
    }

    #[test]
    fn test_format_from_name() {
        assert_eq!(
            SerializerFormat::from_name("json").unwrap(),
            SerializerFormat::Json
        );
        assert!(SerializerFormat::from_name("foobar").is_err());
    }
}
