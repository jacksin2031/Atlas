"""Persistent JSON-lines Desktop host for the Atlas Workflow Runtime."""
from __future__ import annotations

import json
import re
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from atlas_automation import reference_bundle
from atlas_input import InputSafetyPolicy, InputService, default_input_service
from atlas_knowledge import KnowledgeRuntime, ProjectScope
from atlas_workflow.common import WorkflowEvent, PluginError
from atlas_workflow.node_registry import NodeDefinition
from atlas_workflow.runtime import WorkflowRuntime


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _error_message(error: BaseException) -> str:
    return str(error) or error.__class__.__name__


def _sanitize(value: Any) -> Any:
    secret_markers = ("api_key", "apikey", "authorization", "credential", "secret", "token")
    if isinstance(value, dict):
        return {
            str(key): ("***" if any(marker in str(key).lower() for marker in secret_markers) else _sanitize(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


class BridgeClient:
    """Requests an existing Tauri-owned runtime boundary from the Workflow host."""

    def __init__(self, write: Any) -> None:
        self._write = write
        self._condition = threading.Condition()
        self._responses: dict[str, dict[str, Any]] = {}

    def request(self, bridge: str, command: str, payload: dict[str, Any], timeout: float = 180.0) -> Any:
        request_id = f"workflow-bridge-{uuid.uuid4()}"
        self._write({
            "kind": "bridge_request", "id": request_id, "bridge": bridge,
            "command": command, "payload": payload,
        })
        deadline = time.monotonic() + timeout
        with self._condition:
            while request_id not in self._responses:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RuntimeError(f"{bridge} bridge request timed out")
                self._condition.wait(timeout=min(remaining, 0.25))
            response = self._responses.pop(request_id)
        if not response.get("ok"):
            raise RuntimeError(str(response.get("error") or f"{bridge} bridge request failed"))
        return response.get("result")

    def resolve(self, value: dict[str, Any]) -> None:
        with self._condition:
            self._responses[str(value.get("id", ""))] = value
            self._condition.notify_all()


class DesktopWorkflowHost:
    def __init__(self, input_service: InputService | None = None) -> None:
        self._write_lock = threading.Lock()
        self._session_lock = threading.RLock()
        self._sessions: dict[str, dict[str, Any]] = {}
        self.runtime = WorkflowRuntime()
        self.runtime.event_bus.subscribe_all(self._on_runtime_event)
        self.knowledge_runtime = KnowledgeRuntime()
        self.knowledge_runtime.add_event_listener(self._on_knowledge_event)
        self.bridge = BridgeClient(self.write)
        self.input_service = input_service or default_input_service()
        self.input_service.add_emergency_stop_listener(self._cancel_active_for_emergency)
        self._dynamic_plugins: dict[str, set[str]] = {}
        self._marketplace_nodes: dict[str, dict[str, Any]] = {}
        self._marketplace_revision = -1
        self._register_nodes()

    def write(self, value: dict[str, Any]) -> None:
        with self._write_lock:
            sys.stdout.write(json.dumps(_sanitize(value), separators=(",", ":"), default=str) + "\n")
            sys.stdout.flush()

    def respond(self, command_id: str, result: Any = None, error: str | None = None) -> None:
        self.write({"kind": "response", "id": command_id, "ok": error is None, "result": result, "error": error})

    def emit(self, event: dict[str, Any]) -> None:
        self.write({"kind": "event", "event": "workflow://runtime-event", "payload": event})

    @staticmethod
    def _first(inputs: dict[str, Any], default: Any = None) -> Any:
        return next(iter(inputs.values()), default)

    def _register(self, node_type: str, handler: Any, capabilities: list[str] | None = None) -> None:
        self.runtime.node_registry.register(NodeDefinition(
            node_id=f"atlas.builtin.{node_type}", node_type=node_type,
            label=node_type.replace("_", " ").title(), capabilities=capabilities or [],
        ))
        self.runtime.plugin_bridge.register_handler(node_type, handler)

    def _register_nodes(self) -> None:
        passthrough = lambda node_id, configuration, inputs, metadata: {"value": self._first(inputs, configuration.get("value"))}
        self._register("entry", lambda node_id, configuration, inputs, metadata: {"output": self._first(inputs, configuration.get("value"))})
        self._register("exit", passthrough)
        self._register("constant", lambda node_id, configuration, inputs, metadata: {"value": configuration.get("value")})
        self._register("transform", self._transform)
        self._register("map", self._transform)
        self._register("condition", self._condition)
        self._register("delay", self._delay)
        self._register("output", passthrough)
        self._register("set_variable", passthrough)
        self._register("get_variable", passthrough)
        self._register("ai_inference", self._ai_inference, ["ai"])
        self._register("vision_current_frame", self._vision_current_frame, ["vision"])
        self._register("vision_template_match", self._vision_reference_handler("template"), ["vision"])
        self._register("vision_detect", self._vision_reference_handler("detection"), ["vision"])
        self._register("vision_ocr", self._vision_reference_handler("ocr"), ["vision"])
        self._register("vision_validate", self._vision_validate, ["vision"])
        self._register("ai_operation", self._ai_inference, ["ai"])
        self._register("vision_operation", self._vision_current_frame, ["vision"])
        self._register("knowledge_operation", self._knowledge_operation, ["knowledge"])
        self._register("knowledge_search", self._knowledge_search, ["knowledge"])
        self._register("knowledge_write", self._knowledge_write, ["knowledge"])
        self._register("knowledge_validate", self._knowledge_validate, ["knowledge"])
        self._register("plugin_test", self._plugin_test, ["plugin"])
        for node_type in (
            "mouse_move", "mouse_click", "mouse_double_click", "mouse_drag", "mouse_scroll",
            "keyboard_press", "keyboard_hotkey", "keyboard_type", "key_down", "key_up",
            "input_wait", "input_release_all",
        ):
            self._register(node_type, self._input_handler(node_type), ["input.control"])
        self._register("noop", passthrough)

    def register_plugin(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Register a constrained data-driven plugin without loading arbitrary code."""
        manifest = payload.get("plugin") or payload
        if not isinstance(manifest, dict):
            raise RuntimeError("Plugin manifest must be an object")
        plugin_id = str(manifest.get("id", "")).strip()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,79}", plugin_id):
            raise RuntimeError("Plugin id must contain 3-80 safe identifier characters")
        raw_nodes = manifest.get("nodes")
        if not isinstance(raw_nodes, list) or not raw_nodes:
            raise RuntimeError("Plugin manifest must declare at least one node")

        for old_type in self._dynamic_plugins.pop(plugin_id, set()):
            self.runtime.plugin_bridge.unregister_handler(old_type)
            self.runtime.node_registry.unregister(f"{plugin_id}.{old_type}")

        registrations: list[dict[str, Any]] = []
        registered_types: set[str] = set()
        for raw in raw_nodes:
            if not isinstance(raw, dict):
                raise RuntimeError("Plugin node declaration must be an object")
            node_type = str(raw.get("typeName", "")).strip()
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,79}", node_type):
                raise RuntimeError("Plugin node type must contain 3-80 safe identifier characters")
            if self.runtime.plugin_bridge.has_handler(node_type):
                raise RuntimeError(f"Plugin node type is already registered: {node_type}")
            operation = str(raw.get("operation", "prefix")).lower()
            if operation not in {"prefix", "uppercase", "lowercase"}:
                raise RuntimeError(f"Unsupported safe plugin operation: {operation}")
            default_prefix = str(raw.get("prefix", "plugin:"))

            def handler(
                node_id: str,
                configuration: dict[str, Any],
                inputs: dict[str, Any],
                metadata: dict[str, Any],
                *,
                selected_operation: str = operation,
                selected_prefix: str = default_prefix,
            ) -> dict[str, Any]:
                del node_id, metadata
                value = self._first(inputs, configuration.get("value", ""))
                if selected_operation == "uppercase":
                    result = str(value).upper()
                elif selected_operation == "lowercase":
                    result = str(value).lower()
                else:
                    result = str(configuration.get("prefix", selected_prefix)) + str(value)
                return {"value": result}

            definition_id = f"{plugin_id}.{node_type}"
            self.runtime.node_registry.register(NodeDefinition(
                node_id=definition_id,
                node_type=node_type,
                label=str(raw.get("label") or node_type.replace("_", " ").title()),
                capabilities=["plugin.dynamic"],
            ))
            self.runtime.plugin_bridge.register_handler(node_type, handler)
            registered_types.add(node_type)
            registrations.append({
                "nodeId": definition_id,
                "typeName": node_type,
                "category": "plugin",
                "label": str(raw.get("label") or node_type.replace("_", " ").title()),
                "description": str(raw.get("description") or "Dynamically registered safe plugin node"),
                "inputs": [{"id": "in_0", "name": "input", "type": "any", "multiple": False}],
                "outputs": [{"id": "out_0", "name": "value", "type": "string", "multiple": False}],
                "parameters": {"prefix": default_prefix} if operation == "prefix" else {},
                "version": str(manifest.get("version", "1.0.0")),
                "capabilities": ["plugin.dynamic"],
                "pluginId": plugin_id,
            })
        self._dynamic_plugins[plugin_id] = registered_types
        return {"pluginId": plugin_id, "registrations": registrations}

    def sync_marketplace(self, payload: dict[str, Any]) -> dict[str, Any]:
        revision = int(payload.get("revision", -1))
        if revision <= self._marketplace_revision:
            return {"revision": self._marketplace_revision}
        registrations = payload.get("registrations", [])
        incoming = {}
        definitions = {}
        owned_ids = {old["nodeId"] for old in self._marketplace_nodes.values()}
        incoming_ids = set()
        for registration in registrations:
            node_type = registration["typeName"]
            plugin_id = registration["pluginId"]
            if not node_type.startswith(plugin_id + ".") or node_type in incoming:
                raise RuntimeError("Invalid Marketplace node ownership")
            if self.runtime.plugin_bridge.has_handler(node_type) and node_type not in self._marketplace_nodes:
                raise RuntimeError("Marketplace node type conflicts with existing registration")
            node_id = registration["nodeId"]
            if not node_id.startswith(plugin_id + ".") or node_id in incoming_ids or (self.runtime.node_registry.lookup(node_id) and node_id not in owned_ids):
                raise RuntimeError("Marketplace node identity conflicts with existing registration")
            capabilities = registration["capabilities"]
            if not isinstance(capabilities, list) or not all(isinstance(cap, str) for cap in capabilities):
                raise RuntimeError("Invalid Marketplace capabilities")
            definitions[node_type] = NodeDefinition(node_id=node_id, node_type=node_type,
                label=registration["label"], capabilities=capabilities,
                version=registration.get("version", "1.0.0"))
            incoming_ids.add(node_id)
            incoming[node_type] = registration
        for node_type, old in self._marketplace_nodes.items():
            self.runtime.plugin_bridge.unregister_handler(node_type)
            self.runtime.node_registry.unregister(old["nodeId"])
        self._marketplace_nodes = incoming
        for node_type, registration in incoming.items():
            self.runtime.node_registry.register(definitions[node_type])
            self.runtime.plugin_bridge.register_handler(node_type, self._marketplace_handler(registration["pluginId"], node_type))
        self._marketplace_revision = revision
        return {"revision": revision, "registrations": registrations}

    def _marketplace_handler(self, plugin_id: str, node_type: str) -> Any:
        def handler(node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
            try:
                return self.bridge.request("plugin", "execute", {
                    "pluginId": plugin_id, "nodeType": node_type,
                    "configuration": configuration, "inputs": inputs,
                    "requestId": f"plugin-node-{node_id}-{uuid.uuid4().hex}",
                }, timeout=30)
            except RuntimeError as error:
                try:
                    detail = json.loads(str(error))
                except ValueError:
                    detail = {"code": "PLUGIN_UNAVAILABLE", "message": "Plugin Runtime bridge unavailable"}
                raise PluginError(detail.get("message", "Plugin execution failed"), plugin_name=plugin_id, details=detail) from error
        return handler

    def _input_handler(self, action: str) -> Any:
        def handler(node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any], context: Any = None) -> dict[str, Any]:
            cancelled = (lambda: bool(context and context.control and context.control.is_cancelled))
            return {"result": self.input_service.execute(action, {**configuration, **inputs}, cancelled)}
        return handler

    def _transform(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        value = self._first(inputs, configuration.get("value"))
        operation = str(configuration.get("operation", "pass")).lower()
        if operation == "uppercase" and isinstance(value, str):
            value = value.upper()
        elif operation == "lowercase" and isinstance(value, str):
            value = value.lower()
        return {"value": value}

    def _condition(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        value = self._first(inputs, configuration.get("value", False))
        branch = "true" if bool(value) else "false"
        return {branch: value}

    def _delay(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any], context: Any = None) -> dict[str, Any]:
        duration = max(0.0, min(float(configuration.get("seconds", 0.1)), 300.0))
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            if context and context.control and context.control.is_cancelled:
                raise RuntimeError("Execution cancelled")
            time.sleep(min(0.02, deadline - time.monotonic()))
        return {"value": self._first(inputs, configuration.get("value"))}

    def _ai_inference(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any], context: Any = None) -> dict[str, Any]:
        prompt_value = inputs.get("prompt")
        prompt = str(configuration.get("prompt", "") if prompt_value is None else prompt_value)
        provider_id = str(configuration.get("providerId", configuration.get("provider_id", "")))
        model_id = str(configuration.get("modelId", configuration.get("model_id", "")))
        if not provider_id or not model_id:
            raise RuntimeError("AI node requires providerId and modelId")
        request_id = f"workflow-ai-{context.instance_id if context else uuid.uuid4()}-{node_id}"
        context_references = inputs.get("context", [])
        knowledge_context: list[dict[str, Any]] = []
        if isinstance(context_references, list) and context_references:
            scope = self._workflow_project_scope(context)
            knowledge_context = self.knowledge_runtime.assemble_ai_context(scope, context_references)
        response = self.bridge.request("ai", "ai_infer", {"request": {
            "requestId": request_id, "providerId": provider_id, "modelId": model_id,
            "messages": [{"id": f"msg-{node_id}", "role": "user", "content": prompt}],
            "parameters": {"stream": True}, "attachments": inputs.get("attachments", []),
            "contextReferences": context_references, "knowledgeContext": knowledge_context, "tools": [],
        }})
        return {"response": response, "text": (response or {}).get("content", "")}

    def _vision_current_frame(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        frame = self.bridge.request("vision", "vision_capture_frame", {})
        return {"frame": frame}

    @staticmethod
    def _frame_input(inputs: dict[str, Any], configuration: dict[str, Any]) -> dict[str, Any]:
        frame = inputs.get("frame") or configuration.get("frame")
        if not isinstance(frame, dict):
            frame = next((value for value in inputs.values() if isinstance(value, dict) and value.get("url")), None)
        if not isinstance(frame, dict) or not frame.get("url"):
            raise RuntimeError("Vision node requires a captured frame reference")
        return frame

    def _resolve_vision(self, operation: str, frame: dict[str, Any], configuration: dict[str, Any]) -> dict[str, Any]:
        configured = configuration.get("results") or configuration.get("matches")
        if operation == "ocr" and isinstance(configured, list):
            return {"operation": operation, "matched": bool(configured), "matches": configured}
        result = self.bridge.request("vision", "vision_resolve_target", {
            "operation": operation,
            "frame": frame,
            "configuration": configuration,
        })
        if not isinstance(result, dict):
            raise RuntimeError(f"Vision {operation} provider returned an invalid result")
        return result

    def _vision_reference_handler(self, operation: str) -> Any:
        def handler(node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
            frame = self._frame_input(inputs, configuration)
            raw = self._resolve_vision(operation, frame, configuration)
            matches = raw.get("matches")
            if not isinstance(matches, list) or not matches or not isinstance(matches[0], dict):
                raise RuntimeError(f"Vision {operation} did not resolve a target")
            references = reference_bundle(matches[0], frame, node_id)
            text = str(matches[0].get("text", matches[0].get("label", ""))) if operation == "ocr" else ""
            return {**references, "text": text, "matches": matches, "providerResult": raw, "frame": frame}
        return handler

    def _vision_validate(self, node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        frame = self._frame_input(inputs, configuration)
        operation = str(configuration.get("operation", "detection"))
        raw = self._resolve_vision(operation, frame, configuration)
        matched = bool(raw.get("matched") or raw.get("matches"))
        expected = str(configuration.get("expect", "present")).lower()
        valid = matched if expected == "present" else not matched
        return {"valid": valid, "result": {"valid": valid, "expected": expected, "operation": operation, "providerResult": raw}}

    def _workflow_project_scope(self, context: Any) -> ProjectScope:
        if context is None:
            raise RuntimeError("Knowledge workflow operation requires execution context")
        with self._session_lock:
            session = self._sessions.get(str(context.instance_id))
            project = dict(session.get("projectContext") or {}) if session else {}
        return self._project_scope(project)

    @staticmethod
    def _project_scope(value: dict[str, Any]) -> ProjectScope:
        return ProjectScope(
            project_id=str(value.get("projectId", value.get("project_id", ""))),
            project_path=str(value.get("projectPath", value.get("path", value.get("project_path", "")))),
        )

    @staticmethod
    def _knowledge_value(inputs: dict[str, Any], configuration: dict[str, Any], key: str, default: Any = None) -> Any:
        value = inputs.get(key)
        if value is not None:
            return value
        return configuration.get(key, default)

    def _knowledge_search(
        self,
        node_id: str,
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        metadata: dict[str, Any],
        context: Any = None,
    ) -> dict[str, Any]:
        del metadata
        scope = self._workflow_project_scope(context)
        query = str(self._knowledge_value(inputs, configuration, "query", ""))
        response = self.knowledge_runtime.search(
            scope,
            query,
            entry_types=list(configuration.get("types") or []),
            tags=list(configuration.get("tags") or []),
            limit=int(configuration.get("limit", 25)),
            request_id=f"workflow-{context.instance_id}-{node_id}",
        )
        references = [item["reference"] for item in response["results"]]
        return {"results": response["results"], "references": references, "context": references, "retrieval": response}

    def _knowledge_write(
        self,
        node_id: str,
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        metadata: dict[str, Any],
        context: Any = None,
    ) -> dict[str, Any]:
        del metadata
        scope = self._workflow_project_scope(context)
        content_value = self._knowledge_value(inputs, configuration, "content")
        if content_value is None:
            content_value = self._first(inputs, "")
        if isinstance(content_value, (dict, list)):
            content = json.dumps(content_value, ensure_ascii=False, default=str)
        else:
            content = str(content_value)
        source = dict(configuration.get("source") or {"type": "workflow", "workflow_id": context.workflow_id, "node_id": node_id})
        provider_result = inputs.get("providerResult")
        if isinstance(provider_result, dict) and provider_result.get("operation") == "ocr":
            frame = inputs.get("frame")
            source = {"type": "vision_ocr", "workflow_id": context.workflow_id, "node_id": node_id}
            if isinstance(frame, dict) and frame.get("frameId"):
                source["frame_reference"] = str(frame["frameId"])
        entry = self.knowledge_runtime.create(scope, {
            "type": configuration.get("type", "observation" if source.get("type") == "vision_ocr" else "fact"),
            "title": self._knowledge_value(inputs, configuration, "title", "Workflow knowledge"),
            "content": content,
            "tags": configuration.get("tags", []),
            "metadata": {**dict(configuration.get("metadata") or {}), "workflow_id": context.workflow_id, "workflow_node_id": node_id},
            "source": source,
            "provenance": dict(configuration.get("provenance") or {}),
        }, correlation_id=f"workflow-{context.instance_id}-{node_id}")
        return {"entry": entry.to_dict(), "reference": entry.reference.to_dict(), "persistentId": entry.id}

    def _knowledge_validate(
        self,
        node_id: str,
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        metadata: dict[str, Any],
        context: Any = None,
    ) -> dict[str, Any]:
        del node_id, metadata, context
        value = self._knowledge_value(inputs, configuration, "results", self._first(inputs, []))
        expected = str(self._knowledge_value(inputs, configuration, "expected", "")).strip()
        if not expected:
            raise RuntimeError("Knowledge validation requires an expected value")
        serialized = json.dumps(value, ensure_ascii=False, default=str)
        valid = expected.casefold() in serialized.casefold()
        result = {"valid": valid, "expected": expected, "results": value}
        if not valid and bool(configuration.get("failOnInvalid", True)):
            raise RuntimeError(f"Knowledge validation failed: expected {expected!r}")
        return {"valid": valid, "result": result}

    def _knowledge_operation(
        self,
        node_id: str,
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        metadata: dict[str, Any],
        context: Any = None,
    ) -> dict[str, Any]:
        operation = str(configuration.get("operation", "search")).lower()
        if operation in {"search", "query"}:
            return self._knowledge_search(node_id, configuration, inputs, metadata, context)
        if operation in {"create", "write"}:
            return self._knowledge_write(node_id, configuration, inputs, metadata, context)
        scope = self._workflow_project_scope(context)
        entry_id = str(self._knowledge_value(inputs, configuration, "entryId", self._knowledge_value(inputs, configuration, "entry_id", "")))
        if operation == "get":
            entry = self.knowledge_runtime.get(scope, entry_id)
            return {"entry": entry.to_dict(), "reference": entry.reference.to_dict()}
        if operation == "update":
            changes = dict(configuration.get("changes") or {})
            if "content" in inputs:
                changes["content"] = inputs["content"]
            entry = self.knowledge_runtime.update(scope, entry_id, changes, correlation_id=f"workflow-{context.instance_id}-{node_id}")
            return {"entry": entry.to_dict(), "reference": entry.reference.to_dict()}
        if operation == "delete":
            return self.knowledge_runtime.delete(scope, entry_id, correlation_id=f"workflow-{context.instance_id}-{node_id}")
        raise RuntimeError(f"Unsupported Knowledge operation: {operation}")

    def knowledge_command(self, command: str, payload: dict[str, Any]) -> Any:
        scope = self._project_scope(payload)
        correlation_id = str(payload.get("requestId", "")) or None
        if command == "knowledge_status":
            return self.knowledge_runtime.status(scope)
        if command == "knowledge_list":
            return self.knowledge_runtime.list_entries(scope, entry_type=payload.get("type"), tags=list(payload.get("tags") or []), offset=int(payload.get("offset", 0)), limit=int(payload.get("limit", 100)))
        if command == "knowledge_get":
            return self.knowledge_runtime.get(scope, str(payload.get("entryId", ""))).to_dict()
        if command == "knowledge_create":
            return self.knowledge_runtime.create(scope, dict(payload.get("entry") or {}), correlation_id=correlation_id).to_dict()
        if command == "knowledge_update":
            return self.knowledge_runtime.update(scope, str(payload.get("entryId", "")), dict(payload.get("changes") or {}), correlation_id=correlation_id).to_dict()
        if command == "knowledge_delete":
            return self.knowledge_runtime.delete(scope, str(payload.get("entryId", "")), correlation_id=correlation_id)
        if command == "knowledge_search":
            return self.knowledge_runtime.search(scope, str(payload.get("query", "")), entry_types=list(payload.get("types") or []), tags=list(payload.get("tags") or []), limit=int(payload.get("limit", 25)), request_id=correlation_id)
        if command == "knowledge_import":
            return self.knowledge_runtime.import_content(scope, filename=str(payload.get("filename", "")), content=str(payload.get("content", "")), format_name=str(payload.get("format", "")), correlation_id=correlation_id)
        if command == "knowledge_export":
            return self.knowledge_runtime.export(scope, str(payload.get("format", "json")))
        if command == "knowledge_events":
            return self.knowledge_runtime.events(scope, int(payload.get("limit", 100)))
        if command == "knowledge_context":
            return self.knowledge_runtime.assemble_ai_context(scope, list(payload.get("references") or []))
        raise RuntimeError(f"Unknown Knowledge host command: {command}")

    @staticmethod
    def _plugin_test(node_id: str, configuration: dict[str, Any], inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        return {"value": configuration.get("prefix", "plugin:") + str(next(iter(inputs.values()), configuration.get("value", "ok")))}

    def _on_runtime_event(self, event: WorkflowEvent) -> None:
        raw = event.to_dict()
        execution_id = event.instance_id
        payload = {
            "eventId": raw["event_id"], "eventType": raw["event_type"],
            "timestamp": raw["timestamp"], "workflowId": raw["workflow_id"],
            "executionId": execution_id, "nodeId": raw["node_id"] or None,
            "correlationId": raw["correlation_id"] or execution_id,
            "data": raw["data"],
        }
        with self._session_lock:
            session = self._sessions.get(execution_id)
            if session:
                session["history"].append(payload)
                session["history"] = session["history"][-500:]
                event_type = event.event_type.value
                state_map = {
                    "WorkflowStarted": "running", "WorkflowPaused": "paused",
                    "WorkflowResumed": "running", "WorkflowCompleted": "completed",
                    "WorkflowFailed": "failed", "WorkflowCancelled": "cancelled",
                }
                if event_type in state_map:
                    session["status"] = state_map[event_type]
                node_state_map = {
                    "NodeStarted": "running", "NodeCompleted": "completed",
                    "NodeFailed": "failed", "NodeSkipped": "skipped",
                }
                if event.node_id and event_type in node_state_map:
                    session["nodeStates"][event.node_id] = node_state_map[event_type]
                    session["currentNodeId"] = event.node_id
                if event_type == "NodeCompleted" and event.node_id:
                    session["nodeResults"][event.node_id] = raw["data"]
                if event_type == "VariableChanged":
                    session["variables"][str(raw["data"].get("name", ""))] = raw["data"].get("value")
        self.emit(payload)

    def _on_knowledge_event(self, event: Any) -> None:
        self.write({"kind": "event", "event": "knowledge://runtime-event", "payload": event.to_dict()})

    def _cancel_active_for_emergency(self) -> None:
        with self._session_lock:
            active = [
                key for key, session in self._sessions.items()
                if session["status"] in {"scheduled", "running", "paused"}
            ]
        for execution_id in active:
            self.runtime.cancel(execution_id)

    def _state(self, execution_id: str) -> dict[str, Any]:
        with self._session_lock:
            session = self._sessions.get(execution_id)
            if not session:
                raise RuntimeError(f"Execution not found: {execution_id}")
            started = session["startedAt"]
            finished_epoch = session.get("completedEpoch", time.time())
            duration_ms = max(0, int((finished_epoch - session["startedEpoch"]) * 1000))
            completed_nodes = sum(v == "completed" for v in session["nodeStates"].values())
            return _sanitize({
                "executionId": execution_id, "workflowId": session["workflowId"],
                "status": session["status"], "currentNodeId": session["currentNodeId"],
                "nodeStates": dict(session["nodeStates"]), "nodeResults": dict(session["nodeResults"]),
                "variables": dict(session["variables"]), "startedAt": started,
                "completedAt": session.get("completedAt"),
                "metrics": {"totalNodes": session["totalNodes"], "completedNodes": completed_nodes, "failedNodes": sum(v == "failed" for v in session["nodeStates"].values()), "duration": duration_ms, "throughput": (completed_nodes * 1000 / duration_ms) if duration_ms else 0},
            })

    def validate(self, definition: dict[str, Any]) -> dict[str, Any]:
        try:
            for node in definition.get("nodes", []):
                plugin_id = (node.get("metadata") or {}).get("plugin_id")
                if plugin_id and plugin_id != "builtin" and not self.runtime.plugin_bridge.has_handler(node.get("type", "")):
                    raise PluginError("PLUGIN_UNAVAILABLE: " + str(plugin_id), plugin_name=str(plugin_id), details={"code": "PLUGIN_UNAVAILABLE", "node_id": node.get("id")})
            manifest = self.runtime.create_manifest(definition)
            graph = self.runtime.compile(manifest)
            return {"valid": True, "errors": [], "plan": graph.topological_order()}
        except Exception as error:
            violations = getattr(error, "details", {}).get("violations", []) if hasattr(error, "details") else []
            return {"valid": False, "errors": violations or [_error_message(error)], "plan": []}

    def start(self, payload: dict[str, Any]) -> dict[str, Any]:
        definition = payload.get("definition") or {}
        input_nodes = {
            "mouse_move", "mouse_click", "mouse_double_click", "mouse_drag", "mouse_scroll",
            "keyboard_press", "keyboard_hotkey", "keyboard_type", "key_down", "key_up",
        }
        if any(str(node.get("type", "")) in input_nodes for node in definition.get("nodes", []) if isinstance(node, dict)):
            if not self.input_service.safety_status()["armed"]:
                raise RuntimeError("Input Runtime is not armed. Grant input permission before starting this workflow.")
        validation = self.validate(definition)
        if not validation["valid"]:
            raise RuntimeError("Workflow validation failed: " + "; ".join(validation["errors"]))
        manifest = self.runtime.create_manifest(definition)
        graph = self.runtime.compile(manifest)
        execution_id = str(payload.get("executionId") or f"execution-{uuid.uuid4()}")
        inputs = dict(payload.get("inputs") or {})
        for variable in definition.get("variables", []):
            if isinstance(variable, dict) and variable.get("name") not in inputs:
                inputs[str(variable.get("name"))] = variable.get("default")
        breakpoints = {str(item) for item in payload.get("breakpoints", [])}
        instance = self.runtime.create_instance(
            graph, inputs=inputs, metadata={"projectContext": payload.get("projectContext") or {}},
            instance_id=execution_id, breakpoints=breakpoints,
        )
        with self._session_lock:
            self._sessions[execution_id] = {
                "executionId": execution_id, "workflowId": graph.workflow_id,
                "definition": definition, "inputs": inputs,
                "projectContext": payload.get("projectContext") or {}, "breakpoints": list(breakpoints),
                "instance": instance, "status": "scheduled", "nodeStates": {node_id: "pending" for node_id in graph.nodes},
                "nodeResults": {}, "variables": dict(inputs), "history": [], "result": None,
                "currentNodeId": None, "startedAt": _now(), "startedEpoch": time.time(),
                "totalNodes": len(graph.nodes),
            }
        thread = threading.Thread(target=self._execute, args=(execution_id,), daemon=True)
        thread.start()
        return self._state(execution_id)

    def _execute(self, execution_id: str) -> None:
        with self._session_lock:
            session = self._sessions[execution_id]
            instance = session["instance"]
        try:
            result = self.runtime.execute(instance)
            completed_epoch = time.time()
            result_value = {
                "executionId": execution_id, "workflowId": result.workflow_id,
                "status": result.state.value.lower(), "success": result.success,
                "output": result.output, "error": result.error,
                "durationMs": result.duration_ms if result.duration_ms is not None else max(0, int((completed_epoch - session["startedEpoch"]) * 1000)), "metadata": result.metadata,
            }
            with self._session_lock:
                session = self._sessions[execution_id]
                session["result"] = result_value
                session["completedAt"] = _now()
                session["completedEpoch"] = completed_epoch
                if session["status"] not in {"cancelled", "failed"}:
                    session["status"] = "completed" if result.success else "failed"
        except Exception as error:
            with self._session_lock:
                session = self._sessions[execution_id]
                session["status"] = "failed"
                session["completedAt"] = _now()
                session["completedEpoch"] = time.time()
                session["result"] = {"executionId": execution_id, "workflowId": session["workflowId"], "status": "failed", "success": False, "output": {}, "error": _error_message(error)}
            self.emit({"eventId": str(uuid.uuid4()), "eventType": "WorkflowFailed", "timestamp": _now(), "workflowId": session["workflowId"], "executionId": execution_id, "nodeId": None, "correlationId": execution_id, "data": {"error": _error_message(error)}})
        finally:
            try:
                self.input_service.execute("input_release_all", {})
            except Exception:
                pass

    def control(self, execution_id: str, action: str) -> Any:
        with self._session_lock:
            session = self._sessions.get(execution_id)
            if not session:
                raise RuntimeError(f"Execution not found: {execution_id}")
        operations = {
            "pause": self.runtime.pause, "resume": self.runtime.resume,
            "stop": self.runtime.cancel, "step": self.runtime.step,
        }
        if action not in operations or not operations[action](execution_id):
            return False
        if action == "stop":
            # Cancellation is platform-independent. Releasing held physical input is
            # best-effort because non-Windows/test hosts intentionally expose an
            # unavailable provider.
            try:
                self.input_service.execute("input_release_all", {})
            except Exception:
                pass
        return self._state(execution_id)

    def restart(self, execution_id: str) -> dict[str, Any]:
        with self._session_lock:
            session = self._sessions.get(execution_id)
            if not session:
                raise RuntimeError(f"Execution not found: {execution_id}")
            payload = {key: session[key] for key in ("definition", "inputs", "projectContext", "breakpoints")}
        return self.start(payload)

    def result(self, execution_id: str) -> Any:
        with self._session_lock:
            session = self._sessions.get(execution_id)
            if not session:
                raise RuntimeError(f"Execution not found: {execution_id}")
            return _sanitize({"result": session["result"], "state": self._state(execution_id), "history": list(session["history"])})

    def handle(self, value: dict[str, Any]) -> None:
        if value.get("kind") == "bridge_response":
            self.bridge.resolve(value)
            return
        command_id = str(value.get("id", ""))
        command = str(value.get("command", ""))
        payload = value.get("payload") or {}
        try:
            if command == "workflow_validate":
                result = self.validate(payload.get("definition") or {})
            elif command == "workflow_start":
                result = self.start(payload)
            elif command in {"workflow_pause", "workflow_resume", "workflow_stop", "workflow_step"}:
                result = self.control(str(payload.get("executionId", "")), command.removeprefix("workflow_"))
            elif command == "workflow_restart":
                result = self.restart(str(payload.get("executionId", "")))
            elif command == "workflow_get_state":
                result = self._state(str(payload.get("executionId", "")))
            elif command == "workflow_get_result":
                result = self.result(str(payload.get("executionId", "")))
            elif command == "workflow_input_arm":
                result = self.input_service.arm(InputSafetyPolicy.from_dict(payload.get("policy") or {}))
            elif command == "workflow_input_status":
                result = self.input_service.safety_status()
            elif command == "workflow_emergency_stop":
                result = self.input_service.emergency_stop()
            elif command == "workflow_plugin_sync":
                result = self.sync_marketplace(payload)
            elif command == "workflow_plugin_register":
                result = self.register_plugin(payload)
            elif command.startswith("knowledge_"):
                result = self.knowledge_command(command, payload)
            else:
                raise RuntimeError(f"Unknown Workflow host command: {command}")
            self.respond(command_id, result)
        except Exception as error:
            self.respond(command_id, error=_error_message(error))


def main() -> int:
    host = DesktopWorkflowHost()
    for line in sys.stdin:
        try:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("Host message must be a JSON object")
            host.handle(value)
        except Exception as error:
            host.respond("", error=_error_message(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
