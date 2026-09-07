use super::{failure, DistributionError};
use crate::{PluginManifest, SemanticVersion};
use base64::{engine::general_purpose::STANDARD, Engine};
use ed25519_dalek::{Signature, VerifyingKey};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    io::{Cursor, Read},
    path::Path,
};

pub const MAX_PACKAGE_BYTES: usize = 8 * 1024 * 1024;
pub const PERMISSIONS: &[&str] = &[
    "PERM-FILESYSTEM-READ",
    "PERM-FILESYSTEM-WRITE",
    "PERM-NETWORK-OUTBOUND",
    "PERM-NETWORK-INBOUND",
    "PERM-IPC-SEND",
    "PERM-IPC-RECEIVE",
    "PERM-EVENT-PUBLISH",
    "PERM-EVENT-SUBSCRIBE",
    "PERM-CONFIG-READ",
    "PERM-CONFIG-WRITE",
    "PERM-MARKETPLACE-ACCESS",
    "PERM-RESOURCE-LIMIT",
    "PERM-AUDIT-LOG",
    "PERM-HOST-INTEGRATION",
];

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, rename_all = "camelCase")]
pub struct PackageNode {
    pub type_name: String,
    pub label: String,
    pub operation: String,
    #[serde(default)]
    pub value: String,
    #[serde(default)]
    pub permission: Option<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Program {
    pub format: String,
    pub platforms: Vec<String>,
    pub architectures: Vec<String>,
    pub nodes: Vec<PackageNode>,
    #[serde(default)]
    pub fail_health: bool,
}

#[derive(Clone)]
pub struct VerifiedPackage {
    pub manifest: PluginManifest,
    pub program: Program,
    pub digest: String,
    pub bytes: Vec<u8>,
}

pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

pub fn safe_identifier(value: &str) -> bool {
    (3..=120).contains(&value.len())
        && value.as_bytes()[0].is_ascii_alphanumeric()
        && value
            .bytes()
            .all(|c| c.is_ascii_alphanumeric() || b"_.-".contains(&c))
}

fn safe_path(name: &str) -> bool {
    !name.is_empty()
        && !name.contains(['\\', ':', '\0'])
        && !name.starts_with('/')
        && !name.chars().any(char::is_control)
        && name.split('/').all(|p| {
            !p.is_empty()
                && p != "."
                && p != ".."
                && !p.ends_with([' ', '.'])
                && !matches!(
                    p.split('.')
                        .next()
                        .unwrap_or("")
                        .to_ascii_uppercase()
                        .as_str(),
                    "CON"
                        | "PRN"
                        | "AUX"
                        | "NUL"
                        | "COM1"
                        | "COM2"
                        | "COM3"
                        | "COM4"
                        | "COM5"
                        | "COM6"
                        | "COM7"
                        | "COM8"
                        | "COM9"
                        | "LPT1"
                        | "LPT2"
                        | "LPT3"
                        | "LPT4"
                        | "LPT5"
                        | "LPT6"
                        | "LPT7"
                        | "LPT8"
                        | "LPT9"
                )
        })
}

pub fn read_bounded(path: &Path) -> Result<Vec<u8>, DistributionError> {
    let metadata = std::fs::symlink_metadata(path)
        .map_err(|_| failure("PACKAGE_NOT_FOUND", "Package file unavailable"))?;
    if !metadata.is_file()
        || metadata.file_type().is_symlink()
        || metadata.len() > MAX_PACKAGE_BYTES as u64
    {
        return Err(failure(
            "INVALID_PACKAGE",
            "Package must be a bounded regular file",
        ));
    }
    let mut data = Vec::new();
    std::fs::File::open(path)
        .map_err(super::storage_error)?
        .take(MAX_PACKAGE_BYTES as u64 + 1)
        .read_to_end(&mut data)
        .map_err(super::storage_error)?;
    if data.len() > MAX_PACKAGE_BYTES {
        return Err(failure("INVALID_PACKAGE", "Package too large"));
    }
    Ok(data)
}

pub fn verify(
    bytes: Vec<u8>,
    expected: Option<&str>,
    key: &[u8; 32],
    runtime: &SemanticVersion,
) -> Result<VerifiedPackage, DistributionError> {
    if bytes.len() > MAX_PACKAGE_BYTES {
        return Err(failure("INVALID_PACKAGE", "Package too large"));
    }
    let hash = digest(&bytes);
    if expected.is_some_and(|e| e != hash) {
        return Err(failure(
            "PACKAGE_INTEGRITY_FAILURE",
            "Package digest mismatch",
        ));
    }
    let mut zip = zip::ZipArchive::new(Cursor::new(&bytes))
        .map_err(|_| failure("INVALID_PACKAGE", "Invalid ZIP archive"))?;
    if zip.len() > 128 {
        return Err(failure("INVALID_PACKAGE", "Too many package entries"));
    }
    let mut files = BTreeMap::new();
    let mut names = BTreeSet::new();
    let mut total = 0;
    for i in 0..zip.len() {
        let mut file = zip
            .by_index(i)
            .map_err(|_| failure("INVALID_PACKAGE", "Unreadable ZIP entry"))?;
        let name = file.name().to_string();
        if !safe_path(&name)
            || file
                .unix_mode()
                .is_some_and(|m| m & 0o170000 != 0 && m & 0o170000 != 0o100000)
            || !names.insert(name.to_ascii_lowercase())
        {
            return Err(failure(
                "INVALID_PACKAGE",
                "Unsafe, linked, or duplicate package path",
            ));
        }
        let mut data = Vec::new();
        (&mut file)
            .take(MAX_PACKAGE_BYTES as u64 + 1)
            .read_to_end(&mut data)
            .map_err(|_| failure("INVALID_PACKAGE", "Invalid ZIP content"))?;
        total += data.len();
        if total > MAX_PACKAGE_BYTES {
            return Err(failure("INVALID_PACKAGE", "Expanded package too large"));
        }
        files.insert(name, data);
    }
    let required = |name: &str| {
        files
            .get(name)
            .ok_or_else(|| failure("INVALID_PACKAGE", "Required package file missing"))
    };
    let checksums = required("checksum.sha256")?;
    let mut calculated = String::new();
    for (name, data) in &files {
        if name != "signature.sig" && name != "checksum.sha256" {
            calculated.push_str(&format!("{}  {}\n", digest(data), name));
        }
    }
    if checksums != calculated.as_bytes() {
        return Err(failure(
            "PACKAGE_INTEGRITY_FAILURE",
            "Content checksum mismatch",
        ));
    }
    let mut signed = Sha256::new();
    for (name, data) in &files {
        if name != "signature.sig" {
            signed.update((name.len() as u64).to_be_bytes());
            signed.update(name.as_bytes());
            signed.update((data.len() as u64).to_be_bytes());
            signed.update(data);
        }
    }
    let signature = std::str::from_utf8(required("signature.sig")?)
        .ok()
        .and_then(|s| s.strip_prefix("Ed25519:"))
        .and_then(|s| STANDARD.decode(s).ok())
        .and_then(|s| Signature::from_slice(&s).ok())
        .ok_or_else(|| failure("SIGNATURE_FAILURE", "Valid Ed25519 signature required"))?;
    VerifyingKey::from_bytes(key)
        .map_err(|_| failure("SIGNATURE_FAILURE", "Invalid signing key"))?
        .verify_strict(&signed.finalize(), &signature)
        .map_err(|_| {
            failure(
                "SIGNATURE_FAILURE",
                "Signature does not match configured provider key",
            )
        })?;
    let manifest = PluginManifest::from_json(
        std::str::from_utf8(required("manifest.json")?)
            .map_err(|_| failure("INVALID_MANIFEST", "Manifest must be UTF-8"))?,
    )
    .map_err(|e| failure("INVALID_MANIFEST", &e.to_string()))?;
    if !safe_identifier(&manifest.plugin_id)
        || manifest.plugin_name.trim().is_empty()
        || manifest.manifest_version != "1.0.0"
    {
        return Err(failure(
            "INVALID_MANIFEST",
            "Unsupported schema or invalid identity/name",
        ));
    }
    manifest
        .check_compatibility(runtime, &SemanticVersion::parse("1.0.0").unwrap())
        .map_err(|e| failure("INCOMPATIBLE_PLUGIN", &e.to_string()))?;
    let mut permissions = BTreeSet::new();
    for p in &manifest.permissions {
        if !PERMISSIONS.contains(&p.name.as_str()) || !permissions.insert(&p.name) {
            return Err(failure(
                "INVALID_MANIFEST",
                "Unknown or duplicate permission",
            ));
        }
    }
    if !safe_path(&manifest.entry_point) || !manifest.entry_point.starts_with("bin/") {
        return Err(failure("INVALID_MANIFEST", "Invalid package entrypoint"));
    }
    let program: Program = serde_json::from_slice(required(&manifest.entry_point)?)
        .map_err(|_| failure("INVALID_MANIFEST", "Unsupported declarative entrypoint"))?;
    if program.format != "atlas.safe-workflow.v1"
        || program.nodes.is_empty()
        || program.nodes.len() > 32
    {
        return Err(failure(
            "INVALID_MANIFEST",
            "Unsupported program format or node count",
        ));
    }
    if !program.platforms.iter().any(|p| p == std::env::consts::OS)
        || !program
            .architectures
            .iter()
            .any(|p| p == std::env::consts::ARCH)
    {
        return Err(failure(
            "INCOMPATIBLE_PLUGIN",
            "Platform or architecture not supported",
        ));
    }
    if !manifest
        .provided_capabilities()
        .contains(&crate::PluginCapability::Workflow)
    {
        return Err(failure(
            "PERMISSION_DENIED",
            "Workflow capability must be declared",
        ));
    }
    let mut node_types = BTreeSet::new();
    for node in &program.nodes {
        if !safe_identifier(&node.type_name)
            || !node
                .type_name
                .starts_with(&format!("{}.", manifest.plugin_id))
            || !node_types.insert(&node.type_name)
            || node.label.trim().is_empty()
            || ![
                "echo",
                "constant",
                "prefix",
                "uppercase",
                "lowercase",
                "fail",
                "require_permission",
            ]
            .contains(&node.operation.as_str())
        {
            return Err(failure(
                "INVALID_MANIFEST",
                "Invalid, duplicate, unowned, or unsupported node",
            ));
        }
    }
    drop(zip);
    Ok(VerifiedPackage {
        manifest,
        program,
        digest: hash,
        bytes,
    })
}
