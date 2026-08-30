"""Desktop AI host protocol and streaming integration tests."""
from __future__ import annotations

import json
import os
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from atlas_ai.host import DesktopAIHost


class _OpenAIHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/v1/models":
            self._json({"data": [{"id": "gpt-host-test"}]})
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/chat/completions":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length))
        if not payload.get("stream"):
            self._json({"choices": [{"message": {"content": "Hello Atlas"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 2, "completion_tokens": 2, "total_tokens": 4}})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        for token in ("Hello", " Atlas"):
            value = {"choices": [{"delta": {"content": token}, "finish_reason": None}]}
            self.wfile.write(f"data: {json.dumps(value)}\n\n".encode())
            self.wfile.flush()
            time.sleep(.02)
        final = {"choices": [{"delta": {}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 2, "completion_tokens": 2, "total_tokens": 4}}
        self.wfile.write(f"data: {json.dumps(final)}\n\ndata: [DONE]\n\n".encode())
        self.wfile.flush()

    def _json(self, value: object) -> None:
        body = json.dumps(value).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class TestDesktopAIHost(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _OpenAIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.environment = patch.dict(os.environ, {
            "ATLAS_AI_API_KEY": "test-only",
            "ATLAS_AI_BASE_URL": f"http://127.0.0.1:{self.server.server_port}/v1",
            "ATLAS_OLLAMA_URL": "http://127.0.0.1:1",
        })
        self.environment.start()
        self.host = DesktopAIHost()
        self.messages: list[dict[str, object]] = []
        self.host.write = self.messages.append  # type: ignore[method-assign]

    def tearDown(self) -> None:
        self.host.runtime.stop()
        self.environment.stop()
        self.server.shutdown()
        self.server.server_close()

    def test_discover_provider_and_models(self) -> None:
        snapshot = self.host.discover()
        self.assertEqual(snapshot["runtimeHealth"], "healthy")
        self.assertEqual(snapshot["providers"][0]["providerId"], "openai")
        self.assertEqual(snapshot["models"][0]["modelId"], "gpt-host-test")

    def test_streaming_inference_emits_chunks_and_final_response(self) -> None:
        request = {
            "requestId": "request-1",
            "providerId": "openai",
            "modelId": "gpt-host-test",
            "messages": [{"role": "user", "content": "Say hello"}],
            "parameters": {"stream": True, "maxTokens": 16},
            "attachments": [],
        }
        self.host.infer_async("command-1", request)
        deadline = time.time() + 3
        while time.time() < deadline and not any(item.get("kind") == "response" for item in self.messages):
            time.sleep(.01)
        events = [item["payload"] for item in self.messages if item.get("kind") == "event"]
        chunks = [item["delta"] for item in events if item["eventType"] == "inference_chunk"]
        response = next(item for item in self.messages if item.get("kind") == "response")
        self.assertEqual(chunks, ["Hello", " Atlas"])
        self.assertEqual(response["result"]["content"], "Hello Atlas")
        self.assertEqual(response["result"]["usage"]["totalTokens"], 4)
        self.assertTrue(any(item["eventType"] == "inference_completed" for item in events))

    def test_provider_actions_and_unknown_cancellation(self) -> None:
        self.assertTrue(self.host.provider_action("openai", "test"))
        self.assertTrue(self.host.provider_action("openai", "disconnect"))
        self.assertFalse(self.host.cancel("missing"))

    def test_connect_acknowledges_bridge_even_when_provider_is_unhealthy(self) -> None:
        self.host.providers["openai"].base_url = "http://127.0.0.1:1/v1"  # type: ignore[attr-defined]
        self.assertTrue(self.host.provider_action("openai", "connect"))
        snapshot = self.host.discover()
        provider = next(item for item in snapshot["providers"] if item["providerId"] == "openai")
        self.assertEqual(provider["health"], "unhealthy")
        self.assertEqual(provider["connectionState"], "disconnected")
        self.assertFalse(self.host.provider_action("openai", "test"))

    def test_active_stream_can_be_cancelled(self) -> None:
        request = {
            "requestId": "request-cancel",
            "providerId": "openai",
            "modelId": "gpt-host-test",
            "messages": [{"role": "user", "content": "Cancel me"}],
            "parameters": {"stream": True},
            "attachments": [],
        }
        self.host.infer_async("command-cancel", request)
        self.assertTrue(self.host.cancel("request-cancel"))
        deadline = time.time() + 3
        while time.time() < deadline and not any(item.get("kind") == "response" for item in self.messages):
            time.sleep(.01)
        response = next(item for item in self.messages if item.get("kind") == "response")
        events = [item["payload"] for item in self.messages if item.get("kind") == "event"]
        self.assertFalse(response["ok"])
        self.assertEqual(response["error"], "Inference cancelled.")
        self.assertTrue(any(item["eventType"] == "inference_cancelled" for item in events))


if __name__ == "__main__":
    unittest.main()
