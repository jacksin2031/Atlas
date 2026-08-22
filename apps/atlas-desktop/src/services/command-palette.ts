import { useLogStore, useProjectStore } from "../stores";
import type { CommandPaletteItem } from "../types";

export class CommandPaletteService {
  private commands = new Map<string, CommandPaletteItem>();

  register(command: CommandPaletteItem): void {
    this.commands.set(command.id, command);
    useProjectStore.getState().registerCommand(command);
  }

  search(query: string): CommandPaletteItem[] {
    return useProjectStore.getState().searchCommands(query);
  }

  execute(id: string): void {
    const command = this.commands.get(id);
    if (command) {
      command.handler();
      useProjectStore.getState().recordCommandUsed(command.label);
      useLogStore.getState().addEntry({
        timestamp: Date.now(),
        level: "debug",
        source: "CommandPaletteService",
        message: `Command executed: ${command.label}`,
      });
    }
  }

  getAllCommands(): CommandPaletteItem[] {
    return [...this.commands.values()];
  }

  getRecentCommands(): string[] {
    return useProjectStore.getState().getRecentCommands();
  }
}

export const commandPaletteService = new CommandPaletteService();
