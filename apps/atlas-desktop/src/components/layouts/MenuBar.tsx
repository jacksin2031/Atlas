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
    <MenuDropdown label="File" items={[{label:"Open Project",action:run("desktop.open-project")},{label:"Open Image",action:run("vision.open-image"),disabled:active!=="vision"},{label:"Save",action:run("vision.save"),shortcut:"Ctrl+S",disabled:active!=="vision"},{label:"Export",action:run("vision.export"),disabled:active!=="vision"},separator,{label:"Close Project",action:run("desktop.close-project")},{label:"Exit",action:run("desktop.exit")}]} />
    <MenuDropdown label="Edit" items={[{label:"Undo",action:run("vision.undo"),shortcut:"Ctrl+Z"},{label:"Redo",action:run("vision.redo"),shortcut:"Ctrl+Y"},separator,{label:"Cut",action:run("desktop.cut")},{label:"Copy",action:run("vision.copy"),shortcut:"Ctrl+C"},{label:"Paste",action:run("vision.paste"),shortcut:"Ctrl+V"},{label:"Duplicate",action:run("vision.duplicate"),shortcut:"Ctrl+D"},{label:"Delete",action:run("vision.delete"),shortcut:"Delete"}]} />
    <MenuDropdown label="View" items={[{label:"Command Palette",shortcut:"Ctrl+Shift+P",action:onToggleCommandPalette},separator,{label:"Workflow Workspace",action:()=>workspaceService.switchWorkspace("workflow")},{label:"Vision Workspace",action:()=>workspaceService.switchWorkspace("vision")},separator,...panels,separator,{label:"Grid",action:run("vision.grid"),disabled:active!=="vision"},{label:"Rulers",action:run("vision.rulers"),disabled:active!=="vision"},{label:"Reset Layout",action:()=>workspaceService.resetActiveLayout()}]} />
    <MenuDropdown label="Run" items={[{label:"Start All Runtimes",action:run("desktop.start-runtimes")},{label:"Stop All Runtimes",action:run("desktop.stop-runtimes")},separator,{label:"Restart Selected",action:run("desktop.restart-runtime")}]} />
    <MenuDropdown label="Tools" items={[{label:"OCR",action:run("vision.ocr"),disabled:active!=="vision"},{label:"Detection",action:run("vision.detect"),disabled:active!=="vision"},{label:"Template Matching",action:run("vision.template-match"),disabled:active!=="vision"},separator,{label:"Export Logs",action:run("desktop.export-logs")},{label:"Clear Logs",action:run("desktop.clear-logs")},{label:"Settings",action:run("desktop.settings")}]} />
    <MenuDropdown label="Help" items={[{label:"About Atlas",action:run("desktop.about")}]} />
  </nav>;
};

const MenuDropdown: React.FC<{ label: string; items: readonly MenuItem[] }> = ({ label, items }) => { const [open,setOpen]=React.useState(false); const timer=React.useRef<ReturnType<typeof setTimeout>|null>(null); const show=()=>{if(timer.current)clearTimeout(timer.current);setOpen(true)}; const hide=()=>{timer.current=setTimeout(()=>setOpen(false),150)}; return <div className="menu-dropdown" onMouseEnter={show} onMouseLeave={hide}><button aria-haspopup="menu" aria-expanded={open} onClick={()=>setOpen(!open)}>{label}</button>{open&&<div className="menu-popup" role="menu">{items.map((item,i)=>"separator" in item?<hr key={i}/>:<button role="menuitem" key={`${item.label}-${i}`} disabled={item.disabled} onClick={()=>{item.action?.();setOpen(false)}}><span>{item.label}</span>{item.shortcut&&<kbd>{item.shortcut}</kbd>}</button>)}</div>}</div>; };
