//! Signed package distribution; PluginManager remains the execution authority.
pub mod package;
mod runtime;

use crate::{
    DependencyResolver, DependencyType, PluginManager, PluginManagerImpl, PluginManifest,
    PluginPermission, SemanticVersion,
};
use base64::{engine::general_purpose::STANDARD, Engine};
use fs2::FileExt;
use package::{read_bounded, verify, VerifiedPackage};
use runtime::PackageProvider;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs::{self, File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
    sync::Arc,
};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DistributionError {
    pub code: String,
    pub message: String,
}
impl std::fmt::Display for DistributionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}: {}", self.code, self.message)
    }
}
impl std::error::Error for DistributionError {}
pub fn failure(code: &str, message: &str) -> DistributionError {
    DistributionError {
        code: code.into(),
        message: message.into(),
    }
}
fn storage_error(_: impl std::fmt::Display) -> DistributionError {
    failure("STORAGE_FAILURE", "Package storage operation failed")
}

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Listing {
    pub plugin_id: String,
    pub version: String,
    pub filename: String,
    pub digest: String,
}
pub trait MarketplaceProvider: Send + Sync {
    fn source(&self) -> &str;
    fn discover(&self, query: &str) -> Result<Vec<Listing>, DistributionError>;
    fn acquire(&self, listing: &Listing) -> Result<Vec<u8>, DistributionError>;
    fn verification_key(&self) -> [u8; 32];
}

pub struct LocalRegistry {
    root: PathBuf,
    key: [u8; 32],
}
impl LocalRegistry {
    pub fn with_key(root: PathBuf, key: &str) -> Result<Self, DistributionError> {
        let key: [u8; 32] = STANDARD
            .decode(key.trim())
            .ok()
            .and_then(|b| b.try_into().ok())
            .ok_or_else(|| failure("SIGNATURE_FAILURE", "Invalid registry signing key"))?;
        Ok(Self { root, key })
    }
    pub fn new(root: PathBuf) -> Result<Self, DistributionError> {
        let key = fs::read_to_string(root.join("public-key.txt")).map_err(|_| {
            failure(
                "MARKETPLACE_UNAVAILABLE",
                "Local Development Registry unavailable",
            )
        })?;
        Self::with_key(root, &key)
    }
}
impl MarketplaceProvider for LocalRegistry {
    fn source(&self) -> &str {
        "Local Development Registry"
    }
    fn verification_key(&self) -> [u8; 32] {
        self.key
    }
    fn discover(&self, query: &str) -> Result<Vec<Listing>, DistributionError> {
        let entries: Vec<Listing> =
            serde_json::from_slice(&read_bounded(&self.root.join("index.json")).map_err(|_| {
                failure(
                    "MARKETPLACE_UNAVAILABLE",
                    "Local Development Registry unavailable",
                )
            })?)
            .map_err(|_| failure("MARKETPLACE_UNAVAILABLE", "Invalid registry index"))?;
        if entries.len() > 1000 {
            return Err(failure(
                "MARKETPLACE_UNAVAILABLE",
                "Registry index exceeds provider limit",
            ));
        }
        let mut identities = BTreeSet::new();
        for entry in &entries {
            if !identities.insert((&entry.plugin_id, &entry.version)) {
                return Err(failure(
                    "IDENTITY_COLLISION",
                    "Duplicate package identity in registry",
                ));
            }
        }
        Ok(entries
            .into_iter()
            .filter(|e| e.plugin_id.to_lowercase().contains(&query.to_lowercase()))
            .take(100)
            .collect())
    }
    fn acquire(&self, listing: &Listing) -> Result<Vec<u8>, DistributionError> {
        if !package::safe_identifier(&listing.filename)
            || !listing.filename.ends_with(".atlas-plugin")
        {
            return Err(failure("INVALID_PACKAGE", "Unsafe registry filename"));
        }
        read_bounded(&self.root.join(&listing.filename))
    }
}

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Installed {
    pub manifest: PluginManifest,
    pub digest: String,
    pub enabled: bool,
    pub approved_permissions: Vec<PluginPermission>,
    pub source: String,
    pub acquired_at: String,
}
#[derive(Default, Clone, Serialize, Deserialize)]
struct State {
    installed: BTreeMap<String, Installed>,
    audit: Vec<Value>,
    identities: BTreeMap<String, String>,
    revision: u64,
}

/// Immutable package blobs plus one atomically replaced commit record. Orphan blobs
/// are never loaded; interrupted install/update retains the last committed state.
pub struct PackageStore {
    root: PathBuf,
    _lock: File,
}
impl PackageStore {
    pub fn open(root: PathBuf) -> Result<Self, DistributionError> {
        fs::create_dir_all(&root).map_err(storage_error)?;
        let meta = fs::symlink_metadata(&root).map_err(storage_error)?;
        #[cfg(windows)]
        {
            use std::os::windows::fs::MetadataExt;
            if meta.file_attributes() & 0x400 != 0 {
                return Err(failure(
                    "STORAGE_FAILURE",
                    "Package store cannot be a reparse point",
                ));
            }
        }
        if meta.file_type().is_symlink() {
            return Err(failure("STORAGE_FAILURE", "Package store cannot be a link"));
        }
        let lock = OpenOptions::new()
            .create(true)
            .truncate(false)
            .write(true)
            .open(root.join("store.lock"))
            .map_err(storage_error)?;
        lock.try_lock_exclusive()
            .map_err(|_| failure("OPERATION_BUSY", "Package store already in use"))?;
        Ok(Self { root, _lock: lock })
    }
    fn load(&self) -> Result<State, DistributionError> {
        let path = self.root.join("installed.json");
        if !path.exists() {
            return Ok(State::default());
        }
        serde_json::from_slice(&read_bounded(&path).map_err(storage_error)?).map_err(|_| {
            failure(
                "RECOVERY_FAILED",
                "Installed state is corrupt; activation blocked",
            )
        })
    }
    fn commit(&self, state: &State) -> Result<(), DistributionError> {
        let temp = self.root.join(format!("{}.staging", uuid::Uuid::new_v4()));
        let mut file = OpenOptions::new()
            .create_new(true)
            .write(true)
            .open(&temp)
            .map_err(storage_error)?;
        file.write_all(&serde_json::to_vec(state).map_err(storage_error)?)
            .map_err(storage_error)?;
        file.sync_all().map_err(storage_error)?;
        fs::rename(&temp, self.root.join("installed.json")).map_err(storage_error)?;
        Ok(())
    }
    fn blob(&self, hash: &str) -> Result<PathBuf, DistributionError> {
        if hash.len() != 64 || !hash.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err(failure("RECOVERY_FAILED", "Invalid stored package digest"));
        }
        Ok(self.root.join(format!("{hash}.atlas-plugin")))
    }
    fn stage(&self, package: &VerifiedPackage) -> Result<(), DistributionError> {
        let path = self.blob(&package.digest)?;
        if path.exists() {
            if package::digest(&read_bounded(&path)?) != package.digest {
                return Err(failure(
                    "PACKAGE_INTEGRITY_FAILURE",
                    "Stored package was modified",
                ));
            }
            return Ok(());
        }
        let temp = self.root.join(format!("{}.staging", uuid::Uuid::new_v4()));
        let result = (|| {
            let mut file = OpenOptions::new()
                .create_new(true)
                .write(true)
                .open(&temp)
                .map_err(storage_error)?;
            file.write_all(&package.bytes).map_err(storage_error)?;
            file.sync_all().map_err(storage_error)?;
            drop(file);
            fs::rename(&temp, path).map_err(storage_error)
        })();
        if result.is_err() {
            let _ = fs::remove_file(&temp);
        }
        result
    }
    fn clean_uncommitted(&self, state: &State) {
        let retained: BTreeSet<_> = state
            .installed
            .values()
            .map(|i| format!("{}.atlas-plugin", i.digest))
            .collect();
        let Ok(entries) = fs::read_dir(&self.root) else {
            return;
        };
        for entry in entries.flatten() {
            let name = entry.file_name().to_string_lossy().into_owned();
            let staging = name
                .strip_suffix(".staging")
                .is_some_and(|s| uuid::Uuid::parse_str(s).is_ok());
            let blob = name
                .strip_suffix(".atlas-plugin")
                .is_some_and(|s| s.len() == 64 && s.bytes().all(|b| b.is_ascii_hexdigit()));
            if (staging || (blob && !retained.contains(&name)))
                && entry.file_type().is_ok_and(|t| t.is_file())
            {
                let _ = fs::remove_file(entry.path());
            }
        }
    }
}

pub struct MarketplaceService {
    provider: Arc<dyn MarketplaceProvider>,
    store: PackageStore,
    state: State,
    packages: BTreeMap<String, VerifiedPackage>,
    runtime_provider: Arc<PackageProvider>,
    runtime: Arc<PluginManagerImpl>,
    runtime_version: SemanticVersion,
    failures: BTreeMap<String, DistributionError>,
    inspections: BTreeMap<String, VerifiedPackage>,
    registration_sync:
        Option<Arc<dyn Fn(Vec<Value>, u64) -> Result<(), DistributionError> + Send + Sync>>,
}
impl MarketplaceService {
    pub fn open(
        provider: Arc<dyn MarketplaceProvider>,
        store: PackageStore,
        runtime_version: &str,
    ) -> Result<Self, DistributionError> {
        let state = store.load()?;
        store.clean_uncommitted(&state);
        let runtime_version = SemanticVersion::parse(runtime_version)
            .map_err(|_| failure("INCOMPATIBLE_PLUGIN", "Invalid Atlas version"))?;
        let runtime_provider = Arc::new(PackageProvider::default());
        let runtime = PluginManagerImpl::new(
            runtime_provider.clone(),
            runtime_version.clone(),
            SemanticVersion::parse("1.0.0").unwrap(),
        );
        runtime.set_runtime_state(atlas_contracts::RuntimeState::Running);
        let mut service = Self {
            provider,
            store,
            state,
            packages: BTreeMap::new(),
            runtime_provider,
            runtime,
            runtime_version,
            failures: BTreeMap::new(),
            inspections: BTreeMap::new(),
            registration_sync: None,
        };
        for (id, installed) in service.state.installed.clone() {
            let result = (|| {
                let p = verify(
                    read_bounded(&service.store.blob(&installed.digest)?)?,
                    Some(&installed.digest),
                    &service.provider.verification_key(),
                    &service.runtime_version,
                )?;
                if p.manifest != installed.manifest || p.manifest.plugin_id != id {
                    return Err(failure(
                        "RECOVERY_FAILED",
                        "Stored manifest does not match package",
                    ));
                }
                service.packages.insert(id.clone(), p);
                Ok(())
            })();
            if let Err(error) = result {
                service.failures.insert(id, error);
            }
        }
        let manifests: Vec<_> = service
            .packages
            .values()
            .map(|p| p.manifest.clone())
            .collect();
        match DependencyResolver::new().resolve(&manifests) {
            Ok(order) => {
                for id in order.load_order {
                    if service.state.installed[&id].enabled {
                        let result = service.activate(&id);
                        if let Err(error) = result {
                            service.failures.insert(id, error);
                        }
                    }
                }
            }
            Err(_) => {
                for id in service.packages.keys() {
                    service.failures.insert(
                        id.clone(),
                        failure("DEPENDENCY_FAILURE", "Stored dependency graph is invalid"),
                    );
                }
            }
        }
        Ok(service)
    }

    pub fn set_registration_sync(
        &mut self,
        sync: Arc<dyn Fn(Vec<Value>, u64) -> Result<(), DistributionError> + Send + Sync>,
    ) {
        self.registration_sync = Some(sync);
    }

    fn synchronize(&self) -> Result<(), DistributionError> {
        if let Some(sync) = &self.registration_sync {
            sync(self.registrations(), self.state.revision)?;
        }
        Ok(())
    }

    fn activate(&self, id: &str) -> Result<(), DistributionError> {
        let p = self
            .packages
            .get(id)
            .ok_or_else(|| failure("PLUGIN_UNAVAILABLE", "Installed package is unavailable"))?;
        let installed = &self.state.installed[id];
        if installed.approved_permissions != p.manifest.permissions {
            return Err(failure("PERMISSION_DENIED", "Permission review required"));
        }
        for dep in &p.manifest.dependencies {
            if dep.dependency_type == DependencyType::Required
                && (!self
                    .state
                    .installed
                    .get(&dep.plugin_id)
                    .is_some_and(|i| i.enabled)
                    || self.failures.contains_key(&dep.plugin_id))
            {
                return Err(failure(
                    "DEPENDENCY_FAILURE",
                    "Required dependency is not enabled and healthy",
                ));
            }
        }
        self.runtime_provider.insert(
            p.clone(),
            installed
                .approved_permissions
                .iter()
                .map(|p| p.name.clone())
                .collect(),
        );
        let result = self
            .runtime
            .install(p.manifest.clone())
            .and_then(|_| self.runtime.start_plugin(id));
        if let Err(e) = result {
            let _ = self.runtime.unload_plugin(id);
            self.runtime_provider.remove(id);
            return Err(failure("LOAD_FAILED", &e.to_string()));
        }
        Ok(())
    }
    fn deactivate(&self, id: &str) -> Result<(), DistributionError> {
        if self.runtime.registry().lookup(id).is_some() {
            self.runtime
                .unload_plugin(id)
                .map_err(|e| failure("UNLOAD_FAILED", &e.to_string()))?;
        }
        self.runtime_provider.remove(id);
        Ok(())
    }
    fn package(&self, id: &str, version: &str) -> Result<VerifiedPackage, DistributionError> {
        let listing = self
            .provider
            .discover(id)?
            .into_iter()
            .find(|e| e.plugin_id == id && e.version == version)
            .ok_or_else(|| failure("PACKAGE_NOT_FOUND", "Package version not found"))?;
        let package = verify(
            self.provider.acquire(&listing)?,
            Some(&listing.digest),
            &self.provider.verification_key(),
            &self.runtime_version,
        )?;
        if package.manifest.plugin_id != id || package.manifest.version != version {
            return Err(failure(
                "IDENTITY_COLLISION",
                "Registry and manifest identity mismatch",
            ));
        }
        Ok(package)
    }
    pub fn inspect(&mut self, id: &str, version: &str) -> Result<Value, DistributionError> {
        let p = self.package(id, version)?;
        self.remember_inspection(p)
    }
    pub fn inspect_local(&mut self, path: &Path) -> Result<Value, DistributionError> {
        let p = verify(
            read_bounded(path)?,
            None,
            &self.provider.verification_key(),
            &self.runtime_version,
        )?;
        self.remember_inspection(p)
    }
    fn remember_inspection(&mut self, p: VerifiedPackage) -> Result<Value, DistributionError> {
        if self.inspections.len() >= 32 {
            self.inspections.clear();
        }
        let review_id = uuid::Uuid::new_v4().to_string();
        let value = json!({"reviewId":review_id,"manifest":p.manifest,"digest":p.digest,"source":self.provider.source(),"trust":"Development — signature checked against local registry key","nodes":p.program.nodes});
        self.inspections.insert(review_id, p);
        Ok(value)
    }
    fn event(&mut self, id: &str, action: &str, request_id: &str) {
        self.state.revision += 1;
        let installation = self.state.installed.get(id);
        self.state.audit.push(json!({"pluginId":id,"action":action,"requestId":request_id,"timestamp":chrono::Utc::now().to_rfc3339(),"revision":self.state.revision,"version":installation.map(|i| &i.manifest.version),"digest":installation.map(|i| &i.digest),"source":self.provider.source(),"trust":"Development"}));
        if self.state.audit.len() > 100 {
            self.state.audit.remove(0);
        }
    }
    pub fn record_failure(&mut self, id: &str, error: &DistributionError, request_id: &str) {
        self.event(
            id,
            if error.code == "PERMISSION_DENIED" || error.code == "SIGNATURE_FAILURE" {
                "PEVT-SECURITY-VIOLATION"
            } else {
                "PEVT-FAILED"
            },
            request_id,
        );
        if let Some(event) = self.state.audit.last_mut() {
            event["error"] = json!(error);
        }
        let _ = self.store.commit(&self.state);
        self.store.clean_uncommitted(&self.state);
    }
    pub fn install(
        &mut self,
        review: &str,
        approved: Vec<PluginPermission>,
        request_id: &str,
    ) -> Result<Value, DistributionError> {
        let p = self.inspections.get(review).cloned().ok_or_else(|| {
            failure(
                "PERMISSION_DENIED",
                "Inspect this exact package before installation",
            )
        })?;
        if p.manifest.permissions != approved {
            return Err(failure(
                "PERMISSION_DENIED",
                "Explicit review of all requested permissions is required",
            ));
        }
        let id = p.manifest.plugin_id.clone();
        let identity = format!("{id}@{}", p.manifest.version);
        if self
            .state
            .identities
            .get(&identity)
            .is_some_and(|digest| digest != &p.digest)
        {
            return Err(failure(
                "IDENTITY_COLLISION",
                "Identity/version already belongs to different content",
            ));
        }
        let previous = self.state.installed.get(&id).cloned();
        if let Some(old) = &previous {
            if p.manifest.semantic_version() <= old.manifest.semantic_version() {
                return Err(failure("INVALID_UPDATE", "Update version must be newer"));
            }
            if let Some(old_package) = self.packages.get(&id) {
                let before: Vec<_> = old_package
                    .program
                    .nodes
                    .iter()
                    .map(|n| &n.type_name)
                    .collect();
                let after: Vec<_> = p.program.nodes.iter().map(|n| &n.type_name).collect();
                if before != after {
                    return Err(failure(
                        "INCOMPATIBLE_PLUGIN",
                        "Node schema migration is not supported; update changes contributed types",
                    ));
                }
            }
        }
        let mut manifests: Vec<_> = self
            .state
            .installed
            .values()
            .filter(|i| i.manifest.plugin_id != id)
            .map(|i| i.manifest.clone())
            .collect();
        manifests.push(p.manifest.clone());
        DependencyResolver::new()
            .resolve(&manifests)
            .map_err(|e| failure("DEPENDENCY_FAILURE", &e.to_string()))?;
        self.store.stage(&p)?;
        let old_state = self.state.clone();
        let old_failures = self.failures.clone();
        let old_package = self.packages.get(&id).cloned();
        self.deactivate(&id)?;
        let enabled = previous.as_ref().is_some_and(|p| p.enabled);
        self.state.installed.insert(
            id.clone(),
            Installed {
                manifest: p.manifest.clone(),
                digest: p.digest.clone(),
                enabled,
                approved_permissions: approved,
                source: self.provider.source().into(),
                acquired_at: chrono::Utc::now().to_rfc3339(),
            },
        );
        self.packages.insert(id.clone(), p.clone());
        let result = (|| {
            self.activate(&id)?;
            self.failures.remove(&id);
            if !enabled {
                self.deactivate(&id)?;
            }
            self.state.identities.insert(identity, p.digest.clone());
            self.event(
                &id,
                if previous.is_some() {
                    "PEVT-UPDATED"
                } else {
                    "PEVT-INSTALLED"
                },
                request_id,
            );
            self.synchronize()?;
            self.store.commit(&self.state)
        })();
        if let Err(error) = result {
            let rollback_revision = self.state.revision + 1;
            self.deactivate(&id)?;
            self.state = old_state;
            self.failures = old_failures;
            self.state.revision = rollback_revision;
            self.packages.remove(&id);
            if let Some(old) = old_package {
                self.packages.insert(id.clone(), old);
            }
            if previous.is_some_and(|p| p.enabled) {
                self.activate(&id).map_err(|_| {
                    failure("RECOVERY_FAILED", "Previous version could not be restored")
                })?;
            }
            self.store.clean_uncommitted(&self.state);
            self.synchronize().map_err(|_| {
                failure(
                    "RECOVERY_FAILED",
                    "Package rolled back; Workflow host must restart to restore registrations",
                )
            })?;
            return Err(error);
        }
        self.failures.remove(&id);
        self.inspections.remove(review);
        self.store.clean_uncommitted(&self.state);
        self.snapshot("")
    }
    pub fn change(
        &mut self,
        id: &str,
        action: &str,
        request_id: &str,
    ) -> Result<Value, DistributionError> {
        let old = self.state.clone();
        let old_failures = self.failures.clone();
        let installed = self
            .state
            .installed
            .get(id)
            .ok_or_else(|| failure("PACKAGE_NOT_FOUND", "Plugin is not installed"))?;
        let was_enabled = installed.enabled;
        if action != "enable"
            && self.state.installed.values().any(|i| {
                i.manifest
                    .dependencies
                    .iter()
                    .any(|d| d.plugin_id == id && d.dependency_type == DependencyType::Required)
            })
        {
            return Err(failure(
                "DEPENDENCY_FAILURE",
                "Another installed plugin requires this plugin",
            ));
        }
        match action {
            "enable" if !was_enabled || self.failures.contains_key(id) => {
                self.activate(id)?;
                self.state.installed.get_mut(id).unwrap().enabled = true;
            }
            "enable" => return self.snapshot(""),
            "disable" => {
                self.deactivate(id)?;
                self.state.installed.get_mut(id).unwrap().enabled = false;
            }
            "uninstall" => {
                self.deactivate(id)?;
                self.state.installed.remove(id);
            }
            _ => return Err(failure("INVALID_OPERATION", "Unknown package operation")),
        }
        self.failures.remove(id);
        self.event(
            id,
            match action {
                "enable" => "PEVT-ACTIVATED",
                "disable" => "PEVT-DEACTIVATED",
                _ => "PEVT-REMOVED",
            },
            request_id,
        );
        if let Err(error) = self
            .synchronize()
            .and_then(|_| self.store.commit(&self.state))
        {
            let rollback_revision = self.state.revision + 1;
            self.deactivate(id)?;
            self.state = old;
            self.failures = old_failures;
            self.state.revision = rollback_revision;
            if was_enabled {
                self.activate(id)?;
            }
            self.synchronize().map_err(|_| {
                failure(
                    "RECOVERY_FAILED",
                    "Package rolled back; Workflow host must restart to restore registrations",
                )
            })?;
            return Err(error);
        }
        self.failures.remove(id);
        if action == "uninstall" {
            self.packages.remove(id);
            let _ = fs::remove_file(self.store.blob(&old.installed[id].digest)?);
        }
        self.store.clean_uncommitted(&self.state);
        self.snapshot("")
    }
    pub fn registrations(&self) -> Vec<Value> {
        self.packages.iter().filter(|(id, _)| self.state.installed.get(*id).is_some_and(|i| i.enabled) && !self.failures.contains_key(*id)).flat_map(|(id, p)| p.program.nodes.iter().map(move |n| json!({
            "nodeId":format!("{id}.{}", n.type_name),"typeName":n.type_name,"label":n.label,"category":"plugin","description":format!("Provided by {id}"),
            "pluginId":id,"version":p.manifest.version,"capabilities":["workflow"],"parameters":{},
            "inputs":[{"id":"in_0","name":"input","type":"any","multiple":false}],"outputs":[{"id":"out_0","name":"value","type":"any","multiple":false}]
        }))).collect()
    }
    pub fn snapshot(&self, query: &str) -> Result<Value, DistributionError> {
        let mut available = Vec::new();
        let mut provider_error = None;
        match self.provider.discover("") {
            Ok(entries) => {
                for e in entries {
                    match self.package(&e.plugin_id, &e.version) {
                    Ok(p) => available.push(json!({"manifest":p.manifest,"digest":p.digest,"compatible":true})),
                    Err(error) => available.push(json!({"pluginId":e.plugin_id,"version":e.version,"compatible":false,"error":error})),
                }
                }
            }
            Err(error) => provider_error = Some(error),
        }
        available.sort_by(|a, b| {
            let av = a
                .pointer("/manifest/version")
                .and_then(Value::as_str)
                .and_then(|v| SemanticVersion::parse(v).ok());
            let bv = b
                .pointer("/manifest/version")
                .and_then(Value::as_str)
                .and_then(|v| SemanticVersion::parse(v).ok());
            bv.cmp(&av)
        });
        let installed: Vec<_> = self.state.installed.iter().map(|(id, i)| {
            let update = available.iter().filter(|a| a.pointer("/manifest/plugin_id").and_then(Value::as_str) == Some(id.as_str())).find(|a| a.pointer("/manifest/version").and_then(Value::as_str).and_then(|v| SemanticVersion::parse(v).ok()).is_some_and(|v| v > i.manifest.semantic_version()));
            json!({"installation":i,"health":if self.failures.contains_key(id){"error"}else if i.enabled{"healthy"}else{"unavailable"},"error":self.failures.get(id),"update":update})
        }).collect();
        available.retain(|a| {
            a.pointer("/manifest/plugin_id")
                .or_else(|| a.get("pluginId"))
                .and_then(Value::as_str)
                .is_some_and(|id| id.to_lowercase().contains(&query.to_lowercase()))
        });
        Ok(
            json!({"source":self.provider.source(),"scope":"User installation; shared across projects; no project or credential access","trust":"Development — local registry key; no production certification","available":available,"installed":installed,"registrations":self.registrations(),"providerError":provider_error,"revision":self.state.revision,"audit":self.state.audit.iter().rev().take(100).collect::<Vec<_>>()}),
        )
    }
    pub fn execute(
        &self,
        id: &str,
        node_type: &str,
        configuration: &Value,
        inputs: &Value,
    ) -> Result<Value, DistributionError> {
        if !self.state.installed.get(id).is_some_and(|i| i.enabled)
            || self.failures.contains_key(id)
        {
            return Err(failure(
                "PLUGIN_UNAVAILABLE",
                "Plugin is disabled, missing, or unhealthy",
            ));
        }
        self.runtime
            .execute_workflow_node(id, node_type, configuration, inputs)
            .map_err(|e| {
                failure(
                    if matches!(
                        e,
                        crate::PluginError::Sandbox(crate::error::SandboxError::PermissionDenied(
                            _
                        ))
                    ) {
                        "PERMISSION_DENIED"
                    } else {
                        "PLUGIN_EXECUTION_FAILED"
                    },
                    &e.to_string(),
                )
            })
    }
}

#[cfg(test)]
mod tests;
