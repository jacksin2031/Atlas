import React from "react";
import { invoke } from "@tauri-apps/api/core";
import { Button } from "../../design-system";
import { useProjectStore } from "../../stores";
import { projectService } from "../../services/project";
import { selectProjectDirectory } from "../../ipc/bridge";
import type { ProjectDescriptor } from "../../types";

export interface BetaSystemInfo {
  version: string; platform: string; architecture: string; buildType: string; commit: string;
  runtimes: Array<{ name: string; status: string; detail: string }>;
}
export const showBetaHelp = (): void => { window.dispatchEvent(new Event("atlas:beta-help")); };

export function GettingStarted() {
  return <section aria-label="Getting started"><h2>Getting started</h2><ol>
    <li>Create a project: choose a dedicated folder. Atlas initializes its .atlas metadata there. Open Project reopens an existing folder.</li>
    <li>Workflow: create or load a workflow, review its nodes, then Run. A runtime failure is shown as an error.</li>
    <li>Vision: capture a frame before detection or template matching. Input starts unarmed; review the target before explicitly arming. Emergency Stop and global Pause/Break stop desktop input.</li>
    <li>Knowledge: create, search and save entries within your project.</li>
    <li>Marketplace currently uses a local development registry. It is not a production Marketplace.</li>
    <li>AI: configure a provider and model in AI Studio. Missing credentials are an external configuration condition, not proof of a failed AI Runtime. No live-provider acceptance is implied.</li>
    <li>Help → About / Diagnostics shows runtime health and exports a local diagnostic file.</li>
  </ol></section>;
}

export function RuntimeHealth({ info }: { info: BetaSystemInfo | null }) {
  return <section aria-label="Runtime health"><h2>Runtime health</h2>{info ? <ul>{info.runtimes.map((runtime) => <li key={runtime.name}><strong>{runtime.name}</strong>: {runtime.status} — {runtime.detail}</li>)}</ul> : <p>Checking installed runtime health…</p>}</section>;
}

export function BetaWelcome() {
  const recent = useProjectStore((state) => state.recentProjects);
  const notifications = useProjectStore((state) => state.notifications);
  const [busy, setBusy] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [info, setInfo] = React.useState<BetaSystemInfo | null>(null);
  React.useEffect(() => { let alive = true; void invoke<BetaSystemInfo>("beta_system_info").then((value) => { if (alive) setInfo(value); }).catch(() => { if (alive) setError("Runtime health is unavailable. Open About / Diagnostics to retry; the installed backend must be running."); }); return () => { alive = false; }; }, []);
  const open = async (project?: ProjectDescriptor) => {
    setBusy(true); setError(null);
    try {
      if (project) await projectService.openProject(project);
      else { const path = await selectProjectDirectory(); if (path) { const now = Date.now(); await projectService.openProject({ id: "", name: path.split(/[\\/]/).filter(Boolean).at(-1) ?? "Atlas Project", path, createdAt: now, updatedAt: now, settings: { theme: "system", language: "en", autoSave: true, tabSize: 2 } }); } }
    } catch { setError("The project could not be opened. Check folder access and project compatibility, then try again. Your project was not marked as open."); }
    finally { setBusy(false); }
  };
  return <main className="beta-welcome" aria-busy={busy}><h1>Welcome to Atlas</h1><p>Create a project or open an existing project to begin.</p>
    <div className="atlas-empty-actions"><Button disabled={busy} onClick={() => void open()}>Create Project</Button><Button disabled={busy} onClick={() => void open()}>Open Project</Button><Button onClick={showBetaHelp}>About / Diagnostics</Button></div>
    {error && <p role="alert">{error}</p>}{notifications.filter((item) => item.severity === "error").slice(-1).map((item) => <p role="alert" key={item.id}>{item.title}: {item.message}</p>)}
    <section aria-label="Open recent"><h2>Open recent</h2>{recent.length ? recent.map((project) => <p key={project.id}><Button disabled={busy} onClick={() => void open(project)}>{project.name}</Button> <small>{project.path}</small></p>) : <p>No recent projects in this session. Open Project can locate projects from an earlier session.</p>}</section>
    <RuntimeHealth info={info}/><GettingStarted/>
  </main>;
}

export function BetaHelp() {
  const dialog = React.useRef<HTMLDialogElement>(null);
  const [info, setInfo] = React.useState<BetaSystemInfo | null>(null);
  const [message, setMessage] = React.useState("");
  const [busy, setBusy] = React.useState(false);
  const refresh = () => { setInfo(null); setMessage(""); void invoke<BetaSystemInfo>("beta_system_info").then(setInfo).catch(() => setMessage("Could not query the installed backend. Restart Atlas and retry.")); };
  React.useEffect(() => { const show = () => { dialog.current?.showModal(); refresh(); }; window.addEventListener("atlas:beta-help", show); return () => window.removeEventListener("atlas:beta-help", show); }, []);
  const exportBundle = async () => { setBusy(true); setMessage(""); try { const result = await invoke<{ path: string | null }>("export_diagnostics"); setMessage(result.path ? `Diagnostics saved: ${result.path}` : "Export cancelled."); } catch { setMessage("Diagnostics export failed. Check destination permissions and retry."); } finally { setBusy(false); } };
  return <dialog ref={dialog} className="beta-help" aria-labelledby="beta-help-title"><h1 id="beta-help-title">About Atlas / Diagnostics</h1><Button onClick={() => dialog.current?.close()}>Close</Button>
    {info && <p>Atlas {info.version} · {info.platform} / {info.architecture} · {info.buildType} · {info.commit}</p>}<RuntimeHealth info={info}/>
    <p>Diagnostics are saved locally only. The export includes allowlisted version, system and runtime metadata. It excludes credentials, Knowledge content, AI conversations, screenshots and arbitrary project files.</p>
    <Button onClick={refresh}>Refresh health</Button> <Button disabled={busy} onClick={() => void exportBundle()}>Export Diagnostics</Button><p role="status">{message}</p><GettingStarted/>
  </dialog>;
}
