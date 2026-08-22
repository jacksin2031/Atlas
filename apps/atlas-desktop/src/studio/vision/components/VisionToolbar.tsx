import React from "react";
import { IconButton, ToolbarGroup } from "../../../design-system";
import { commandPaletteService } from "../../../services";
import { useVisionDocumentStore, useVisionTimelineStore } from "../stores";
import type { IconName } from "../../../design-system";

const button = (id: string, label: string, icon: IconName, shortcut?: string) => ({ id, label, icon, shortcut });
const groups = [
  ["Capture", [button("vision.capture", "Capture", "capture"), button("vision.freeze", "Freeze", "freeze"), button("vision.record", "Record", "record"), button("vision.stop", "Stop", "stop")]],
  ["Playback", [button("vision.play", "Play", "play"), button("vision.pause", "Pause", "pause"), button("vision.previous-frame", "Previous Frame", "previous"), button("vision.next-frame", "Next Frame", "next")]],
  ["File", [button("vision.open-image", "Open Image", "open"), button("vision.save", "Save", "save"), button("vision.export", "Export", "export")]],
  ["Edit", [button("vision.undo", "Undo", "undo", "Ctrl+Z"), button("vision.redo", "Redo", "redo", "Ctrl+Y")]],
  ["View", [button("vision.zoom-in", "Zoom In", "zoom-in"), button("vision.zoom-out", "Zoom Out", "zoom-out"), button("vision.fit", "Fit", "fit", "F"), button("vision.actual-size", "Actual Size", "actual"), button("vision.grid", "Grid", "grid"), button("vision.rulers", "Rulers", "rulers")]],
  ["Analysis", [button("vision.ocr", "OCR", "ocr"), button("vision.detect", "Detect Objects", "detect"), button("vision.template-match", "Template Match", "template"), button("vision.color-inspector", "Color Inspector", "eyedropper")]],
] as const;

export const VisionToolbar: React.FC<{ onCommandPalette: () => void }> = ({ onCommandPalette }) => {
  const grid = useVisionDocumentStore((s) => s.grid); const rulers = useVisionDocumentStore((s) => s.rulers); const playing = useVisionTimelineStore((s) => s.playing);
  return <div className="vision-toolbar" aria-label="Vision toolbar">{groups.map(([name, items]) => <ToolbarGroup key={name} label={name}>{items.map((item) => <IconButton key={item.id} icon={item.icon} label={`${item.label}${item.shortcut ? ` (${item.shortcut})` : ""}`} active={(item.id === "vision.grid" && grid) || (item.id === "vision.rulers" && rulers) || (item.id === "vision.play" && playing)} onClick={() => commandPaletteService.execute(item.id)} />)}</ToolbarGroup>)}<div className="toolbar-spacer"/><IconButton icon="command" label="Command Palette (Ctrl+Shift+P)" onClick={onCommandPalette}/></div>;
};
