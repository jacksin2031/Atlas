# Atlas Vision Runtime Security

"""
Permission validation, capture authorization, provider isolation,
resource validation, input validation, and capability validation.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class Permission(Enum):
    """Security permissions."""

    CAPTURE_DESKTOP = "capture_desktop"
    CAPTURE_WINDOW = "capture_window"
    CAPTURE_REGION = "capture_region"
    CAPTURE_CAMERA = "capture_camera"
    CAPTURE_IMAGE = "capture_image"
    CAPTURE_VIDEO = "capture_video"
    CAPTURE_STREAM = "capture_stream"
    PROVIDER_ACCESS = "provider_access"
    RESOURCE_ACCESS = "resource_access"
    CONFIGURATION = "configuration"


class SecurityValidator:
    """Validates security constraints for Vision Runtime operations."""

    def __init__(self) -> None:
        self._permissions: dict[str, set[Permission]] = {}

    def grant_permissions(self, caller_id: str, permissions: list[Permission]) -> None:
        self._permissions[caller_id] = set(permissions)

    def has_permission(self, caller_id: str, required: Permission) -> bool:
        perms = self._permissions.get(caller_id, set())
        return required in perms

    def validate_capture_authorization(
        self, caller_id: str, source_type: str
    ) -> bool:
        perm_map = {
            "desktop": Permission.CAPTURE_DESKTOP,
            "window": Permission.CAPTURE_WINDOW,
            "region": Permission.CAPTURE_REGION,
            "camera": Permission.CAPTURE_CAMERA,
            "image": Permission.CAPTURE_IMAGE,
            "video": Permission.CAPTURE_VIDEO,
            "stream": Permission.CAPTURE_STREAM,
        }
        required = perm_map.get(source_type)
        if required is None:
            return False
        return self.has_permission(caller_id, required)

    def validate_provider_isolation(self, caller_id: str, provider_id: str) -> bool:
        return self.has_permission(caller_id, Permission.PROVIDER_ACCESS)

    def validate_resource_access(
        self, caller_id: str, resource_type: str
    ) -> bool:
        return self.has_permission(caller_id, Permission.RESOURCE_ACCESS)

    def validate_input(self, data: Any, expected_type: type) -> bool:
        if data is None:
            return False
        return isinstance(data, expected_type)

    def validate_capability(
        self, caller_id: str, capability: str
    ) -> bool:
        perms = self._permissions.get(caller_id, set())
        return Permission.CONFIGURATION in perms

    def check_plugin_isolation(self, plugin_id: str) -> bool:
        perms = self._permissions.get(plugin_id, set())
        return Permission.CAPTURE_DESKTOP not in perms
