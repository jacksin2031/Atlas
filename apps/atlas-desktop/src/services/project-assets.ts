import { loadProjectAssets, saveProjectAssets } from "../ipc/bridge";
import { useAIStudioStore } from "../studio/ai/store";
import { useVisionDocumentStore, useVisionTimelineStore } from "../studio/vision/stores";
import { useExecutionStore, useWorkflowStore } from "../studio/workflow/stores";
import type { WorkflowDefinition, WorkflowRun, WorkflowRunStatus } from "../studio/workflow/types";
import { useProjectStore } from "../stores";
import { layoutStorageKey } from "../workspace/persistence";
import { useWorkspaceStore } from "../workspace/store";
import type { WorkspaceId } from "../workspace/types";

const RECOVERABLE: ReadonlySet<WorkflowRunStatus> = new Set(["created", "initializing", "validated", "scheduled", "running", "paused", "restarting"]);
const SENSITIVE_KEYS = new Set(["apikey", "authorization", "credential", "credentials", "secret", "password", "accesstoken", "refreshtoken", "bearertoken", "privatekey"]);
const normalizeKey = (key: string): string => key.replaceAll(/[^a-zA-Z0-9]/g, "").toLowerCase();

export function assertCredentialFree(value: unknown, path = "assets"): void {
  if (Array.isArray(value)) { value.forEach((item, index) => assertCredentialFree(item, `${path}[${index}]`)); return; }
  if (!value || typeof value !== "object") return;
  Object.entries(value as Record<string, unknown>).forEach(([key, item]) => {
    const next = `${path}.${key}`;
    if (SENSITIVE_KEYS.has(normalizeKey(key))) throw new Error(`Project assets cannot contain credential-shaped field: ${next}`);
    assertCredentialFree(item, next);
  });
}

export function interruptRecoverableRuns(runs: Record<string, WorkflowRun>): Record<string, WorkflowRun> {
  return Object.fromEntries(Object.entries(runs).map(([id, run]) => {
    if (!RECOVERABLE.has(run.status)) return [id, run];
    return [id, { ...run, status: "interrupted" as WorkflowRunStatus, completedAt: Date.now(), errors: [...run.errors, {
      nodeId: run.currentNodeId ?? "", errorCode: "INTERRUPTED", message: "Execution was interrupted by a host or application restart.", timestamp: Date.now(),
    }] }];
  }));
}

const layouts = (): Record<string, unknown> => {
  if (typeof localStorage === "undefined") return {};
  return Object.fromEntries((["workflow", "vision", "ai", "knowledge"] as WorkspaceId[]).flatMap((workspace) => {
    const raw = localStorage.getItem(layoutStorageKey(workspace));
    if (!raw) return [];
    try { return [[workspace, JSON.parse(raw) as unknown]]; } catch { return []; }
  }));
};

export function collectProjectAssets(): Record<string, unknown> {
  const ai = useAIStudioStore.getState(), execution = useExecutionStore.getState();
  const vision = useVisionDocumentStore.getState(), timeline = useVisionTimelineStore.getState();
  const assets: Record<string, unknown> = {
    ai: { mode: ai.mode, sessions: ai.sessions, activeSessionId: ai.activeSessionId, selectedProviderId: ai.selectedProviderId, selectedModelId: ai.selectedModelId, systemPrompt: ai.systemPrompt, userInput: ai.userInput, messages: ai.messages, parameters: ai.parameters, contexts: ai.contexts, prompt: ai.prompt, promptB: ai.promptB },
    workflow: useWorkflowStore.getState().exportToDefinition(),
    execution: { runs: interruptRecoverableRuns(execution.runs), activeRunId: execution.activeRunId, status: RECOVERABLE.has(execution.status) ? "interrupted" : execution.status, result: execution.result },
    vision: { source: vision.source, tool: vision.tool, overlays: vision.overlays, selectedId: vision.selectedId, zoom: vision.zoom, pan: vision.pan, grid: vision.grid, rulers: vision.rulers, guides: vision.guides, crosshair: vision.crosshair, revision: vision.revision, frames: timeline.frames, current: timeline.current, loop: timeline.loop, speed: timeline.speed },
    workspace: { activeWorkspace: useWorkspaceStore.getState().activeWorkspace, layouts: layouts() },
    recovery: { savedAt: new Date().toISOString(), semantics: "active executions restore as interrupted and require explicit restart" },
  };
  assertCredentialFree(assets);
  return assets;
}

const record = (value: unknown): Record<string, unknown> | null => value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : null;

export function restoreProjectAssets(assets: Record<string, unknown>): void {
  assertCredentialFree(assets);
  const ai = record(assets.ai) as ReturnType<typeof useAIStudioStore.getState> | null;
  if (ai) useAIStudioStore.setState({ mode: ai.mode, sessions: ai.sessions, activeSessionId: ai.activeSessionId, selectedProviderId: ai.selectedProviderId, selectedModelId: ai.selectedModelId, systemPrompt: ai.systemPrompt, userInput: ai.userInput, messages: ai.messages, parameters: ai.parameters, contexts: ai.contexts, prompt: ai.prompt, promptB: ai.promptB, running: false, streaming: false, startedAt: null, lastRequest: null, lastResponse: null, streamContent: "", error: null });
  const workflow = record(assets.workflow);
  if (workflow) useWorkflowStore.getState().loadFromDefinition(workflow as unknown as WorkflowDefinition);
  const execution = record(assets.execution);
  if (execution) {
    const runs = interruptRecoverableRuns((record(execution.runs) ?? {}) as Record<string, WorkflowRun>);
    const active = typeof execution.activeRunId === "string" ? execution.activeRunId : null;
    const status: WorkflowRunStatus = active && runs[active] ? runs[active].status : "interrupted";
    useExecutionStore.setState({ runs, activeRunId: active, status, isRunning: false, isPaused: false, result: execution.result as ReturnType<typeof useExecutionStore.getState>["result"] });
  }
  const vision = record(assets.vision);
  if (vision) {
    useVisionDocumentStore.setState(vision as unknown as Partial<ReturnType<typeof useVisionDocumentStore.getState>>);
    useVisionTimelineStore.setState({ ...(vision as unknown as Partial<ReturnType<typeof useVisionTimelineStore.getState>>), playing: false });
  }
  const workspace = record(assets.workspace), savedLayouts = record(workspace?.layouts);
  if (typeof localStorage !== "undefined" && savedLayouts) for (const id of ["workflow", "vision", "ai", "knowledge"] as WorkspaceId[]) if (savedLayouts[id]) localStorage.setItem(layoutStorageKey(id), JSON.stringify(savedLayouts[id]));
  if (workspace && ["workflow", "vision", "ai", "knowledge"].includes(String(workspace.activeWorkspace))) useWorkspaceStore.getState().setActiveWorkspace(workspace.activeWorkspace as WorkspaceId);
  if (typeof window !== "undefined") window.dispatchEvent(new Event("atlas:project-assets-restored"));
}

class ProjectAssetService {
  private projectPath: string | null = null;
  private timer: ReturnType<typeof setTimeout> | null = null;
  private unsubscribers: Array<() => void> = [];

  async open(projectPath: string): Promise<void> { this.stop(); this.projectPath = projectPath; const assets = await loadProjectAssets(projectPath); if (assets) restoreProjectAssets(assets); this.start(); if (!assets) await this.saveNow(); }
  scheduleSave(): void { if (!this.projectPath) return; if (this.timer) clearTimeout(this.timer); this.timer = setTimeout(() => { this.timer = null; void this.saveNow(); }, 300); }
  async saveNow(): Promise<void> { if (!this.projectPath) return; try { await saveProjectAssets(this.projectPath, collectProjectAssets()); } catch (error) { useProjectStore.getState().addNotification({ title: "Project persistence failed", message: error instanceof Error ? error.message : String(error), severity: "error", acknowledged: false }); } }
  async close(): Promise<void> { await this.saveNow(); this.stop(); this.projectPath = null; }
  stop(): void { if (this.timer) clearTimeout(this.timer); this.timer = null; this.unsubscribers.splice(0).forEach((unsubscribe) => unsubscribe()); }
  private start(): void { const schedule = () => this.scheduleSave(); this.unsubscribers = [useAIStudioStore.subscribe(schedule), useWorkflowStore.subscribe(schedule), useExecutionStore.subscribe(schedule), useVisionDocumentStore.subscribe(schedule), useVisionTimelineStore.subscribe(schedule), useWorkspaceStore.subscribe(schedule)]; }
}

export const projectAssetService = new ProjectAssetService();
