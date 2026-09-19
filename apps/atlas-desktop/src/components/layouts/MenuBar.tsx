import React from "react";
import { commandPaletteService } from "../../services";
import { useThemeStore } from "../../stores";
import { getWorkspacePanels, useWorkspaceStore, workspaceService } from "../../workspace";

interface MenuBarProps { onToggleCommandPalette: () => void }
type MenuItem = { label: string; action?: () => void; shortcut?: string; disabled?: boolean } | { separator: true };
const separator = { separator: true } as const;
export const MenuBar: React.FC<MenuBarProps> = ({ onToggleCommandPalette }) => {
  const theme = useThemeStore((s) => s.resolvedTheme); const active = useWorkspaceStore((s) => s.activeWorkspace); const run = (id: string) => () => commandPaletteService.execute(id);
  const panels = getWorkspacePanels(active).map((panel) => ({ label: panel.title, action: () => workspaceService.openPanel(panel.id) }));
  return <nav className="menu-bar" data-theme={theme} aria-label="Application menu"><span className="atlas-wordmark">Atlas</span>
    <MenuDropdown label="File" items={[{label:"Create Project",action:run("desktop.open-project")},{label:"Open Project",action:run("desktop.open-project")},{label:"Open Project by Path",action:run("desktop.open-project-path")},{label:active==="knowledge"?"Import Knowledge":"Open Image",action:run(active==="knowledge"?"knowledge.import":active==="ai"?"ai.context.image":"vision.open-image"),disabled:active==="workflow"},{label:"Save",action:run(active==="knowledge"?"knowledge.save":active==="ai"?"ai.session.save":"vision.save"),shortcut:"Ctrl+S",disabled:active==="workflow"},{label:"Export",action:run(active==="knowledge"?"knowledge.export.json":"vision.export"),disabled:!(["vision","knowledge"] as string[]).includes(active)},separator,{label:"Close Project",action:run("desktop.close-project")},{label:"Exit",action:run("desktop.exit")}]} />
    <MenuDropdown label="Edit" items={[{label:"Undo",action:run("vision.undo"),shortcut:"Ctrl+Z"},{label:"Redo",action:run("vision.redo"),shortcut:"Ctrl+Y"},separator,{label:"Cut",action:run("desktop.cut")},{label:"Copy",action:run("vision.copy"),shortcut:"Ctrl+C"},{label:"Paste",action:run("vision.paste"),shortcut:"Ctrl+V"},{label:"Duplicate",action:run("vision.duplicate"),shortcut:"Ctrl+D"},{label:"Delete",action:run("vision.delete"),shortcut:"Delete"}]} />
    <MenuDropdown label="View" items={[{label:"Command Palette",shortcut:"Ctrl+Shift+P",action:onToggleCommandPalette},separator,{label:"Workflow Workspace",action:()=>workspaceService.switchWorkspace("workflow")},{label:"Vision Workspace",action:()=>workspaceService.switchWorkspace("vision")},{label:"AI Workspace",action:()=>workspaceService.switchWorkspace("ai")},{label:"Knowledge Workspace",action:()=>workspaceService.switchWorkspace("knowledge")},separator,...panels,separator,{label:"Grid",action:run("vision.grid"),disabled:active!=="vision"},{label:"Rulers",action:run("vision.rulers"),disabled:active!=="vision"},{label:"Reset Layout",action:()=>workspaceService.resetActiveLayout()}]} />
    <MenuDropdown label="Run" items={active === "workflow" ? [{label:"Run Workflow",action:run("workflow.run"),shortcut:"F5"},{label:"Pause / Resume",action:run("workflow.pause-resume"),shortcut:"F8"},{label:"Step",action:run("workflow.step"),shortcut:"F7"},{label:"Stop",action:run("workflow.stop"),shortcut:"Shift+F5"},separator,{label:"Restart",action:run("workflow.restart"),shortcut:"Ctrl+Shift+F5"}] : [{label:"Start All Runtimes",action:run("desktop.start-runtimes")},{label:"Stop All Runtimes",action:run("desktop.stop-runtimes")},separator,{label:"Restart Selected",action:run("desktop.restart-runtime")}]} />
    <MenuDropdown label="Tools" items={[{label:"OCR",action:run("vision.ocr"),disabled:active!=="vision"},{label:"Detection",action:run("vision.detect"),disabled:active!=="vision"},{label:"Template Matching",action:run("vision.template-match"),disabled:active!=="vision"},separator,{label:"Export Logs",action:run("desktop.export-logs")},{label:"Clear Logs",action:run("desktop.clear-logs")},{label:"Settings",action:run("desktop.settings")}]} />
    <MenuDropdown label="AI" items={[{label:"New Session",action:run("ai.session.new"),shortcut:"Ctrl+N",disabled:active!=="ai"},{label:"Run",action:run("ai.inference.run"),shortcut:"Ctrl+Enter",disabled:active!=="ai"},{label:"Stop",action:run("ai.inference.stop"),shortcut:"Escape",disabled:active!=="ai"},separator,{label:"Manage Providers",action:()=>workspaceService.openPanel("ai.providers"),disabled:active!=="ai"},{label:"Prompt Studio",action:run("ai.prompt.open"),disabled:active!=="ai"},{label:"Conversation",action:run("ai.conversation.open"),disabled:active!=="ai"},{label:"Memory",action:run("ai.memory.open"),disabled:active!=="ai"},{label:"Tools",action:run("ai.tools.open"),disabled:active!=="ai"},{label:"Agent Inspector",action:run("ai.agent.open"),disabled:active!=="ai"},separator,{label:"Clear Context",action:run("ai.context.clear"),disabled:active!=="ai"}]} />
    <MenuDropdown label="Knowledge" items={[{label:"New Knowledge",action:run("knowledge.new"),shortcut:"Ctrl+N",disabled:active!=="knowledge"},{label:"Search",action:run("knowledge.search"),shortcut:"Ctrl+K",disabled:active!=="knowledge"},{label:"Save",action:run("knowledge.save"),shortcut:"Ctrl+S",disabled:active!=="knowledge"},{label:"Delete",action:run("knowledge.delete"),disabled:active!=="knowledge"},separator,{label:"Import",action:run("knowledge.import"),disabled:active!=="knowledge"},{label:"Export JSON",action:run("knowledge.export.json"),disabled:active!=="knowledge"},{label:"Refresh",action:run("knowledge.refresh"),disabled:active!=="knowledge"}]} />
    <MenuDropdown label="Help" items={[{label:"Getting Started",action:run("desktop.about")},{label:"About / Diagnostics",action:run("desktop.about")}]} />
  </nav>;
};

const MenuDropdown: React.FC<{ label: string; items: readonly MenuItem[] }> = ({ label, items }) => {
  const [open, setOpen] = React.useState(false);
  const timer = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  const root = React.useRef<HTMLDivElement>(null);
  const trigger = React.useRef<HTMLButtonElement>(null);
  const pendingFocus = React.useRef<"first" | "last" | "next" | "previous" | null>(null);
  const menuId = React.useId();
  const show = () => { if (timer.current) clearTimeout(timer.current); setOpen(true); };
  const hide = () => { timer.current = setTimeout(() => setOpen(false), 2000); };
  const focusItem = (container: HTMLDivElement, direction: "first" | "last" | "next" | "previous") => {
    const buttons = Array.from(container.querySelectorAll<HTMLButtonElement>("[role=menuitem]:not(:disabled)"));
    if (!buttons.length) return;
    const current = buttons.indexOf(document.activeElement as HTMLButtonElement);
    let index = 0;
    if (direction === "last") index = buttons.length - 1;
    else if (direction === "next") index = current < 0 ? 0 : (current + 1) % buttons.length;
    else if (direction === "previous") index = current < 0 ? buttons.length - 1 : (current - 1 + buttons.length) % buttons.length;
    buttons[index]?.focus();
  };
  React.useLayoutEffect(() => {
    if (!open || !pendingFocus.current || !root.current) return;
    focusItem(root.current, pendingFocus.current);
    pendingFocus.current = null;
  }, [open]);
  return <div
    ref={root}
    className="menu-dropdown"
    onMouseEnter={show}
    onMouseLeave={hide}
    onFocus={show}
    onBlur={(event) => { if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setOpen(false); }}
    onKeyDown={(event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopPropagation();
        setOpen(false);
        trigger.current?.focus();
        return;
      }
      if (event.key === "ArrowDown" || event.key === "ArrowUp" || event.key === "Home" || event.key === "End") {
        event.preventDefault();
        const direction = event.key === "ArrowDown" ? "next" : event.key === "ArrowUp" ? "previous" : event.key === "Home" ? "first" : "last";
        if (!open) {
          pendingFocus.current = direction;
          setOpen(true);
        } else {
          focusItem(event.currentTarget, direction);
        }
      }
    }}
  >
    <button ref={trigger} aria-haspopup="menu" aria-expanded={open} aria-controls={open ? menuId : undefined} onClick={() => setOpen(true)}>{label}</button>
    {open && <div id={menuId} className="menu-popup" role="menu" aria-label={label}>
      {items.map((item, i) => "separator" in item
        ? <hr role="separator" key={i}/>
        : <button role="menuitem" key={`${item.label}-${i}`} disabled={item.disabled} onClick={() => { item.action?.(); setOpen(false); trigger.current?.focus(); }}>
            <span>{item.label}</span>{item.shortcut && <kbd>{item.shortcut}</kbd>}
          </button>)}
    </div>}
  </div>;
};
