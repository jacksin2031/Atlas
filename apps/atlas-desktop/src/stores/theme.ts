import { create } from "zustand";
import type { ThemeMode } from "../types";

interface ThemeState {
  mode: ThemeMode;
  resolvedTheme: "dark" | "light";
  setMode: (mode: ThemeMode) => void;
  toggle: () => void;
}

function resolveTheme(mode: ThemeMode): "dark" | "light" {
  if (mode === "system") {
    if (typeof window !== "undefined" && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }
  return mode;
}

export const useThemeStore = create<ThemeState>((set) => ({
  mode: "dark",
  resolvedTheme: "dark",
  setMode: (mode: ThemeMode) => {
    set({ mode, resolvedTheme: resolveTheme(mode) });
  },
  toggle: () =>
    set((state) => {
      const next = state.resolvedTheme === "dark" ? "light" : "dark";
      return { mode: next as ThemeMode, resolvedTheme: next };
    }),
}));
