import { useLogStore } from "../stores";
import type { ThemeMode } from "../types";

export class ThemeService {
  private systemMediaQuery: MediaQueryList | null = null;

  initialize(): void {
    const systemMQ = typeof window !== "undefined"
      ? window.matchMedia("(prefers-color-scheme: dark)")
      : null;
    this.systemMediaQuery = systemMQ;
    if (systemMQ) {
      systemMQ.addEventListener("change", this.handleSystemChange);
    }
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ThemeService",
      message: "Theme service initialized",
    });
  }

  setTheme(mode: ThemeMode): void {
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "ThemeService",
      message: `Theme changed to: ${mode}`,
    });
  }

  private handleSystemChange = (): void => {
    // Theme store handles re-resolution
  };

  destroy(): void {
    if (this.systemMediaQuery) {
      this.systemMediaQuery.removeEventListener("change", this.handleSystemChange);
    }
  }
}

export const themeService = new ThemeService();

