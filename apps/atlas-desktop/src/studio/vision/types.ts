export type VisionTool = "pointer" | "pan" | "zoom" | "rectangle-selection" | "ellipse-selection" | "polygon-selection" | "lasso" | "rectangle" | "ellipse" | "line" | "arrow" | "text" | "ocr-region" | "object-region" | "template-region" | "color-sampler" | "pixel-probe" | "measure";
export type OverlayType = "rectangle" | "ellipse" | "polygon" | "line" | "arrow" | "ocr-region" | "object-detection" | "template-region" | "color-sample" | "measurement" | "anchor-point" | "mask" | "label";

export interface VisionSource { name: string; url: string; width: number; height: number; kind: "image" | "screenshot" | "frame" }
export interface VisionOverlay {
  id: string; name: string; type: OverlayType; x: number; y: number; width: number; height: number;
  rotation: number; opacity: number; visible: boolean; locked: boolean; disabled?: boolean; points?: { x: number; y: number }[];
  language?: string; engine?: string; confidenceThreshold?: number; model?: string; className?: string; threshold?: number;
  templateName?: string; scale?: number; rotationTolerance?: number; color?: string; tolerance?: number;
}
export interface OcrResult { id: string; overlayId: string; text: string; confidence: number; language: string; box: string; source: string; region: string }
export interface DetectionResult { id: string; overlayId: string; className: string; confidence: number; coordinates: string; visible: boolean; locked: boolean }
export interface ColorSample { id: string; overlayId?: string; coordinate: string; hex: string; rgb: string; hsv: string; lab: string; cmyk?: string; tolerance: number }
export interface TemplateResult { id: string; overlayId: string; name: string; similarity: number; threshold: number; coordinates: string; scale: number; visible: boolean; matchCount: number }
export interface VisionFrame { id: string; number: number; timestamp: number; thumbnail?: string; markers: string[]; annotations: string[] }
