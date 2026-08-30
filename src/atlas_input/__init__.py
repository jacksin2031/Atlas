"""Atlas Input Runtime public API."""
import sys

from .contracts import *  # noqa: F401,F403
from .provider import InputProvider, TestInputProvider, UnavailableInputProvider
from .service import InputService
from .safety import InputSafetyController, InputSafetyError, InputSafetyPolicy
from .windows import WindowsInputProvider


def default_input_service() -> InputService:
    provider: InputProvider
    if sys.platform == "win32":
        provider = WindowsInputProvider()
    else:
        provider = UnavailableInputProvider(f"No InputProvider is available for {sys.platform}")
    service = InputService(provider, InputSafetyController(InputSafetyPolicy()))
    service.start_emergency_watch()
    return service


__all__ = ["InputProvider", "InputService", "InputSafetyController", "InputSafetyError", "InputSafetyPolicy", "TestInputProvider", "WindowsInputProvider", "default_input_service"]
