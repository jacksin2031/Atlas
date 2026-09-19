use serde_json::Value;
use std::{
    fs,
    io::Write,
    path::Path,
    sync::atomic::{AtomicU64, Ordering},
};

pub const VERSION: u64 = 1;
static NEXT_TEMP: AtomicU64 = AtomicU64::new(0);

/// Refuse redirected storage locations, including Windows junctions.
/// This is a static path check, not a defence against a hostile concurrent rename.
pub fn check_path(path: &Path) -> Result<(), String> {
    for component in path.components() {
        if matches!(component, std::path::Component::ParentDir) {
            return Err("Parent traversal is not supported for Atlas persistence.".into());
        }
        #[cfg(windows)]
        if let std::path::Component::Prefix(prefix) = component {
            if !matches!(
                prefix.kind(),
                std::path::Prefix::Disk(_) | std::path::Prefix::VerbatimDisk(_)
            ) {
                return Err(
                    "Atlas persistence requires a local drive, not a network or device path."
                        .into(),
                );
            }
        }
    }
    for part in path.ancestors() {
        match fs::symlink_metadata(part) {
            Ok(metadata) => {
                #[cfg(windows)]
                let redirected = {
                    use std::os::windows::fs::MetadataExt;
                    metadata.file_attributes() & 0x400 != 0
                };
                #[cfg(not(windows))]
                let redirected = metadata.file_type().is_symlink();
                if redirected {
                    return Err(
                        "Atlas persistence refuses symbolic links or reparse points.".into(),
                    );
                }
            }
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {}
            Err(error) => return Err(format!("Unable to inspect persistence path: {error}")),
        }
    }
    Ok(())
}

/// Identity migration for the sole supported schema. Unknown fields survive.
pub fn validate(document: Value) -> Result<Value, String> {
    let version = document
        .get("version")
        .and_then(Value::as_u64)
        .ok_or("Project asset version is missing or invalid.")?;
    if version != VERSION {
        return Err(format!("Unsupported project asset version {version}; this Atlas supports version {VERSION}. Open with a compatible Atlas release; the file was not changed."));
    }
    if !document.get("assets").is_some_and(Value::is_object) {
        return Err("Project assets must contain an assets object.".into());
    }
    Ok(document)
}

pub fn read(path: &Path) -> Result<Value, String> {
    check_path(path)?;
    let bytes = fs::read(path).map_err(|e| format!("Unable to read project assets: {e}"))?;
    let document = serde_json::from_slice(&bytes)
        .map_err(|e| format!("Unable to parse project assets: {e}"))?;
    validate(document)
}

// Unknown versions must never be treated as ordinary corruption or overwritten.
pub fn refuse_incompatible(path: &Path) -> Result<(), String> {
    check_path(path)?;
    if !path.exists() {
        return Ok(());
    }
    let bytes = fs::read(path).map_err(|e| format!("Unable to inspect project assets: {e}"))?;
    if let Ok(document) = serde_json::from_slice::<Value>(&bytes) {
        if let Some(version) = document.get("version").and_then(Value::as_u64) {
            if version != VERSION {
                validate(document)?;
            }
        }
    }
    Ok(())
}

pub struct WriterLock(fs::File);
impl Drop for WriterLock {
    fn drop(&mut self) {
        let _ = fs2::FileExt::unlock(&self.0);
    }
}
pub fn lock(path: &Path) -> Result<WriterLock, String> {
    let lock = path.with_extension("write-lock");
    check_path(&lock)?;
    let file = fs::OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(false)
        .open(&lock)
        .map_err(|e| format!("Unable to open persistence lock: {e}"))?;
    fs2::FileExt::try_lock_exclusive(&file)
        .map_err(|e| format!("Persistence is in use by another Atlas writer: {e}"))?;
    Ok(WriterLock(file))
}

pub fn atomic_write(path: &Path, bytes: &[u8]) -> Result<(), String> {
    check_path(path)?;
    let temporary = path.with_extension(format!(
        "{}.{}.tmp",
        std::process::id(),
        NEXT_TEMP.fetch_add(1, Ordering::Relaxed)
    ));
    let result = (|| {
        let mut file = fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&temporary)
            .map_err(|e| format!("Unable to create persistence temporary file: {e}"))?;
        file.write_all(bytes)
            .and_then(|_| file.sync_all())
            .map_err(|e| format!("Unable to flush persistence temporary file: {e}"))?;
        drop(file);
        check_path(path)?;
        fs::rename(&temporary, path)
            .map_err(|e| format!("Unable to atomically replace persistence file: {e}"))?;
        Ok(())
    })();
    if result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    result
}

pub fn load(path: &Path, backup: &Path) -> Result<Value, String> {
    refuse_incompatible(path)?;
    check_path(backup)?;
    if path.exists() {
        match read(path) {
            Ok(document) => return Ok(document["assets"].clone()),
            Err(primary) if backup.exists() => {
                return read(backup)
                    .map(|v| v["assets"].clone())
                    .map_err(|other| format!("{primary} Recovery backup also failed: {other}"))
            }
            Err(error) => return Err(error),
        }
    }
    if backup.exists() {
        return read(backup).map(|v| v["assets"].clone());
    }
    Ok(Value::Null)
}

pub fn save(path: &Path, backup: &Path, document: Value) -> Result<(), String> {
    validate(document.clone())?;
    check_path(path)?;
    check_path(backup)?;
    fs::create_dir_all(path.parent().ok_or("Invalid persistence directory.")?)
        .map_err(|e| e.to_string())?;
    let _lock = lock(path)?;
    refuse_incompatible(path)?;
    refuse_incompatible(backup)?;
    // Never rotate a corrupt primary over the last good recovery copy.
    if path.exists() {
        match read(path) {
            Ok(previous) => atomic_write(
                backup,
                &serde_json::to_vec_pretty(&previous).map_err(|e| e.to_string())?,
            )?,
            Err(error) => {
                if !backup.exists() || read(backup).is_err() {
                    return Err(error);
                }
            }
        }
    }
    atomic_write(
        path,
        &serde_json::to_vec_pretty(&document).map_err(|e| e.to_string())?,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    struct Fixture(std::path::PathBuf);
    impl Fixture {
        fn new() -> Self {
            let path = std::env::temp_dir().join(format!(
                "Atlas 資料 persistence {} {}",
                std::process::id(),
                NEXT_TEMP.fetch_add(1, Ordering::Relaxed)
            ));
            fs::create_dir_all(&path).unwrap();
            Self(path)
        }
        fn paths(&self) -> (std::path::PathBuf, std::path::PathBuf) {
            (self.0.join("assets.json"), self.0.join("backup.json"))
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn historical_v1_identity_preserves_all_payload_fields() {
        let fixture: Value = serde_json::from_str(include_str!(
            "../../../../tests/fixtures/project-v1/project-assets.v1.json"
        ))
        .unwrap();
        let f = Fixture::new();
        let (path, backup) = f.paths();
        save(&path, &backup, fixture.clone()).unwrap();
        assert_eq!(load(&path, &backup).unwrap(), fixture["assets"]);
        assert_eq!(read(&path).unwrap(), fixture);
    }
    #[test]
    fn future_primary_cannot_fall_back_or_be_downgraded() {
        let f = Fixture::new();
        let (path, backup) = f.paths();
        let old = json!({"version":1,"assets":{"old":true}});
        save(&path, &backup, old.clone()).unwrap();
        save(&path, &backup, old.clone()).unwrap();
        let future = b"{\"version\":2,\"assets\":{}}";
        fs::write(&path, future).unwrap();
        assert!(load(&path, &backup).unwrap_err().contains("compatible"));
        assert!(save(&path, &backup, old).is_err());
        assert_eq!(fs::read(path).unwrap(), future);
    }
    #[test]
    fn corrupt_primary_does_not_replace_valid_backup() {
        let f = Fixture::new();
        let (path, backup) = f.paths();
        save(&path, &backup, json!({"version":1,"assets":{"n":1}})).unwrap();
        save(&path, &backup, json!({"version":1,"assets":{"n":2}})).unwrap();
        fs::write(&path, "broken").unwrap();
        assert_eq!(load(&path, &backup).unwrap()["n"], 1);
        save(&path, &backup, json!({"version":1,"assets":{"n":3}})).unwrap();
        assert_eq!(read(&backup).unwrap()["assets"]["n"], 1);
    }
    #[test]
    fn invalid_destination_and_failed_commit_preserve_source() {
        let f = Fixture::new();
        let (path, backup) = f.paths();
        save(&path, &backup, json!({"version":1,"assets":{"n":1}})).unwrap();
        let before = fs::read(&path).unwrap();
        assert!(save(&path, &backup, json!({"version":1,"assets":null})).is_err());
        assert_eq!(fs::read(&path).unwrap(), before);
        let directory = f.0.join("blocked");
        fs::create_dir(&directory).unwrap();
        assert!(atomic_write(&directory, b"replacement").is_err());
        assert!(directory.is_dir());
        assert!(!fs::read_dir(&f.0).unwrap().any(|e| e
            .unwrap()
            .path()
            .extension()
            .is_some_and(|x| x == "tmp")));
    }
    #[test]
    fn writers_are_exclusive_and_unlock_on_drop() {
        let f = Fixture::new();
        let (path, _) = f.paths();
        let first = lock(&path).unwrap();
        assert!(lock(&path).is_err());
        drop(first);
        assert!(lock(&path).is_ok());
    }
    #[test]
    fn malformed_envelopes_are_not_empty_projects() {
        for value in [
            json!({"version":1}),
            json!({"version":true,"assets":{}}),
            json!([]),
        ] {
            assert!(validate(value).is_err());
        }
    }
    #[cfg(windows)]
    #[test]
    fn junction_storage_is_refused_without_touching_target() {
        let f = Fixture::new();
        let target = f.0.join("outside");
        let junction = f.0.join("redirected");
        fs::create_dir(&target).unwrap();
        let status = std::process::Command::new("cmd")
            .args(["/C", "mklink", "/J"])
            .arg(&junction)
            .arg(&target)
            .output()
            .unwrap();
        assert!(
            status.status.success(),
            "junction setup failed: {:?}",
            status
        );
        let result = atomic_write(&junction.join("assets.json"), b"must not write");
        fs::remove_dir(&junction).unwrap();
        assert!(result.unwrap_err().contains("reparse"));
        assert!(!target.join("assets.json").exists());
    }
}
