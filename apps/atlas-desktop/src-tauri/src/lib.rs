use base64::{engine::general_purpose::STANDARD, Engine as _};
use image::{codecs::png::PngEncoder, ColorType, ImageEncoder};
use screenshots::Screen;
use serde::Serialize;

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
struct VisionFrameSource {
    name: String,
    url: String,
    width: u32,
    height: u32,
    kind: &'static str,
}

#[tauri::command]
fn vision_capture_frame() -> Result<VisionFrameSource, String> {
    let screen = Screen::all()
        .map_err(|error| format!("Unable to enumerate displays: {error}"))?
        .into_iter()
        .next()
        .ok_or_else(|| "No display is available for capture".to_owned())?;
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

    Ok(VisionFrameSource {
        name: format!("{} capture", screen.display_info.id),
        url: format!("data:image/png;base64,{}", STANDARD.encode(png)),
        width: image.width(),
        height: image.height(),
        kind: "screenshot",
    })
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![vision_capture_frame])
        .run(tauri::generate_context!())
        .expect("failed to run Atlas desktop application");
}
