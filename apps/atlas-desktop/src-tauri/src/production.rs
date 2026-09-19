//! Installed-product boundaries. Development discovery is never a release fallback.
use super::*;

pub fn host_command(app: &AppHandle, module: &str, workflow: bool) -> Result<Command, String> {
    #[cfg(debug_assertions)]
    {
        let _ = app;
        let root = find_repo_root()?;
        let variable = if workflow {
            "ATLAS_WORKFLOW_PYTHON"
        } else {
            "ATLAS_AI_PYTHON"
        };
        let python = env::var_os(variable).unwrap_or_else(|| "python".into());
        let mut command = Command::new(python);
        command
            .arg("-B")
            .arg("-u")
            .arg("-m")
            .arg(module)
            .current_dir(&root)
            .env(
                "PYTHONPATH",
                if workflow {
                    workflow_python_path(&root)?
                } else {
                    python_path(&root)?
                },
            );
        Ok(command)
    }
    #[cfg(not(debug_assertions))]
    {
        let _ = workflow;
        let root = app
            .path()
            .resource_dir()
            .map_err(|_| "RUNTIME_RESOURCES_UNAVAILABLE")?
            .join("runtime");
        installed_host_command(&root, module)
    }
}

#[cfg(any(not(debug_assertions), test))]
pub fn installed_host_command(root: &Path, module: &str) -> Result<Command, String> {
    if !matches!(module, "atlas_ai.host" | "atlas_workflow.host") {
        return Err("RUNTIME_MODULE_DENIED".into());
    }
    let interpreter = root.join("python.exe");
    if !interpreter.is_file() || !root.join("python313._pth").is_file() {
        return Err("BUNDLED_RUNTIME_MISSING: Reinstall Atlas to restore its runtime.".into());
    }
    let mut command = Command::new(interpreter);
    command
        .args(["-I", "-B", "-u", "-m", module])
        .current_dir(root);
    for name in [
        "PYTHONPATH",
        "PYTHONHOME",
        "ATLAS_ROOT",
        "ATLAS_AI_PYTHON",
        "ATLAS_WORKFLOW_PYTHON",
        "OPENAI_API_KEY",
        "ATLAS_AI_API_KEY",
        "ATLAS_AI_BASE_URL",
        "ATLAS_OLLAMA_URL",
    ] {
        command.env_remove(name);
    }
    Ok(command)
}

pub fn registry_dir(app: &AppHandle) -> Result<PathBuf, String> {
    #[cfg(debug_assertions)]
    {
        let _ = app;
        Ok(find_repo_root()?.join("marketplace/local-development"))
    }
    #[cfg(not(debug_assertions))]
    {
        app.path()
            .resource_dir()
            .map(|p| p.join("local-development-registry"))
            .map_err(|_| "REGISTRY_RESOURCES_UNAVAILABLE".into())
    }
}

// An OS-owned lock releases automatically after crashes, unlike a persistent lock marker.
pub struct InstanceGuard {
    _file: fs::File,
}
pub fn instance_lock(app: &AppHandle) -> Result<InstanceGuard, String> {
    let directory = app
        .path()
        .app_data_dir()
        .map_err(|_| "APP_DATA_UNAVAILABLE")?;
    fs::create_dir_all(&directory).map_err(|_| "APP_DATA_UNWRITABLE")?;
    let file = fs::OpenOptions::new()
        .create(true)
        .truncate(false)
        .read(true)
        .write(true)
        .open(directory.join("desktop-instance.lock"))
        .map_err(|_| "INSTANCE_LOCK_UNAVAILABLE")?;
    fs2::FileExt::try_lock_exclusive(&file).map_err(|_| {
        "ATLAS_ALREADY_RUNNING: Close the other Atlas window before opening this one."
    })?;
    Ok(InstanceGuard { _file: file })
}

#[cfg(windows)]
pub struct RuntimeJob {
    _handle: std::os::windows::io::OwnedHandle,
}
#[cfg(windows)]
impl RuntimeJob {
    pub fn attach(child: &mut Child) -> Result<Self, String> {
        use std::os::windows::io::{AsRawHandle, FromRawHandle, OwnedHandle};
        use windows::Win32::{Foundation::HANDLE, System::JobObjects::*};
        let result = (|| unsafe {
            let handle = CreateJobObjectW(None, windows::core::PCWSTR::null())
                .map_err(|_| "RUNTIME_JOB_CREATE_FAILED")?;
            let owned = OwnedHandle::from_raw_handle(handle.0);
            let mut limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION::default();
            limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
            SetInformationJobObject(
                handle,
                JobObjectExtendedLimitInformation,
                &limits as *const _ as *const _,
                std::mem::size_of_val(&limits) as u32,
            )
            .map_err(|_| "RUNTIME_JOB_CONFIG_FAILED")?;
            AssignProcessToJobObject(handle, HANDLE(child.as_raw_handle()))
                .map_err(|_| "RUNTIME_JOB_ATTACH_FAILED")?;
            Ok(Self { _handle: owned })
        })();
        if result.is_err() {
            let _ = child.kill();
            let _ = child.wait();
        }
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn missing_bundle_never_falls_back_to_global_python() {
        assert!(
            installed_host_command(Path::new("missing-runtime"), "atlas_workflow.host").is_err()
        );
        assert!(installed_host_command(Path::new("."), "os").is_err());
    }
}
