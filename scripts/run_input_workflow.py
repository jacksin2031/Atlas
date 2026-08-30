"""Run an Atlas Studio workflow through the real Workflow/Input Runtime chain."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from atlas_input import InputService, TestInputProvider  # noqa: E402
from atlas_workflow.host import DesktopWorkflowHost  # noqa: E402


def canonical(definition: dict[str, Any]) -> dict[str, Any]:
    nodes = []
    for node in definition.get("nodes", []):
        inputs = node.get("inputs", [])
        outputs = node.get("outputs", [])
        nodes.append({
            "id": node["id"], "type": node["type"], "label": node.get("label", node["type"]),
            "config": node.get("parameters", {}),
            "inputs": [port["name"] for port in inputs], "outputs": [port["name"] for port in outputs],
            "ports_in": [port["id"] for port in inputs], "ports_out": [port["id"] for port in outputs],
            "metadata": {
                "category": node.get("category", "core"), "capabilities": node.get("capabilities", []),
                "input_ports": {port["id"]: port["name"] for port in inputs},
                "output_ports": {port["id"]: port["name"] for port in outputs},
                "input_port_types": {port["id"]: port["type"] for port in inputs},
                "output_port_types": {port["id"]: port["type"] for port in outputs},
            },
        })
    return {
        "name": definition.get("id", definition.get("name", "input-workflow")),
        "version": definition.get("version", "1.0.0"),
        "metadata": {"name": definition.get("id", definition.get("name", "input-workflow"))},
        "nodes": nodes,
        "edges": [{
            "id": edge.get("id", ""), "source": edge["source"], "target": edge["target"],
            "source_port": edge.get("sourcePort", ""), "target_port": edge.get("targetPort", ""),
            "metadata": {"edge_type": edge.get("edgeType", "data")},
        } for edge in definition.get("edges", [])],
        "variables": definition.get("variables", []),
        "entry_nodes": [node["id"] for node in nodes if node["type"] == "entry"],
        "exit_nodes": [node["id"] for node in nodes if node["type"] == "exit"],
        "capabilities": [{"name": "input.control", "minimum_version": "1.0.0"}],
        "plugins": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--execute", action="store_true", help="use the platform InputProvider")
    parser.add_argument("--confirm", action="store_true", help="required with --execute")
    args = parser.parse_args(argv)
    if args.execute and not args.confirm:
        parser.error("real input requires both --execute and --confirm")
    definition = canonical(json.loads(args.workflow.read_text(encoding="utf-8")))
    provider = None if args.execute else TestInputProvider()
    host = DesktopWorkflowHost(input_service=None if provider is None else InputService(provider))
    host.write = lambda value: None  # type: ignore[method-assign]
    started = host.start({"definition": definition})
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        result = host.result(started["executionId"])["result"]
        if result is not None:
            output = {"mode": "execute" if args.execute else "test", "result": result}
            if provider is not None:
                output["requests"] = [request.__class__.__name__ for request in provider.requests]
            print(json.dumps(output, ensure_ascii=False))
            return 0 if result["success"] else 1
        time.sleep(0.02)
    raise TimeoutError("workflow did not finish within 30 seconds")


if __name__ == "__main__":
    raise SystemExit(main())
