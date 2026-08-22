//! Semantic versioning for plugins (RFC-0212 §9).
//!
//! Implements Semantic Versioning 2.0.0 parsing, validation, ordering, and
//! version-constraint matching. Version constraints support the operators
//! required by RFC-0226 (dependency resolution): exact (`=`/`==`), caret (`^`),
//! tilde (`~`), comparison (`>=`, `>`, `<=`, `<`), and wildcard (`*`).
//!
//! The module is dependency-free apart from the plugin error types so that
//! manifest validation can reuse it without pulling in execution concerns.

use crate::error::ManifestError;
use serde::{Deserialize, Serialize};
use std::cmp::Ordering;
use std::fmt;

/// A semantic version conforming to SemVer 2.0.0.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SemanticVersion {
    pub major: u64,
    pub minor: u64,
    pub patch: u64,
    #[serde(default)]
    pub pre_release: Option<String>,
    #[serde(default)]
    pub build_metadata: Option<String>,
}

impl SemanticVersion {
    /// Parse a SemVer 2.0.0 string.
    ///
    /// Accepts `MAJOR.MINOR.PATCH`, `MAJOR.MINOR.PATCH-prerelease`, and
    /// `MAJOR.MINOR.PATCH-prerelease+build`. Rejects missing patch segments
    /// (e.g. `1.0`) per AC-0202-004.
    pub fn parse(input: &str) -> Result<Self, ManifestError> {
        let input = input.trim();
        if input.is_empty() {
            return Err(ManifestError::InvalidVersion("empty version".to_string()));
        }

        let (core_and_pre, build_metadata) = match input.split_once('+') {
            Some((c, b)) => {
                if b.is_empty() {
                    return Err(ManifestError::InvalidVersion(format!(
                        "empty build metadata in '{input}'"
                    )));
                }
                (c, Some(b.to_string()))
            }
            None => (input, None),
        };

        let (core, pre_release) = match core_and_pre.split_once('-') {
            Some((c, p)) => {
                if p.is_empty() || !is_valid_pre_release(p) {
                    return Err(ManifestError::InvalidVersion(format!(
                        "invalid pre-release '{p}'"
                    )));
                }
                (c, Some(p.to_string()))
            }
            None => (core_and_pre, None),
        };

        let parts: Vec<&str> = core.split('.').collect();
        if parts.len() != 3 {
            return Err(ManifestError::InvalidVersion(format!(
                "version must have MAJOR.MINOR.PATCH: '{input}'"
            )));
        }
        let major = parse_num(parts[0], "major", input)?;
        let minor = parse_num(parts[1], "minor", input)?;
        let patch = parse_num(parts[2], "patch", input)?;
        Ok(Self {
            major,
            minor,
            patch,
            pre_release,
            build_metadata,
        })
    }

    /// Whether this version has a pre-release identifier.
    pub fn is_pre_release(&self) -> bool {
        self.pre_release.is_some()
    }

    /// Two versions are compatible when they share the same major version
    /// (RFC-0212 §10: backward compatibility within a major version).
    pub fn is_compatible_with(&self, other: &Self) -> bool {
        self.major == other.major
    }

    /// The major version component.
    pub fn major(&self) -> u64 {
        self.major
    }
}

fn parse_num(s: &str, field: &str, input: &str) -> Result<u64, ManifestError> {
    if s.is_empty() {
        return Err(ManifestError::InvalidVersion(format!(
            "empty {field} in '{input}'"
        )));
    }
    if !s.chars().all(|c| c.is_ascii_digit()) {
        return Err(ManifestError::InvalidVersion(format!(
            "non-numeric {field} '{s}' in '{input}'"
        )));
    }
    s.parse::<u64>()
        .map_err(|_| ManifestError::InvalidVersion(format!("overflowing {field} in '{input}'")))
}

fn is_valid_pre_release(s: &str) -> bool {
    s.split('.').all(|ident| {
        !ident.is_empty() && ident.chars().all(|c| c.is_ascii_alphanumeric() || c == '-')
    })
}
impl fmt::Display for SemanticVersion {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)?;
        if let Some(pre) = &self.pre_release {
            write!(f, "-{pre}")?;
        }
        if let Some(build) = &self.build_metadata {
            write!(f, "+{build}")?;
        }
        Ok(())
    }
}

impl PartialOrd for SemanticVersion {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for SemanticVersion {
    fn cmp(&self, other: &Self) -> Ordering {
        self.major
            .cmp(&other.major)
            .then(self.minor.cmp(&other.minor))
            .then(self.patch.cmp(&other.patch))
            .then(cmp_pre_release(&self.pre_release, &other.pre_release))
    }
}

/// Pre-release has lower precedence than a normal release (SemVer §11).
fn cmp_pre_release(a: &Option<String>, b: &Option<String>) -> Ordering {
    match (a, b) {
        (None, None) => Ordering::Equal,
        (None, Some(_)) => Ordering::Greater,
        (Some(_), None) => Ordering::Less,
        (Some(x), Some(y)) => cmp_pre_release_ids(x, y),
    }
}

fn cmp_pre_release_ids(x: &str, y: &str) -> Ordering {
    let xi: Vec<&str> = x.split('.').collect();
    let yi: Vec<&str> = y.split('.').collect();
    for i in 0..xi.len().max(yi.len()) {
        match (xi.get(i), yi.get(i)) {
            (Some(a), Some(b)) => {
                let ord = cmp_ident(a, b);
                if ord != Ordering::Equal {
                    return ord;
                }
            }
            (Some(_), None) => return Ordering::Greater,
            (None, Some(_)) => return Ordering::Less,
            (None, None) => return Ordering::Equal,
        }
    }
    Ordering::Equal
}

fn cmp_ident(a: &str, b: &str) -> Ordering {
    match (a.parse::<u64>(), b.parse::<u64>()) {
        (Ok(x), Ok(y)) => x.cmp(&y),
        (Ok(_), Err(_)) => Ordering::Less,
        (Err(_), Ok(_)) => Ordering::Greater,
        (Err(_), Err(_)) => a.cmp(b),
    }
}
/// A version constraint used in plugin dependencies (RFC-0226 §13).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct VersionConstraint {
    pub operator: ConstraintOperator,
    pub version: Option<SemanticVersion>,
}

/// Supported constraint operators.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ConstraintOperator {
    /// Any version (`*`).
    Any,
    /// Exact match (`=` or `==`).
    Eq,
    /// Compatible with (same major, >= given): caret (`^`).
    Caret,
    /// Approximately equivalent (same major+minor, >= given): tilde (`~`).
    Tilde,
    /// Greater-than-or-equal (`>=`).
    Gte,
    /// Greater-than (`>`).
    Gt,
    /// Less-than-or-equal (`<=`).
    Lte,
    /// Less-than (`<`).
    Lt,
}

impl VersionConstraint {
    /// Parse a constraint expression such as `^1.2.0`, `>=1.0.0`, `*`.
    pub fn parse(expr: &str) -> Result<Self, ManifestError> {
        let expr = expr.trim();
        if expr.is_empty() || expr == "*" {
            return Ok(Self {
                operator: ConstraintOperator::Any,
                version: None,
            });
        }
        let (op_str, ver_str) = split_operator(expr);
        let operator = match op_str {
            "^" => ConstraintOperator::Caret,
            "~" => ConstraintOperator::Tilde,
            ">=" => ConstraintOperator::Gte,
            ">" => ConstraintOperator::Gt,
            "<=" => ConstraintOperator::Lte,
            "<" => ConstraintOperator::Lt,
            "=" | "==" | "" => ConstraintOperator::Eq,
            other => {
                return Err(ManifestError::InvalidVersion(format!(
                    "unknown constraint operator '{other}'"
                )))
            }
        };
        let version = Some(SemanticVersion::parse(ver_str)?);
        Ok(Self { operator, version })
    }

    /// Whether `version` satisfies this constraint.
    pub fn satisfies(&self, version: &SemanticVersion) -> bool {
        let Some(target) = &self.version else {
            return true;
        };
        match self.operator {
            ConstraintOperator::Any => true,
            ConstraintOperator::Eq => version == target,
            ConstraintOperator::Gte => version >= target,
            ConstraintOperator::Gt => version > target,
            ConstraintOperator::Lte => version <= target,
            ConstraintOperator::Lt => version < target,
            ConstraintOperator::Caret => {
                if version < target {
                    return false;
                }
                if target.major > 0 {
                    version.major == target.major
                } else if target.minor > 0 {
                    version.major == 0 && version.minor == target.minor
                } else {
                    version.major == 0 && version.minor == 0 && version.patch == target.patch
                }
            }
            ConstraintOperator::Tilde => {
                if version < target {
                    return false;
                }
                version.major == target.major && version.minor == target.minor
            }
        }
    }
}

impl fmt::Display for VersionConstraint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let op = match self.operator {
            ConstraintOperator::Any => return write!(f, "*"),
            ConstraintOperator::Eq => "=",
            ConstraintOperator::Caret => "^",
            ConstraintOperator::Tilde => "~",
            ConstraintOperator::Gte => ">=",
            ConstraintOperator::Gt => ">",
            ConstraintOperator::Lte => "<=",
            ConstraintOperator::Lt => "<",
        };
        match &self.version {
            Some(v) => write!(f, "{op}{v}"),
            None => write!(f, "{op}"),
        }
    }
}

fn split_operator(expr: &str) -> (&str, &str) {
    for prefix in ["^", "~", ">=", "<=", ">", "<", "==", "="] {
        if let Some(rest) = expr.strip_prefix(prefix) {
            return (prefix, rest.trim());
        }
    }
    ("", expr.trim())
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_full_version() {
        let v = SemanticVersion::parse("1.2.3").unwrap();
        assert_eq!((v.major, v.minor, v.patch), (1, 2, 3));
        assert!(!v.is_pre_release());
    }

    #[test]
    fn test_parse_pre_release_and_build() {
        let v = SemanticVersion::parse("1.0.0-beta+build.123").unwrap();
        assert_eq!(v.pre_release.as_deref(), Some("beta"));
        assert_eq!(v.build_metadata.as_deref(), Some("build.123"));
    }

    #[test]
    fn test_parse_rejects_missing_patch() {
        assert!(SemanticVersion::parse("1.0").is_err());
    }

    #[test]
    fn test_parse_rejects_non_numeric() {
        assert!(SemanticVersion::parse("1.2.x").is_err());
    }

    #[test]
    fn test_ordering() {
        let a = SemanticVersion::parse("1.0.0").unwrap();
        let b = SemanticVersion::parse("1.0.1").unwrap();
        let c = SemanticVersion::parse("2.0.0").unwrap();
        assert!(a < b);
        assert!(b < c);
    }

    #[test]
    fn test_pre_release_lower_than_release() {
        let pre = SemanticVersion::parse("1.0.0-beta").unwrap();
        let rel = SemanticVersion::parse("1.0.0").unwrap();
        assert!(pre < rel);
    }

    #[test]
    fn test_compatible_same_major() {
        let v = SemanticVersion::parse("1.5.0").unwrap();
        assert!(v.is_compatible_with(&SemanticVersion::parse("1.9.9").unwrap()));
        assert!(!v.is_compatible_with(&SemanticVersion::parse("2.0.0").unwrap()));
    }

    #[test]
    fn test_constraint_caret() {
        let c = VersionConstraint::parse("^1.2.0").unwrap();
        assert!(c.satisfies(&SemanticVersion::parse("1.2.0").unwrap()));
        assert!(c.satisfies(&SemanticVersion::parse("1.9.9").unwrap()));
        assert!(!c.satisfies(&SemanticVersion::parse("2.0.0").unwrap()));
        assert!(!c.satisfies(&SemanticVersion::parse("1.1.9").unwrap()));
    }

    #[test]
    fn test_constraint_gte() {
        let c = VersionConstraint::parse(">=1.0.0").unwrap();
        assert!(c.satisfies(&SemanticVersion::parse("1.0.0").unwrap()));
        assert!(c.satisfies(&SemanticVersion::parse("2.0.0").unwrap()));
        assert!(!c.satisfies(&SemanticVersion::parse("0.9.0").unwrap()));
    }

    #[test]
    fn test_constraint_any() {
        let c = VersionConstraint::parse("*").unwrap();
        assert!(c.satisfies(&SemanticVersion::parse("99.0.0").unwrap()));
    }

    #[test]
    fn test_constraint_eq() {
        let c = VersionConstraint::parse("=1.2.3").unwrap();
        assert!(c.satisfies(&SemanticVersion::parse("1.2.3").unwrap()));
        assert!(!c.satisfies(&SemanticVersion::parse("1.2.4").unwrap()));
    }

    #[test]
    fn test_constraint_tilde() {
        let c = VersionConstraint::parse("~1.2.3").unwrap();
        assert!(c.satisfies(&SemanticVersion::parse("1.2.3").unwrap()));
        assert!(c.satisfies(&SemanticVersion::parse("1.2.9").unwrap()));
        assert!(!c.satisfies(&SemanticVersion::parse("1.3.0").unwrap()));
    }

    #[test]
    fn test_constraint_display() {
        assert_eq!(
            VersionConstraint::parse(">=1.0.0").unwrap().to_string(),
            ">=1.0.0"
        );
    }
}
