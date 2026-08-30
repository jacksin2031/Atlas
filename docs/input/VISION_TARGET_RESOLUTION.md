# Vision Target Resolution

Sprint 15.4 establishes one provider-neutral contract between Vision and Input.

## Reference contract

`PointReference`, `BoundsReference`, and `RegionReference` use contract
`atlas.automation.reference/v1`, screen coordinates, a source frame id, confidence,
and a semantic label. Vision Template, Detection, and OCR executors emit all three
representations. Input target ports accept the `target_reference` supertype and
resolve a Region or Bounds to its center without node-level coordinates.

On Windows the shared screen coordinate space uses physical pixels. The Input host
opts into Per-Monitor DPI Aware V2 before calling Win32 cursor APIs, preventing DPI
virtualization from shifting targets on scaled displays.

The Python contract is implemented in `src/atlas_automation/references.py`.
Provider output is normalized by the Workflow host before it reaches Input Runtime.

## Runtime path

```text
Workflow Vision Capture
  -> Tauri primary-screen capture (frame id + screen origin)
  -> Vision resolver/provider result
  -> RegionReference / BoundsReference / PointReference
  -> InputService
  -> WindowsInputProvider
```

The built-in deterministic Detection resolver locates a configured RGB target in a
real captured frame. Template matching uses a PNG data URL. OCR accepts provider
result boxes and normalizes them through the same contract, leaving OCR engine choice
behind the Vision provider boundary.

## Windows acceptance

Click `Load Visual Loop` (or import `sample-workflow-vision-closed-loop.json`) in Workflow Studio. The Atlas toolbar
contains a magenta `VISUAL TARGET` owned by the application. Run the workflow: it detects
the target, clicks the emitted RegionReference, captures again, and validates that the
button changed to the lime `TARGET CLICKED` state. No coordinate is stored in the
workflow.
