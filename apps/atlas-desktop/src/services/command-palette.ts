import { useLogStore, useProjectStore } from "../stores";
import type { CommandPaletteItem } from "../types";

export class CommandPaletteService {
  private commands: CommandPaletteItem[] = [];

  register(command: CommandPaletteItem): void {
    this.commands.push(command);
    useProjectStore.getState().registerCommand(command);
  }

  search(query: string): CommandPaletteItem[] {
    return useProjectStore.getState().searchCommands(query);
  }

  execute(id: string): void {
    const command = this.commands.find((c) => c.id === id);
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
    return [...this.commands];
  }

  getRecentCommands(): string[] {
    return useProjectStore.getState().getRecentCommands();
  }
}

export const commandPaletteService = new CommandPaletteService();

