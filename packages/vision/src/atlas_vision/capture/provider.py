# Atlas Vision Runtime Capture Provider

"""
Abstract capture provider interface.

All concrete capture implementations must subclass CaptureProviderABC
and implement the required lifecycle methods.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from atlas_vision.capture.sources import CaptureDescriptor, CaptureSource
from atlas_vision.models.frame import Frame


class CaptureProviderABC(ABC):
    """Abstract base class for capture providers."""

    @abstractmethod
    def supports(self, descriptor: CaptureDescriptor) -> bool:
        """Return True if this provider supports the given descriptor."""
        ...

    @abstractmethod
    def create_session(self, source: CaptureSource) -> Any:
        """Create a capture session for the given source."""
        ...

    @abstractmethod
    def start_session(self, session: Any) -> bool:
        """Start the capture session."""
        ...

    @abstractmethod
    def stop_session(self, session: Any) -> None:
        """Stop the capture session."""
        ...

    @abstractmethod
    def capture_frame(self, session: Any) -> Optional[Frame]:
        """Capture a single frame from the session."""
        ...

    @abstractmethod
    def release_session(self, session: Any) -> None:
        """Release resources held by the session."""
        ...

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the provider is healthy."""
        ...

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Return list of supported capability names."""
        ...
