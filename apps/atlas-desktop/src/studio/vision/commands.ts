import { commandPaletteService } from "../../services";
import { workspaceService } from "../../workspace";
import { useLogStore, useRuntimeStore } from "../../stores";
import { projectService } from "../../services";
import { useVisionDocumentStore, useVisionTimelineStore } from "./stores";
import { visionCaptureService, visionExportService, visionImportService } from "./services/vision-service";
import type { CommandPaletteItem } from "../../types";
import type { VisionTool } from "./types";
import { selectProjectDirectory } from "../../ipc/bridge";

const log = (message: string) => useLogStore.getState().addEntry({ timestamp: Date.now(), level: "info", source: "VisionStudio", message });
const openProjectPicker = (): void => {
  void selectProjectDirectory().then((path) => {
    if (!path) return;
    const name = path.split(/[\\\\/]/).filter(Boolean).at(-1) ?? "Atlas Project";
    projectService.openProject({id:"project-"+Date.now(),name,path,createdAt:Date.now(),updatedAt:Date.now(),settings:{theme:"system",language:"en",autoSave:true,tabSize:2}});
  }).catch((error) => {
    log(error instanceof Error ? error.message : "Native project picker is unavailable.");
  });
};
const openProjectPathPrompt = (): void => {
  const path = window.prompt("Atlas project directory path:", "");
  if (!path?.trim()) return;
  const normalized = path.trim();
  const name = normalized.split(/[\\/]/).filter(Boolean).at(-1) ?? "Atlas Project";
  projectService.openProject({id:"project-"+Date.now(),name,path:normalized,createdAt:Date.now(),updatedAt:Date.now(),settings:{theme:"system",language:"en",autoSave:true,tabSize:2}});
};
const setRuntimeStatus = (status: "running"|"terminated"): void => { const state=useRuntimeStore.getState(); state.runtimes.forEach((runtime)=>state.setStatus(runtime.name,status)); log(`All runtimes ${status}`); };
export function registerVisionCommands(): void {
  const command = (id: string, label: string, category: string, handler: () => void, shortcut?: string): CommandPaletteItem => ({ id, label, category, description: `${label} in Vision Studio`, handler, shortcut });
  const commands = [
    command("desktop.open-project", "Open Project", "File", openProjectPicker), command("desktop.open-project-path", "Open Project by Path", "File", openProjectPathPrompt), command("desktop.close-project", "Close Project", "File", () => projectService.closeProject()), command("desktop.exit", "Exit", "File", () => log("Exit requested by user")),
    command("desktop.cut", "Cut", "Edit", () => { useVisionDocumentStore.getState().copySelected(); useVisionDocumentStore.getState().deleteSelected(); }), command("desktop.start-runtimes", "Start All Runtimes", "Run", () => setRuntimeStatus("running")), command("desktop.stop-runtimes", "Stop All Runtimes", "Run", () => setRuntimeStatus("terminated")), command("desktop.restart-runtime", "Restart Selected", "Run", () => { setRuntimeStatus("terminated"); setRuntimeStatus("running"); }), command("desktop.export-logs", "Export Logs", "Tools", () => log("Log export requested")), command("desktop.clear-logs", "Clear Logs", "Tools", () => useLogStore.getState().clearEntries()), command("desktop.settings", "Open Settings", "Tools", () => log("Settings requested")), command("desktop.about", "About Atlas", "Help", () => log("Atlas Desktop 0.15.0-alpha")),
    command("vision.capture", "Capture Screen", "Vision / Capture", () => void visionCaptureService.captureScreen()), command("vision.freeze", "Freeze Frame", "Vision / Capture", () => log("Freeze requested through capture service")),
    command("vision.record", "Start Recording", "Vision / Capture", () => log("Recording requested through runtime boundary")), command("vision.stop", "Stop Capture or Playback", "Vision / Capture", () => { useVisionTimelineStore.getState().pause(); log("Stop requested"); }),
    command("vision.play", "Play Timeline", "Vision / Playback", () => useVisionTimelineStore.getState().play()), command("vision.pause", "Pause Timeline", "Vision / Playback", () => useVisionTimelineStore.getState().pause()),
    command("vision.previous-frame", "Previous Frame", "Vision / Playback", () => useVisionTimelineStore.getState().previous()), command("vision.next-frame", "Next Frame", "Vision / Playback", () => useVisionTimelineStore.getState().next()),
    command("vision.open-image", "Open Image", "Vision / File", () => void visionImportService.openImagePicker()), command("vision.save", "Save Vision Session", "Vision / File", () => visionExportService.exportSession()), command("vision.export", "Export Vision Session", "Vision / File", () => visionExportService.exportSession()),
    command("vision.undo", "Undo Vision Edit", "Vision / Edit", () => useVisionDocumentStore.getState().undo(), "Ctrl+Z"), command("vision.redo", "Redo Vision Edit", "Vision / Edit", () => useVisionDocumentStore.getState().redo(), "Ctrl+Y"),
    command("vision.copy", "Copy Overlay", "Vision / Edit", () => useVisionDocumentStore.getState().copySelected(), "Ctrl+C"), command("vision.paste", "Paste Overlay", "Vision / Edit", () => useVisionDocumentStore.getState().paste(), "Ctrl+V"), command("vision.duplicate", "Duplicate Overlay", "Vision / Edit", () => useVisionDocumentStore.getState().duplicateSelected(), "Ctrl+D"), command("vision.delete", "Delete Overlay", "Vision / Edit", () => useVisionDocumentStore.getState().deleteSelected(), "Delete"),
    command("vision.rename", "Rename Overlay", "Vision / Edit", () => { const s=useVisionDocumentStore.getState(); const selected=s.overlays.find((item)=>item.id===s.selectedId); if(selected){const name=prompt("Overlay name",selected.name);if(name)s.updateOverlay(selected.id,{name});} }, "F2"),
    command("vision.zoom-in", "Zoom In", "Vision / View", () => { const s=useVisionDocumentStore.getState(); s.setZoom(s.zoom*1.1); }), command("vision.zoom-out", "Zoom Out", "Vision / View", () => { const s=useVisionDocumentStore.getState(); s.setZoom(s.zoom*.9); }),
    command("vision.fit", "Fit to Screen", "Vision / View", () => useVisionDocumentStore.getState().fit(), "F"), command("vision.actual-size", "Actual Size", "Vision / View", () => useVisionDocumentStore.getState().actualSize()), command("vision.grid", "Toggle Grid", "Vision / View", () => useVisionDocumentStore.getState().toggleGrid()), command("vision.rulers", "Toggle Rulers", "Vision / View", () => useVisionDocumentStore.getState().toggleRulers()),
    command("vision.ocr", "Run OCR", "Vision / Analysis", () => workspaceService.openPanel("vision.ocr")), command("vision.detect", "Detect Objects", "Vision / Analysis", () => workspaceService.openPanel("vision.detection")), command("vision.template-match", "Template Match", "Vision / Analysis", () => workspaceService.openPanel("vision.template")), command("vision.color-inspector", "Color Inspector", "Vision / Analysis", () => workspaceService.openPanel("vision.color")),
  ];
  commands.forEach((item) => commandPaletteService.register(item));
}

export function isTextInput(target: EventTarget | null): boolean { return target instanceof HTMLElement && (target.isContentEditable || ["INPUT","TEXTAREA","SELECT"].includes(target.tagName)); }
export function installVisionShortcuts(): () => void {
  const handler = (event: KeyboardEvent) => { if (isTextInput(event.target)) return; const key=event.key.toLowerCase(); const id = event.ctrlKey ? ({ z:"vision.undo", y:"vision.redo", c:"vision.copy", v:"vision.paste", d:"vision.duplicate" } as Record<string,string>)[key] : ({ f:"vision.fit", delete:"vision.delete", f2:"vision.rename" } as Record<string,string>)[key]; const tool = !event.ctrlKey ? ({v:"pointer",h:"pan",z:"zoom",m:event.shiftKey?"ellipse-selection":"rectangle-selection",p:"polygon-selection",l:"lasso",r:"rectangle",e:"ellipse",i:"line",a:"arrow",t:event.shiftKey?"template-region":"text",o:"ocr-region",d:"object-region",c:"color-sampler",x:"pixel-probe",u:"measure"} as Record<string, VisionTool>)[key] : undefined; if(id) commandPaletteService.execute(id); else if(tool) useVisionDocumentStore.getState().setTool(tool); if(id||tool) event.preventDefault(); };
  window.addEventListener("keydown",handler); return()=>window.removeEventListener("keydown",handler);
}
