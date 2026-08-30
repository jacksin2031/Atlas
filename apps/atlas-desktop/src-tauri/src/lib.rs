use base64::{engine::general_purpose::STANDARD, Engine as _};
use image::{codecs::png::PngEncoder, ColorType, ImageEncoder, RgbaImage};
use screenshots::Screen;
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};
use std::process::{Child, ChildStdin, Command, Stdio};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tauri::{AppHandle, Emitter, Manager, State};

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct VisionFrameSource {
    frame_id: String,
    name: String,
    url: String,
    width: u32,
    height: u32,
    origin_x: i32,
    origin_y: i32,
    scale_factor: f32,
    coordinate_space: &'static str,
    captured_at: u128,
    kind: &'static str,
}

#[tauri::command]
fn vision_capture_frame() -> Result<VisionFrameSource, String> {
    let mut screens =
        Screen::all().map_err(|error| format!("Unable to enumerate displays: {error}"))?;
    if screens.is_empty() {
        return Err("No display is available for capture".to_owned());
    }
    let primary_index = screens
        .iter()
        .position(|candidate| candidate.display_info.is_primary)
        .unwrap_or(0);
    let screen = screens.swap_remove(primary_index);
    let image = screen
        .capture()
        .map_err(|error| format!("Unable to capture display: {error}"))?;
    let mut png = Vec::new();
    PngEncoder::new(&mut png)
        .write_image(
            image.as_raw(),
            image.width(),
            image.height(),
            ColorType::Rgba8.into(),
        )
        .map_err(|error| format!("Unable to encode captured frame: {error}"))?;

    let captured_at = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|error| format!("System clock error: {error}"))?
        .as_millis();
    Ok(VisionFrameSource {
        frame_id: format!("frame-{}-{captured_at}", screen.display_info.id),
        name: format!("{} capture", screen.display_info.id),
        url: format!("data:image/png;base64,{}", STANDARD.encode(png)),
        width: image.width(),
        height: image.height(),
        origin_x: screen.display_info.x,
        origin_y: screen.display_info.y,
        scale_factor: screen.display_info.scale_factor,
        coordinate_space: "screen",
        captured_at,
        kind: "screenshot",
    })
}

fn decode_image_data_url(url: &str) -> Result<RgbaImage, String> {
    let bytes = decode_image_data_url_bytes(url)?;
    image::load_from_memory(&bytes)
        .map(|image| image.to_rgba8())
        .map_err(|error| format!("Unable to read Vision frame image: {error}"))
}

fn decode_image_data_url_bytes(url: &str) -> Result<Vec<u8>, String> {
    let encoded = url
        .split_once(',')
        .map(|(_, value)| value)
        .ok_or_else(|| "Vision frame must be an image data URL.".to_owned())?;
    STANDARD
        .decode(encoded)
        .map_err(|error| format!("Unable to decode Vision frame: {error}"))
}

fn parse_rgb(value: &str) -> Result<[u8; 3], String> {
    let hex = value.trim().trim_start_matches('#');
    if hex.len() != 6 {
        return Err("targetColor must use #RRGGBB format.".to_owned());
    }
    let channel = |start| {
        u8::from_str_radix(&hex[start..start + 2], 16)
            .map_err(|error| format!("Invalid targetColor: {error}"))
    };
    Ok([channel(0)?, channel(2)?, channel(4)?])
}

fn frame_origin(payload: &Value) -> (i64, i64, &str) {
    let frame = payload.get("frame").unwrap_or(&Value::Null);
    (
        frame.get("originX").and_then(Value::as_i64).unwrap_or(0),
        frame.get("originY").and_then(Value::as_i64).unwrap_or(0),
        frame
            .get("frameId")
            .and_then(Value::as_str)
            .unwrap_or("unknown-frame"),
    )
}

fn vision_color_detection(payload: &Value) -> HostResult {
    let frame = payload
        .get("frame")
        .ok_or_else(|| "Vision resolver requires frame.".to_owned())?;
    let configuration = payload.get("configuration").unwrap_or(&Value::Null);
    let image = decode_image_data_url(
        frame
            .get("url")
            .and_then(Value::as_str)
            .ok_or_else(|| "Vision frame has no URL.".to_owned())?,
    )?;
    let target = parse_rgb(
        configuration
            .get("targetColor")
            .and_then(Value::as_str)
            .unwrap_or("#ff00c8"),
    )?;
    let tolerance = configuration
        .get("tolerance")
        .and_then(Value::as_u64)
        .unwrap_or(6)
        .min(255) as i16;
    let min_area = configuration
        .get("minArea")
        .and_then(Value::as_u64)
        .unwrap_or(24);
    let mut min_x = image.width();
    let mut min_y = image.height();
    let mut max_x = 0;
    let mut max_y = 0;
    let mut count = 0_u64;
    for (x, y, pixel) in image.enumerate_pixels() {
        let close = (0..3).all(|channel| {
            (i16::from(pixel[channel]) - i16::from(target[channel])).abs() <= tolerance
        });
        if close {
            min_x = min_x.min(x);
            min_y = min_y.min(y);
            max_x = max_x.max(x);
            max_y = max_y.max(y);
            count += 1;
        }
    }
    if count < min_area {
        return Ok(
            json!({"operation":"detection","matched":false,"matches":[],"sampleCount":count}),
        );
    }
    let (origin_x, origin_y, frame_id) = frame_origin(payload);
    let width = max_x - min_x + 1;
    let height = max_y - min_y + 1;
    let density = count as f64 / f64::from(width * height);
    Ok(json!({
        "operation":"detection",
        "matched":true,
        "matches":[{
            "x": origin_x + i64::from(min_x), "y": origin_y + i64::from(min_y),
            "width": width, "height": height, "confidence": density,
            "label": configuration.get("label").and_then(Value::as_str).unwrap_or("color-target"),
            "sourceFrameId": frame_id
        }],
        "sampleCount":count
    }))
}

fn vision_template_match(payload: &Value) -> HostResult {
    let frame = payload
        .get("frame")
        .ok_or_else(|| "Template resolver requires frame.".to_owned())?;
    let configuration = payload.get("configuration").unwrap_or(&Value::Null);
    let source = decode_image_data_url(
        frame
            .get("url")
            .and_then(Value::as_str)
            .ok_or_else(|| "Vision frame has no URL.".to_owned())?,
    )?;
    let template = decode_image_data_url(
        configuration
            .get("templateUrl")
            .and_then(Value::as_str)
            .filter(|value| !value.is_empty())
            .ok_or_else(|| "Image Detection requires a template image.".to_owned())?,
    )?;
    if template.width() > source.width() || template.height() > source.height() {
        return Ok(json!({"operation":"template","matched":false,"matches":[]}));
    }
    let threshold = configuration
        .get("threshold")
        .and_then(Value::as_f64)
        .unwrap_or(0.95)
        .clamp(0.0, 1.0);
    let sample_step = configuration
        .get("sampleStep")
        .and_then(Value::as_u64)
        .unwrap_or(2)
        .max(1) as u32;
    let mut best = (0.0_f64, 0_u32, 0_u32);
    for y in (0..=source.height() - template.height()).step_by(sample_step as usize) {
        for x in (0..=source.width() - template.width()).step_by(sample_step as usize) {
            let mut difference = 0_u64;
            let mut samples = 0_u64;
            for ty in (0..template.height()).step_by(sample_step as usize) {
                for tx in (0..template.width()).step_by(sample_step as usize) {
                    let a = source.get_pixel(x + tx, y + ty);
                    let b = template.get_pixel(tx, ty);
                    difference += (0..3)
                        .map(|channel| {
                            (i16::from(a[channel]) - i16::from(b[channel])).unsigned_abs() as u64
                        })
                        .sum::<u64>();
                    samples += 3;
                }
            }
            let similarity = 1.0 - difference as f64 / (samples.max(1) as f64 * 255.0);
            if similarity > best.0 {
                best = (similarity, x, y);
            }
        }
    }
    if best.0 < threshold {
        return Ok(
            json!({"operation":"template","matched":false,"matches":[],"bestSimilarity":best.0}),
        );
    }
    let (origin_x, origin_y, frame_id) = frame_origin(payload);
    Ok(json!({"operation":"template","matched":true,"matches":[{
        "x":origin_x + i64::from(best.1), "y":origin_y + i64::from(best.2),
        "width":template.width(), "height":template.height(), "confidence":best.0,
        "label":configuration.get("label").and_then(Value::as_str).unwrap_or("template-match"),
        "sourceFrameId":frame_id
    }]}))
}

#[cfg(windows)]
fn vision_windows_ocr(payload: &Value) -> HostResult {
    use windows::Graphics::Imaging::BitmapDecoder;
    use windows::Media::Ocr::OcrEngine;
    use windows::Storage::Streams::{DataWriter, InMemoryRandomAccessStream};

    let frame = payload
        .get("frame")
        .ok_or_else(|| "OCR resolver requires frame.".to_owned())?;
    let bytes = decode_image_data_url_bytes(
        frame
            .get("url")
            .and_then(Value::as_str)
            .ok_or_else(|| "Vision frame has no URL.".to_owned())?,
    )?;
    let stream = InMemoryRandomAccessStream::new()
        .map_err(|error| format!("Unable to create OCR image stream: {error}"))?;
    let output = stream
        .GetOutputStreamAt(0)
        .map_err(|error| format!("Unable to open OCR image stream: {error}"))?;
    let writer = DataWriter::CreateDataWriter(&output)
        .map_err(|error| format!("Unable to create OCR image writer: {error}"))?;
    writer
        .WriteBytes(&bytes)
        .map_err(|error| format!("Unable to write OCR image: {error}"))?;
    let store = writer
        .StoreAsync()
        .map_err(|error| format!("Unable to store OCR image: {error}"))?;
    store
        .join()
        .map_err(|error| format!("Unable to store OCR image: {error}"))?;
    let flush = writer
        .FlushAsync()
        .map_err(|error| format!("Unable to flush OCR image: {error}"))?;
    flush
        .join()
        .map_err(|error| format!("Unable to flush OCR image: {error}"))?;
    stream
        .Seek(0)
        .map_err(|error| format!("Unable to rewind OCR image: {error}"))?;
    let decode = BitmapDecoder::CreateAsync(&stream)
        .map_err(|error| format!("Unable to decode OCR image: {error}"))?;
    let decoder = decode
        .join()
        .map_err(|error| format!("Unable to decode OCR image: {error}"))?;
    let software_bitmap = decoder
        .GetSoftwareBitmapAsync()
        .map_err(|error| format!("Unable to create OCR bitmap: {error}"))?;
    let bitmap = software_bitmap
        .join()
        .map_err(|error| format!("Unable to create OCR bitmap: {error}"))?;
    let engine = OcrEngine::TryCreateFromUserProfileLanguages()
        .map_err(|error| format!("No Windows OCR language is available: {error}"))?;
    let recognition = engine
        .RecognizeAsync(&bitmap)
        .map_err(|error| format!("Windows OCR failed: {error}"))?;
    let result = recognition
        .join()
        .map_err(|error| format!("Windows OCR failed: {error}"))?;
    let contains = payload
        .get("configuration")
        .and_then(|value| value.get("contains"))
        .and_then(Value::as_str)
        .map(str::to_lowercase);
    let (origin_x, origin_y, frame_id) = frame_origin(payload);
    let mut matches = Vec::new();
    for line in result
        .Lines()
        .map_err(|error| format!("Unable to read OCR lines: {error}"))?
    {
        for word in line
            .Words()
            .map_err(|error| format!("Unable to read OCR words: {error}"))?
        {
            let text = word
                .Text()
                .map_err(|error| format!("Unable to read OCR text: {error}"))?
                .to_string();
            if contains
                .as_ref()
                .is_some_and(|needle| !text.to_lowercase().contains(needle))
            {
                continue;
            }
            let bounds = word
                .BoundingRect()
                .map_err(|error| format!("Unable to read OCR bounds: {error}"))?;
            matches.push(json!({
                "x": origin_x + bounds.X.floor() as i64,
                "y": origin_y + bounds.Y.floor() as i64,
                "width": bounds.Width.ceil().max(1.0) as u32,
                "height": bounds.Height.ceil().max(1.0) as u32,
                "text": text,
                "label": text,
                "sourceFrameId": frame_id,
            }));
        }
    }
    Ok(json!({
        "operation": "ocr",
        "matched": !matches.is_empty(),
        "matches": matches,
        "text": result.Text().map(|value| value.to_string()).unwrap_or_default(),
        "provider": "windows.media.ocr",
    }))
}

#[cfg(not(windows))]
fn vision_windows_ocr(_payload: &Value) -> HostResult {
    Err("The native OCR provider is not implemented for this platform.".to_owned())
}

fn vision_resolve_target(payload: &Value) -> HostResult {
    match payload
        .get("operation")
        .and_then(Value::as_str)
        .unwrap_or("detection")
    {
        "detection" => vision_color_detection(payload),
        "template" => vision_template_match(payload),
        "ocr" => vision_windows_ocr(payload),
        operation => Err(format!(
            "Unsupported Vision resolver operation: {operation}"
        )),
    }
}

const PROJECT_ASSET_VERSION: u64 = 1;
const PROJECT_SESSION_VERSION: u64 = 1;

fn project_asset_paths(project_path: &str) -> Result<(PathBuf, PathBuf), String> {
    let root = PathBuf::from(project_path);
    if !root.is_absolute() || !root.is_dir() {
        return Err(
            "Project asset persistence requires an existing absolute project directory.".to_owned(),
        );
    }
    let directory = root.join(".atlas");
    Ok((
        directory.join("project-assets.v1.json"),
        directory.join("project-assets.v1.backup.json"),
    ))
}

#[tauri::command]
fn project_select_directory() -> Option<String> {
    rfd::FileDialog::new()
        .set_title("Open Atlas Project")
        .pick_folder()
        .map(|path| path.to_string_lossy().into_owned())
}

fn write_project_session(path: &Path, project_path: &str) -> Result<(), String> {
    let project = PathBuf::from(project_path);
    if !project.is_absolute() || !project.is_dir() {
        return Err("Project session requires an existing absolute project directory.".to_owned());
    }
    let directory = path
        .parent()
        .ok_or_else(|| "Project session directory is invalid.".to_owned())?;
    fs::create_dir_all(directory)
        .map_err(|error| format!("Unable to create project session directory: {error}"))?;
    let temporary = path.with_extension("tmp");
    let bytes = serde_json::to_vec(&json!({
        "version": PROJECT_SESSION_VERSION,
        "projectPath": project_path,
    }))
    .map_err(|error| format!("Unable to encode project session: {error}"))?;
    fs::write(&temporary, bytes)
        .map_err(|error| format!("Unable to write project session: {error}"))?;
    fs::rename(&temporary, path)
        .map_err(|error| format!("Unable to commit project session: {error}"))
}

fn read_project_session(path: &Path) -> Result<Option<String>, String> {
    if !path.is_file() {
        return Ok(None);
    }
    let raw = fs::read_to_string(path)
        .map_err(|error| format!("Unable to read project session: {error}"))?;
    let value: Value = serde_json::from_str(&raw)
        .map_err(|error| format!("Unable to parse project session: {error}"))?;
    if value.get("version").and_then(Value::as_u64) != Some(PROJECT_SESSION_VERSION) {
        return Err("Project session version is not supported.".to_owned());
    }
    let project_path = value
        .get("projectPath")
        .and_then(Value::as_str)
        .ok_or_else(|| "Project session has no project path.".to_owned())?;
    let project = PathBuf::from(project_path);
    if !project.is_absolute() || !project.is_dir() {
        return Ok(None);
    }
    Ok(Some(project_path.to_owned()))
}

fn project_session_path(app: &AppHandle) -> Result<PathBuf, String> {
    app.path()
        .app_data_dir()
        .map(|directory| directory.join("project-session.v1.json"))
        .map_err(|error| format!("Unable to resolve Atlas application data: {error}"))
}

#[tauri::command(rename_all = "camelCase")]
fn project_session_remember(app: AppHandle, project_path: String) -> Result<(), String> {
    write_project_session(&project_session_path(&app)?, &project_path)
}

#[tauri::command]
fn project_session_restore(app: AppHandle) -> Result<Option<String>, String> {
    read_project_session(&project_session_path(&app)?)
}

#[tauri::command]
fn project_session_clear(app: AppHandle) -> Result<(), String> {
    let path = project_session_path(&app)?;
    if path.is_file() {
        fs::remove_file(path)
            .map_err(|error| format!("Unable to clear project session: {error}"))?;
    }
    Ok(())
}

fn credential_shaped_key(key: &str) -> bool {
    let normalized: String = key
        .chars()
        .filter(|value| value.is_ascii_alphanumeric())
        .map(|value| value.to_ascii_lowercase())
        .collect();
    matches!(
        normalized.as_str(),
        "apikey"
            | "authorization"
            | "credential"
            | "credentials"
            | "secret"
            | "password"
            | "accesstoken"
            | "refreshtoken"
            | "bearertoken"
            | "privatekey"
    )
}

fn reject_credentials(value: &Value, path: &str) -> Result<(), String> {
    match value {
        Value::Object(values) => {
            for (key, item) in values {
                let next = if path.is_empty() {
                    key.clone()
                } else {
                    format!("{path}.{key}")
                };
                if credential_shaped_key(key) {
                    return Err(format!(
                        "Project assets rejected credential-shaped field: {next}"
                    ));
                }
                reject_credentials(item, &next)?;
            }
        }
        Value::Array(values) => {
            for (index, item) in values.iter().enumerate() {
                reject_credentials(item, &format!("{path}[{index}]"))?;
            }
        }
        _ => {}
    }
    Ok(())
}

fn read_project_asset_file(path: &Path) -> Result<Value, String> {
    let raw = fs::read_to_string(path)
        .map_err(|error| format!("Unable to read project assets: {error}"))?;
    let document: Value = serde_json::from_str(&raw)
        .map_err(|error| format!("Unable to parse project assets: {error}"))?;
    if document.get("version").and_then(Value::as_u64) != Some(PROJECT_ASSET_VERSION) {
        return Err("Project asset version is not supported.".to_owned());
    }
    Ok(document.get("assets").cloned().unwrap_or_else(|| json!({})))
}

#[tauri::command(rename_all = "camelCase")]
fn project_assets_load(project_path: String) -> HostResult {
    let (path, backup) = project_asset_paths(&project_path)?;
    if path.is_file() {
        match read_project_asset_file(&path) {
            Ok(value) => return Ok(value),
            Err(primary_error) if backup.is_file() => {
                return read_project_asset_file(&backup).map_err(|backup_error| {
                    format!("{primary_error} Recovery backup also failed: {backup_error}")
                });
            }
            Err(error) => return Err(error),
        }
    }
    if backup.is_file() {
        return read_project_asset_file(&backup);
    }
    Ok(Value::Null)
}

#[tauri::command(rename_all = "camelCase")]
fn project_assets_save(project_path: String, assets: Value) -> Result<(), String> {
    reject_credentials(&assets, "assets")?;
    let (path, backup) = project_asset_paths(&project_path)?;
    let directory = path
        .parent()
        .ok_or_else(|| "Project asset directory is invalid.".to_owned())?;
    fs::create_dir_all(directory)
        .map_err(|error| format!("Unable to create project asset directory: {error}"))?;
    let temporary = directory.join("project-assets.v1.tmp.json");
    let saved_at = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|error| error.to_string())?
        .as_millis();
    let bytes = serde_json::to_vec_pretty(
        &json!({"version": PROJECT_ASSET_VERSION, "savedAt": saved_at, "assets": assets}),
    )
    .map_err(|error| format!("Unable to encode project assets: {error}"))?;
    fs::write(&temporary, bytes)
        .map_err(|error| format!("Unable to write project assets: {error}"))?;
    if path.is_file() {
        if backup.is_file() {
            fs::remove_file(&backup)
                .map_err(|error| format!("Unable to replace project recovery backup: {error}"))?;
        }
        fs::rename(&path, &backup)
            .map_err(|error| format!("Unable to create project recovery backup: {error}"))?;
    }
    if let Err(error) = fs::rename(&temporary, &path) {
        if backup.is_file() && !path.exists() {
            let _ = fs::rename(&backup, &path);
        }
        return Err(format!("Unable to commit project assets: {error}"));
    }
    Ok(())
}

type HostResult = Result<Value, String>;
type PendingRequests = Arc<Mutex<HashMap<String, mpsc::SyncSender<HostResult>>>>;
const CREDENTIAL_SERVICE: &str = "Atlas AI Provider";

fn validate_provider_id(provider_id: &str) -> Result<(), String> {
    if provider_id.is_empty()
        || !provider_id
            .chars()
            .all(|value| value.is_ascii_alphanumeric() || matches!(value, '-' | '_' | '.'))
    {
        return Err("Provider ID contains unsupported characters.".to_owned());
    }
    Ok(())
}

#[cfg(windows)]
fn credential_entry(provider_id: &str) -> Result<keyring::Entry, String> {
    validate_provider_id(provider_id)?;
    keyring::Entry::new(CREDENTIAL_SERVICE, provider_id)
        .map_err(|error| format!("Unable to access the system credential vault: {error}"))
}

#[cfg(windows)]
fn load_provider_credential(provider_id: &str) -> Result<Option<String>, String> {
    match credential_entry(provider_id)?.get_password() {
        Ok(value) => Ok(Some(value)),
        Err(keyring::Error::NoEntry) => Ok(None),
        Err(error) => Err(format!(
            "Unable to read the system credential vault: {error}"
        )),
    }
}

#[cfg(not(windows))]
fn load_provider_credential(provider_id: &str) -> Result<Option<String>, String> {
    validate_provider_id(provider_id)?;
    Err("The secure credential vault is not implemented for this platform.".to_owned())
}

struct AIHostProcess {
    child: Child,
    stdin: Arc<Mutex<ChildStdin>>,
    pending: PendingRequests,
}

impl Drop for AIHostProcess {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

#[derive(Default)]
struct AIHostManager {
    process: Mutex<Option<AIHostProcess>>,
    next_id: AtomicU64,
}

impl AIHostManager {
    fn restart(&self) -> Result<(), String> {
        let mut process = self
            .process
            .lock()
            .map_err(|_| "AI Runtime host lock is poisoned.".to_owned())?;
        *process = None;
        Ok(())
    }

    fn request(&self, app: AppHandle, command: &str, payload: Value) -> HostResult {
        let request_id = format!(
            "desktop-{}-{}",
            std::process::id(),
            self.next_id.fetch_add(1, Ordering::Relaxed)
        );
        let (sender, receiver) = mpsc::sync_channel(1);

        {
            let mut process_guard = self
                .process
                .lock()
                .map_err(|_| "AI Runtime host lock is poisoned.".to_owned())?;
            if process_guard.is_none() {
                *process_guard = Some(start_ai_host(app)?);
            }
            let process = process_guard
                .as_mut()
                .ok_or_else(|| "AI Runtime host failed to start.".to_owned())?;
            process
                .pending
                .lock()
                .map_err(|_| "AI Runtime pending-request lock is poisoned.".to_owned())?
                .insert(request_id.clone(), sender);

            let message = json!({"id": request_id, "command": command, "payload": payload});
            let write_result = process
                .stdin
                .lock()
                .map_err(|_| "AI Runtime stdin lock is poisoned.".to_owned())
                .and_then(|mut stdin| {
                    serde_json::to_writer(&mut *stdin, &message)
                        .map_err(|error| format!("Unable to encode AI Runtime command: {error}"))?;
                    stdin
                        .write_all(b"\n")
                        .and_then(|_| stdin.flush())
                        .map_err(|error| format!("Unable to send AI Runtime command: {error}"))
                });
            if let Err(error) = write_result {
                process
                    .pending
                    .lock()
                    .ok()
                    .map(|mut pending| pending.remove(&request_id));
                *process_guard = None;
                return Err(error);
            }
        }

        match receiver.recv_timeout(Duration::from_secs(180)) {
            Ok(result) => result,
            Err(_) => {
                if let Ok(mut process_guard) = self.process.lock() {
                    if let Some(process) = process_guard.as_mut() {
                        if let Ok(mut pending) = process.pending.lock() {
                            pending.remove(&request_id);
                        }
                    }
                }
                Err(format!("AI Runtime command {command} timed out."))
            }
        }
    }
}

fn find_repo_root() -> Result<PathBuf, String> {
    if let Some(root) = env::var_os("ATLAS_ROOT").map(PathBuf::from) {
        if root.join("packages/ai/src/atlas_ai/host.py").is_file() {
            return Ok(root);
        }
    }
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let current = env::current_dir()
        .map_err(|error| format!("Unable to inspect working directory: {error}"))?;
    for start in [&manifest, &current] {
        for candidate in start.ancestors() {
            if candidate.join("packages/ai/src/atlas_ai/host.py").is_file() {
                return Ok(candidate.to_path_buf());
            }
        }
    }
    Err(
        "Unable to locate packages/ai/src/atlas_ai/host.py. Set ATLAS_ROOT to the repository root."
            .to_owned(),
    )
}

fn workflow_python_path(root: &Path) -> Result<std::ffi::OsString, String> {
    let mut paths = vec![
        root.join("src"),
        root.join("packages/ai/src"),
        root.join("packages/vision/src"),
    ];
    if let Some(existing) = env::var_os("PYTHONPATH") {
        paths.extend(env::split_paths(&existing));
    }
    env::join_paths(paths)
        .map_err(|error| format!("Unable to configure Workflow Python module path: {error}"))
}

fn python_path(root: &Path) -> Result<std::ffi::OsString, String> {
    let mut paths = vec![root.join("packages/ai/src")];
    if let Some(existing) = env::var_os("PYTHONPATH") {
        paths.extend(env::split_paths(&existing));
    }
    env::join_paths(paths)
        .map_err(|error| format!("Unable to configure Python module path: {error}"))
}

fn start_ai_host(app: AppHandle) -> Result<AIHostProcess, String> {
    let root = find_repo_root()?;
    let python = env::var_os("ATLAS_AI_PYTHON").unwrap_or_else(|| "python".into());
    let mut command = Command::new(python);
    command
        .arg("-u")
        .arg("-m")
        .arg("atlas_ai.host")
        .current_dir(&root)
        .env("PYTHONPATH", python_path(&root)?)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    if let Some(credential) = load_provider_credential("openai")? {
        command.env("ATLAS_AI_API_KEY", credential);
    }

    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        command.creation_flags(0x08000000);
    }

    let mut child = command
        .spawn()
        .map_err(|error| format!("Unable to start Python AI Runtime host: {error}"))?;
    let stdin = child
        .stdin
        .take()
        .ok_or_else(|| "Python AI Runtime host has no stdin pipe.".to_owned())?;
    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "Python AI Runtime host has no stdout pipe.".to_owned())?;
    let stderr = child
        .stderr
        .take()
        .ok_or_else(|| "Python AI Runtime host has no stderr pipe.".to_owned())?;
    let pending: PendingRequests = Arc::new(Mutex::new(HashMap::new()));
    let stdout_pending = Arc::clone(&pending);

    std::thread::spawn(move || {
        for line in BufReader::new(stdout).lines() {
            let Ok(line) = line else { break };
            let Ok(message) = serde_json::from_str::<Value>(&line) else {
                continue;
            };
            match message.get("kind").and_then(Value::as_str) {
                Some("response") => {
                    let id = message
                        .get("id")
                        .and_then(Value::as_str)
                        .unwrap_or_default();
                    let sender = stdout_pending
                        .lock()
                        .ok()
                        .and_then(|mut values| values.remove(id));
                    if let Some(sender) = sender {
                        let result = if message.get("ok").and_then(Value::as_bool).unwrap_or(false)
                        {
                            Ok(message.get("result").cloned().unwrap_or(Value::Null))
                        } else {
                            Err(message
                                .get("error")
                                .and_then(Value::as_str)
                                .unwrap_or("AI Runtime host command failed.")
                                .to_owned())
                        };
                        let _ = sender.send(result);
                    }
                }
                Some("event") => {
                    let event_name = message
                        .get("event")
                        .and_then(Value::as_str)
                        .unwrap_or("ai://runtime-event");
                    let payload = message.get("payload").cloned().unwrap_or(Value::Null);
                    let _ = app.emit(event_name, payload);
                }
                _ => {}
            }
        }
        if let Ok(mut values) = stdout_pending.lock() {
            for (_, sender) in values.drain() {
                let _ = sender.send(Err(
                    "Python AI Runtime host stopped unexpectedly.".to_owned()
                ));
            }
        }
    });

    std::thread::spawn(move || {
        for line in BufReader::new(stderr).lines().map_while(Result::ok) {
            eprintln!("[AI Runtime Host] {line}");
        }
    });

    Ok(AIHostProcess {
        child,
        stdin: Arc::new(Mutex::new(stdin)),
        pending,
    })
}

async fn request_ai_host(
    manager: Arc<AIHostManager>,
    app: AppHandle,
    command: &'static str,
    payload: Value,
) -> HostResult {
    tauri::async_runtime::spawn_blocking(move || manager.request(app, command, payload))
        .await
        .map_err(|error| format!("AI Runtime host task failed: {error}"))?
}

#[tauri::command]
async fn ai_discover(app: AppHandle, state: State<'_, Arc<AIHostManager>>) -> HostResult {
    request_ai_host(state.inner().clone(), app, "ai_discover", json!({})).await
}

#[tauri::command]
async fn ai_infer(
    app: AppHandle,
    state: State<'_, Arc<AIHostManager>>,
    request: Value,
) -> HostResult {
    request_ai_host(
        state.inner().clone(),
        app,
        "ai_infer",
        json!({"request": request}),
    )
    .await
}

#[tauri::command(rename_all = "camelCase")]
async fn ai_cancel(
    app: AppHandle,
    state: State<'_, Arc<AIHostManager>>,
    request_id: String,
) -> Result<bool, String> {
    let value = request_ai_host(
        state.inner().clone(),
        app,
        "ai_cancel",
        json!({"requestId": request_id}),
    )
    .await?;
    Ok(value.as_bool().unwrap_or(false))
}

#[tauri::command(rename_all = "camelCase")]
async fn ai_provider_action(
    app: AppHandle,
    state: State<'_, Arc<AIHostManager>>,
    provider_id: String,
    action: String,
) -> Result<bool, String> {
    let value = request_ai_host(
        state.inner().clone(),
        app,
        "ai_provider_action",
        json!({"providerId": provider_id, "action": action}),
    )
    .await?;
    Ok(value.as_bool().unwrap_or(false))
}

#[tauri::command(rename_all = "camelCase")]
fn ai_credential_status(provider_id: String) -> Result<bool, String> {
    Ok(load_provider_credential(&provider_id)?.is_some())
}

#[cfg(windows)]
#[tauri::command(rename_all = "camelCase")]
fn ai_credential_set(
    state: State<'_, Arc<AIHostManager>>,
    provider_id: String,
    credential: String,
) -> Result<(), String> {
    if credential.trim().is_empty() {
        return Err("Credential cannot be empty.".to_owned());
    }
    credential_entry(&provider_id)?
        .set_password(&credential)
        .map_err(|error| format!("Unable to write the system credential vault: {error}"))?;
    state.restart()
}

#[cfg(not(windows))]
#[tauri::command(rename_all = "camelCase")]
fn ai_credential_set(
    _state: State<'_, Arc<AIHostManager>>,
    provider_id: String,
    _credential: String,
) -> Result<(), String> {
    validate_provider_id(&provider_id)?;
    Err("The secure credential vault is not implemented for this platform.".to_owned())
}

#[cfg(windows)]
#[tauri::command(rename_all = "camelCase")]
fn ai_credential_delete(
    state: State<'_, Arc<AIHostManager>>,
    provider_id: String,
) -> Result<(), String> {
    match credential_entry(&provider_id)?.delete_credential() {
        Ok(()) | Err(keyring::Error::NoEntry) => state.restart(),
        Err(error) => Err(format!("Unable to delete the system credential: {error}")),
    }
}

#[cfg(not(windows))]
#[tauri::command(rename_all = "camelCase")]
fn ai_credential_delete(
    _state: State<'_, Arc<AIHostManager>>,
    provider_id: String,
) -> Result<(), String> {
    validate_provider_id(&provider_id)?;
    Err("The secure credential vault is not implemented for this platform.".to_owned())
}

struct WorkflowHostProcess {
    child: Child,
    stdin: Arc<Mutex<ChildStdin>>,
    pending: PendingRequests,
}

impl Drop for WorkflowHostProcess {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

#[derive(Default)]
struct WorkflowHostManager {
    process: Mutex<Option<WorkflowHostProcess>>,
    next_id: AtomicU64,
}

impl WorkflowHostManager {
    fn request(&self, app: AppHandle, command: &str, payload: Value) -> HostResult {
        let request_id = format!(
            "workflow-desktop-{}-{}",
            std::process::id(),
            self.next_id.fetch_add(1, Ordering::Relaxed)
        );
        let (sender, receiver) = mpsc::sync_channel(1);
        {
            let mut guard = self
                .process
                .lock()
                .map_err(|_| "Workflow Runtime host lock is poisoned.".to_owned())?;
            if guard.is_none() {
                *guard = Some(start_workflow_host(app)?);
            }
            let process = guard
                .as_mut()
                .ok_or_else(|| "Workflow Runtime host failed to start.".to_owned())?;
            process
                .pending
                .lock()
                .map_err(|_| "Workflow Runtime pending-request lock is poisoned.".to_owned())?
                .insert(request_id.clone(), sender);
            let message = json!({"id": request_id, "command": command, "payload": payload});
            if let Err(error) = write_host_message(&process.stdin, &message, "Workflow Runtime") {
                process
                    .pending
                    .lock()
                    .ok()
                    .map(|mut values| values.remove(&request_id));
                *guard = None;
                return Err(error);
            }
        }
        match receiver.recv_timeout(Duration::from_secs(180)) {
            Ok(result) => result,
            Err(_) => {
                if let Ok(mut guard) = self.process.lock() {
                    if let Some(process) = guard.as_mut() {
                        if let Ok(mut pending) = process.pending.lock() {
                            pending.remove(&request_id);
                        }
                    }
                }
                Err(format!("Workflow Runtime command {command} timed out."))
            }
        }
    }
}

fn write_host_message(
    stdin: &Arc<Mutex<ChildStdin>>,
    message: &Value,
    runtime_name: &str,
) -> Result<(), String> {
    let mut writer = stdin
        .lock()
        .map_err(|_| format!("{runtime_name} stdin lock is poisoned."))?;
    serde_json::to_writer(&mut *writer, message)
        .map_err(|error| format!("Unable to encode {runtime_name} command: {error}"))?;
    writer
        .write_all(b"\n")
        .and_then(|_| writer.flush())
        .map_err(|error| format!("Unable to send {runtime_name} command: {error}"))
}

fn start_workflow_host(app: AppHandle) -> Result<WorkflowHostProcess, String> {
    let root = find_repo_root()?;
    if !root.join("src/atlas_workflow/host.py").is_file() {
        return Err("Unable to locate src/atlas_workflow/host.py.".to_owned());
    }
    let python = env::var_os("ATLAS_WORKFLOW_PYTHON")
        .or_else(|| env::var_os("ATLAS_AI_PYTHON"))
        .unwrap_or_else(|| "python".into());
    let mut command = Command::new(python);
    command
        .arg("-u")
        .arg("-m")
        .arg("atlas_workflow.host")
        .current_dir(&root)
        .env("PYTHONPATH", workflow_python_path(&root)?)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        command.creation_flags(0x08000000);
    }
    let mut child = command
        .spawn()
        .map_err(|error| format!("Unable to start Python Workflow Runtime host: {error}"))?;
    let stdin = Arc::new(Mutex::new(child.stdin.take().ok_or_else(|| {
        "Python Workflow Runtime host has no stdin pipe.".to_owned()
    })?));
    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "Python Workflow Runtime host has no stdout pipe.".to_owned())?;
    let stderr = child
        .stderr
        .take()
        .ok_or_else(|| "Python Workflow Runtime host has no stderr pipe.".to_owned())?;
    let pending: PendingRequests = Arc::new(Mutex::new(HashMap::new()));
    let stdout_pending = Arc::clone(&pending);
    let bridge_stdin = Arc::clone(&stdin);
    let bridge_app = app.clone();

    std::thread::spawn(move || {
        for line in BufReader::new(stdout).lines() {
            let Ok(line) = line else { break };
            let Ok(message) = serde_json::from_str::<Value>(&line) else {
                continue;
            };
            match message.get("kind").and_then(Value::as_str) {
                Some("response") => {
                    let id = message
                        .get("id")
                        .and_then(Value::as_str)
                        .unwrap_or_default();
                    let sender = stdout_pending
                        .lock()
                        .ok()
                        .and_then(|mut values| values.remove(id));
                    if let Some(sender) = sender {
                        let result = if message.get("ok").and_then(Value::as_bool).unwrap_or(false)
                        {
                            Ok(message.get("result").cloned().unwrap_or(Value::Null))
                        } else {
                            Err(message
                                .get("error")
                                .and_then(Value::as_str)
                                .unwrap_or("Workflow Runtime host command failed.")
                                .to_owned())
                        };
                        let _ = sender.send(result);
                    }
                }
                Some("event") => {
                    let event_name = message
                        .get("event")
                        .and_then(Value::as_str)
                        .unwrap_or("workflow://runtime-event");
                    let payload = message.get("payload").cloned().unwrap_or(Value::Null);
                    let _ = app.emit(event_name, payload);
                }
                Some("bridge_request") => {
                    let request = message.clone();
                    let worker_stdin = Arc::clone(&bridge_stdin);
                    let worker_app = bridge_app.clone();
                    std::thread::spawn(move || {
                        let id = request
                            .get("id")
                            .and_then(Value::as_str)
                            .unwrap_or_default();
                        let bridge = request
                            .get("bridge")
                            .and_then(Value::as_str)
                            .unwrap_or_default();
                        let command = request
                            .get("command")
                            .and_then(Value::as_str)
                            .unwrap_or_default();
                        let payload = request.get("payload").cloned().unwrap_or_else(|| json!({}));
                        let result: HostResult = match (bridge, command) {
                            ("ai", _) => {
                                let manager =
                                    worker_app.state::<Arc<AIHostManager>>().inner().clone();
                                manager.request(worker_app.clone(), command, payload)
                            }
                            ("vision", "vision_capture_frame") => {
                                vision_capture_frame().and_then(|frame| {
                                    serde_json::to_value(frame).map_err(|error| error.to_string())
                                })
                            }
                            ("vision", "vision_resolve_target") => vision_resolve_target(&payload),
                            _ => Err(format!(
                                "Unsupported Workflow runtime bridge: {bridge}/{command}"
                            )),
                        };
                        let response = match result {
                            Ok(value) => {
                                json!({"kind":"bridge_response","id":id,"ok":true,"result":value})
                            }
                            Err(error) => {
                                json!({"kind":"bridge_response","id":id,"ok":false,"error":error})
                            }
                        };
                        let _ = write_host_message(&worker_stdin, &response, "Workflow Runtime");
                    });
                }
                _ => {}
            }
        }
        if let Ok(mut values) = stdout_pending.lock() {
            for (_, sender) in values.drain() {
                let _ = sender.send(Err(
                    "Python Workflow Runtime host stopped unexpectedly.".to_owned()
                ));
            }
        }
    });
    std::thread::spawn(move || {
        for line in BufReader::new(stderr).lines().map_while(Result::ok) {
            eprintln!("[Workflow Runtime Host] {line}");
        }
    });
    Ok(WorkflowHostProcess {
        child,
        stdin,
        pending,
    })
}

async fn request_workflow_host(
    manager: Arc<WorkflowHostManager>,
    app: AppHandle,
    command: &'static str,
    payload: Value,
) -> HostResult {
    tauri::async_runtime::spawn_blocking(move || manager.request(app, command, payload))
        .await
        .map_err(|error| format!("Workflow Runtime host task failed: {error}"))?
}

#[tauri::command(rename_all = "camelCase")]
async fn workflow_validate(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
    definition: Value,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_validate",
        json!({"definition": definition}),
    )
    .await
}

#[tauri::command(rename_all = "camelCase")]
async fn workflow_start(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
    definition: Value,
    inputs: Option<Value>,
    project_context: Option<Value>,
    breakpoints: Option<Vec<String>>,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_start",
        json!({
            "definition": definition, "inputs": inputs.unwrap_or_else(|| json!({})),
            "projectContext": project_context.unwrap_or_else(|| json!({})),
            "breakpoints": breakpoints.unwrap_or_default(),
        }),
    )
    .await
}

macro_rules! workflow_control_command {
    ($name:ident, $command:literal) => {
        #[tauri::command(rename_all = "camelCase")]
        async fn $name(app: AppHandle, state: State<'_, Arc<WorkflowHostManager>>, execution_id: String) -> HostResult {
            request_workflow_host(state.inner().clone(), app, $command, json!({"executionId": execution_id})).await
        }
    };
}

workflow_control_command!(workflow_pause, "workflow_pause");
workflow_control_command!(workflow_resume, "workflow_resume");
workflow_control_command!(workflow_stop, "workflow_stop");
workflow_control_command!(workflow_step, "workflow_step");
workflow_control_command!(workflow_restart, "workflow_restart");
workflow_control_command!(workflow_get_state, "workflow_get_state");
workflow_control_command!(workflow_get_result, "workflow_get_result");

#[tauri::command(rename_all = "camelCase")]
async fn workflow_input_arm(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
    policy: Value,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_input_arm",
        json!({"policy": policy}),
    )
    .await
}

#[tauri::command]
async fn workflow_input_status(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_input_status",
        json!({}),
    )
    .await
}

#[tauri::command]
async fn workflow_emergency_stop(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_emergency_stop",
        json!({}),
    )
    .await
}

#[tauri::command(rename_all = "camelCase")]
async fn workflow_plugin_register(
    app: AppHandle,
    state: State<'_, Arc<WorkflowHostManager>>,
    plugin: Value,
) -> HostResult {
    request_workflow_host(
        state.inner().clone(),
        app,
        "workflow_plugin_register",
        json!({"plugin": plugin}),
    )
    .await
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(Arc::new(AIHostManager::default()))
        .manage(Arc::new(WorkflowHostManager::default()))
        .invoke_handler(tauri::generate_handler![
            vision_capture_frame,
            ai_discover,
            ai_infer,
            ai_cancel,
            ai_provider_action,
            ai_credential_status,
            ai_credential_set,
            ai_credential_delete,
            workflow_validate,
            workflow_start,
            workflow_pause,
            workflow_resume,
            workflow_stop,
            workflow_step,
            workflow_restart,
            workflow_get_state,
            workflow_get_result,
            workflow_input_arm,
            workflow_input_status,
            workflow_emergency_stop,
            workflow_plugin_register,
            project_select_directory,
            project_session_remember,
            project_session_restore,
            project_session_clear,
            project_assets_load,
            project_assets_save
        ])
        .run(tauri::generate_context!())
        .expect("failed to run Atlas desktop application");
}

#[cfg(test)]
mod hardening_tests {
    use super::*;

    #[test]
    fn project_assets_reject_credentials_without_masking_usage_metrics() {
        assert!(reject_credentials(&json!({"provider":{"apiKey":"secret"}}), "assets").is_err());
        assert!(reject_credentials(
            &json!({"metrics":{"inputTokens":12,"totalTokens":20}}),
            "assets"
        )
        .is_ok());
    }

    #[test]
    fn provider_ids_are_bounded_before_keyring_access() {
        assert!(validate_provider_id("openai-compatible_1").is_ok());
        assert!(validate_provider_id("../openai").is_err());
    }

    #[cfg(windows)]
    #[test]
    fn windows_credential_vault_round_trip_is_real_and_disposable() {
        let provider_id = format!("atlas-acceptance-{}", std::process::id());
        let credential = "atlas-disposable-credential";
        let entry = credential_entry(&provider_id).unwrap();
        let _ = entry.delete_credential();

        entry.set_password(credential).unwrap();
        assert_eq!(
            load_provider_credential(&provider_id).unwrap().as_deref(),
            Some(credential)
        );

        credential_entry(&provider_id)
            .unwrap()
            .delete_credential()
            .unwrap();
        assert_eq!(load_provider_credential(&provider_id).unwrap(), None);
    }

    #[test]
    fn project_assets_round_trip_and_recover_from_backup() {
        let unique = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let root = env::temp_dir().join(format!(
            "atlas-project-assets-{}-{unique}",
            std::process::id()
        ));
        fs::create_dir_all(&root).unwrap();
        let path = root.to_string_lossy().into_owned();
        project_assets_save(path.clone(), json!({"prompt":"first"})).unwrap();
        assert_eq!(
            project_assets_load(path.clone()).unwrap()["prompt"],
            "first"
        );
        project_assets_save(path.clone(), json!({"prompt":"second"})).unwrap();
        fs::write(root.join(".atlas/project-assets.v1.json"), b"corrupt").unwrap();
        assert_eq!(project_assets_load(path).unwrap()["prompt"], "first");
        fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn project_session_round_trip_requires_manual_reopen_pointer() {
        let unique = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let root = env::temp_dir().join(format!(
            "atlas-project-session-{}-{unique}",
            std::process::id()
        ));
        let project = root.join("project");
        let pointer = root.join("state/project-session.v1.json");
        fs::create_dir_all(&project).unwrap();
        write_project_session(&pointer, &project.to_string_lossy()).unwrap();
        assert_eq!(
            read_project_session(&pointer).unwrap(),
            Some(project.to_string_lossy().into_owned())
        );
        fs::remove_dir_all(root).unwrap();
    }
}
