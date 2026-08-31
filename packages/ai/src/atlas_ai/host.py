"""Desktop JSON-lines host for the Atlas AI Runtime.

The host keeps provider credentials below the Desktop IPC boundary. Commands
arrive on stdin and responses/runtime events are emitted on stdout as one JSON
object per line. stderr is reserved for sanitized diagnostics.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable

from atlas_ai.inference import InferenceRequest, InferenceResult
from atlas_ai.services import AIRuntime


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_request(url: str, *, method: str = "GET", payload: Any = None,
                  headers: dict[str, str] | None = None, timeout: float = 10.0):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request_headers = {"Accept": "application/json", **(headers or {})}
    if body is not None:
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    return urllib.request.urlopen(request, timeout=timeout)


def _read_json(response: Any) -> dict[str, Any]:
    raw = response.read().decode("utf-8")
    value = json.loads(raw)
    return value if isinstance(value, dict) else {}


def _usage(value: dict[str, Any]) -> dict[str, int]:
    usage = value.get("usage") or {}
    prompt = int(usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0)
    completion = int(usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0)
    total = int(usage.get("total_tokens", prompt + completion) or 0)
    return {"inputTokens": prompt, "outputTokens": completion, "totalTokens": total}


def _error_message(error: BaseException) -> str:
    if isinstance(error, urllib.error.HTTPError):
        return f"Provider returned HTTP {error.code}."
    if isinstance(error, urllib.error.URLError):
        return f"Provider connection failed: {error.reason}"
    return str(error) or error.__class__.__name__


@dataclass
class ProviderModel:
    model_id: str
    name: str
    version: str = "unknown"
    capabilities: tuple[str, ...] = ("chat", "streaming")
    context_window: int | None = None

    def descriptor(self, provider_id: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "modelId": self.model_id,
            "name": self.name,
            "providerId": provider_id,
            "version": self.version,
            "capabilities": list(self.capabilities),
            "modality": ["text", "image"] if "vision" in self.capabilities else ["text"],
            "state": "ready",
            "supportedParameters": ["temperature", "topP", "maxTokens", "stopSequences", "stream", "responseFormat", "seed", "toolChoice"],
        }
        if self.context_window:
            result["contextWindow"] = self.context_window
        return result


class ProviderBackend:
    provider_id = ""
    name = ""
    provider_type = ""
    version = "1"
    capabilities: tuple[str, ...] = ("chat", "streaming")

    def discover_models(self) -> list[ProviderModel]:
        raise NotImplementedError

    def health(self) -> bool:
        try:
            self.discover_models()
            return True
        except Exception:
            return False

    def infer(self, request: dict[str, Any], cancel: threading.Event) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    def descriptor(self, healthy: bool, enabled: bool) -> dict[str, Any]:
        return {
            "providerId": self.provider_id,
            "name": self.name,
            "providerType": self.provider_type,
            "version": self.version,
            "capabilities": list(self.capabilities),
            "health": "healthy" if healthy else "unhealthy",
            "connectionState": "connected" if healthy and enabled else "disconnected",
            "enabled": enabled,
        }


class OpenAIBackend(ProviderBackend):
    provider_id = "openai"
    name = "OpenAI"
    provider_type = "openai-compatible"
    capabilities = ("chat", "completion", "vision", "streaming", "tool_calling", "structured_output", "reasoning")

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def discover_models(self) -> list[ProviderModel]:
        with _json_request(f"{self.base_url}/models", headers=self.headers, timeout=15) as response:
            values = _read_json(response).get("data") or []
        models: list[ProviderModel] = []
        for value in values:
            model_id = str(value.get("id", ""))
            if not model_id:
                continue
            lowered = model_id.lower()
            if not any(marker in lowered for marker in ("gpt", "o1", "o3", "o4", "chat")):
                continue
            capabilities = ["chat", "streaming", "tool_calling", "structured_output"]
            if any(marker in lowered for marker in ("gpt-4o", "gpt-4.1", "gpt-5", "o3", "o4")):
                capabilities.append("vision")
            if any(marker in lowered for marker in ("o1", "o3", "o4", "gpt-5")):
                capabilities.append("reasoning")
            models.append(ProviderModel(model_id, model_id, capabilities=tuple(capabilities)))
        return sorted(models, key=lambda item: item.model_id)

    def _messages(self, request: dict[str, Any]) -> list[dict[str, Any]]:
        messages = [{"role": item.get("role", "user"), "content": item.get("content", "")} for item in request.get("messages", [])]
        images = [item.get("dataUrl") for item in request.get("attachments", []) if item.get("dataUrl")]
        if images and messages:
            last = messages[-1]
            text = str(last.get("content", ""))
            last["content"] = [{"type": "text", "text": text}, *({"type": "image_url", "image_url": {"url": image}} for image in images)]
        return messages

    def infer(self, request: dict[str, Any], cancel: threading.Event) -> Iterable[dict[str, Any]]:
        parameters = request.get("parameters") or {}
        streaming = bool(parameters.get("stream", False))
        payload: dict[str, Any] = {
            "model": request["modelId"],
            "messages": self._messages(request),
            "stream": streaming,
        }
        parameter_map = {"temperature": "temperature", "topP": "top_p", "maxTokens": "max_tokens", "stopSequences": "stop", "seed": "seed"}
        for source, target in parameter_map.items():
            if source in parameters:
                payload[target] = parameters[source]
        if parameters.get("responseFormat"):
            payload["response_format"] = {"type": parameters["responseFormat"]}
        with _json_request(f"{self.base_url}/chat/completions", method="POST", payload=payload, headers=self.headers, timeout=120) as response:
            if not streaming:
                value = _read_json(response)
                choice = (value.get("choices") or [{}])[0]
                yield {"delta": str((choice.get("message") or {}).get("content") or ""), "finishReason": choice.get("finish_reason") or "stop", "usage": _usage(value)}
                return
            usage: dict[str, int] = {}
            finish_reason = "stop"
            for raw in response:
                if cancel.is_set():
                    return
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                value = json.loads(data)
                if value.get("usage"):
                    usage = _usage(value)
                choice = (value.get("choices") or [{}])[0]
                delta = str((choice.get("delta") or {}).get("content") or "")
                finish_reason = choice.get("finish_reason") or finish_reason
                if delta:
                    yield {"delta": delta, "finishReason": finish_reason, "usage": usage}
            yield {"delta": "", "finishReason": finish_reason, "usage": usage}


class OllamaBackend(ProviderBackend):
    provider_id = "ollama"
    name = "Ollama"
    provider_type = "local"
    capabilities = ("chat", "completion", "vision", "streaming")

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def discover_models(self) -> list[ProviderModel]:
        with _json_request(f"{self.base_url}/api/tags", timeout=3) as response:
            values = _read_json(response).get("models") or []
        return [ProviderModel(str(value.get("name", "")), str(value.get("name", "")), str(value.get("details", {}).get("family", "local")), ("chat", "streaming", "vision")) for value in values if value.get("name")]

    def infer(self, request: dict[str, Any], cancel: threading.Event) -> Iterable[dict[str, Any]]:
        parameters = request.get("parameters") or {}
        streaming = bool(parameters.get("stream", False))
        messages = [{"role": item.get("role", "user"), "content": item.get("content", "")} for item in request.get("messages", [])]
        images = [str(item["dataUrl"]).split(",", 1)[-1] for item in request.get("attachments", []) if item.get("dataUrl")]
        if images and messages:
            messages[-1]["images"] = images
        payload = {"model": request["modelId"], "messages": messages, "stream": streaming, "options": {"temperature": parameters.get("temperature", .7), "top_p": parameters.get("topP", .9), "num_predict": parameters.get("maxTokens", 2048)}}
        with _json_request(f"{self.base_url}/api/chat", method="POST", payload=payload, timeout=120) as response:
            if not streaming:
                value = _read_json(response)
                yield {"delta": str((value.get("message") or {}).get("content") or ""), "finishReason": value.get("done_reason") or "stop", "usage": {"inputTokens": int(value.get("prompt_eval_count", 0)), "outputTokens": int(value.get("eval_count", 0)), "totalTokens": int(value.get("prompt_eval_count", 0)) + int(value.get("eval_count", 0))}}
                return
            for raw in response:
                if cancel.is_set():
                    return
                if not raw.strip():
                    continue
                value = json.loads(raw.decode("utf-8"))
                yield {"delta": str((value.get("message") or {}).get("content") or ""), "finishReason": value.get("done_reason") or "stop", "usage": {"inputTokens": int(value.get("prompt_eval_count", 0)), "outputTokens": int(value.get("eval_count", 0)), "totalTokens": int(value.get("prompt_eval_count", 0)) + int(value.get("eval_count", 0))}}


class DesktopAIHost:
    def __init__(self) -> None:
        self.runtime = AIRuntime()
        self.runtime.initialize()
        self.runtime.start()
        self._write_lock = threading.Lock()
        self._active: dict[str, threading.Event] = {}
        self._disabled: set[str] = set()
        self._events: list[dict[str, Any]] = []
        self._metrics = {"requestCount": 0, "successCount": 0, "failureCount": 0, "inputTokens": 0, "outputTokens": 0, "totalTokens": 0}
        self.providers: dict[str, ProviderBackend] = {}
        openai_key = os.environ.get("ATLAS_AI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        openai_base = os.environ.get("ATLAS_AI_BASE_URL", "https://api.openai.com/v1")
        # Always expose the provider so Desktop can configure its system-vault
        # credential even on first launch. An empty key remains unhealthy.
        self.providers["openai"] = OpenAIBackend(openai_base, openai_key or "")
        self.providers["ollama"] = OllamaBackend(os.environ.get("ATLAS_OLLAMA_URL", "http://127.0.0.1:11434"))

    def write(self, value: dict[str, Any]) -> None:
        with self._write_lock:
            sys.stdout.write(json.dumps(value, separators=(",", ":")) + "\n")
            sys.stdout.flush()

    def respond(self, command_id: str, result: Any = None, error: str | None = None) -> None:
        self.write({"kind": "response", "id": command_id, "ok": error is None, "result": result, "error": error})

    def emit(self, event_type: str, request_id: str = "", **values: Any) -> None:
        event = {"eventId": str(uuid.uuid4()), "eventType": event_type, "timestamp": _now(), "requestId": request_id, "correlationId": request_id, "source": "Python AI Runtime Host", **values}
        self._events.append({key: value for key, value in event.items() if key not in {"delta", "response"}})
        self._events = self._events[-200:]
        self.write({"kind": "event", "event": "ai://runtime-event", "payload": event})

    def discover(self) -> dict[str, Any]:
        providers: list[dict[str, Any]] = []
        models: list[dict[str, Any]] = []
        for provider_id, provider in self.providers.items():
            enabled = provider_id not in self._disabled
            try:
                discovered = provider.discover_models() if enabled else []
                healthy = enabled
            except Exception:
                discovered = []
                healthy = False
            if healthy or provider_id == "openai":
                providers.append(provider.descriptor(healthy, enabled))
                models.extend(model.descriptor(provider_id) for model in discovered)
        health = "healthy" if any(item["health"] == "healthy" for item in providers) else "unhealthy"
        return {"runtimeHealth": health, "providers": providers, "models": models, "memories": [], "tools": [], "agents": [], "events": self._events, "metrics": dict(self._metrics)}

    def provider_action(self, provider_id: str, action: str) -> bool:
        provider = self.providers.get(provider_id)
        if not provider or action not in {"connect", "disconnect", "refresh", "test"}:
            return False
        if action == "disconnect":
            self._disabled.add(provider_id)
            return True
        self._disabled.discard(provider_id)
        # Connect/refresh acknowledge that the Desktop command reached and
        # enabled a known provider. Discovery reports its health separately;
        # conflating an unhealthy provider with an unavailable IPC bridge made
        # the AI Studio surface a false integration error.
        return provider.health() if action == "test" else True

    def cancel(self, request_id: str) -> bool:
        cancel = self._active.get(request_id)
        if not cancel:
            return False
        cancel.set()
        return True

    def infer_async(self, command_id: str, request: dict[str, Any]) -> None:
        request_id = str(request.get("requestId") or uuid.uuid4())
        cancel = threading.Event()
        self._active[request_id] = cancel
        thread = threading.Thread(target=self._infer, args=(command_id, request, request_id, cancel), daemon=True)
        thread.start()

    def _infer(self, command_id: str, request: dict[str, Any], request_id: str, cancel: threading.Event) -> None:
        started = time.monotonic()
        provider_id = str(request.get("providerId", ""))
        model_id = str(request.get("modelId", ""))
        provider = self.providers.get(provider_id)
        self._metrics["requestCount"] += 1
        self.runtime.metrics.increment_counter("inference_total")
        self.emit("inference_started", request_id, summary=f"Inference started with {provider_id}/{model_id}")
        try:
            if not provider or provider_id in self._disabled:
                raise RuntimeError(f"Provider {provider_id or 'unknown'} is unavailable.")
            knowledge_context = request.get("knowledgeContext") or []
            if knowledge_context:
                sections = []
                for item in knowledge_context[:50]:
                    reference = item.get("reference") or {}
                    sections.append(
                        f"[Knowledge reference {reference.get('entry_id', '')}: {item.get('title', '')}]\n{item.get('content', '')}"
                    )
                request = {
                    **request,
                    "messages": [
                        {"role": "system", "content": "Use the following explicitly selected Atlas project knowledge as context.\n\n" + "\n\n".join(sections)},
                        *list(request.get("messages") or []),
                    ],
                }
            prompt = "\n".join(str(item.get("content", "")) for item in request.get("messages", []))
            runtime_request = InferenceRequest(prompt=prompt, model_id=model_id, request_id=request_id, stream=bool((request.get("parameters") or {}).get("stream")))
            content = ""
            finish_reason = "stop"
            usage: dict[str, int] = {}
            first_token_ms: float | None = None
            for chunk in provider.infer(request, cancel):
                if cancel.is_set():
                    self.emit("inference_cancelled", request_id, summary="Inference cancelled")
                    self.respond(command_id, error="Inference cancelled.")
                    return
                delta = str(chunk.get("delta", ""))
                finish_reason = str(chunk.get("finishReason") or finish_reason)
                if chunk.get("usage"):
                    usage = chunk["usage"]
                if delta:
                    if first_token_ms is None:
                        first_token_ms = (time.monotonic() - started) * 1000
                    content += delta
                    self.emit("inference_chunk", request_id, delta=delta, summary="Streaming response chunk")
            if cancel.is_set():
                self.emit("inference_cancelled", request_id, summary="Inference cancelled")
                self.respond(command_id, error="Inference cancelled.")
                return
            latency_ms = (time.monotonic() - started) * 1000
            result = InferenceResult(request_id=request_id, text=content, token_count=int(usage.get("outputTokens", 0)), model_id=runtime_request.model_id, finish_reason=finish_reason, usage={"input_tokens": int(usage.get("inputTokens", 0)), "output_tokens": int(usage.get("outputTokens", 0)), "total_tokens": int(usage.get("totalTokens", 0))}, duration_ms=latency_ms)
            response = {"requestId": request_id, "correlationId": request_id, "providerId": provider_id, "modelId": model_id, "content": result.text, "finishReason": result.finish_reason, "latencyMs": result.duration_ms, "usage": usage, "metadata": {"firstTokenLatencyMs": first_token_ms, "runtime": "atlas-ai-python", "knowledgeReferenceCount": len(knowledge_context), "knowledgeReferenceIds": [str((item.get("reference") or {}).get("entry_id", "")) for item in knowledge_context]}}
            self._metrics["successCount"] += 1
            for key in ("inputTokens", "outputTokens", "totalTokens"):
                self._metrics[key] += int(usage.get(key, 0))
            self._metrics["latencyMs"] = latency_ms
            if first_token_ms is not None:
                self._metrics["firstTokenLatencyMs"] = first_token_ms
            self.runtime.metrics.observe_histogram("inference_latency_ms", latency_ms)
            self.emit("inference_completed", request_id, response=response, metrics=dict(self._metrics), summary="Inference completed")
            self.respond(command_id, response)
        except Exception as error:
            message = _error_message(error)
            self._metrics["failureCount"] += 1
            self.runtime.metrics.increment_counter("inference_failed")
            self.emit("inference_failed", request_id, error=message, metrics=dict(self._metrics), summary=message)
            self.respond(command_id, error=message)
        finally:
            self._active.pop(request_id, None)

    def handle(self, value: dict[str, Any]) -> None:
        command_id = str(value.get("id", ""))
        command = value.get("command")
        payload = value.get("payload") or {}
        try:
            if command == "ai_discover":
                self.respond(command_id, self.discover())
            elif command == "ai_infer":
                self.infer_async(command_id, payload.get("request") or {})
            elif command == "ai_cancel":
                self.respond(command_id, self.cancel(str(payload.get("requestId", ""))))
            elif command == "ai_provider_action":
                self.respond(command_id, self.provider_action(str(payload.get("providerId", "")), str(payload.get("action", ""))))
            else:
                self.respond(command_id, error=f"Unknown AI host command: {command}")
        except Exception as error:
            self.respond(command_id, error=_error_message(error))


def main() -> int:
    host = DesktopAIHost()
    for line in sys.stdin:
        try:
            value = json.loads(line)
            if isinstance(value, dict):
                host.handle(value)
        except Exception as error:
            host.respond("", error=_error_message(error))
    host.runtime.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
