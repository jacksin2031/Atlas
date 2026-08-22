//! Plugin sandbox abstraction (RFC-0208).
//!
//! Defines the architecture for sandboxed plugin execution: a permission model,
//! resource limits, lifecycle boundaries, and security validation. This module
//! defines the **abstraction only** — it MUST NOT implement any OS-specific
//! sandbox technology (RFC-0208 §3, Plugin Runtime scope). Concrete executors
//! implement the [`SandboxExecutor`] trait; a [`NoopSandboxExecutor`] is
//! provided as a policy-validating default that performs no OS-level isolation.

use crate::error::SandboxError;
use crate::manifest::{PermissionLevel, PluginManifest, PluginPermission, PluginResourceLimits};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;

/// Isolation boundary strength, mapped from a plugin's permission level
/// (RFC-0219 §8: restricted → Maximal, low → Strict, normal → Standard,
/// elevated → Relaxed, privileged → Minimal, trusted → None).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum SandboxBoundary {
    /// No isolation boundary (full trust).
    None,
    /// Minimal isolation.
    Minimal,
    /// Relaxed isolation.
    Relaxed,
    /// Standard isolation.
    Standard,
    /// Strict isolation.
    Strict,
    /// Maximal isolation.
    Maximal,
}

impl SandboxBoundary {
    /// Map a permission level to its isolation boundary.
    pub fn from_permission_level(level: PermissionLevel) -> Self {
        match level {
            PermissionLevel::Trusted => Self::None,
            PermissionLevel::Privileged => Self::Minimal,
            PermissionLevel::Elevated => Self::Relaxed,
            PermissionLevel::Normal => Self::Standard,
            PermissionLevel::Low => Self::Strict,
            PermissionLevel::Restricted => Self::Maximal,
        }
    }
}

/// The sandbox policy derived from a plugin manifest (RFC-0208 §9, RFC-0219).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SandboxPolicy {
    pub permission_level: PermissionLevel,
    pub permissions: Vec<PluginPermission>,
    pub resource_limits: PluginResourceLimits,
}

impl SandboxPolicy {
    /// Derive a sandbox policy from a plugin manifest.
    ///
    /// The effective permission level is the maximum declared permission level
    /// (least-privilege baseline is `Restricted`).
    pub fn from_manifest(manifest: &PluginManifest) -> Self {
        let permission_level = manifest
            .permissions
            .iter()
            .map(|p| p.level)
            .max()
            .unwrap_or(PermissionLevel::Restricted);
        Self {
            permission_level,
            permissions: manifest.permissions.clone(),
            resource_limits: manifest.resource_limits.clone(),
        }
    }

    /// The isolation boundary for this policy.
    pub fn boundary(&self) -> SandboxBoundary {
        SandboxBoundary::from_permission_level(self.permission_level)
    }

    /// Whether a named permission is granted by this policy.
    pub fn allows(&self, name: &str) -> bool {
        self.permissions.iter().any(|p| p.name == name)
    }

    /// The maximum declared permission level.
    pub fn max_permission_level(&self) -> PermissionLevel {
        self.permission_level
    }

    /// Security validation (RFC-0208 §17): the policy must be internally
    /// consistent. A policy whose boundary is weaker than a declared permission
    /// level requires is rejected (a `Trusted` boundary cannot host a
    /// `Restricted` plugin's required permissions safely).
    pub fn validate(&self) -> Result<(), SandboxError> {
        for perm in &self.permissions {
            if perm.required && perm.level > self.permission_level {
                return Err(SandboxError::SecurityValidationFailed(format!(
                    "required permission '{}' at level {:?} exceeds policy level {:?}",
                    perm.name, perm.level, self.permission_level
                )));
            }
        }
        if let Some(mem) = self.resource_limits.max_memory_mb {
            if mem == 0 {
                return Err(SandboxError::SecurityValidationFailed(
                    "max_memory_mb must be greater than zero".to_string(),
                ));
            }
        }
        Ok(())
    }
}

/// A snapshot of resource usage by a plugin, checked against policy limits
/// (RFC-0208 §11).
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct ResourceUsage {
    pub memory_mb: u64,
    pub cpu_cores: u32,
    pub vram_mb: u64,
    pub filesystem_mb: u64,
    pub threads: u32,
}

impl ResourceUsage {
    /// Check this usage against the given resource limits.
    pub fn check_against(&self, limits: &PluginResourceLimits) -> Result<(), SandboxError> {
        if let Some(max) = limits.max_memory_mb {
            if self.memory_mb > max {
                return Err(SandboxError::ResourceLimitExceeded(format!(
                    "memory {} MB exceeds limit {} MB",
                    self.memory_mb, max
                )));
            }
        }
        if let Some(max) = limits.max_cpu_cores {
            if self.cpu_cores > max {
                return Err(SandboxError::ResourceLimitExceeded(format!(
                    "cpu {} cores exceeds limit {}",
                    self.cpu_cores, max
                )));
            }
        }
        if let Some(max) = limits.max_vram_mb {
            if self.vram_mb > max {
                return Err(SandboxError::ResourceLimitExceeded(format!(
                    "vram {} MB exceeds limit {} MB",
                    self.vram_mb, max
                )));
            }
        }
        if let Some(max) = limits.max_filesystem_mb {
            if self.filesystem_mb > max {
                return Err(SandboxError::ResourceLimitExceeded(format!(
                    "filesystem {} MB exceeds limit {} MB",
                    self.filesystem_mb, max
                )));
            }
        }
        if let Some(max) = limits.max_threads {
            if self.threads > max {
                return Err(SandboxError::ResourceLimitExceeded(format!(
                    "threads {} exceeds limit {}",
                    self.threads, max
                )));
            }
        }
        Ok(())
    }
}

/// Abstract sandbox executor contract (RFC-0208 §8).
///
/// Defines the lifecycle boundaries of sandboxed execution: preparing a
/// sandbox for a plugin, enforcing permission and resource checks, and
/// tearing it down. Implementations MUST NOT assume any specific operating
/// system; this trait is the platform-independent boundary.
pub trait SandboxExecutor: Send + Sync {
    /// Prepare a sandbox for `plugin_id` using `policy`. Validates the policy.
    fn prepare(&self, plugin_id: &str, policy: &SandboxPolicy) -> Result<(), SandboxError>;
    /// Check whether `plugin_id` holds `permission`.
    fn check_permission(&self, plugin_id: &str, permission: &str) -> Result<(), SandboxError>;
    /// Check whether `usage` for `plugin_id` is within policy limits.
    fn check_resource(&self, plugin_id: &str, usage: &ResourceUsage) -> Result<(), SandboxError>;
    /// Tear down the sandbox for `plugin_id`.
    fn teardown(&self, plugin_id: &str) -> Result<(), SandboxError>;
    /// Return the boundary currently in effect for `plugin_id`.
    fn boundary(&self, plugin_id: &str) -> Option<SandboxBoundary>;
}

/// A policy-validating executor that performs no OS-level isolation.
///
/// This is the default executor used when no concrete sandbox backend is
/// available. It validates policies and enforces permission/resource checks
/// in-process, satisfying the abstraction contract without OS-specific
/// technology (RFC-0208 §3).
pub struct NoopSandboxExecutor {
    policies: Mutex<HashMap<String, SandboxPolicy>>,
}

impl NoopSandboxExecutor {
    pub fn new() -> Self {
        Self {
            policies: Mutex::new(HashMap::new()),
        }
    }
}

impl Default for NoopSandboxExecutor {
    fn default() -> Self {
        Self::new()
    }
}

impl SandboxExecutor for NoopSandboxExecutor {
    fn prepare(&self, plugin_id: &str, policy: &SandboxPolicy) -> Result<(), SandboxError> {
        policy.validate()?;
        self.policies
            .lock()
            .expect("sandbox policies mutex poisoned")
            .insert(plugin_id.to_string(), policy.clone());
        Ok(())
    }

    fn check_permission(&self, plugin_id: &str, permission: &str) -> Result<(), SandboxError> {
        let policies = self
            .policies
            .lock()
            .expect("sandbox policies mutex poisoned");
        let policy = policies.get(plugin_id).ok_or_else(|| {
            SandboxError::LifecycleViolation(format!("no sandbox for {plugin_id}"))
        })?;
        if policy.allows(permission) {
            Ok(())
        } else {
            Err(SandboxError::PermissionDenied(format!(
                "plugin {plugin_id} lacks permission '{permission}'"
            )))
        }
    }

    fn check_resource(&self, plugin_id: &str, usage: &ResourceUsage) -> Result<(), SandboxError> {
        let policies = self
            .policies
            .lock()
            .expect("sandbox policies mutex poisoned");
        let policy = policies.get(plugin_id).ok_or_else(|| {
            SandboxError::LifecycleViolation(format!("no sandbox for {plugin_id}"))
        })?;
        usage.check_against(&policy.resource_limits)
    }

    fn teardown(&self, plugin_id: &str) -> Result<(), SandboxError> {
        self.policies
            .lock()
            .expect("sandbox policies mutex poisoned")
            .remove(plugin_id);
        Ok(())
    }

    fn boundary(&self, plugin_id: &str) -> Option<SandboxBoundary> {
        self.policies
            .lock()
            .expect("sandbox policies mutex poisoned")
            .get(plugin_id)
            .map(|p| p.boundary())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::capability::{CapabilityDeclaration, PluginCapability};
    use crate::manifest::{
        DependencyType, PluginCompatibility, PluginDependency, PluginManifest, PluginPermission,
        PluginResourceLimits, PluginType,
    };

    fn manifest_with_perms(
        perms: Vec<PluginPermission>,
        limits: PluginResourceLimits,
    ) -> PluginManifest {
        PluginManifest {
            manifest_version: "1.0.0".to_string(),
            plugin_id: "p1".to_string(),
            plugin_name: "P1".to_string(),
            version: "1.0.0".to_string(),
            description: String::new(),
            author: String::new(),
            license: "MIT".to_string(),
            plugin_type: PluginType::Extension,
            entry_point: "main".to_string(),
            capabilities: vec![CapabilityDeclaration::new(PluginCapability::Vision)],
            dependencies: vec![PluginDependency {
                plugin_id: "dep".to_string(),
                version: "*".to_string(),
                dependency_type: DependencyType::Optional,
                capability: None,
            }],
            permissions: perms,
            compatibility: PluginCompatibility::default(),
            resource_limits: limits,
        }
    }

    #[test]
    fn test_boundary_mapping() {
        assert_eq!(
            SandboxBoundary::from_permission_level(PermissionLevel::Restricted),
            SandboxBoundary::Maximal
        );
        assert_eq!(
            SandboxBoundary::from_permission_level(PermissionLevel::Normal),
            SandboxBoundary::Standard
        );
        assert_eq!(
            SandboxBoundary::from_permission_level(PermissionLevel::Trusted),
            SandboxBoundary::None
        );
    }

    #[test]
    fn test_policy_from_manifest_takes_max_level() {
        let m = manifest_with_perms(
            vec![
                PluginPermission {
                    name: "a".to_string(),
                    level: PermissionLevel::Low,
                    required: false,
                },
                PluginPermission {
                    name: "b".to_string(),
                    level: PermissionLevel::Elevated,
                    required: false,
                },
            ],
            PluginResourceLimits::default(),
        );
        let policy = SandboxPolicy::from_manifest(&m);
        assert_eq!(policy.max_permission_level(), PermissionLevel::Elevated);
        assert_eq!(policy.boundary(), SandboxBoundary::Relaxed);
        assert!(policy.allows("a"));
        assert!(!policy.allows("c"));
    }

    #[test]
    fn test_policy_validate_rejects_required_above_policy_level() {
        let policy = SandboxPolicy {
            permission_level: PermissionLevel::Low,
            permissions: vec![PluginPermission {
                name: "x".to_string(),
                level: PermissionLevel::Privileged,
                required: true,
            }],
            resource_limits: PluginResourceLimits::default(),
        };
        assert!(policy.validate().is_err());
    }

    #[test]
    fn test_policy_validate_rejects_zero_memory() {
        let policy = SandboxPolicy {
            permission_level: PermissionLevel::Normal,
            permissions: vec![],
            resource_limits: PluginResourceLimits {
                max_memory_mb: Some(0),
                ..Default::default()
            },
        };
        assert!(policy.validate().is_err());
    }

    #[test]
    fn test_resource_usage_check() {
        let limits = PluginResourceLimits {
            max_memory_mb: Some(512),
            max_threads: Some(4),
            ..Default::default()
        };
        let usage = ResourceUsage {
            memory_mb: 1024,
            ..Default::default()
        };
        assert!(usage.check_against(&limits).is_err());
        let ok = ResourceUsage {
            memory_mb: 256,
            threads: 2,
            ..Default::default()
        };
        assert!(ok.check_against(&limits).is_ok());
    }

    #[test]
    fn test_noop_executor_lifecycle() {
        let exec = NoopSandboxExecutor::new();
        let policy = SandboxPolicy {
            permission_level: PermissionLevel::Normal,
            permissions: vec![PluginPermission {
                name: "screen.capture".to_string(),
                level: PermissionLevel::Normal,
                required: false,
            }],
            resource_limits: PluginResourceLimits {
                max_memory_mb: Some(256),
                ..Default::default()
            },
        };
        exec.prepare("p1", &policy).unwrap();
        assert_eq!(exec.boundary("p1"), Some(SandboxBoundary::Standard));
        assert!(exec.check_permission("p1", "screen.capture").is_ok());
        assert!(exec.check_permission("p1", "network").is_err());
        assert!(exec
            .check_resource(
                "p1",
                &ResourceUsage {
                    memory_mb: 100,
                    ..Default::default()
                }
            )
            .is_ok());
        assert!(exec
            .check_resource(
                "p1",
                &ResourceUsage {
                    memory_mb: 999,
                    ..Default::default()
                }
            )
            .is_err());
        exec.teardown("p1").unwrap();
        assert!(exec.boundary("p1").is_none());
    }

    #[test]
    fn test_noop_executor_check_without_prepare() {
        let exec = NoopSandboxExecutor::new();
        assert!(exec.check_permission("none", "x").is_err());
    }
}
