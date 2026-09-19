//! Privacy boundary: no arbitrary messages, provider payloads or project data enter logs.
use super::*;
use std::sync::OnceLock;

static LOG_PATH: OnceLock<PathBuf> = OnceLock::new();
static EVENTS: Mutex<Vec<Value>> = Mutex::new(Vec::new());

pub fn initialize(app: &AppHandle) {
    if let Ok(directory) = app.path().app_log_dir() {
        if fs::create_dir_all(&directory).is_ok() {
            let _ = LOG_PATH.set(directory.join("atlas.jsonl"));
        }
    }
    record("desktop", "INFO", "APPLICATION_STARTED");
    std::panic::set_hook(Box::new(|_| {
        record("desktop", "ERROR", "APPLICATION_PANIC")
    }));
}

pub fn record(subsystem: &'static str, severity: &'static str, code: &'static str) {
    record_event(subsystem, severity, code, None);
}

pub fn request_started(subsystem: &'static str, request_id: &str) {
    let suffix = request_id
        .strip_prefix("workflow-desktop-")
        .or_else(|| request_id.strip_prefix("desktop-"));
    let valid = suffix.is_some_and(|s| {
        s.split('-').count() == 2 && s.split('-').all(|n| n.parse::<u64>().is_ok())
    });
    record_event(
        subsystem,
        "INFO",
        "REQUEST_STARTED",
        valid.then_some(request_id),
    );
}

fn record_event(
    subsystem: &'static str,
    severity: &'static str,
    code: &'static str,
    correlation: Option<&str>,
) {
    let value = json!({"timestamp":SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default().as_millis(),
        "severity":severity,"subsystem":subsystem,"code":code,"correlationId":correlation});
    // Only internal static call sites may provide these values. Never pass stderr/error text.
    if let Ok(mut events) = EVENTS.lock() {
        if events.len() >= 200 {
            events.remove(0);
        }
        events.push(value.clone());
        if let Some(path) = LOG_PATH.get() {
            if fs::metadata(path)
                .map(|m| m.len() > 256 * 1024)
                .unwrap_or(false)
            {
                let _ = fs::remove_file(path);
            }
            if let Ok(mut file) = fs::OpenOptions::new().create(true).append(true).open(path) {
                let _ = writeln!(file, "{value}");
            }
        }
    }
}

fn health(name: &str, available: bool, detail: &str) -> Value {
    json!({"name":name,"status":if available {"available"} else {"unavailable"},"detail":detail})
}

#[tauri::command]
pub async fn beta_system_info(app: AppHandle) -> HostResult {
    tauri::async_runtime::spawn_blocking(move || {
        let workflow = app.state::<Arc<WorkflowHostManager>>().request(app.clone(), "workflow_input_status", json!({})).is_ok();
        let ai = app.state::<Arc<AIHostManager>>().request(app.clone(), "ai_health", json!({})).is_ok();
        let credential = load_provider_credential("openai").ok().flatten().is_some();
        let plugin = app.state::<marketplace::MarketplaceHost>().healthy(&app);
        let storage = app.path().app_data_dir().ok().is_some_and(|path| {
            let probe = path.join(format!("health-{}.tmp", std::process::id()));
            match fs::OpenOptions::new().create_new(true).write(true).open(&probe) {
                Ok(file) => { drop(file); fs::remove_file(probe).is_ok() }, Err(_) => false,
            }
        });
        let vision = Screen::all().map(|s| !s.is_empty()).unwrap_or(false);
        json!({"version":env!("CARGO_PKG_VERSION"),"platform":env::consts::OS,"architecture":env::consts::ARCH,
            "commit":env!("ATLAS_BUILD_COMMIT"),"buildType":if cfg!(debug_assertions) {"development"} else {"release-alpha"},
            "runtimes":[health("Workflow Runtime",workflow,"Host responsiveness; Input is never armed by this check."),
                health("Vision Runtime",vision,"Native display enumeration; capture requires a separate action."),
                health("AI Runtime",ai,if credential {"Provider credential configured; live inference not verified."} else {"OpenAI credential not configured; live inference remains an external condition."}),
                health("Knowledge Runtime",workflow,"Hosted with Workflow; project storage is checked when opened."),
                health("Plugin Runtime",plugin,"Local Development Registry; development trust only."),
                health("Storage",storage,"Application data write probe.")]})
    }).await.map_err(|_| "DIAGNOSTICS_HEALTH_FAILED".into())
}

fn bundle(info: Value) -> Value {
    json!({"schemaVersion":1,"system":info,"recentLogs":EVENTS.lock().map(|e|e.clone()).unwrap_or_default(),
        "inclusionPolicy":"Version, OS family, architecture, build identity, runtime health and static diagnostic event codes only. No credentials, project paths/files, Knowledge, conversations, screenshots, provider responses or raw stderr. Local export only."})
}

#[tauri::command]
pub async fn export_diagnostics(app: AppHandle) -> HostResult {
    let info = beta_system_info(app).await?;
    tauri::async_runtime::spawn_blocking(move || {
        let Some(path) = rfd::FileDialog::new()
            .set_title("Export safe Atlas diagnostics (new file)")
            .set_file_name("atlas-diagnostics.json")
            .add_filter("JSON", &["json"])
            .save_file()
        else {
            return Ok(json!({"path":null}));
        };
        let bytes =
            serde_json::to_vec_pretty(&bundle(info)).map_err(|_| "DIAGNOSTICS_ENCODING_FAILED")?;
        project_persistence::check_path(&path)?;
        // create_new rejects existing files, symlinks and accidental overwrite of user content.
        let mut file = fs::OpenOptions::new()
            .create_new(true)
            .write(true)
            .open(&path)
            .map_err(|_| "DIAGNOSTICS_PATH_UNAVAILABLE: Choose a new writable filename.")?;
        file.write_all(&bytes)
            .and_then(|_| file.sync_all())
            .map_err(|_| "DIAGNOSTICS_WRITE_FAILED")?;
        Ok(json!({"path":path.to_string_lossy()}))
    })
    .await
    .map_err(|_| "DIAGNOSTICS_EXPORT_FAILED".to_owned())?
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn diagnostic_bundle_contains_only_metadata() {
        request_started(
            "ai",
            "sk-disposable-secret Authorization: Bearer PRIVATE_KNOWLEDGE data:image/png;base64",
        );
        request_started("workflow", "workflow-desktop-12-34");
        let result = bundle(json!({"version":"test"})).to_string();
        for forbidden in [
            "sk-disposable-secret",
            "Authorization:",
            "Bearer ",
            "PRIVATE_KNOWLEDGE",
            "data:image/png;base64",
        ] {
            assert!(!result.contains(forbidden));
        }
        assert!(result.contains("inclusionPolicy"));
        assert!(result.contains("workflow-desktop-12-34"));
    }
}
