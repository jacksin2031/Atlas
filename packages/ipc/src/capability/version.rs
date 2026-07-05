//! Semantic version matching for capability negotiation.

use serde::{Deserialize, Serialize};

/// Semantic version component.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Version {
    pub major: u32,
    pub minor: u32,
    pub patch: u32,
}

impl Version {
    pub fn new(major: u32, minor: u32, patch: u32) -> Self {
        Self { major, minor, patch }
    }

    /// Parse a version string like "1.2.3".
    pub fn parse(version_str: &str) -> Option<Self> {
        let parts: Vec<&str> = version_str.split('.').collect();
        if parts.len() < 2 {
            return None;
        }
        let major = parts[0].parse().ok()?;
        let minor = parts[1].parse().ok()?;
        let patch = parts.get(2).and_then(|p| p.parse().ok()).unwrap_or(0);
        Some(Self { major, minor, patch })
    }
}

impl Default for Version {
    fn default() -> Self {
        Self::new(1, 0, 0)
    }
}

impl core::fmt::Display for Version {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)
    }
}

/// Version range for compatibility checking.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VersionRange {
    pub min: Version,
    pub max: Version,
}

impl VersionRange {
    /// Create a version range.
    pub fn new(min: Version, max: Version) -> Self {
        Self { min, max }
    }

    /// Create a range with only a minimum version.
    pub fn at_least(min: Version) -> Self {
        Self {
            min,
            max: Version::new(u32::MAX, u32::MAX, u32::MAX),
        }
    }

    /// Check if a version falls within this range.
    pub fn contains(&self, version: &Version) -> bool {
        version.major > self.min.major
            || (version.major == self.min.major && version.minor > self.min.minor)
            || (version.major == self.min.major && version.minor == self.min.minor && version.patch >= self.min.patch)
            && (
                version.major < self.max.major
                || (version.major == self.max.major && version.minor < self.max.minor)
                || (version.major == self.max.major && version.minor == self.max.minor && version.patch <= self.max.patch)
            )
    }

    /// Check backward compatibility: can version N communicate with version N-1?
    pub fn is_backward_compatible(&self, v1: &Version, v2: &Version) -> bool {
        v1.major == v2.major
    }

    /// Check forward compatibility: can version N communicate with version N+1?
    pub fn is_forward_compatible(&self, v1: &Version, v2: &Version) -> bool {
        v1.major == v2.major
    }
}

/// Version matcher for comparing endpoint versions.
pub struct VersionMatcher;

impl VersionMatcher {
    /// Check if two versions are compatible (same major version).
    pub fn are_compatible(v1: &Version, v2: &Version) -> bool {
        v1.major == v2.major
    }

    /// Check if v1 is greater than or equal to v2.
    pub fn gte(v1: &Version, v2: &Version) -> bool {
        v1.major > v2.major
            || (v1.major == v2.major && v1.minor > v2.minor)
            || (v1.major == v2.major && v1.minor == v2.minor && v1.patch >= v2.patch)
    }

    /// Check if v1 is less than v2.
    pub fn lt(v1: &Version, v2: &Version) -> bool {
        !Self::gte(v1, v2)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_parse() {
        let v = Version::parse("1.2.3").unwrap();
        assert_eq!(v.major, 1);
        assert_eq!(v.minor, 2);
        assert_eq!(v.patch, 3);
    }

    #[test]
    fn test_version_compatible() {
        assert!(VersionMatcher::are_compatible(&Version::new(1, 0, 0), &Version::new(1, 5, 0)));
        assert!(!VersionMatcher::are_compatible(&Version::new(1, 0, 0), &Version::new(2, 0, 0)));
    }

    #[test]
    fn test_version_gte() {
        assert!(VersionMatcher::gte(&Version::new(1, 2, 0), &Version::new(1, 1, 0)));
        assert!(VersionMatcher::gte(&Version::new(2, 0, 0), &Version::new(1, 9, 0)));
        assert!(!VersionMatcher::gte(&Version::new(1, 0, 0), &Version::new(1, 1, 0)));
    }
}