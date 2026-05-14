from pathlib import Path

from project_brain.core.doctor_checks.analysis import run_analysis_checks
from project_brain.core.doctor_checks.environment import run_environment_checks
from project_brain.core.doctor_checks.exports import run_export_checks
from project_brain.core.doctor_checks.llm import run_llm_checks
from project_brain.core.doctor_checks.repository import run_repository_checks


def run_doctor(root: Path):
    checks = []

    checks.extend(run_environment_checks(root))
    checks.extend(run_repository_checks(root))
    checks.extend(run_analysis_checks(root))
    checks.extend(run_export_checks(root))
    checks.extend(run_llm_checks(root))

    failures = [c for c in checks if c.status == "fail"]
    warnings = [c for c in checks if c.status == "warn"]

    if failures:
        status = "NOT READY"
    elif warnings:
        status = "PARTIAL"
    else:
        status = "READY"

    return checks, status