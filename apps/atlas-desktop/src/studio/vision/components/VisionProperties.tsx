import React from "react";
import { EmptyState, Field } from "../../../design-system";
import { useVisionDocumentStore } from "../stores";
import type { VisionOverlay } from "../types";

const numberValue = (value: string): number => Number.isFinite(Number(value)) ? Number(value) : 0;
export const VisionProperties: React.FC = () => {
  const selectedId = useVisionDocumentStore((s) => s.selectedId); const overlay = useVisionDocumentStore((s) => s.overlays.find((o) => o.id === selectedId));
  if (!overlay) return <EmptyState title="Nothing selected" description="Select an overlay on the canvas to edit its properties." icon="pointer"/>;
  const update = (patch: Partial<VisionOverlay>) => useVisionDocumentStore.getState().updateOverlay(overlay.id, patch);
  return <div className="property-grid"><Field label="Name"><input value={overlay.name} onChange={(e) => update({ name: e.target.value })}/></Field><Field label="Type"><input value={overlay.type} disabled/></Field>
    {(["x","y","width","height","rotation","opacity"] as const).map((key) => <Field key={key} label={key[0]!.toUpperCase()+key.slice(1)}><input type="number" step={key === "opacity" ? .05 : 1} value={overlay[key]} onChange={(e) => update({ [key]: numberValue(e.target.value) })}/></Field>)}
    <Field label="Visible"><input type="checkbox" checked={overlay.visible} onChange={(e) => update({ visible: e.target.checked })}/></Field><Field label="Locked"><input type="checkbox" checked={overlay.locked} onChange={(e) => update({ locked: e.target.checked })}/></Field>
    {overlay.type === "ocr-region" && <><Field label="Language"><select value={overlay.language ?? "auto"} onChange={(e) => update({ language: e.target.value })}><option>auto</option><option>English</option><option>Chinese</option></select></Field><Field label="Engine"><select value={overlay.engine ?? "runtime"} onChange={(e) => update({ engine: e.target.value })}><option>runtime</option><option>tesseract</option><option>paddle</option></select></Field><Field label="Confidence"><input type="number" step=".05" value={overlay.confidenceThreshold} onChange={(e) => update({ confidenceThreshold: numberValue(e.target.value) })}/></Field></>}
    {overlay.type === "object-detection" && <><Field label="Model"><input value={overlay.model ?? "Default"} onChange={(e) => update({ model: e.target.value })}/></Field><Field label="Class"><input value={overlay.className ?? "Any"} onChange={(e) => update({ className: e.target.value })}/></Field><Field label="Confidence"><input type="number" step=".05" value={overlay.confidenceThreshold} onChange={(e) => update({ confidenceThreshold: numberValue(e.target.value) })}/></Field></>}
    {overlay.type === "template-region" && <><Field label="Template"><input value={overlay.templateName ?? ""} onChange={(e) => update({ templateName: e.target.value })}/></Field><Field label="Threshold"><input type="number" step=".05" value={overlay.threshold} onChange={(e) => update({ threshold: numberValue(e.target.value) })}/></Field><Field label="Scale"><input type="number" step=".1" value={overlay.scale} onChange={(e) => update({ scale: numberValue(e.target.value) })}/></Field><Field label="Rotation tolerance"><input type="number" value={overlay.rotationTolerance} onChange={(e) => update({ rotationTolerance: numberValue(e.target.value) })}/></Field></>}
    {overlay.type === "color-sample" && <><Field label="HEX"><input value={overlay.color ?? "#000000"} onChange={(e) => update({ color: e.target.value })}/></Field><Field label="Tolerance"><input type="number" value={overlay.tolerance} onChange={(e) => update({ tolerance: numberValue(e.target.value) })}/></Field></>}
  </div>;
};
