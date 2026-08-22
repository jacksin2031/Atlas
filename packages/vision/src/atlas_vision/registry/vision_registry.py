# Atlas Vision Runtime Registry

"""
Central service registry for Vision Runtime services.

Handles registration, lookup, health checks, and version compatibility.
"""
from __future__ import annotations

from typing import Any

from atlas_vision.errors import DuplicateRegistrationError, RegistryError


class VisionRegistry:
    """Central registry for Vision Runtime services."""

    def __init__(self) -> None:
        self._services: dict[str, dict[str, Any]] = {}
        self._versions: dict[str, str] = {}

    def register(
        self,
        service_id: str,
        service: Any,
        version: str = "1.0.0",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if service_id in self._services:
            raise DuplicateRegistrationError(
                f"Service {service_id} already registered", service_id
            )
        self._services[service_id] = {
            "instance": service,
            "metadata": metadata or {},
        }
        self._versions[service_id] = version

    def get(self, service_id: str) -> Any | None:
        entry = self._services.get(service_id)
        if entry is None:
            return None
        return entry["instance"]

    def list_services(self) -> list[str]:
        return list(self._services.keys())

    def is_registered(self, service_id: str) -> bool:
        return service_id in self._services

    def health_check(self, service_id: str) -> dict[str, Any]:
        if service_id not in self._services:
            return {"status": "not_found", "service_id": service_id}
        svc = self._services[service_id]["instance"]
        if hasattr(svc, "health_check"):
            try:
                return {"status": "healthy", "details": svc.health_check()}
            except Exception as exc:
                return {"status": "unhealthy", "error": str(exc)}
        return {"status": "healthy", "service_id": service_id}

    def check_version_compatibility(
        self, service_id: str, required_version: str
    ) -> bool:
        if service_id not in self._versions:
            return False
        actual = self._versions[service_id]
        return self._versions_match(actual, required_version)

    @staticmethod
    def _versions_match(actual: str, required: str) -> bool:
        return actual.split(".")[0] == required.split(".")[0]

    def initialize(self) -> None:
        pass

    def clear(self) -> None:
        self._services.clear()
        self._versions.clear()

    def to_dict(self) -> dict[str, Any]:
        return {
            "services": list(self._services.keys()),
            "versions": dict(self._versions),
        }
