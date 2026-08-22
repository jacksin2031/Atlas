import { captureVisionFrame } from "../../../ipc/bridge";
import { useVisionDocumentStore, useVisionResultsStore } from "../stores";

export class VisionImportService {
  async openImagePicker(): Promise<void> {
    const input = document.createElement("input"); input.type = "file"; input.accept = "image/*";
    input.addEventListener("change", () => { const file = input.files?.[0]; if (file) void this.openFile(file); }, { once: true });
    input.click();
  }
  async openFile(file: File): Promise<void> {
    if (!file.type.startsWith("image/")) throw new Error("Only image files are supported");
    const url = URL.createObjectURL(file);
    const dimensions = await new Promise<{ width: number; height: number }>((resolve, reject) => { const image = new Image(); image.onload = () => resolve({ width: image.naturalWidth, height: image.naturalHeight }); image.onerror = () => reject(new Error("Unable to decode image")); image.src = url; });
    const previous = useVisionDocumentStore.getState().source; if (previous?.url.startsWith("blob:")) URL.revokeObjectURL(previous.url);
    useVisionDocumentStore.getState().setSource({ name: file.name, url, ...dimensions, kind: "image" });
  }
}

export class VisionCaptureService {
  async captureScreen(): Promise<void> {
    const result = await captureVisionFrame();
    if (result) useVisionDocumentStore.getState().setSource(result);
  }
}

export class VisionExportService {
  exportSession(): void {
    const state = useVisionDocumentStore.getState(); const results = useVisionResultsStore.getState();
    const blob = new Blob([JSON.stringify({ source: state.source?.name ?? null, overlays: state.overlays, results: { ocr: results.ocr, detections: results.detections, colors: results.colors, templates: results.templates } }, null, 2)], { type: "application/json" });
    const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = "atlas-vision-session.json"; link.click(); setTimeout(() => URL.revokeObjectURL(link.href), 0);
  }
}

export const visionImportService = new VisionImportService();
export const visionCaptureService = new VisionCaptureService();
export const visionExportService = new VisionExportService();
