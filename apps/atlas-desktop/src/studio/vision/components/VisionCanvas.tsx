import React, { useCallback, useRef, useState } from "react";
import { Button, EmptyState } from "../../../design-system";
import { createOverlay, useVisionDocumentStore } from "../stores";
import { visionCaptureService, visionImportService } from "../services/vision-service";
import type { OverlayType, VisionTool } from "../types";

const overlayForTool: Partial<Record<VisionTool, OverlayType>> = { rectangle: "rectangle", ellipse: "ellipse", line: "line", arrow: "arrow", "ocr-region": "ocr-region", "object-region": "object-detection", "template-region": "template-region", "color-sampler": "color-sample", measure: "measurement", text: "label" };

export const VisionCanvas: React.FC = () => {
  const source = useVisionDocumentStore((s) => s.source); const overlays = useVisionDocumentStore((s) => s.overlays); const selectedId = useVisionDocumentStore((s) => s.selectedId);
  const zoom = useVisionDocumentStore((s) => s.zoom); const pan = useVisionDocumentStore((s) => s.pan); const grid = useVisionDocumentStore((s) => s.grid); const rulers = useVisionDocumentStore((s) => s.rulers); const crosshair = useVisionDocumentStore((s) => s.crosshair); const tool = useVisionDocumentStore((s) => s.tool);
  const rootRef = useRef<HTMLDivElement>(null); const dragRef = useRef<{ x: number; y: number; panX: number; panY: number } | null>(null); const [space, setSpace] = useState(false); const [menu, setMenu] = useState<{ x: number; y: number; overlay: boolean } | null>(null);

  React.useEffect(() => { const down = (e: KeyboardEvent) => { if (e.code === "Space") setSpace(true); }; const up = (e: KeyboardEvent) => { if (e.code === "Space") setSpace(false); }; window.addEventListener("keydown", down); window.addEventListener("keyup", up); return () => { window.removeEventListener("keydown", down); window.removeEventListener("keyup", up); }; }, []);
  const toImagePoint = useCallback((clientX: number, clientY: number) => { const rect = rootRef.current?.getBoundingClientRect(); return { x: Math.round(((clientX - (rect?.left ?? 0)) - pan.x) / zoom), y: Math.round(((clientY - (rect?.top ?? 0)) - pan.y) / zoom) }; }, [pan, zoom]);

  const onPointerDown = (event: React.PointerEvent) => {
    setMenu(null); const point = toImagePoint(event.clientX, event.clientY);
    if (space || tool === "pan" || event.button === 1) { dragRef.current = { x: event.clientX, y: event.clientY, panX: pan.x, panY: pan.y }; event.currentTarget.setPointerCapture(event.pointerId); return; }
    const overlayType = overlayForTool[tool]; if (overlayType && source) useVisionDocumentStore.getState().addOverlay(createOverlay(overlayType, point.x, point.y)); else useVisionDocumentStore.getState().selectOverlay(null);
  };
  const onPointerMove = (event: React.PointerEvent) => { const point = toImagePoint(event.clientX, event.clientY); useVisionDocumentStore.getState().setCursor(point); if (dragRef.current) useVisionDocumentStore.getState().setPan({ x: dragRef.current.panX + event.clientX - dragRef.current.x, y: dragRef.current.panY + event.clientY - dragRef.current.y }); };
  const endDrag = () => { dragRef.current = null; };
  const onWheel = (event: React.WheelEvent) => { if (event.ctrlKey || tool === "zoom") { event.preventDefault(); useVisionDocumentStore.getState().setZoom(zoom * (event.deltaY < 0 ? 1.1 : .9)); } };
  const onDrop = (event: React.DragEvent) => { event.preventDefault(); const file = event.dataTransfer.files[0]; if (file) void visionImportService.openFile(file); };

  if (!source) return <div className="vision-canvas empty" onDragOver={(e) => e.preventDefault()} onDrop={onDrop}><EmptyState title="No visual source loaded" description="Capture the screen, open an image, or drop an image anywhere on this canvas." actions={<><Button icon="capture" onClick={() => void visionCaptureService.captureScreen()}>Capture Screen</Button><Button icon="open" onClick={() => void visionImportService.openImagePicker()}>Open Image</Button><Button disabled>Open Recent Session</Button></>} /></div>;
  return <div ref={rootRef} className={`vision-canvas${grid ? " show-grid" : ""}${rulers ? " show-rulers" : ""}`} tabIndex={0} onPointerDown={onPointerDown} onPointerMove={onPointerMove} onPointerUp={endDrag} onPointerCancel={endDrag} onWheel={onWheel} onDragOver={(e) => e.preventDefault()} onDrop={onDrop} onContextMenu={(e) => { e.preventDefault(); setMenu({ x: e.clientX, y: e.clientY, overlay: Boolean(selectedId) }); }}>
    {rulers && <><div className="ruler horizontal"/><div className="ruler vertical"/></>}
    <div className="vision-stage" style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`, width: source.width, height: source.height }}>
      <img src={source.url} alt={source.name} draggable={false}/>
      {overlays.filter((o) => o.visible).map((overlay) => <div key={overlay.id} className={`vision-overlay type-${overlay.type}${overlay.id === selectedId ? " selected" : ""}${overlay.locked ? " locked" : ""}${overlay.disabled ? " disabled" : ""}`} style={{ left: overlay.x, top: overlay.y, width: overlay.width, height: overlay.height, opacity: overlay.opacity, transform: `rotate(${overlay.rotation}deg)` }} onPointerDown={(e) => { e.stopPropagation(); useVisionDocumentStore.getState().selectOverlay(overlay.id); }}><span>{overlay.name}</span>{overlay.id === selectedId && !overlay.locked && ["nw","ne","sw","se"].map((handle) => <i key={handle} className={`resize-handle ${handle}`}/>)}</div>)}
    </div>
    {crosshair && <CanvasCoordinate zoom={zoom}/>} 
    {menu && <div className="atlas-context-menu" style={{ left: menu.x, top: menu.y }} onPointerDown={(e) => e.stopPropagation()}>{menu.overlay ? <>{["Rename","Duplicate","Delete","Lock / Unlock","Hide","Bring Forward","Send Backward"].map((label) => <button key={label} onClick={() => { const s = useVisionDocumentStore.getState(); const selected = s.overlays.find((o) => o.id === s.selectedId); if (label === "Duplicate") s.duplicateSelected(); else if (label === "Delete") s.deleteSelected(); else if (label === "Lock / Unlock" && selected) s.updateOverlay(selected.id, { locked: !selected.locked }); else if (label === "Hide" && selected) s.updateOverlay(selected.id, { visible: false }); else if (label === "Bring Forward") s.moveSelected("forward"); else if (label === "Send Backward") s.moveSelected("backward"); else if (label === "Rename" && selected) { const name = prompt("Overlay name", selected.name); if (name) s.updateOverlay(selected.id, { name }); } setMenu(null); }}>{label}</button>)}</> : <>{["Paste","Fit","Reset View","Grid","Rulers"].map((label) => <button key={label} onClick={() => { const s = useVisionDocumentStore.getState(); if (label === "Fit") s.fit(); else if (label === "Reset View") s.actualSize(); else if (label === "Grid") s.toggleGrid(); else if (label === "Rulers") s.toggleRulers(); setMenu(null); }}>{label}</button>)}</>}</div>}
  </div>;
};

const CanvasCoordinate: React.FC<{ zoom: number }> = React.memo(({ zoom }) => { const cursor=useVisionDocumentStore((s)=>s.cursor); return <div className="canvas-coordinate">{cursor.x}, {cursor.y} px · {Math.round(zoom * 100)}%</div>; });
