use super::*;
use atlas_plugin::distribution::{
    failure, DistributionError, LocalRegistry, MarketplaceService, PackageStore,
};

#[derive(Default)]
pub struct MarketplaceHost {
    service: Mutex<Option<MarketplaceService>>,
}
impl MarketplaceHost {
    fn with<T>(
        &self,
        app: &AppHandle,
        operation: impl FnOnce(&mut MarketplaceService) -> Result<T, DistributionError>,
    ) -> Result<T, DistributionError> {
        let mut guard = self
            .service
            .lock()
            .map_err(|_| failure("RUNTIME_UNAVAILABLE", "Plugin Runtime lock failed"))?;
        if guard.is_none() {
            let root = app
                .path()
                .app_data_dir()
                .map_err(|_| failure("STORAGE_FAILURE", "Application data directory unavailable"))?
                .join("plugins")
                .join("v1");
            let registry = find_repo_root()
                .map(|repo| repo.join("marketplace/local-development"))
                .unwrap_or_else(|_| root.join("registry-unavailable"));
            let provider = Arc::new(LocalRegistry::with_key(
                registry,
                include_str!("../../../../marketplace/local-development/public-key.txt"),
            )?);
            *guard = Some(MarketplaceService::open(
                provider,
                PackageStore::open(root)?,
                env!("CARGO_PKG_VERSION"),
            )?);
        }
        operation(guard.as_mut().unwrap())
    }
    pub fn execute(&self, app: &AppHandle, payload: &Value) -> HostResult {
        self.with(app, |s| {
            let result = s.execute(
                payload["pluginId"].as_str().unwrap_or_default(),
                payload["nodeType"].as_str().unwrap_or_default(),
                &payload["configuration"],
                &payload["inputs"],
            );
            if let Err(error) = &result {
                s.record_failure(
                    payload["pluginId"].as_str().unwrap_or_default(),
                    error,
                    payload["requestId"].as_str().unwrap_or_default(),
                );
            }
            result
        })
        .map_err(|e| serde_json::to_string(&e).unwrap_or_default())
    }
}

pub fn sync(app: &AppHandle, manager: &Arc<WorkflowHostManager>) -> HostResult {
    let snapshot = app
        .state::<MarketplaceHost>()
        .with(app, |s| s.snapshot(""))
        .map_err(|e| e.to_string())?;
    manager.request(
        app.clone(),
        "workflow_plugin_sync",
        json!({"registrations":snapshot["registrations"],"revision":snapshot["revision"]}),
    )
}

#[tauri::command(rename_all = "camelCase")]
pub async fn marketplace_request(
    app: AppHandle,
    command: String,
    payload: Value,
) -> Result<Value, DistributionError> {
    tauri::async_runtime::spawn_blocking(move || {
        let local = if command == "inspect_local" {
            rfd::FileDialog::new()
                .set_title("Inspect signed Atlas plugin package")
                .add_filter("Atlas Plugin", &["atlas-plugin"])
                .pick_file()
        } else {
            None
        };
        if command == "inspect_local" && local.is_none() {
            return Ok(Value::Null);
        }
        let result = app.state::<MarketplaceHost>().with(&app, |s| {
            let manager = app.state::<Arc<WorkflowHostManager>>().inner().clone();
            let sync_app = app.clone();
            s.set_registration_sync(Arc::new(move |registrations, revision| {
                manager
                    .request(
                        sync_app.clone(),
                        "workflow_plugin_sync",
                        json!({"registrations":registrations,"revision":revision}),
                    )
                    .map(|_| ())
                    .map_err(|_| {
                        failure(
                            "REGISTRATION_FAILED",
                            "Workflow host rejected package registrations",
                        )
                    })
            }));
            let id = payload["pluginId"].as_str().unwrap_or_default();
            let request_id = payload["requestId"].as_str().unwrap_or_default();
            let result = match command.as_str() {
                "snapshot" => s.snapshot(payload["query"].as_str().unwrap_or_default()),
                "inspect" => s.inspect(id, payload["version"].as_str().unwrap_or_default()),
                "inspect_local" => s.inspect_local(local.as_ref().unwrap()),
                "install" => {
                    let approved = serde_json::from_value(payload["approvedPermissions"].clone())
                        .map_err(|_| {
                        failure("PERMISSION_DENIED", "Permission review is required")
                    })?;
                    s.install(
                        payload["reviewId"].as_str().unwrap_or_default(),
                        approved,
                        request_id,
                    )
                }
                "enable" | "disable" | "uninstall" => s.change(id, &command, request_id),
                _ => Err(failure(
                    "INVALID_OPERATION",
                    "Unsupported Marketplace command",
                )),
            };
            if let Err(error) = &result {
                s.record_failure(id, error, request_id);
            }
            result
        })?;
        if command == "snapshot" {
            let manager = app.state::<Arc<WorkflowHostManager>>().inner().clone();
            manager
                .request(
                    app.clone(),
                    "workflow_plugin_sync",
                    json!({"registrations":result["registrations"],"revision":result["revision"]}),
                )
                .map_err(|_| {
                    failure(
                        "REGISTRATION_FAILED",
                        "Workflow host could not synchronize; refresh to retry",
                    )
                })?;
        }
        if matches!(
            command.as_str(),
            "install" | "enable" | "disable" | "uninstall"
        ) {
            let _ = app.emit(
                "plugin://marketplace-changed",
                json!({"revision":result["revision"],"requestId":payload["requestId"]}),
            );
        }
        Ok(result)
    })
    .await
    .map_err(|_| failure("RUNTIME_UNAVAILABLE", "Marketplace worker failed"))?
}
