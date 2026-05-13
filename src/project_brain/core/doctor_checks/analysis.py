import json
from datetime import datetime
from pathlib import Path

from project_brain.core.doctor_checks.models import DoctorCheck


def run_analysis_checks(root: Path):
    checks = []

    brain_dir = root / ".brain"

    if brain_dir.exists():
        checks.append(
            DoctorCheck(
                "Analysis",
                "Initialization",
                "pass",
                ".brain directory exists",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Analysis",
                "Initialization",
                "fail",
                "Project not initialized",
                "Run:\nbrain project init",
            )
        )
        return checks

    data_path = brain_dir / "data.json"

    if not data_path.exists():
        checks.append(
            DoctorCheck(
                "Analysis",
                "Analysis",
                "fail",
                "Analysis missing",
                "Run:\nbrain project analyze .",
            )
        )
        return checks

    checks.append(
        DoctorCheck(
            "Analysis",
            "Analysis",
            "pass",
            "data.json exists",
        )
    )

    try:
        data = json.loads(data_path.read_text())

        total_files = data.get("project", {}).get("total_files", 0)

        checks.append(
            DoctorCheck(
                "Analysis",
                "Analyzed Files",
                "info",
                str(total_files),
            )
        )

        modified = datetime.fromtimestamp(
            data_path.stat().st_mtime
        )

        age_hours = (
            datetime.now() - modified
        ).total_seconds() / 3600

        if age_hours > 24:
            checks.append(
                DoctorCheck(
                    "Analysis",
                    "Freshness",
                    "warn",
                    "Analysis may be stale",
                    "Run:\nbrain project analyze .",
                )
            )
        else:
            checks.append(
                DoctorCheck(
                    "Analysis",
                    "Freshness",
                    "pass",
                    "Analysis is recent",
                )
            )

    except Exception:
        checks.append(
            DoctorCheck(
                "Analysis",
                "Integrity",
                "fail",
                "Invalid data.json",
                "Re-run analysis",
            )
        )

    return checks