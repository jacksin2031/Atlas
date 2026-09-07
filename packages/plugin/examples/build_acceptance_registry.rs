//! Generates disposable packages signed by a PUBLIC development key, never a production key.
use base64::{engine::general_purpose::STANDARD, Engine};
use ed25519_dalek::{Signer, SigningKey};
use serde_json::json;
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs,
    io::{Cursor, Write},
    path::PathBuf,
};

fn main() {
    let root = PathBuf::from(
        std::env::args()
            .nth(1)
            .expect("output registry directory required"),
    );
    fs::create_dir_all(&root).unwrap();
    let key = SigningKey::from_bytes(&[17; 32]);
    fs::write(
        root.join("public-key.txt"),
        STANDARD.encode(key.verifying_key().to_bytes()),
    )
    .unwrap();
    let mut index = Vec::new();
    for (id, version, operation, extra_permission, fail_health) in [
        ("atlas.acceptance.echo", "1.0.0", "echo", false, false),
        ("atlas.acceptance.echo", "1.1.0", "constant", false, false),
        ("atlas.acceptance.echo", "1.2.0", "echo", true, false),
        ("atlas.acceptance.failure", "1.0.0", "fail", false, false),
        (
            "atlas.acceptance.denied",
            "1.0.0",
            "require_permission",
            false,
            false,
        ),
        ("atlas.acceptance.unhealthy", "1.0.0", "echo", false, true),
    ] {
        let manifest = json!({
            "manifest_version":"1.0.0", "plugin_id":id, "plugin_name":if id.ends_with("echo") {"Marketplace Echo"} else {id},
            "description":"Disposable acceptance package from the Local Development Registry", "author":"Atlas acceptance", "license":"MIT", "version":version,
            "entry_point":"bin/workflow.json", "capabilities":[{"capability":"Workflow","enabled":true}],
            "permissions": if extra_permission {json!([{"name":"PERM-NETWORK-OUTBOUND","level":"Elevated","required":true}])} else {json!([])},
            "dependencies":[], "compatibility":{"minimum_runtime_version":"0.15.0-alpha","api_version":"1.0.0"}
        });
        let program = json!({"format":"atlas.safe-workflow.v1","platforms":["windows","linux","macos"],"architectures":["x86_64","aarch64"],"fail_health":fail_health,
            "nodes":[{"typeName":format!("{id}.echo"),"label":if id.ends_with("echo"){"Marketplace Echo"}else{id},"operation":operation,"value":"ATLAS_MARKETPLACE_1710","permission":"PERM-NETWORK-OUTBOUND"}]});
        let mut files = BTreeMap::from([
            (
                "manifest.json".to_string(),
                serde_json::to_vec_pretty(&manifest).unwrap(),
            ),
            (
                "bin/workflow.json".to_string(),
                serde_json::to_vec_pretty(&program).unwrap(),
            ),
        ]);
        let sums = files
            .iter()
            .map(|(name, data)| format!("{:x}  {name}\n", Sha256::digest(data)))
            .collect::<String>();
        files.insert("checksum.sha256".into(), sums.into_bytes());
        let mut hash = Sha256::new();
        for (name, data) in &files {
            hash.update((name.len() as u64).to_be_bytes());
            hash.update(name.as_bytes());
            hash.update((data.len() as u64).to_be_bytes());
            hash.update(data);
        }
        files.insert(
            "signature.sig".into(),
            format!(
                "Ed25519:{}",
                STANDARD.encode(key.sign(&hash.finalize()).to_bytes())
            )
            .into_bytes(),
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
        let bytes = zip.finish().unwrap().into_inner();
        let filename = format!("{id}-{version}.atlas-plugin");
        fs::write(root.join(&filename), &bytes).unwrap();
        index.push(json!({"pluginId":id,"version":version,"filename":filename,"digest":format!("{:x}",Sha256::digest(&bytes))}));
    }
    fs::write(
        root.join("index.json"),
        serde_json::to_vec_pretty(&index).unwrap(),
    )
    .unwrap();
    println!("Generated {} signed development packages", index.len());
}
