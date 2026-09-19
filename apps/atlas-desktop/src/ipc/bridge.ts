/**
 * IPC bridge layer for communicating with Tauri backend commands.
 * Maps desktop shell operations to Tauri commands.
 */

import { getVersion as tauriGetVersion } from "@tauri-apps/api/app";
import { invoke as tauriInvoke } from "@tauri-apps/api/core";
import { listen, type UnlistenFn } from "@tauri-apps/api/event";

/**
 * Invoke a Tauri backend command.
 * Returns the typed result or throws on error.
 */
async function invoke<T>(command: string, args?: Record<string, unknown>): Promise<T> {
  try {
    return await tauriInvoke<T>(command, args);
  } catch (error) {
    // Vite browser mode has no Tauri host; keep the UI usable there.
    console.debug(`[IPC] ${command} unavailable`, error);
    return null as unknown as T;
  }
}

async function invokeRequired<T>(command: string, args?: Record<string, unknown>): Promise<T> {
  return tauriInvoke<T>(command, args);
}


export interface BetaSystemInfo {
  version: string;
  platform: string;
  architecture: string;
  buildType: string;
  commit: string;
  runtimes: Array<{ name: string; status: string; detail: string }>;
}

export interface DiagnosticsExportResult {
  path: string | null;
}

/** Queries installed-product identity and runtime health without exposing credentials. */
export async function getBetaSystemInfo(): Promise<BetaSystemInfo> {
  return invokeRequired<BetaSystemInfo>("beta_system_info");
}

/** Exports the allowlisted local diagnostics bundle through the native save dialog. */
export async function exportDiagnostics(): Promise<DiagnosticsExportResult> {
  return invokeRequired<DiagnosticsExportResult>("export_diagnostics");
}

/** Returns the native Tauri package version without exposing Tauri imports to React components. */
export async function getNativeAppVersion(): Promise<string> {
  return tauriGetVersion();
}

/** Generic Marketplace command boundary. */
export async function requestMarketplace<T>(command: string, payload: Record<string, unknown>): Promise<T> {
  return invokeRequired<T>("marketplace_request", { command, payload });
}

/** Marketplace revision event boundary. */
export async function listenMarketplaceChanged(handler: (revision: number) => void): Promise<UnlistenFn> {
  return listen<{ revision: number }>("plugin://marketplace-changed", ({ payload }) => handler(payload.revision));
}

/**
 * Open a project via the Tauri backend.
 */
export async function openProject(path: string): Promise<void> {
  await invoke<void>("open_project", { path });
}

/** Opens the native desktop folder picker and returns an absolute path. */
export async function selectProjectDirectory(): Promise<string | null> {
  return invokeRequired<string | null>("project_select_directory");
}

/** Persists only the last project directory pointer in app data for restart recovery. */
export async function rememberProjectSession(projectPath: string): Promise<void> {
  await invokeRequired<void>("project_session_remember", { projectPath });
}

export async function restoreProjectSession(): Promise<string | null> {
  return invokeRequired<string | null>("project_session_restore");
}

export async function clearProjectSession(): Promise<void> {
  await invokeRequired<void>("project_session_clear");
}

/**
 * Close the current project via the Tauri backend.
 */
export async function closeProject(): Promise<void> {
  await invoke<void>("close_project");
}

/**
 * Get recent projects list.
 */
export async function getRecentProjects(): Promise<string[]> {
  return invoke<string[]>("get_recent_projects");
}

/**
 * Save the current window layout.
 */
export async function saveLayout(layout: unknown): Promise<void> {
  await invoke<void>("save_layout", { layout });
}

/**
 * Load the persisted window layout.
 */
export async function loadLayout(): Promise<unknown> {
  return invoke<unknown>("load_layout");
}

/**
 * Export logs to a file.
 */
export async function exportLogs(content: string, filename: string): Promise<void> {
  await invoke<void>("export_logs", { content, filename });
}

/**
 * Show a system notification.
 */
export async function showNotification(title: string, body: string): Promise<void> {
  await invoke<void>("show_notification", { title, body });
}

/**
 * Toggle the command palette visibility.
 */
export async function toggleCommandPalette(): Promise<void> {
  await invoke<void>("toggle_command_palette");
}

/**
 * Get the current application theme mode.
 */
export async function getThemeMode(): Promise<string> {
  return invoke<string>("get_theme_mode");
}

/**
 * Set the application theme mode.
 */
export async function setThemeMode(mode: string): Promise<void> {
  await invoke<void>("set_theme_mode", { mode });
}

export interface VisionFrameSource {
  frameId: string;
  name: string;
  url: string;
  width: number;
  height: number;
  originX: number;
  originY: number;
  scaleFactor: number;
  coordinateSpace: "screen";
  capturedAt: number;
  kind: "screenshot";
}

/** Runtime boundary for screen capture. The backend may return null when no provider is connected. */
export async function captureVisionFrame(): Promise<VisionFrameSource | null> {
  return invokeRequired<VisionFrameSource | null>("vision_capture_frame");
}

/** AI Runtime discovery boundary. No credentials are accepted or returned here. */
export async function discoverAIRuntime(): Promise<import("../studio/ai/types").AIRuntimeSnapshot | null> {
  return invokeRequired<import("../studio/ai/types").AIRuntimeSnapshot | null>("ai_discover");
}

/** Sends Atlas's normalized inference request to the hosted AI Runtime. */
export async function executeAIInference(request: import("../studio/ai/types").AINormalizedRequest): Promise<import("../studio/ai/types").AINormalizedResponse | null> {
  return invokeRequired<import("../studio/ai/types").AINormalizedResponse | null>("ai_infer", { request });
}

export async function cancelAIInference(requestId: string): Promise<boolean | null> {
  return invokeRequired<boolean | null>("ai_cancel", { requestId });
}

export async function controlAIProvider(providerId: string, action: "connect" | "disconnect" | "refresh" | "test"): Promise<boolean | null> {
  return invokeRequired<boolean | null>("ai_provider_action", { providerId, action });
}

/** Stores a provider credential directly in the OS vault. The value is never returned to React. */
export async function setAIProviderCredential(providerId: string, credential: string): Promise<void> {
  await invokeRequired<void>("ai_credential_set", { providerId, credential });
}

export async function deleteAIProviderCredential(providerId: string): Promise<void> {
  await invokeRequired<void>("ai_credential_delete", { providerId });
}

export async function hasAIProviderCredential(providerId: string): Promise<boolean | null> {
  return invokeRequired<boolean>("ai_credential_status", { providerId });
}

/** Subscribes to normalized inference lifecycle and streaming events from Tauri. */
export async function listenAIRuntimeEvents(handler: (event: import("../studio/ai/types").AIRuntimeTransportEvent) => void): Promise<UnlistenFn> {
  try {
    return await listen<import("../studio/ai/types").AIRuntimeTransportEvent>("ai://runtime-event", ({ payload }) => handler(payload));
  } catch (error) {
    console.debug("[IPC] ai://runtime-event unavailable", error);
    return () => undefined;
  }
}

export async function validateWorkflowRuntime(definition: unknown): Promise<import("../studio/workflow/types").WorkflowValidationResponse | null> {
  return invokeRequired("workflow_validate", { definition });
}

export async function startWorkflowRuntime(
  definition: unknown,
  inputs: Record<string, unknown>,
  projectContext: Record<string, unknown>,
  breakpoints: string[],
): Promise<import("../studio/workflow/types").WorkflowRuntimeState | null> {
  return invokeRequired("workflow_start", { definition, inputs, projectContext, breakpoints });
}

type WorkflowControlCommand = "workflow_pause" | "workflow_resume" | "workflow_stop" | "workflow_step" | "workflow_restart";
export async function controlWorkflowRuntime(command: WorkflowControlCommand, executionId: string): Promise<import("../studio/workflow/types").WorkflowRuntimeState | null> {
  return invokeRequired(command, { executionId });
}

export async function getWorkflowRuntimeState(executionId: string): Promise<import("../studio/workflow/types").WorkflowRuntimeState | null> {
  return invokeRequired("workflow_get_state", { executionId });
}

export async function getWorkflowRuntimeResult(executionId: string): Promise<import("../studio/workflow/types").WorkflowResultEnvelope | null> {
  return invokeRequired("workflow_get_result", { executionId });
}

export async function listenWorkflowRuntimeEvents(handler: (event: import("../studio/workflow/types").WorkflowRuntimeEvent) => void): Promise<UnlistenFn> {
  try {
    return await listen<import("../studio/workflow/types").WorkflowRuntimeEvent>("workflow://runtime-event", ({ payload }) => handler(payload));
  } catch (error) {
    console.debug("[IPC] workflow://runtime-event unavailable", error);
    return () => undefined;
  }
}

export interface InputSafetyStatus {
  armed: boolean;
  emergencyStopped: boolean;
  allowedWindowTitle: string | null;
  maxActionsPerSecond: number;
  maxTextLength: number;
  dangerousActionsAllowed: boolean;
}

export interface InputSafetyPolicy {
  permissionGranted: boolean;
  allowedWindowTitle: string;
  maxActionsPerSecond: number;
  maxTextLength: number;
  allowDangerousActions: boolean;
}

export async function armInputRuntime(policy: InputSafetyPolicy): Promise<InputSafetyStatus | null> {
  return invokeRequired("workflow_input_arm", { policy });
}

export async function getInputRuntimeStatus(): Promise<InputSafetyStatus | null> {
  return invokeRequired("workflow_input_status");
}

export async function emergencyStopInputRuntime(): Promise<InputSafetyStatus | null> {
  return invokeRequired("workflow_emergency_stop");
}

export interface WorkflowPluginRegistrationResult {
  pluginId: string;
  registrations: import("../studio/workflow/types").PluginNodeRegistration[];
}

export async function registerWorkflowPlugin(plugin: Record<string, unknown>): Promise<WorkflowPluginRegistrationResult> {
  return invokeRequired("workflow_plugin_register", { plugin });
}

export async function loadProjectAssets(projectPath: string): Promise<Record<string, unknown> | null> {
  return invokeRequired("project_assets_load", { projectPath });
}

export async function saveProjectAssets(projectPath: string, assets: Record<string, unknown>): Promise<void> {
  await invokeRequired("project_assets_save", { projectPath, assets });
}

export interface KnowledgeProjectScope { projectId: string; projectPath: string }
const knowledgeArgs=(scope:KnowledgeProjectScope,args:Record<string,unknown>={}):Record<string,unknown>=>({...scope,...args});
export async function activateKnowledgeProject(scope:KnowledgeProjectScope):Promise<void>{await invokeRequired("knowledge_activate",knowledgeArgs(scope));}
export async function getKnowledgeStatus(scope:KnowledgeProjectScope):Promise<unknown>{return invokeRequired("knowledge_status",knowledgeArgs(scope));}
export async function listKnowledgeEntries(scope:KnowledgeProjectScope,options:{type?:string;tags?:string[];offset?:number;limit?:number}={}):Promise<unknown>{return invokeRequired("knowledge_list",knowledgeArgs(scope,{entryType:options.type,tags:options.tags,offset:options.offset,limit:options.limit}));}
export async function getKnowledgeEntry(scope:KnowledgeProjectScope,entryId:string):Promise<unknown>{return invokeRequired("knowledge_get",knowledgeArgs(scope,{entryId}));}
export async function createKnowledgeEntry(scope:KnowledgeProjectScope,entry:Record<string,unknown>,requestId?:string):Promise<unknown>{return invokeRequired("knowledge_create",knowledgeArgs(scope,{entry,requestId}));}
export async function updateKnowledgeEntry(scope:KnowledgeProjectScope,entryId:string,changes:Record<string,unknown>,requestId?:string):Promise<unknown>{return invokeRequired("knowledge_update",knowledgeArgs(scope,{entryId,changes,requestId}));}
export async function deleteKnowledgeEntry(scope:KnowledgeProjectScope,entryId:string,requestId?:string):Promise<unknown>{return invokeRequired("knowledge_delete",knowledgeArgs(scope,{entryId,requestId}));}
export async function searchKnowledge(scope:KnowledgeProjectScope,request:{query:string;types?:string[];tags?:string[];limit?:number;requestId?:string}):Promise<unknown>{return invokeRequired("knowledge_search",knowledgeArgs(scope,request));}
export async function importKnowledgeContent(scope:KnowledgeProjectScope,request:{filename:string;content:string;format:string;requestId?:string}):Promise<unknown>{return invokeRequired("knowledge_import",knowledgeArgs(scope,request));}
export async function exportKnowledge(scope:KnowledgeProjectScope,format:"json"|"md"):Promise<unknown>{return invokeRequired("knowledge_export",knowledgeArgs(scope,{format}));}
export async function listKnowledgeEvents(scope:KnowledgeProjectScope,limit=100):Promise<unknown>{return invokeRequired("knowledge_events",knowledgeArgs(scope,{limit}));}
export async function listenKnowledgeRuntimeEvents(handler:(event:unknown)=>void):Promise<UnlistenFn>{try{return await listen<unknown>("knowledge://runtime-event",({payload})=>handler(payload));}catch(error){console.debug("[IPC] knowledge://runtime-event unavailable",error);return()=>undefined;}}
