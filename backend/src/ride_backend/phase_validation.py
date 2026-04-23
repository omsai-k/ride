from __future__ import annotations

from dataclasses import dataclass

from ride_backend.ops import ReleaseChecklist


@dataclass(frozen=True)
class ValidationResult:
    name: str
    passed: bool


class Phase8Validator:
    def __init__(self, checklist: ReleaseChecklist) -> None:
        self._checklist = checklist

    def run(self, completed_gates: set[str]) -> list[ValidationResult]:
        return [
            ValidationResult("unit-tests", "unit-tests" in completed_gates),
            ValidationResult("integration-tests", "integration-tests" in completed_gates),
            ValidationResult("performance-tests", "performance-tests" in completed_gates),
            ValidationResult("security-check", "security-check" in completed_gates),
            ValidationResult("release-ready", self._checklist.is_ready(completed_gates)),
        ]
