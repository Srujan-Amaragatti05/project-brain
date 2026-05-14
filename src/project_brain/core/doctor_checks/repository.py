from pathlib import Path

from project_brain.core.differ import is_git_repo, run_git_command
from project_brain.core.doctor_checks.models import DoctorCheck


def get_repo_size(root: Path):
    total = 0

    try:
        for path in root.rglob("*"):
            if path.is_file():
                total += path.stat().st_size
    except Exception:
        return "Unknown"

    return f"{round(total / (1024 * 1024), 2)} MB"


def run_repository_checks(root: Path):
    checks = []

    if not is_git_repo(root):
        checks.append(
            DoctorCheck(
                "Repository",
                "Git Repository",
                "warn",
                "Not a git repository",
                "Run:\ngit init",
            )
        )
        return checks

    checks.append(
        DoctorCheck(
            "Repository",
            "Git Repository",
            "pass",
            "Git repository detected",
        )
    )

    branch = run_git_command(
        ["branch", "--show-current"],
        root,
    )

    if branch:
        checks.append(
            DoctorCheck(
                "Repository",
                "Branch",
                "pass",
                branch,
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Repository",
                "Branch",
                "warn",
                "Detached HEAD state",
            )
        )

    commit = run_git_command(
        ["rev-parse", "--short", "HEAD"],
        root,
    )

    if commit:
        checks.append(
            DoctorCheck(
                "Repository",
                "Latest Commit",
                "pass",
                commit,
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "Repository",
                "Latest Commit",
                "warn",
                "No commits found",
                "Create initial commit",
            )
        )

    checks.append(
        DoctorCheck(
            "Repository",
            "Repository Size",
            "info",
            get_repo_size(root),
        )
    )

    return checks