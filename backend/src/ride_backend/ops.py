from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeploymentTarget:
    name: str
    region: str
    replicas: int


class DeploymentPlanner:
    def backend_target(self) -> DeploymentTarget:
        return DeploymentTarget(name="ride-backend", region="us-central1", replicas=2)

    def signaling_target(self) -> DeploymentTarget:
        return DeploymentTarget(name="ride-signaling", region="us-central1", replicas=2)


class MetricsRegistry:
    def __init__(self) -> None:
        self._counters: dict[str, int] = {}

    def inc(self, metric: str, delta: int = 1) -> None:
        self._counters[metric] = self._counters.get(metric, 0) + delta

    def get(self, metric: str) -> int:
        return self._counters.get(metric, 0)


class ReleaseChecklist:
    REQUIRED_GATES = {
        "unit-tests",
        "integration-tests",
        "performance-tests",
        "security-check",
    }

    def is_ready(self, completed_gates: set[str]) -> bool:
        return self.REQUIRED_GATES.issubset(completed_gates)
