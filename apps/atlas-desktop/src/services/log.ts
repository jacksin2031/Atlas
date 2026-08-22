import { useLogStore } from "../stores";
import type { LogEntry } from "../types";

export class LogService {
  private buffer: LogEntry[] = [];
  private bufferSizeLimit = 10000;

  addLog(entry: Omit<LogEntry, "id">): void {
    this.buffer.push({ ...entry, id: "svc-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8) });
    if (this.buffer.length > this.bufferSizeLimit) {
      this.buffer = this.buffer.slice(-this.bufferSizeLimit / 2);
    }
    useLogStore.getState().addEntry(entry);
  }

  getFilteredLogs(filter: { level: string; source: string; query: string }): LogEntry[] {
    return this.buffer.filter((entry) => {
      if (filter.level !== "all" && entry.level !== filter.level) return false;
      if (filter.source !== "all" && entry.source !== filter.source) return false;
      if (filter.query && !entry.message.toLowerCase().includes(filter.query.toLowerCase())) return false;
      return true;
    });
  }

  exportLogs(filter?: { level: string; source: string; query: string }): string {
    const entries = filter ? this.getFilteredLogs(filter) : this.buffer;
    return entries.map((e) => "[" + new Date(e.timestamp).toISOString() + "] " + e.level.toUpperCase() + " [" + e.source + "]" + (e.runtime ? " (" + e.runtime + ")" : "") + " " + e.message).join("\n");
  }

  searchLogs(query: string): LogEntry[] {
    return this.buffer.filter((e) => e.message.toLowerCase().includes(query.toLowerCase()));
  }

  clearLogs(): void {
    this.buffer = [];
    useLogStore.getState().clearEntries();
  }

  getBuffer(): LogEntry[] {
    return [...this.buffer];
  }
}

export const logService = new LogService();
