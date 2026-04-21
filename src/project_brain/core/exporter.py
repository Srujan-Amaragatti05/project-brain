from pathlib import Path
import yaml

EXCLUDE_DIRS = {".brain", ".git", "node_modules", "venv", ".venv", "__pycache__", "*.egg-info", ".env", "env"}
EXCLUDE_FILES = {".env", ".gitignore", "README.md", "LICENSE", "CHANGELOG.md"}


def should_skip(path: Path):
    if path.name in EXCLUDE_FILES:
        return True

    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True

    return False


def is_test_file(path: Path):
    name = path.name.lower()
    return (
        name.startswith("test_") or
        name.endswith("_test.py") or
        "tests" in path.parts
    )


def load_config(root: Path):
    default = {
        "export": {
            "full_code": {
                "include_tests": False,
                "max_file_size_kb": 200
            },
            "manual_add": {
                "allow_duplicates": True
            }
        }
    }

    config_path = root / "brain.yaml"

    if not config_path.exists():
        return default

    try:
        data = yaml.safe_load(config_path.read_text())
        return data or default
    except Exception:
        return default


def _read_existing_entries(output_path: Path):
    if not output_path.exists():
        return set()

    existing = set()
    try:
        with output_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("=== FILE:"):
                    parts = line.strip().split("=== FILE:")[-1].strip()
                    file_name = parts.replace("===", "").strip()
                    file_name = file_name.replace("(MANUAL ADD)", "").strip()
                    existing.add(file_name)
    except Exception:
        pass

    return existing


def _append_file(out, rel_path: str, content: str, manual: bool):
    tag = " (MANUAL ADD)" if manual else ""
    out.write(f"=== FILE: {rel_path}{tag} ===\n")
    out.write(content)
    out.write("\n\n")


def export_full_code(root: Path):
    config = load_config(root)

    export_cfg = config.get("export", {}).get("full_code", {})
    include_tests = export_cfg.get("include_tests", False)
    max_kb = export_cfg.get("max_file_size_kb", 200)

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "full_code.txt"

    files_exported = 0

    with output_path.open("w", encoding="utf-8") as out:

        for path in root.rglob("*"):
            if path.is_dir():
                continue

            if should_skip(path):
                continue

            if not include_tests and is_test_file(path):
                continue

            try:
                size_kb = path.stat().st_size / 1024
                if size_kb > max_kb:
                    continue

                rel_path = str(path.relative_to(root))

                content = path.read_text(encoding="utf-8", errors="ignore")

                out.write(f"=== FILE: {rel_path} ===\n")
                out.write(content)
                out.write("\n\n")

                files_exported += 1

            except Exception:
                continue  # skip unreadable safely

    return files_exported, output_path


def add_code_file(root: Path, target: Path):
    config = load_config(root)
    max_kb = config["export"]["full_code"]["max_file_size_kb"]
    allow_dup = config["export"]["manual_add"]["allow_duplicates"]

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "full_code.txt"

    if not target.exists():
        return 0, output_path, "❌ File not found"

    if should_skip(target):
        return 0, output_path, "⚠ Skipped (ignored path)"

    existing = _read_existing_entries(output_path) if not allow_dup else set()

    try:
        size_kb = target.stat().st_size / 1024
        if size_kb > max_kb:
            return 0, output_path, "⚠ Skipped (file too large)"

        rel_path = str(target.resolve().relative_to(root))

        if not allow_dup and rel_path in existing:
            return 0, output_path, "⚠ Skipped (duplicate)"

        content = target.read_text(encoding="utf-8", errors="ignore")

        with output_path.open("a", encoding="utf-8") as out:
            _append_file(out, rel_path, content, manual=True)

        return 1, output_path, None

    except Exception:
        return 0, output_path, "⚠ Skipped (unreadable)"


def add_code_dir(root: Path, target: Path):
    config = load_config(root)
    max_kb = config["export"]["full_code"]["max_file_size_kb"]
    allow_dup = config["export"]["manual_add"]["allow_duplicates"]

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "full_code.txt"

    if not target.exists():
        return 0, output_path, "❌ Directory not found"

    existing = _read_existing_entries(output_path) if not allow_dup else set()

    count = 0

    with output_path.open("a", encoding="utf-8") as out:
        for path in target.rglob("*"):
            if path.is_dir():
                continue

            if should_skip(path):
                continue

            try:
                size_kb = path.stat().st_size / 1024
                if size_kb > max_kb:
                    continue

                rel_path = str(path.resolve().relative_to(root))

                if not allow_dup and rel_path in existing:
                    continue

                content = path.read_text(encoding="utf-8", errors="ignore")

                _append_file(out, rel_path, content, manual=True)
                count += 1

            except Exception:
                continue

    return count, output_path, None