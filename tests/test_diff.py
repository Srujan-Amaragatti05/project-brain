import subprocess
from pathlib import Path

from project_brain.core.differ import compute_diff


def git(cmd, cwd):
    subprocess.run(["git"] + cmd, cwd=cwd, check=True)


def test_diff_engine(tmp_path: Path):
    repo = tmp_path

    # Initialize temporary git repo
    git(["init"], repo)

    # IMPORTANT:
    # Configure git identity for CI runners
    git(["config", "user.email", "ci@example.com"], repo)
    git(["config", "user.name", "CI Tester"], repo)

    file = repo / "a.py"

    # First commit
    file.write_text("def foo():\n    pass\n")

    git(["add", "."], repo)
    git(["commit", "-m", "init"], repo)

    # Second commit
    file.write_text("def foo():\n    return 1\n")

    git(["add", "."], repo)
    git(["commit", "-m", "update"], repo)

    result = compute_diff("HEAD~1", "HEAD", repo)

    assert "a.py" in result["modified"]