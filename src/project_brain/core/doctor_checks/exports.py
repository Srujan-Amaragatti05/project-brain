from pathlib import Path

from project_brain.core.doctor_checks.models import DoctorCheck


def check_export(path: Path, name: str):
    if not path.exists():
        return DoctorCheck(
            "Exports",
            name,
            "warn",
            "Export missing",
        )

    if path.stat().st_size == 0:
        return DoctorCheck(
            "Exports",
            name,
            "warn",
            "Export empty",
        )

    return DoctorCheck(
        "Exports",
        name,
        "pass",
        "Export available",
    )


def run_export_checks(root: Path):
    checks = []

    export_dir = root / ".brain" / "exports"

    if not export_dir.exists():
        checks.append(
            DoctorCheck(
                "Exports",
                "Exports Directory",
                "warn",
                "Exports directory missing",
            )
        )
        return checks

    checks.append(
        DoctorCheck(
            "Exports",
            "Exports Directory",
            "pass",
            "Exports directory exists",
        )
    )

    checks.append(
        check_export(
            export_dir / "full_code.txt",
            "Full Code Export",
        )
    )

    checks.append(
        check_export(
            export_dir / "code_changes.txt",
            "Code Changes Export",
        )
    )

    return checks