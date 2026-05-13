import platform
import shutil
import sys
from pathlib import Path

from project_brain.core.doctor_checks.models import DoctorCheck


def run_environment_checks(root: Path):
    checks = []

    # Python version
    version = sys.version_info

    if version.major >= 3 and version.minor >= 10:
        checks.append(
            DoctorCheck(
                "Environment",
                "Python",
                "pass",
                f"Python {version.major}.{version.minor}",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Environment",
                "Python",
                "fail",
                "Python 3.10+ required",
                "Upgrade Python to >=3.10",
            )
        )

    # OS
    checks.append(
        DoctorCheck(
            "Environment",
            "OS",
            "info",
            platform.platform(),
        )
    )

    # Virtual env
    venv_active = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )

    if venv_active:
        checks.append(
            DoctorCheck(
                "Environment",
                "Virtual Environment",
                "pass",
                "Virtual environment active",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Environment",
                "Virtual Environment",
                "warn",
                "No virtual environment detected",
                "Create one:\npython -m venv env",
            )
        )

    # Git installed
    if shutil.which("git"):
        checks.append(
            DoctorCheck(
                "Environment",
                "Git",
                "pass",
                "Git installed",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Environment",
                "Git",
                "fail",
                "Git not installed",
                "Install Git from https://git-scm.com/",
            )
        )

    return checks