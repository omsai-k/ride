from ride_backend.ops import DeploymentPlanner
from ride_backend.ops import MetricsRegistry
from ride_backend.ops import ReleaseChecklist
from ride_backend.phase_validation import Phase8Validator


def test_deployment_planner_targets() -> None:
    planner = DeploymentPlanner()
    backend = planner.backend_target()
    signaling = planner.signaling_target()
    assert backend.name == "ride-backend"
    assert signaling.replicas == 2


def test_metrics_registry_counts() -> None:
    metrics = MetricsRegistry()
    metrics.inc("api_requests_total")
    metrics.inc("api_requests_total", 3)
    assert metrics.get("api_requests_total") == 4


def test_release_checklist_and_phase8_validator() -> None:
    checklist = ReleaseChecklist()
    validator = Phase8Validator(checklist)

    completed = {"unit-tests", "integration-tests", "performance-tests", "security-check"}
    results = validator.run(completed)

    assert checklist.is_ready(completed) is True
    assert any(item.name == "release-ready" and item.passed for item in results)

    incomplete = {"unit-tests"}
    assert checklist.is_ready(incomplete) is False
