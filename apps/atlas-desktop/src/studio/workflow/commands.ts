import { commandPaletteService } from "../../services";
import type { CommandPaletteItem } from "../../types";
import { executorService } from "./services/executor-service";
import { useExecutionStore } from "./stores";

const item = (id: string, label: string, handler: () => void, shortcut?: string): CommandPaletteItem => ({
  id, label, handler, shortcut, category: "Workflow / Execution", description: `${label} using Workflow Runtime`,
});
const report = (error: unknown): void => useExecutionStore.getState().setRuntimeError(error instanceof Error ? error.message : String(error));
const active = (): string | null => useExecutionStore.getState().activeRunId;

const run = (): void => { void executorService.run().catch(report); };
const pauseResume = (): void => {
  const state = useExecutionStore.getState();
  if (!state.activeRunId) return;
  void (state.isPaused ? executorService.resume(state.activeRunId) : executorService.pause(state.activeRunId)).catch(report);
};
const stop = (): void => { const id = active(); if (id) void executorService.stop(id).catch(report); };
const step = (): void => { const id = active(); if (id) void executorService.step(id).catch(report); };
const restart = (): void => { const id = active(); if (id) void executorService.restart(id).catch(report); };
const emergencyStop = (): void => { void executorService.emergencyStop().catch(report); };

export function registerWorkflowCommands(): void {
  [
    item("workflow.run", "Run Workflow", run, "F5"),
    item("workflow.pause-resume", "Pause / Resume Workflow", pauseResume, "F8"),
    item("workflow.stop", "Stop Workflow", stop, "Shift+F5"),
    item("workflow.step", "Step Workflow", step, "F7"),
    item("workflow.restart", "Restart Workflow", restart, "Ctrl+Shift+F5"),
    item("workflow.emergency-stop", "Emergency Stop Input", emergencyStop, "Escape"),
  ].forEach((command) => commandPaletteService.register(command));
}

const isTextInput = (target: EventTarget | null): boolean => target instanceof HTMLElement && (target.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));
export function installWorkflowShortcuts(): () => void {
  const handler = (event: KeyboardEvent): void => {
    if (event.key === "Escape") { emergencyStop(); event.preventDefault(); return; }
    if (isTextInput(event.target)) return;
    const id = event.key === "F7" ? "workflow.step"
      : event.key === "F8" ? "workflow.pause-resume"
      : event.key === "F5" && event.shiftKey && event.ctrlKey ? "workflow.restart"
      : event.key === "F5" && event.shiftKey ? "workflow.stop"
      : event.key === "F5" ? "workflow.run" : undefined;
    if (id) { commandPaletteService.execute(id); event.preventDefault(); }
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}
