# Atlas Input Runtime

The Input domain follows this execution boundary:

```text
Workflow node -> Input node executor -> InputService -> InputProvider -> platform adapter
```

Workflow nodes only create typed requests. They do not import Win32, X11,
Wayland, Quartz, or automation libraries. `WindowsInputProvider` is the first
real adapter; `TestInputProvider` records requests for deterministic tests.

The initial Input palette contains Mouse Move, Mouse Click, Mouse Double Click,
Mouse Drag, Mouse Scroll, Keyboard Press, Keyboard Hotkey, Keyboard Type, Key
Down, Key Up, Input Wait, and Input Release All. Input nodes declare the
`input.control` capability.

Mouse Move and Mouse Click accept either explicit `x`/`y` parameters or a
`target` object. A target may be a coordinate, region, nested `region`/`bounds`,
or object with a `center`; regions resolve to their center automatically.

Input safety rules:

- Workflow cancellation immediately calls Input Release All.
- Normal and failed workflow completion also calls Input Release All.
- Input Wait checks workflow cancellation while blocked.
- The CLI uses TestInputProvider unless both `--execute` and `--confirm` are set.
- Test suites never send operating-system input.

Acceptance samples are `sample-workflow-input.json` and
`sample-workflow-vision-input.json`. The Vision sample uses a configured target
region so it can run without an AI/detection provider; a future detection node
can replace that Constant and feed the same target port directly.

On 2026-08-27 the real Windows acceptance completed through Workflow Runtime,
InputService, and WindowsInputProvider as execution
`execution-ca35713f-ac7e-495c-bef6-52e222975313`. Mouse Move, Mouse Click,
Delay, Keyboard Type, Output, Exit, and automatic release-all all completed.
