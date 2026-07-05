from __future__ import annotations

import pytest
from atlas_conformance.validators import RuntimeContractValidator
from atlas_conformance.contracts.runtimes import (
    RuntimeContract,
    RuntimeHealthContract,
    RuntimeLifecycleContract,
    RuntimeMetricsContract,
    RuntimeProviderContract,
    RuntimeSecurityContract,
    RuntimeServiceContract,
    RuntimeStorageContract,
    ContractType,
)


class TestRuntimeContractValidator:
    def test_validate_returns_contract_and_violations(self):
        validator = RuntimeContractValidator("src")
        contract, violations = validator.validate("test_runtime")
        assert isinstance(contract, RuntimeContract)
        assert isinstance(violations, list)

    def test_health_contract_detected(self):
        validator = RuntimeContractValidator("src")
        contract, _ = validator.validate("atlas_workflow")
        assert contract.health is not None
        assert isinstance(contract.health, RuntimeHealthContract)

    def test_lifecycle_contract_detected(self):
        validator = RuntimeContractValidator("src")
        contract, _ = validator.validate("atlas_workflow")
        assert contract.lifecycle is not None
        assert isinstance(contract.lifecycle, RuntimeLifecycleContract)

    def test_metrics_contract_detected(self):
        validator = RuntimeContractValidator("src")
        contract, _ = validator.validate("atlas_workflow")
        assert contract.metrics is not None
        assert isinstance(contract.metrics, RuntimeMetricsContract)

    def test_contract_types(self):
        validator = RuntimeContractValidator("src")
        contract, _ = validator.validate("atlas_workflow")
        types = contract.contract_types
        assert ContractType.HEALTH in types
        assert ContractType.LIFECYCLE in types
        assert ContractType.METRICS in types

    def test_no_violations_for_known_runtimes(self):
        validator = RuntimeContractValidator("src")
        _, violations = validator.validate("atlas_workflow")
        assert len(violations) == 0
