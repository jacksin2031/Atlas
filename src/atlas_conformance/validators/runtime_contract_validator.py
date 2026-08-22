from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core import (
    ArchitectureViolation,
    RuleCategory,
    ViolationSeverity,
)
from ..contracts.runtimes import (
    RuntimeContract,
    RuntimeHealthContract,
    RuntimeLifecycleContract,
    RuntimeMetricsContract,
    RuntimeProviderContract,
    RuntimeSecurityContract,
    RuntimeServiceContract,
    RuntimeStorageContract,
)


class RuntimeContractValidator:
    def __init__(self, src_root: str | Path) -> None:
        self._src_root = Path(src_root)

    def validate(self, runtime_name: str) -> tuple[RuntimeContract, list[ArchitectureViolation]]:
        violations: list[ArchitectureViolation] = []
        contract = RuntimeContract(runtime_name=runtime_name)

        service_contract = self._check_service_contract(runtime_name)
        if service_contract:
            contract.service = service_contract
            violations.extend(self._validate_service(service_contract, runtime_name))

        lifecycle_contract = self._check_lifecycle_contract(runtime_name)
        if lifecycle_contract:
            contract.lifecycle = lifecycle_contract
            violations.extend(self._validate_lifecycle(lifecycle_contract, runtime_name))

        metrics_contract = self._check_metrics_contract(runtime_name)
        if metrics_contract:
            contract.metrics = metrics_contract
            violations.extend(self._validate_metrics(metrics_contract, runtime_name))

        health_contract = self._check_health_contract(runtime_name)
        if health_contract:
            contract.health = health_contract
            violations.extend(self._validate_health(health_contract, runtime_name))

        provider_contract = self._check_provider_contract(runtime_name)
        if provider_contract:
            contract.provider = provider_contract
            violations.extend(self._validate_provider(provider_contract, runtime_name))

        security_contract = self._check_security_contract(runtime_name)
        if security_contract:
            contract.security = security_contract
            violations.extend(self._validate_security(security_contract, runtime_name))

        storage_contract = self._check_storage_contract(runtime_name)
        if storage_contract:
            contract.storage = storage_contract
            violations.extend(self._validate_storage(storage_contract, runtime_name))

        return contract, violations

    def _check_service_contract(self, runtime_name: str) -> RuntimeServiceContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "class" in text and "Service" in text:
                    return RuntimeServiceContract(
                        service_name=runtime_name,
                        required_methods=("start", "stop", "shutdown"),
                    )
            except Exception:
                pass
        return None

    def _check_lifecycle_contract(self, runtime_name: str) -> RuntimeLifecycleContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                states = ["CREATED", "INITIALIZING", "READY", "RUNNING", "SHUTTING_DOWN", "TERMINATED"]
                found_states = sum(1 for s in states if s in text)
                if found_states >= 4:
                    return RuntimeLifecycleContract()
            except Exception:
                pass
        return None

    def _check_metrics_contract(self, runtime_name: str) -> RuntimeMetricsContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "metric" in text.lower() or "counter" in text.lower() or "gauge" in text.lower():
                    return RuntimeMetricsContract()
            except Exception:
                pass
        return None

    def _check_health_contract(self, runtime_name: str) -> RuntimeHealthContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "health" in text.lower():
                    return RuntimeHealthContract()
            except Exception:
                pass
        return None

    def _check_provider_contract(self, runtime_name: str) -> RuntimeProviderContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "Provider" in text and ("ABC" in text or "abstractmethod" in text):
                    return RuntimeProviderContract()
            except Exception:
                pass
        return None

    def _check_security_contract(self, runtime_name: str) -> RuntimeSecurityContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "security" in text.lower() or "permission" in text.lower():
                    return RuntimeSecurityContract()
            except Exception:
                pass
        return None

    def _check_storage_contract(self, runtime_name: str) -> RuntimeStorageContract | None:
        for py_file in self._src_root.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
                if "storage" in text.lower() or "backend" in text.lower():
                    return RuntimeStorageContract()
            except Exception:
                pass
        return None

    def _validate_service(self, contract: RuntimeServiceContract, runtime_name: str) -> list[ArchitectureViolation]:
        violations: list[ArchitectureViolation] = []
        if not contract.required_methods:
            violations.append(ArchitectureViolation(
                rule_id="RT-SVC-001",
                rule_name="Runtime Service Contract",
                category=RuleCategory.RUNTIME_CONTRACTS,
                severity=ViolationSeverity.ERROR,
                message=f"Runtime {runtime_name} has no required service methods defined",
            ))
        return violations

    def _validate_lifecycle(self, contract: RuntimeLifecycleContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []

    def _validate_metrics(self, contract: RuntimeMetricsContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []

    def _validate_health(self, contract: RuntimeHealthContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []

    def _validate_provider(self, contract: RuntimeProviderContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []

    def _validate_security(self, contract: RuntimeSecurityContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []

    def _validate_storage(self, contract: RuntimeStorageContract, runtime_name: str) -> list[ArchitectureViolation]:
        return []
