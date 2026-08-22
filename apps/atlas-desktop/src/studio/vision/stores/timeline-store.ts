import { create } from "zustand";
import type { VisionFrame } from "../types";

interface TimelineState { frames: VisionFrame[]; current: number; playing: boolean; loop: boolean; speed: number; setFrames: (frames: VisionFrame[]) => void; seek: (index: number) => void; play: () => void; pause: () => void; previous: () => void; next: () => void; setLoop: (loop: boolean) => void; setSpeed: (speed: number) => void; addMarker: (label?: string) => void; removeCurrent: () => void; duplicateCurrent: () => void }
export const useVisionTimelineStore = create<TimelineState>((set, get) => ({
  frames: [], current: 0, playing: false, loop: false, speed: 1,
  setFrames: (frames) => set({ frames, current: 0 }), seek: (current) => set((s) => ({ current: Math.max(0, Math.min(s.frames.length - 1, current)) })),
  play: () => set({ playing: true }), pause: () => set({ playing: false }), previous: () => get().seek(get().current - 1), next: () => { const s = get(); get().seek(s.current + 1 >= s.frames.length && s.loop ? 0 : s.current + 1); },
  setLoop: (loop) => set({ loop }), setSpeed: (speed) => set({ speed }),
  addMarker: (label = "Marker") => set((s) => ({ frames: s.frames.map((f, i) => i === s.current ? { ...f, markers: [...f.markers, label] } : f) })),
  removeCurrent: () => set((s) => ({ frames: s.frames.filter((_, i) => i !== s.current), current: Math.max(0, s.current - 1) })),
  duplicateCurrent: () => set((s) => { const frame = s.frames[s.current]; if (!frame) return s; const frames = [...s.frames]; frames.splice(s.current + 1, 0, { ...frame, id: `frame-${Date.now()}`, number: frame.number + 1 }); return { frames, current: s.current + 1 }; }),
}));
