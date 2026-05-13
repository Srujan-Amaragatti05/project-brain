import subprocess
from pathlib import Path
from project_brain.core.differ import compute_diff


def git(cmd, cwd):
    subprocess.run(["git"] + cmd, cwd=cwd, check=True)


def test_function_diff_accuracy(tmp_path):
    repo = tmp_path

    git(["init"], repo)
    git(["config", "user.email", "t@t.com"], repo)
    git(["config", "user.name", "t"], repo)

    f = repo / "a.py"

    f.write_text("def foo():\n    return 1\n")
    git(["add", "."], repo)
    git(["commit", "-m", "init"], repo)

    f.write_text(
        "def foo():\n    return 2\n\n"
        "def bar():\n    pass\n"
    )
    git(["add", "."], repo)
    git(["commit", "-m", "update"], repo)

    result = compute_diff("HEAD~1", "HEAD", repo)

    fn_diff = result["function_diffs"][0]

    assert "bar" in fn_diff["added"]
    assert "foo" in fn_diff["modified"]
