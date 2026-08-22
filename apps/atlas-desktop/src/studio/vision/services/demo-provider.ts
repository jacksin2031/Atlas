import type { ColorSample, DetectionResult, OcrResult, TemplateResult, VisionFrame } from "../types";

export interface VisionDemoData { ocr: OcrResult[]; detections: DetectionResult[]; colors: ColorSample[]; templates: TemplateResult[]; frames: VisionFrame[] }

export function createVisionDemoData(): VisionDemoData {
  return {
    ocr: [{ id: "demo-ocr-1", overlayId: "demo-ocr-overlay", text: "Atlas demo result", confidence: .98, language: "English", box: "64, 42, 280, 44", source: "Demo frame", region: "Header" }],
    detections: [{ id: "demo-detection-1", overlayId: "demo-detection-overlay", className: "button", confidence: .94, coordinates: "420, 180, 120, 42", visible: true, locked: false }],
    colors: [{ id: "demo-color-1", coordinate: "120, 80", hex: "#007ACC", rgb: "0, 122, 204", hsv: "204°, 100%, 80%", lab: "49, 12, -51", cmyk: "100, 40, 0, 20", tolerance: 8 }],
    templates: [{ id: "demo-template-1", overlayId: "demo-template-overlay", name: "Primary action", similarity: .96, threshold: .8, coordinates: "420, 180", scale: 1, visible: true, matchCount: 1 }],
    frames: Array.from({ length: 12 }, (_, i) => ({ id: `demo-frame-${i}`, number: i + 1, timestamp: i * 100, markers: i === 4 ? ["Action"] : [], annotations: [] })),
  };
}

export const visionDemoModeEnabled = import.meta.env.DEV && import.meta.env.VITE_ATLAS_VISION_DEMO === "true";
