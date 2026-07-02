//! Configuration loader.

use atlas_common::{ConfigError, AtlasError};

#[derive(Debug)]
pub struct ConfigLoader {
    path: String,
}

impl ConfigLoader {
    pub fn load(path: &str) -> Result<Self, AtlasError> {
        if !std::path::Path::new(path).exists() {
            return Err(ConfigError::FileNotFound(path.to_string()).into());
        }
        Ok(Self {
            path: path.to_string(),
        })
    }

    pub fn path(&self) -> &str {
        &self.path
    }
}
