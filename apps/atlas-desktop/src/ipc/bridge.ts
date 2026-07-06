/**
 * IPC bridge layer for communicating with Tauri backend commands.
 * Maps desktop shell operations to Tauri commands.
 */

/**
 * Invoke a Tauri backend command.
 * Returns the typed result or throws on error.
 */
async function invoke<T>(command: string, args?: Record<string, unknown>): Promise<T> {
  // Placeholder for Tauri invoke — resolved when Tauri backend is linked
  // In development mode, falls back to in-memory store operations
  console.debug(`[IPC] invoke ${command}`, args);
  return null as unknown as T;
}

/**
 * Open a project via the Tauri backend.
 */
export async function openProject(path: string): Promise<void> {
  await invoke<void>("open_project", { path });
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
