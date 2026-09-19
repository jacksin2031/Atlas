"""Real bundled-host component smoke; this is not installed-app or clean-VM QA."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/beta/evidence/bundled-runtime-smoke.json"


class Host:
    def __init__(self, runtime, cwd, environment, module):
        self.process = subprocess.Popen(
            [str(runtime / "python.exe"), "-I", "-B", "-u", "-m", module],
            cwd=cwd, env=environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
        )
        self.messages = queue.Queue()
        self.errors = []
        self.sequence = 0
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=self._errors, daemon=True).start()

    def _read(self):
        for line in self.process.stdout:
            self.messages.put(json.loads(line))
        self.messages.put(None)

    def _errors(self):
        self.errors.extend(self.process.stderr.readlines())

    def request(self, command, payload=None):
        self.sequence += 1
        identifier = str(self.sequence)
        self.process.stdin.write(json.dumps({"id": identifier, "command": command, "payload": payload or {}}) + "\n")
        self.process.stdin.flush()
        deadline = time.monotonic() + 30
        while True:
            message = self.messages.get(timeout=max(.001, deadline - time.monotonic()))
            if message is None:
                raise RuntimeError("Host exited: " + "".join(self.errors))
            if message.get("kind") == "bridge_request":
                raise AssertionError("Unexpected external bridge request")
            if message.get("kind") == "response" and message.get("id") == identifier:
                if not message.get("ok"):
                    raise AssertionError(message)
                return message["result"]

    def close(self, force=False):
        if force:
            self.process.kill()
        else:
            self.process.stdin.close()
        try:
            code = self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=10)
            raise AssertionError("Host did not close within 10 seconds")
        if not force:
            assert code == 0, (code, self.errors)
        return code


def definition():
    nodes = []
    for identifier, kind, inputs, outputs, config in [
        ("entry", "entry", [], ["output"], {}),
        ("constant", "constant", ["trigger"], ["value"], {"value": "Atlas smoke"}),
        ("output", "output", ["input"], ["value"], {}),
        ("exit", "exit", ["input"], [], {}),
    ]:
        ports_in = {f"{identifier}:in:{i}": name for i, name in enumerate(inputs)}
        ports_out = {f"{identifier}:out:{i}": name for i, name in enumerate(outputs)}
        nodes.append({"id": identifier, "type": kind, "config": config, "inputs": inputs,
                      "outputs": outputs, "ports_in": list(ports_in), "ports_out": list(ports_out),
                      "metadata": {"input_ports": ports_in, "output_ports": ports_out,
                                   "input_port_types": {p: "any" for p in ports_in},
                                   "output_port_types": {p: "any" for p in ports_out}}})
    return {"name": "bundled-smoke", "version": "1.0.0", "metadata": {"name": "bundled-smoke"},
            "nodes": nodes, "variables": [], "entry_nodes": ["entry"], "exit_nodes": ["exit"],
            "edges": [{"source": a, "target": b, "source_port": f"{a}:out:0", "target_port": f"{b}:in:0"}
                      for a, b in [("entry", "constant"), ("constant", "output"), ("output", "exit")]]}


def main():
    started = time.monotonic()
    report = {"status": "FAIL", "scope": "bundled-host component smoke, not installed app or clean VM",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "command": "python scripts/verify_bundled_runtime.py", "checks": [],
              "limitations": ["No installed UI, Tauri IPC, installer, clean VM, or live provider verification",
                              "Forced kill occurs while idle; no desktop input is armed or injected"]}
    hosts = []
    def check(name, operation):
        start = time.monotonic()
        result = operation()
        report["checks"].append({"name": name, "status": "PASS", "duration_ms": round((time.monotonic()-start)*1000, 2), "result": result})
        return result
    try:
        with tempfile.TemporaryDirectory(prefix="Atlas smoke 日本語 繁體中文 ") as temporary:
            base = Path(temporary)
            runtime = base / "runtime copy"
            source = ROOT / "apps/atlas-desktop/src-tauri/resources/runtime"
            shutil.copytree(source, runtime)
            report["runtime_lock"] = json.loads((runtime / "runtime-lock.json").read_text())
            report["python_sha256"] = hashlib.sha256((runtime / "python.exe").read_bytes()).hexdigest()
            report["runtime_tree_sha256"] = hashlib.sha256(b"".join(
                str(path.relative_to(runtime)).encode("utf-8") + b"\0" + hashlib.sha256(path.read_bytes()).digest()
                for path in sorted(runtime.rglob("*")) if path.is_file())).hexdigest()
            cwd = base / "outside repository"
            cwd.mkdir()
            project = base / "Knowledge 日本語 繁體中文"
            project.mkdir()
            environment = {key: value for key, value in os.environ.items()
                           if key.upper() in {"SYSTEMROOT", "WINDIR", "TEMP", "TMP", "COMSPEC"}}
            environment["PATH"] = ""
            report["isolation"] = {"path": "empty", "environment_keys": sorted(environment),
                                   "cwd_outside_repository": not cwd.is_relative_to(ROOT),
                                   "runtime_path_has_spaces_and_unicode": True}
            def launch(module):
                host = Host(runtime, cwd, environment, module)
                hosts.append(host)
                return host
            for cycle in range(3):
                ai = launch("atlas_ai.host")
                def health():
                    result = ai.request("ai_health")
                    assert result["runtimeHealth"] == "available", result
                    return result
                check(f"ai_health_cycle_{cycle+1}", health)
                check(f"ai_eof_close_cycle_{cycle+1}", ai.close)
            workflow = launch("atlas_workflow.host")
            def unarmed():
                state = workflow.request("workflow_input_status")
                assert state["armed"] is False, state
                return {"armed": state["armed"]}
            check("workflow_starts_unarmed", unarmed)
            def execute():
                execution = workflow.request("workflow_start", {"definition": definition()})["executionId"]
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    result = workflow.request("workflow_get_result", {"executionId": execution})["result"]
                    if result is not None:
                        assert result["success"] is True and result["output"] == {"value": "Atlas smoke"}, result
                        return {"success": True, "output": result["output"]}
                    time.sleep(.02)
                raise AssertionError("Workflow completion timeout")
            check("safe_constant_workflow", execute)
            scope = {"projectId": "bundled-smoke", "projectPath": str(project)}
            def knowledge(command, **payload):
                return workflow.request("knowledge_" + command, {**scope, **payload})
            entry = check("knowledge_create", lambda: knowledge("create", entry={"title": "Smoke", "content": "originalmarker"}))
            def search(marker, count):
                result = knowledge("search", query=marker)
                assert result["result_count"] == count, result
                if count:
                    assert result["results"][0]["entry"]["id"] == entry["id"], result
                return {"result_count": count}
            check("knowledge_search_created", lambda: search("originalmarker", 1))
            check("knowledge_edit", lambda: knowledge("update", entryId=entry["id"], changes={"content": "updatedmarker"}))
            check("workflow_eof_close_1", workflow.close)
            workflow = launch("atlas_workflow.host")
            check("knowledge_edit_survives_restart", lambda: search("updatedmarker", 1))
            check("knowledge_old_content_absent", lambda: search("originalmarker", 0))
            check("workflow_forced_kill", lambda: workflow.close(force=True))
            workflow = launch("atlas_workflow.host")
            check("knowledge_survives_forced_kill", lambda: search("updatedmarker", 1))
            check("input_unarmed_after_forced_restart", unarmed)
            check("knowledge_delete", lambda: knowledge("delete", entryId=entry["id"]))
            check("workflow_eof_close_2", workflow.close)
            workflow = launch("atlas_workflow.host")
            check("knowledge_deleted_after_restart", lambda: search("updatedmarker", 0))
            check("workflow_eof_close_3", workflow.close)
            report["status"] = "PASS"
    except Exception as error:
        report["error"] = f"{type(error).__name__}: {error}"
    finally:
        for host in hosts:
            if host.process.poll() is None:
                host.close(force=True)
        report["duration_ms"] = round((time.monotonic()-started)*1000, 2)
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": len(report["checks"]), "error": report.get("error"), "duration_ms": report["duration_ms"]}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
