use super::package::{Program, VerifiedPackage};
use crate::error::{LifecycleError, SandboxError};
use crate::{
    Plugin, PluginContext, PluginError, PluginFactory, PluginHealthState, PluginManifest,
    PluginMetadata, PluginProvider, PluginState,
};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    sync::{Arc, Mutex},
};

pub struct PackagePlugin {
    metadata: PluginMetadata,
    program: Program,
    state: Mutex<PluginState>,
    grants: Vec<String>,
}

impl PackagePlugin {
    fn set(&self, state: PluginState) {
        *self.state.lock().unwrap() = state;
    }
    fn denied(&self, message: &str) -> PluginError {
        LifecycleError::OperationFailed(self.metadata.id.clone(), message.into()).into()
    }
}

impl Plugin for PackagePlugin {
    fn metadata(&self) -> &PluginMetadata {
        &self.metadata
    }
    fn state(&self) -> PluginState {
        *self.state.lock().unwrap()
    }
    fn initialize(&self, context: &PluginContext) -> Result<(), PluginError> {
        let _ = context;
        self.set(PluginState::Initialized);
        Ok(())
    }
    fn start(&self) -> Result<(), PluginError> {
        if self.program.fail_health {
            return Err(self.denied("LOAD_FAILED: package health check failed"));
        }
        self.set(PluginState::Running);
        Ok(())
    }
    fn pause(&self) -> Result<(), PluginError> {
        self.set(PluginState::Paused);
        Ok(())
    }
    fn resume(&self) -> Result<(), PluginError> {
        self.set(PluginState::Running);
        Ok(())
    }
    fn stop(&self) -> Result<(), PluginError> {
        self.set(PluginState::Stopped);
        Ok(())
    }
    fn shutdown(&self) -> Result<(), PluginError> {
        self.set(PluginState::Stopped);
        Ok(())
    }
    fn dispose(&self) {
        self.set(PluginState::Stopped);
    }
    fn health_check(&self) -> PluginHealthState {
        if self.program.fail_health {
            PluginHealthState::Failed("Package health check failed".into())
        } else {
            PluginHealthState::Healthy
        }
    }
    fn execute_workflow_node(
        &self,
        node_type: &str,
        configuration: &Value,
        inputs: &Value,
    ) -> Result<Value, PluginError> {
        if self.state() != PluginState::Running {
            return Err(self.denied("PLUGIN_UNAVAILABLE"));
        }
        let node = self
            .program
            .nodes
            .iter()
            .find(|n| n.type_name == node_type)
            .ok_or_else(|| self.denied("PLUGIN_UNAVAILABLE: unknown node"))?;
        let value = inputs
            .as_object()
            .and_then(|i| i.values().next())
            .or_else(|| configuration.get("value"))
            .cloned()
            .unwrap_or(Value::String(String::new()));
        let text = value
            .as_str()
            .map(str::to_owned)
            .unwrap_or_else(|| value.to_string());
        let result = match node.operation.as_str() {
            "echo" => value,
            "constant" => json!(node.value),
            "prefix" => json!(format!("{}{text}", node.value)),
            "uppercase" => json!(text.to_uppercase()),
            "lowercase" => json!(text.to_lowercase()),
            "fail" => return Err(self.denied("PLUGIN_EXECUTION_FAILED: controlled plugin failure")),
            "require_permission" => {
                if !node
                    .permission
                    .as_ref()
                    .is_some_and(|p| self.grants.contains(p))
                {
                    return Err(SandboxError::PermissionDenied(
                        "Undeclared or unapproved permission".into(),
                    )
                    .into());
                }
                return Err(SandboxError::PermissionDenied(
                    "Privileged services are unavailable in the constrained provider".into(),
                )
                .into());
            }
            _ => return Err(self.denied("PERMISSION_DENIED: operation unsupported")),
        };
        Ok(json!({"value": result}))
    }
}

#[derive(Default)]
pub struct PackageProvider {
    packages: Mutex<BTreeMap<String, (VerifiedPackage, Vec<String>)>>,
}

impl PackageProvider {
    pub fn insert(&self, package: VerifiedPackage, grants: Vec<String>) {
        self.packages
            .lock()
            .unwrap()
            .insert(package.manifest.plugin_id.clone(), (package, grants));
    }
    pub fn remove(&self, id: &str) {
        self.packages.lock().unwrap().remove(id);
    }
}

struct Factory {
    package: VerifiedPackage,
    grants: Vec<String>,
}
impl PluginFactory for Factory {
    fn supports(&self, id: &str) -> bool {
        self.package.manifest.plugin_id == id
    }
    fn create(&self, manifest: &PluginManifest) -> Result<Arc<dyn Plugin>, PluginError> {
        if manifest != &self.package.manifest {
            return Err(LifecycleError::OperationFailed(
                manifest.plugin_id.clone(),
                "Package identity mismatch".into(),
            )
            .into());
        }
        Ok(Arc::new(PackagePlugin {
            metadata: manifest.metadata(),
            program: self.package.program.clone(),
            state: Mutex::new(PluginState::Created),
            grants: self.grants.clone(),
        }))
    }
}
impl PluginProvider for PackageProvider {
    fn discover(&self) -> Result<Vec<PluginManifest>, PluginError> {
        Ok(self
            .packages
            .lock()
            .unwrap()
            .values()
            .map(|(p, _)| p.manifest.clone())
            .collect())
    }
    fn factory_for(&self, id: &str) -> Result<Arc<dyn PluginFactory>, PluginError> {
        let (package, grants) =
            self.packages
                .lock()
                .unwrap()
                .get(id)
                .cloned()
                .ok_or_else(|| {
                    LifecycleError::OperationFailed(id.into(), "PACKAGE_NOT_FOUND".into())
                })?;
        Ok(Arc::new(Factory { package, grants }))
    }
}
