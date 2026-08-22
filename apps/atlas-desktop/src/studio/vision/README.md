# Atlas Vision Studio

Vision Studio is Atlas Desktop's standalone image and screen-analysis workspace. It is a Layer 8 editor and is intentionally separate from Workflow Studio.

## Architecture

Components read narrow Zustand selectors and invoke UI services. Capture crosses `src/ipc/bridge.ts`; no React component imports the concrete Vision Runtime. FlexLayout stores only panel IDs and geometry.

The production runtime provider remains optional. Demo data is isolated in `services/demo-provider.ts` and is enabled only when both development mode and `VITE_ATLAS_VISION_DEMO=true` are present.

## Implemented surfaces

- Toolbar and keyboard commands
- Toolbox with navigation, selection, draw, and inspection tools
- Image loading/drop, checkerboard canvas, pan, zoom, grid, rulers, coordinates, and overlays
- Selection, common overlay edits, locking, hiding, duplication, deletion, and layer ordering
- Properties for common, OCR, detection, template, and color attributes
- Searchable/sortable/exportable OCR, detection, color, and template panels
- Timeline controls, scrubber, thumbnails, loop/speed, markers, and frame edits

## Known limitations

- The Tauri backend currently has no concrete `vision_capture_frame` command, so capture returns no frame until a runtime adapter is connected.
- OCR, detection, template matching, and live pixel sampling are UI/service surfaces; algorithms remain runtime responsibilities.
- Canvas resize handles are represented visually; pointer-driven resize/rotate interactions are not yet implemented.
