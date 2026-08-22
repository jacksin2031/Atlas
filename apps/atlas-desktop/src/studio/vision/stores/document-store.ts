import { create } from "zustand";
import type { OverlayType, VisionOverlay, VisionSource, VisionTool } from "../types";

interface VisionDocumentState {
  source: VisionSource | null; tool: VisionTool; overlays: VisionOverlay[]; selectedId: string | null;
  zoom: number; pan: { x: number; y: number }; grid: boolean; rulers: boolean; guides: boolean; crosshair: boolean;
  cursor: { x: number; y: number }; revision: number;
  past: VisionSnapshot[]; future: VisionSnapshot[]; copiedOverlay: VisionOverlay | null;
  setSource: (source: VisionSource | null) => void; setTool: (tool: VisionTool) => void; addOverlay: (overlay: VisionOverlay) => void;
  updateOverlay: (id: string, patch: Partial<VisionOverlay>) => void; selectOverlay: (id: string | null) => void;
  deleteSelected: () => void; duplicateSelected: () => void; moveSelected: (direction: "forward" | "backward") => void;
  copySelected: () => void; paste: () => void; undo: () => void; redo: () => void;
  setZoom: (zoom: number) => void; setPan: (pan: { x: number; y: number }) => void; setCursor: (cursor: { x: number; y: number }) => void;
  toggleGrid: () => void; toggleRulers: () => void; fit: () => void; actualSize: () => void; reset: () => void;
}

interface VisionSnapshot { overlays: VisionOverlay[]; selectedId: string | null }
const snapshot = (state: VisionDocumentState): VisionSnapshot => ({ overlays: structuredClone(state.overlays), selectedId: state.selectedId });
const history = (state: VisionDocumentState) => ({ past: [...state.past, snapshot(state)].slice(-100), future: [] as VisionSnapshot[] });

const initial = { source: null, tool: "pointer" as VisionTool, overlays: [] as VisionOverlay[], selectedId: null, zoom: 1, pan: { x: 0, y: 0 }, grid: false, rulers: false, guides: true, crosshair: true, cursor: { x: 0, y: 0 }, revision: 0, past: [] as VisionSnapshot[], future: [] as VisionSnapshot[], copiedOverlay: null as VisionOverlay | null };

export const createOverlay = (type: OverlayType, x: number, y: number, width = 120, height = 80): VisionOverlay => ({
  id: `overlay-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`, name: type.replaceAll("-", " "), type, x, y, width, height,
  rotation: 0, opacity: 1, visible: true, locked: false, confidenceThreshold: .7, threshold: .8, scale: 1, rotationTolerance: 0, tolerance: 8,
});

export const useVisionDocumentStore = create<VisionDocumentState>((set, get) => ({
  ...initial,
  setSource: (source) => set({ source, zoom: 1, pan: { x: 0, y: 0 } }),
  setTool: (tool) => set({ tool }),
  addOverlay: (overlay) => set((s) => ({ ...history(s), overlays: [...s.overlays, overlay], selectedId: overlay.id, revision: s.revision + 1 })),
  updateOverlay: (id, patch) => set((s) => ({ ...history(s), overlays: s.overlays.map((o) => o.id === id ? { ...o, ...patch } : o), revision: s.revision + 1 })),
  selectOverlay: (selectedId) => set({ selectedId }),
  deleteSelected: () => set((s) => ({ ...history(s), overlays: s.overlays.filter((o) => o.id !== s.selectedId || o.locked), selectedId: null, revision: s.revision + 1 })),
  duplicateSelected: () => { const selected = get().overlays.find((o) => o.id === get().selectedId); if (selected) get().addOverlay({ ...selected, id: `overlay-${Date.now()}`, name: `${selected.name} copy`, x: selected.x + 12, y: selected.y + 12 }); },
  moveSelected: (direction) => set((s) => { const i = s.overlays.findIndex((o) => o.id === s.selectedId); if (i < 0) return s; const target = Math.max(0, Math.min(s.overlays.length - 1, i + (direction === "forward" ? 1 : -1))); const overlays = [...s.overlays]; [overlays[i], overlays[target]] = [overlays[target]!, overlays[i]!]; return { ...history(s), overlays, revision: s.revision + 1 }; }),
  copySelected: () => set((s) => ({ copiedOverlay: structuredClone(s.overlays.find((o) => o.id === s.selectedId) ?? null) })),
  paste: () => { const copied=get().copiedOverlay; if(copied) get().addOverlay({ ...structuredClone(copied), id:`overlay-${Date.now()}`, name:`${copied.name} copy`, x:copied.x+12, y:copied.y+12 }); },
  undo: () => set((s) => { const previous=s.past.at(-1); if(!previous)return s; return { overlays:previous.overlays, selectedId:previous.selectedId, past:s.past.slice(0,-1), future:[snapshot(s),...s.future].slice(0,100), revision:s.revision+1 }; }),
  redo: () => set((s) => { const next=s.future[0]; if(!next)return s; return { overlays:next.overlays, selectedId:next.selectedId, past:[...s.past,snapshot(s)].slice(-100), future:s.future.slice(1), revision:s.revision+1 }; }),
  setZoom: (zoom) => set({ zoom: Math.max(.05, Math.min(32, zoom)) }), setPan: (pan) => set({ pan }), setCursor: (cursor) => set({ cursor }),
  toggleGrid: () => set((s) => ({ grid: !s.grid })), toggleRulers: () => set((s) => ({ rulers: !s.rulers })),
  fit: () => set({ zoom: .8, pan: { x: 0, y: 0 } }), actualSize: () => set({ zoom: 1, pan: { x: 0, y: 0 } }),
  reset: () => set({ ...initial }),
}));
