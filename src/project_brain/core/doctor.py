from pathlib import Path
import subprocess
import os
import yaml

from project_brain.core.differ import is_git_repo


def check_project_initialized(root: Path):
    return (root / ".brain").exists()


def check_analyzed(root: Path):
    return (root / ".brain" / "data.json").exists()


def check_git(root: Path):
    return is_git_repo(root)


def load_config(root: Path):
    path = root / "brain.yaml"
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text())
    except Exception:
        return None


def check_ollama():
    try:
        subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except Exception:
        return False


def check_openai():
    return bool(os.getenv("OPENAI_API_KEY"))


def run_doctor(root: Path):
    results = []
    status_flags = []

    # Project init
    if check_project_initialized(root):
        results.append("✔ Project initialized")
        status_flags.append(True)
    else:
        results.append("❌ Project not initialized")
        status_flags.append(False)

    if not (root / ".brain" / "cache").exists():
        results.append("⚠ Cache directory missing")

    # Analysis
    if check_analyzed(root):
        results.append("✔ Project analyzed")
        status_flags.append(True)
    else:
        results.append("❌ Project not analyzed")
        status_flags.append(False)

    # Git
    if check_git(root):
        results.append("✔ Git repository detected")
    else:
        results.append("⚠ Not a git repository")

    # Config
    config = load_config(root)
    if not config:
        results.append("❌ Missing or invalid brain.yaml")
        status_flags.append(False)
        llm_provider = "none"
    else:
        results.append("✔ Config loaded")
        llm_provider = config.get("llm", {}).get("provider", "none")

    # LLM check
    if llm_provider == "ollama":
        if check_ollama():
            results.append("✔ LLM: ollama available")
        else:
            results.append("❌ LLM: ollama not available")
            status_flags.append(False)

    elif llm_provider == "openai":
        if check_openai():
            results.append("✔ LLM: openai key found")
        else:
            results.append("❌ LLM: OPENAI_API_KEY missing")
            status_flags.append(False)

    else:
        results.append("ℹ LLM: disabled (provider=none)")

    # Final status
    if all(status_flags):
        final_status = "READY"
    elif any(status_flags):
        final_status = "PARTIAL"
    else:
        final_status = "NOT READY"

    return results, final_status