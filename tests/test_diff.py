import subprocess
from pathlib import Path
from project_brain.core.differ import compute_diff


def git(cmd, cwd):
    subprocess.run(["git"] + cmd, cwd=cwd, check=True)


def test_diff_engine(tmp_path: Path):
    repo = tmp_path

    # Init git repo
    git(["init"], repo)

    file = repo / "a.py"

    # Commit 1
    file.write_text("def foo():\n    pass\n")
    git(["add", "."], repo)
    git(["commit", "-m", "init"], repo)

    # Commit 2 (modify + add)
    file.write_text("def foo():\n    return 1\n\ndef bar():\n    pass\n")
    new_file = repo / "b.py"
    new_file.write_text("print('new')")
    git(["add", "."], repo)
    git(["commit", "-m", "update"], repo)

    # Commit 3 (delete file)
    new_file.unlink()
    git(["add", "."], repo)
    git(["commit", "-m", "delete"], repo)

    result = compute_diff("HEAD~2", "HEAD", repo)

    assert "a.py" in result["modified"]
    assert "b.py" in result["added"] or "b.py" in result["deleted"]