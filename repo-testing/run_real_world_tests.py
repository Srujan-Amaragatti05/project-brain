import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()

WORKSPACE = ROOT / "repos"
REPORTS = ROOT / "reports"

WORKSPACE.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

REPOS = {
    "small_flask": "https://github.com/pallets/flask.git",
    "small_typer": "https://github.com/fastapi/typer.git",
    "medium_fastapi": "https://github.com/fastapi/fastapi.git",
    "medium_rich": "https://github.com/Textualize/rich.git",
    "large_requests": "https://github.com/psf/requests.git",
}

COMMANDS = [
    ["brain", "project", "init"],
    ["brain", "project", "analyze", "."],
    ["brain", "project", "summary"],
    ["brain", "project", "doctor"],
    ["brain", "export", "full-code"],
]

OPTIONAL_COMMANDS = [
    ["brain", "diff", "show"],
]

results = []


def safe_filename(text: str):
    return (
        text.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )


def clone_repo(name, url):
    repo_dir = WORKSPACE / name

    if repo_dir.exists():
        print(f"Using existing repo: {name}")
        return repo_dir

    print(f"Cloning: {name}")

    subprocess.run(
        ["git", "clone", "--depth", "5", url, str(repo_dir)],
        check=True,
    )

    return repo_dir


def repo_size_mb(path):
    total = 0

    for f in path.rglob("*"):
        if f.is_file():
            try:
                total += f.stat().st_size
            except Exception:
                pass

    return round(total / (1024 * 1024), 2)


def save_output(repo_name, cmd, stdout, stderr):
    stdout_file = REPORTS / f"{repo_name}_stdout.txt"
    stderr_file = REPORTS / f"{repo_name}_stderr.txt"

    separator = (
        "\n"
        + "=" * 80
        + "\n"
        + f"COMMAND: {' '.join(cmd)}\n"
        + "=" * 80
        + "\n"
    )

    with open(
        stdout_file,
        "a",
        encoding="utf-8",
        errors="ignore",
    ) as f:
        f.write(separator)
        f.write(stdout)
        f.write("\n")

    with open(
        stderr_file,
        "a",
        encoding="utf-8",
        errors="ignore",
    ) as f:
        f.write(separator)
        f.write(stderr)
        f.write("\n")

    return stdout_file.name, stderr_file.name


def detect_issues(result):
    issues = []

    stdout = result["stdout"].lower()
    stderr = result["stderr"].lower()

    if result["exit_code"] != 0:
        issues.append("non_zero_exit")

    if "traceback" in stdout or "traceback" in stderr:
        issues.append("python_crash")

    if "unicode" in stdout or "unicode" in stderr:
        issues.append("encoding_issue")

    if "memory" in stdout or "memory" in stderr:
        issues.append("memory_issue")

    if result["runtime_sec"] > 120:
        issues.append("slow_execution")

    if "warning" in stdout or "warning" in stderr:
        issues.append("warnings_present")

    return sorted(set(issues))


def run_command(repo_name, cmd, cwd):
    start = time.time()

    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=300,
        )

        runtime = round(time.time() - start, 2)

        stdout_name, stderr_name = save_output(
            repo_name,
            cmd,
            proc.stdout,
            proc.stderr,
        )

        result = {
            "command": " ".join(cmd),
            "exit_code": proc.returncode,
            "runtime_sec": runtime,
            "stdout_file": stdout_name,
            "stderr_file": stderr_name,
            "stdout": proc.stdout[-5000:],
            "stderr": proc.stderr[-5000:],
        }

        result["issues"] = detect_issues(result)

        return result

    except subprocess.TimeoutExpired:

        result = {
            "command": " ".join(cmd),
            "exit_code": -1,
            "runtime_sec": 300,
            "stdout_file": "",
            "stderr_file": "",
            "stdout": "",
            "stderr": "TIMEOUT",
            "issues": ["timeout"],
        }

        return result

    except Exception as e:

        result = {
            "command": " ".join(cmd),
            "exit_code": -1,
            "runtime_sec": 0,
            "stdout_file": "",
            "stderr_file": "",
            "stdout": "",
            "stderr": str(e),
            "issues": ["execution_exception"],
        }

        return result


print("\n==============================")
print("REAL WORLD REPOSITORY TESTING")
print("==============================")

for repo_name, repo_url in REPOS.items():

    print(f"\n=== TESTING: {repo_name} ===")

    repo_dir = clone_repo(repo_name, repo_url)

    repo_result = {
        "repo": repo_name,
        "url": repo_url,
        "size_mb": repo_size_mb(repo_dir),
        "commands": [],
        "issues": [],
    }

    for cmd in COMMANDS + OPTIONAL_COMMANDS:

        print(f"RUN: {' '.join(cmd)}")

        result = run_command(
            repo_name,
            cmd,
            repo_dir,
        )

        repo_result["commands"].append(result)

        repo_result["issues"].extend(
            result["issues"]
        )

    export_path = (
        repo_dir
        / ".brain"
        / "exports"
        / "full_code.txt"
    )

    if export_path.exists():

        export_size = round(
            export_path.stat().st_size / 1024,
            2,
        )

        repo_result["export_size_kb"] = export_size

        if export_size == 0:
            repo_result["issues"].append(
                "empty_export"
            )

    else:
        repo_result["issues"].append(
            "missing_export"
        )

    repo_result["issues"] = sorted(
        set(repo_result["issues"])
    )

    results.append(repo_result)

json_report = {
    "generated_at": datetime.now().isoformat(),
    "total_repositories": len(results),
    "results": results,
}

json_path = REPORTS / "test_results.json"

json_path.write_text(
    json.dumps(json_report, indent=2),
    encoding="utf-8",
)

md_lines = []

md_lines.append("# REAL WORLD TEST REPORT\n")

md_lines.append(
    f"Generated: {datetime.now().isoformat()}\n"
)

for repo in results:

    md_lines.append(f"## {repo['repo']}\n")

    md_lines.append(
        f"- Repo Size: {repo['size_mb']} MB"
    )

    md_lines.append(
        f"- Export Size: {repo.get('export_size_kb', 0)} KB"
    )

    if repo["issues"]:
        md_lines.append("- Issues:")
        for issue in repo["issues"]:
            md_lines.append(f"  - {issue}")
    else:
        md_lines.append("- Issues: none")

    md_lines.append("\n### Commands\n")

    for cmd in repo["commands"]:

        md_lines.append(
            f"- `{cmd['command']}`"
        )

        md_lines.append(
            f"  - Exit Code: {cmd['exit_code']}"
        )

        md_lines.append(
            f"  - Runtime: {cmd['runtime_sec']} sec"
        )

        md_lines.append(
            f"  - Stdout File: {cmd['stdout_file']}"
        )

        md_lines.append(
            f"  - Stderr File: {cmd['stderr_file']}"
        )

        if cmd["issues"]:
            md_lines.append(
                f"  - Issues: {', '.join(cmd['issues'])}"
            )

    md_lines.append("\n---\n")

md_path = REPORTS / "REAL_WORLD_TESTS.md"

md_path.write_text(
    "\n".join(md_lines),
    encoding="utf-8",
)

print("\n==============================")
print("TESTING COMPLETE")
print("==============================")
print(f"JSON REPORT: {json_path}")
print(f"MARKDOWN REPORT: {md_path}")
print(f"REPORT DIRECTORY: {REPORTS}")