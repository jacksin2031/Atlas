use super::*;
use ed25519_dalek::{Signer, SigningKey};
use sha2::{Digest, Sha256};
use std::io::{Cursor, Read};

fn archive(
    version: &str,
    operation: &str,
    permissions: Vec<PluginPermission>,
    health: bool,
) -> Vec<u8> {
    let manifest = json!({"manifest_version":"1.0.0","plugin_id":"atlas.acceptance.echo","plugin_name":"Marketplace Echo","version":version,"license":"MIT","author":"Atlas acceptance","description":"Disposable local acceptance package","entry_point":"bin/workflow.json","capabilities":[{"capability":"Workflow","enabled":true}],"permissions":permissions,"compatibility":{"minimum_runtime_version":"0.15.0-alpha","api_version":"1.0.0"}});
    let program = json!({"format":"atlas.safe-workflow.v1","platforms":["windows","linux","macos"],"architectures":["x86_64","aarch64"],"fail_health":health,"nodes":[{"typeName":"atlas.acceptance.echo.echo","label":"Marketplace Echo","operation":operation,"value":"ATLAS_MARKETPLACE_1710"}]});
    signed_files(BTreeMap::from([
        (
            "manifest.json".into(),
            serde_json::to_vec(&manifest).unwrap(),
        ),
        (
            "bin/workflow.json".into(),
            serde_json::to_vec(&program).unwrap(),
        ),
    ]))
}
fn signed_files(mut files: BTreeMap<String, Vec<u8>>) -> Vec<u8> {
    let mut sums = String::new();
    for (name, data) in &files {
        sums.push_str(&format!("{}  {}\n", package::digest(data), name));
    }
    files.insert("checksum.sha256".into(), sums.into_bytes());
    let mut hash = Sha256::new();
    for (name, data) in &files {
        hash.update((name.len() as u64).to_be_bytes());
        hash.update(name.as_bytes());
        hash.update((data.len() as u64).to_be_bytes());
        hash.update(data);
    }
    let signature = SigningKey::from_bytes(&[17; 32]).sign(&hash.finalize());
    files.insert(
        "signature.sig".into(),
        format!("Ed25519:{}", STANDARD.encode(signature.to_bytes())).into_bytes(),
    );
    let mut zip = zip::ZipWriter::new(Cursor::new(Vec::new()));
    for (name, data) in files {
        zip.start_file(
            name,
            zip::write::FileOptions::default().unix_permissions(0o644),
        )
        .unwrap();
        zip.write_all(&data).unwrap();
    }
    zip.finish().unwrap().into_inner()
}
struct Fixture {
    directory: tempfile::TempDir,
    provider: Arc<LocalRegistry>,
}
impl Fixture {
    fn new() -> Self {
        let directory = tempfile::tempdir().unwrap();
        fs::write(
            directory.path().join("public-key.txt"),
            STANDARD.encode(SigningKey::from_bytes(&[17; 32]).verifying_key().to_bytes()),
        )
        .unwrap();
        fs::write(directory.path().join("index.json"), "[]").unwrap();
        let provider = Arc::new(LocalRegistry::new(directory.path().to_owned()).unwrap());
        Self {
            directory,
            provider,
        }
    }
    fn publish(&self, version: &str, bytes: &[u8]) {
        let filename = format!("echo-{version}.atlas-plugin");
        fs::write(self.directory.path().join(&filename), bytes).unwrap();
        let mut index = self.provider.discover("").unwrap();
        index.push(Listing {
            plugin_id: "atlas.acceptance.echo".into(),
            version: version.into(),
            filename,
            digest: package::digest(bytes),
        });
        fs::write(
            self.directory.path().join("index.json"),
            serde_json::to_vec(&index).unwrap(),
        )
        .unwrap();
    }
    fn open(&self) -> MarketplaceService {
        MarketplaceService::open(
            self.provider.clone(),
            PackageStore::open(self.directory.path().join("store")).unwrap(),
            "0.15.0-alpha",
        )
        .unwrap()
    }
}
fn install(s: &mut MarketplaceService, version: &str) {
    let review = s.inspect("atlas.acceptance.echo", version).unwrap();
    s.install(review["reviewId"].as_str().unwrap(), vec![], "install-test")
        .unwrap();
}

#[test]
fn lifecycle_execute_disable_update_restart_uninstall_reinstall() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    f.publish("1.1.0", &archive("1.1.0", "constant", vec![], false));
    let mut s = f.open();
    assert_eq!(
        s.snapshot("echo").unwrap()["available"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
    install(&mut s, "1.0.0");
    assert!(s.registrations().is_empty());
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({"input":"ATLAS_MARKETPLACE_1700"})
        )
        .unwrap()["value"],
        "ATLAS_MARKETPLACE_1700"
    );
    s.change("atlas.acceptance.echo", "disable", "d").unwrap();
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({})
        )
        .unwrap_err()
        .code,
        "PLUGIN_UNAVAILABLE"
    );
    drop(s);
    let mut s = f.open();
    assert!(s.registrations().is_empty());
    s.change("atlas.acceptance.echo", "enable", "e2").unwrap();
    s.change("atlas.acceptance.echo", "enable", "e3").unwrap();
    assert_eq!(s.registrations().len(), 1);
    install(&mut s, "1.1.0");
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({})
        )
        .unwrap()["value"],
        "ATLAS_MARKETPLACE_1710"
    );
    drop(s);
    let mut s = f.open();
    assert_eq!(s.registrations().len(), 1);
    s.change("atlas.acceptance.echo", "uninstall", "u").unwrap();
    assert!(s.registrations().is_empty());
    drop(s);
    let mut s = f.open();
    assert!(s.state.installed.is_empty());
    install(&mut s, "1.1.0");
    s.change("atlas.acceptance.echo", "enable", "e4").unwrap();
    assert_eq!(s.registrations().len(), 1);
}
#[test]
fn failed_update_restores_running_version() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    f.publish("1.1.0", &archive("1.1.0", "echo", vec![], true));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    let review = s.inspect("atlas.acceptance.echo", "1.1.0").unwrap();
    assert_eq!(
        s.install(review["reviewId"].as_str().unwrap(), vec![], "bad-update")
            .unwrap_err()
            .code,
        "LOAD_FAILED"
    );
    assert_eq!(
        s.state.installed["atlas.acceptance.echo"].manifest.version,
        "1.0.0"
    );
    assert!(s
        .execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({})
        )
        .is_ok());
    drop(s);
    assert_eq!(
        f.open().state.installed["atlas.acceptance.echo"]
            .manifest
            .version,
        "1.0.0"
    );
}
#[test]
fn permission_escalation_needs_exact_review() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let permission = PluginPermission {
        name: "PERM-NETWORK-OUTBOUND".into(),
        level: crate::PermissionLevel::Elevated,
        required: true,
    };
    f.publish(
        "1.1.0",
        &archive("1.1.0", "echo", vec![permission.clone()], false),
    );
    let mut s = f.open();
    install(&mut s, "1.0.0");
    let r = s.inspect("atlas.acceptance.echo", "1.1.0").unwrap();
    assert_eq!(
        s.install(r["reviewId"].as_str().unwrap(), vec![], "denied")
            .unwrap_err()
            .code,
        "PERMISSION_DENIED"
    );
    assert_eq!(
        s.state.installed["atlas.acceptance.echo"].manifest.version,
        "1.0.0"
    );
    s.install(
        r["reviewId"].as_str().unwrap(),
        vec![permission],
        "approved",
    )
    .unwrap();
}
#[test]
fn corrupt_digest_and_signature_are_rejected() {
    let bytes = archive("1.0.0", "echo", vec![], false);
    let version = SemanticVersion::parse("0.15.0-alpha").unwrap();
    let key = SigningKey::from_bytes(&[17; 32]).verifying_key().to_bytes();
    assert_eq!(
        verify(bytes.clone(), Some("bad"), &key, &version)
            .err()
            .unwrap()
            .code,
        "PACKAGE_INTEGRITY_FAILURE"
    );
    let other = SigningKey::from_bytes(&[18; 32]).verifying_key().to_bytes();
    assert_eq!(
        verify(bytes, None, &other, &version).err().unwrap().code,
        "SIGNATURE_FAILURE"
    );
}
#[test]
fn unsafe_paths_rejected_without_extraction() {
    for name in [
        "../escape",
        "/absolute",
        "C:/outside",
        "a\\escape",
        "con",
        "bin/../escape",
        "COM9.txt",
        "bin/LPT3",
        "bin/line\nbreak",
    ] {
        let bytes = signed_files(BTreeMap::from([(name.into(), b"unsafe".to_vec())]));
        assert_eq!(
            verify(
                bytes,
                None,
                &[0; 32],
                &SemanticVersion::parse("0.15.0-alpha").unwrap()
            )
            .err()
            .unwrap()
            .code,
            "INVALID_PACKAGE"
        );
    }
}
#[test]
fn invalid_manifest_and_platform_rejected() {
    let base = archive("1.0.0", "echo", vec![], false);
    for (file, key, value) in [
        ("manifest.json", "plugin_id", json!("")),
        ("manifest.json", "version", json!("bad")),
        ("manifest.json", "entry_point", json!("../bad")),
        (
            "manifest.json",
            "permissions",
            json!([{"name":"network","level":"Elevated"}]),
        ),
        (
            "manifest.json",
            "compatibility",
            json!({"api_version":"99.0.0"}),
        ),
        ("bin/workflow.json", "platforms", json!(["unknown"])),
    ] {
        let mut zip = zip::ZipArchive::new(Cursor::new(&base)).unwrap();
        let mut files = BTreeMap::new();
        for name in ["manifest.json", "bin/workflow.json"] {
            let mut data = Vec::new();
            zip.by_name(name).unwrap().read_to_end(&mut data).unwrap();
            if name == file {
                let mut v: Value = serde_json::from_slice(&data).unwrap();
                v[key] = value.clone();
                data = serde_json::to_vec(&v).unwrap();
            }
            files.insert(name.into(), data);
        }
        assert!(verify(
            signed_files(files),
            None,
            &SigningKey::from_bytes(&[17; 32]).verifying_key().to_bytes(),
            &SemanticVersion::parse("0.15.0-alpha").unwrap()
        )
        .is_err());
    }
}
#[test]
fn provider_offline_preserves_installed_management() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    fs::remove_file(f.directory.path().join("index.json")).unwrap();
    assert!(!s.snapshot("").unwrap()["providerError"].is_null());
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    s.change("atlas.acceptance.echo", "uninstall", "u").unwrap();
}
#[test]
fn store_lock_rejects_concurrent_process_and_orphan_is_not_activated() {
    let f = Fixture::new();
    let s = f.open();
    assert!(PackageStore::open(f.directory.path().join("store")).is_err());
    let p = verify(
        archive("1.0.0", "echo", vec![], false),
        None,
        &f.provider.verification_key(),
        &s.runtime_version,
    )
    .unwrap();
    s.store.stage(&p).unwrap();
    drop(s);
    assert!(f.open().state.installed.is_empty());
}
#[test]
fn failure_and_unauthorized_operation_are_isolated() {
    for operation in ["fail", "require_permission"] {
        let f = Fixture::new();
        f.publish("1.0.0", &archive("1.0.0", operation, vec![], false));
        let mut s = f.open();
        install(&mut s, "1.0.0");
        s.change("atlas.acceptance.echo", "enable", "e").unwrap();
        assert!(s
            .execute(
                "atlas.acceptance.echo",
                "atlas.acceptance.echo.echo",
                &json!({}),
                &json!({})
            )
            .is_err());
        assert_eq!(s.registrations().len(), 1);
        s.change("atlas.acceptance.echo", "disable", "d").unwrap();
    }
}
#[test]
fn semantic_order_and_empty_search() {
    let f = Fixture::new();
    f.publish("1.9.0", &archive("1.9.0", "echo", vec![], false));
    f.publish("1.10.0", &archive("1.10.0", "echo", vec![], false));
    let s = f.open();
    assert_eq!(
        s.snapshot("").unwrap()["available"][0]["manifest"]["version"],
        "1.10.0"
    );
    assert!(s.snapshot("missing").unwrap()["available"]
        .as_array()
        .unwrap()
        .is_empty());
}

#[test]
fn failed_commit_restores_runtime_and_committed_version() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    f.publish("1.1.0", &archive("1.1.0", "constant", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    let record = s.store.root.join("installed.json");
    let backup = s.store.root.join("installed.backup");
    fs::rename(&record, &backup).unwrap();
    fs::create_dir(&record).unwrap();
    let review = s.inspect("atlas.acceptance.echo", "1.1.0").unwrap();
    assert_eq!(
        s.install(review["reviewId"].as_str().unwrap(), vec![], "fail-commit")
            .unwrap_err()
            .code,
        "STORAGE_FAILURE"
    );
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({"input":42})
        )
        .unwrap()["value"],
        42
    );
    fs::remove_dir(&record).unwrap();
    fs::rename(&backup, &record).unwrap();
    drop(s);
    assert_eq!(
        f.open().state.installed["atlas.acceptance.echo"]
            .manifest
            .version,
        "1.0.0"
    );
}

#[test]
fn missing_registry_after_restart_retains_trusted_installation() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    drop(s);
    let provider = LocalRegistry::with_key(
        f.directory.path().join("missing-registry"),
        &STANDARD.encode(f.provider.verification_key()),
    )
    .unwrap();
    let s = MarketplaceService::open(
        Arc::new(provider),
        PackageStore::open(f.directory.path().join("store")).unwrap(),
        "0.15.0-alpha",
    )
    .unwrap();
    assert!(!s.snapshot("").unwrap()["providerError"].is_null());
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({"input":"offline"})
        )
        .unwrap()["value"],
        "offline"
    );
}

#[test]
fn tampered_committed_blob_is_never_registered_on_restart() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    let blob = s
        .store
        .blob(&s.state.installed["atlas.acceptance.echo"].digest)
        .unwrap();
    drop(s);
    fs::write(blob, "tampered").unwrap();
    let s = f.open();
    assert!(s.registrations().is_empty());
    assert_eq!(
        s.snapshot("").unwrap()["installed"][0]["error"]["code"],
        "PACKAGE_INTEGRITY_FAILURE"
    );
}

#[test]
fn search_does_not_hide_installed_update_metadata() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    f.publish("1.1.0", &archive("1.1.0", "constant", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    let snapshot = s.snapshot("unrelated").unwrap();
    assert!(snapshot["available"].as_array().unwrap().is_empty());
    assert_eq!(
        snapshot["installed"][0]["update"]["manifest"]["version"],
        "1.1.0"
    );
}

#[test]
fn registration_failure_rolls_back_update_before_persistence() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    f.publish("1.1.0", &archive("1.1.0", "constant", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    let seen = Arc::new(std::sync::Mutex::new(Vec::new()));
    let recorded = seen.clone();
    s.set_registration_sync(Arc::new(move |nodes, revision| {
        recorded.lock().unwrap().push(revision);
        if nodes.iter().any(|n| n["version"] == "1.1.0") {
            return Err(failure(
                "REGISTRATION_FAILED",
                "Injected registration rejection",
            ));
        }
        Ok(())
    }));
    let r = s.inspect("atlas.acceptance.echo", "1.1.0").unwrap();
    assert_eq!(
        s.install(r["reviewId"].as_str().unwrap(), vec![], "update")
            .unwrap_err()
            .code,
        "REGISTRATION_FAILED"
    );
    assert_eq!(s.registrations()[0]["version"], "1.0.0");
    let revisions = seen.lock().unwrap();
    assert_eq!(revisions.len(), 2);
    assert!(revisions[1] > revisions[0]);
    drop(s);
    assert_eq!(
        f.open().state.installed["atlas.acceptance.echo"]
            .manifest
            .version,
        "1.0.0"
    );
}

#[test]
fn permission_denial_has_structured_code() {
    let f = Fixture::new();
    f.publish(
        "1.0.0",
        &archive("1.0.0", "require_permission", vec![], false),
    );
    let mut s = f.open();
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    assert_eq!(
        s.execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({})
        )
        .unwrap_err()
        .code,
        "PERMISSION_DENIED"
    );
}

fn edit_package(bytes: Vec<u8>, edit: impl Fn(&mut Value, &mut Value)) -> Vec<u8> {
    let mut zip = zip::ZipArchive::new(Cursor::new(bytes)).unwrap();
    let mut manifest: Value =
        serde_json::from_reader(zip.by_name("manifest.json").unwrap()).unwrap();
    let mut program: Value =
        serde_json::from_reader(zip.by_name("bin/workflow.json").unwrap()).unwrap();
    edit(&mut manifest, &mut program);
    signed_files(BTreeMap::from([
        (
            "manifest.json".into(),
            serde_json::to_vec(&manifest).unwrap(),
        ),
        (
            "bin/workflow.json".into(),
            serde_json::to_vec(&program).unwrap(),
        ),
    ]))
}

#[test]
fn dependency_validation_and_multiple_owners_remain_isolated() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let dependent = edit_package(archive("1.0.0", "echo", vec![], false), |m, p| {
        m["plugin_id"] = json!("atlas.acceptance.dependent");
        m["dependencies"] = json!([{"plugin_id":"atlas.acceptance.echo", "version":">=1.0.0", "dependency_type":"Required"}]);
        p["nodes"][0]["typeName"] = json!("atlas.acceptance.dependent.echo");
    });
    let file = f.directory.path().join("dependent.atlas-plugin");
    fs::write(&file, dependent).unwrap();
    let mut s = f.open();
    let review = s.inspect_local(&file).unwrap();
    assert_eq!(
        s.install(
            review["reviewId"].as_str().unwrap(),
            vec![],
            "missing-dependency"
        )
        .unwrap_err()
        .code,
        "DEPENDENCY_FAILURE"
    );
    install(&mut s, "1.0.0");
    s.change("atlas.acceptance.echo", "enable", "e").unwrap();
    s.install(review["reviewId"].as_str().unwrap(), vec![], "dependent")
        .unwrap();
    s.change("atlas.acceptance.dependent", "enable", "e2")
        .unwrap();
    assert_eq!(s.registrations().len(), 2);
    assert_eq!(
        s.change("atlas.acceptance.echo", "uninstall", "blocked")
            .unwrap_err()
            .code,
        "DEPENDENCY_FAILURE"
    );
    s.change("atlas.acceptance.dependent", "uninstall", "u")
        .unwrap();
    assert_eq!(s.registrations().len(), 1);
    assert!(s
        .execute(
            "atlas.acceptance.echo",
            "atlas.acceptance.echo.echo",
            &json!({}),
            &json!({})
        )
        .is_ok());
}

#[test]
fn unsigned_package_and_undeclared_workflow_capability_are_rejected() {
    let f = Fixture::new();
    let runtime = SemanticVersion::parse("0.15.0-alpha").unwrap();
    let bytes = edit_package(archive("1.0.0", "echo", vec![], false), |m, _| {
        m["capabilities"] = json!([])
    });
    assert_eq!(
        verify(bytes, None, &f.provider.verification_key(), &runtime)
            .err()
            .unwrap()
            .code,
        "PERMISSION_DENIED"
    );
    let mut writer = zip::ZipWriter::new(Cursor::new(Vec::new()));
    writer
        .start_file("manifest.json", zip::write::FileOptions::default())
        .unwrap();
    writer.write_all(b"{}").unwrap();
    assert!(verify(
        writer.finish().unwrap().into_inner(),
        None,
        &f.provider.verification_key(),
        &runtime
    )
    .is_err());
}

#[test]
fn orphan_cleanup_preserves_committed_and_unrelated_files() {
    let f = Fixture::new();
    f.publish("1.0.0", &archive("1.0.0", "echo", vec![], false));
    let mut s = f.open();
    install(&mut s, "1.0.0");
    let root = s.store.root.clone();
    let staging = root.join(format!("{}.staging", uuid::Uuid::new_v4()));
    fs::write(&staging, "interrupted").unwrap();
    let orphan = root.join(format!("{}.atlas-plugin", "0".repeat(64)));
    fs::write(&orphan, "orphan").unwrap();
    fs::write(root.join("user-note.txt"), "keep").unwrap();
    drop(s);
    let s = f.open();
    assert!(!staging.exists());
    assert!(!orphan.exists());
    assert!(root.join("user-note.txt").exists());
    assert!(s
        .store
        .blob(&s.state.installed["atlas.acceptance.echo"].digest)
        .unwrap()
        .exists());
}
