"""CLI client for the Atlas Input Service.

Dry-run is the default. Real desktop input requires both ``--execute`` and
``--confirm`` so tests and accidental invocations cannot control the desktop.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from atlas_input import InputService, TestInputProvider, WindowsInputProvider  # noqa: E402


ACTION_NAMES = {
    "move": "mouse_move",
    "click": "mouse_click",
    "double_click": "mouse_double_click",
    "drag": "mouse_drag",
    "scroll": "mouse_scroll",
    "press": "keyboard_press",
    "hotkey": "keyboard_hotkey",
    "type": "keyboard_type",
    "key_down": "key_down",
    "key_up": "key_up",
    "wait": "input_wait",
    "release_all": "input_release_all",
}


def _load_actions(args: argparse.Namespace) -> list[dict[str, Any]]:
    raw = Path(args.script).read_text(encoding="utf-8") if args.script else args.actions
    parsed = json.loads(raw)
    if not isinstance(parsed, list) or not all(isinstance(item, dict) for item in parsed):
        raise ValueError("script must contain a JSON array of action objects")
    if len(parsed) > 100:
        raise ValueError("script exceeds the 100-action limit")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--script", help="JSON file containing an action array")
    source.add_argument("--actions", help="inline JSON action array")
    parser.add_argument("--execute", action="store_true", help="enable real Windows input")
    parser.add_argument("--confirm", action="store_true", help="required confirmation for real input")
    args = parser.parse_args(argv)
    try:
        if args.execute and not args.confirm:
            raise ValueError("real input requires both --execute and --confirm")
        provider = WindowsInputProvider() if args.execute else TestInputProvider()
        service = InputService(provider)
        results = []
        try:
            for item in _load_actions(args):
                raw_action = str(item.get("action", ""))
                action = ACTION_NAMES.get(raw_action, raw_action)
                if action not in ACTION_NAMES.values():
                    raise ValueError(f"unsupported action: {raw_action or '<missing>'}")
                payload = {key: value for key, value in item.items() if key != "action"}
                results.append(service.execute(action, payload))
        finally:
            service.execute("input_release_all", {})
        print(json.dumps({"mode": "execute" if args.execute else "dry-run", "results": results}, ensure_ascii=False))
        return 0
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"atlas-input-control: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
