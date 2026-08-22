import { create } from "zustand";
import type { ColorSample, DetectionResult, OcrResult, TemplateResult } from "../types";

interface VisionResultsState {
  ocr: OcrResult[]; detections: DetectionResult[]; colors: ColorSample[]; templates: TemplateResult[];
  setOcr: (items: OcrResult[]) => void; setDetections: (items: DetectionResult[]) => void; addColor: (item: ColorSample) => void; setTemplates: (items: TemplateResult[]) => void; clear: () => void;
}
export const useVisionResultsStore = create<VisionResultsState>((set) => ({
  ocr: [], detections: [], colors: [], templates: [], setOcr: (ocr) => set({ ocr }), setDetections: (detections) => set({ detections }),
  addColor: (item) => set((s) => ({ colors: [item, ...s.colors].slice(0, 50) })), setTemplates: (templates) => set({ templates }),
  clear: () => set({ ocr: [], detections: [], colors: [], templates: [] }),
}));
