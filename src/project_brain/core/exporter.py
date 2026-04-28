import ast
import hashlib
from pathlib import Path

from project_brain.core.config_loader import load_config
from project_brain.core.differ import compute_diff, get_file_from_ref
from project_brain.core.logger import log_error


def should_skip(path: Path, ignore_patterns):
    path_str = str(path)

    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            if pattern.rstrip("/") in path_str:
                return True
        elif pattern.startswith("*."):
            if path.name.endswith(pattern.replace("*", "")):
                return True
        else:
            if pattern in path.parts:
                return True

    return False


def is_test_file(path: Path):
    name = path.name.lower()
    return (
        name.startswith("test_") or
        name.endswith("_test.py") or
        "tests" in path.parts
    )



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
    except Exception as e:
        log_error(f"Function failed: {str(e)}")
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
    ignore_paths = config.get("export", {}).get("ignore", [])

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "full_code.txt"

    files_exported = 0
    file_paths = []

    with output_path.open("w", encoding="utf-8") as out:

        for path in root.rglob("*"):
            if path.is_dir():
                continue

            if should_skip(path, ignore_paths):
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
                file_paths.append(rel_path)

            except Exception:
                continue  # skip unreadable safely

    return files_exported, output_path, file_paths


def add_code_file(root: Path, target: Path):
    config = load_config(root)
    max_kb = config["export"]["full_code"]["max_file_size_kb"]
    allow_dup = config["export"]["manual_add"]["allow_duplicates"]
    ingore_paths = config.get("export", {}).get("ignore", [])

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "full_code.txt"

    if not target.exists():
        return 0, output_path, "❌ File not found"

    if should_skip(target, ingore_paths):
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
    ignore_paths = config.get("export", {}).get("ignore", [])

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

            if should_skip(path, ignore_paths):
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


def _extract_functions_with_code(source: str):
    result = {}

    try:
        tree = ast.parse(source)
    except Exception:
        return result

    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = getattr(node, "end_lineno", start + 1)

            code = "\n".join(lines[start:end])
            body_hash = hashlib.sha256(code.encode()).hexdigest()

            result[node.name] = {
                "code": code,
                "hash": body_hash,
                "line": node.lineno
            }

    return result


def export_code_changes(root: Path, from_ref: str, to_ref: str):
    config = load_config(root)
    changes_cfg = config.get("export", {}).get("changes", {})

    mode = changes_cfg.get("mode", "function")
    include_context = changes_cfg.get("include_context", True)

    export_dir = root / ".brain" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    output_path = export_dir / "code_changes.txt"

    diff = compute_diff(from_ref, to_ref, root)
    if not diff:
        return 0, output_path

    files_processed = 0

    with output_path.open("w", encoding="utf-8") as out:

        # ADDED FILES
        for file in diff["added"]:
            new_src = get_file_from_ref(to_ref, file, root)
            if not new_src:
                continue

            out.write(f"=== FILE: {file} (ADDED) ===\n")
            out.write(new_src)
            out.write("\n\n")

            files_processed += 1

        # DELETED FILES
        for file in diff["deleted"]:
            old_src = get_file_from_ref(from_ref, file, root)
            if not old_src:
                continue

            out.write(f"=== FILE: {file} (DELETED) ===\n")
            out.write(old_src)
            out.write("\n\n")

            files_processed += 1

        # MODIFIED FILES
        for file in diff["modified"]:
            if not file.endswith(".py"):
                out.write(f"=== FILE: {file} (MODIFIED - NON PY) ===\n")
                out.write("Changes not analyzed.\n\n")
                files_processed += 1
                continue

            old_src = get_file_from_ref(from_ref, file, root)
            new_src = get_file_from_ref(to_ref, file, root)

            if not old_src or not new_src:
                continue

            if mode == "file":
                out.write(f"=== FILE: {file} (MODIFIED) ===\n")
                out.write("OLD:\n")
                out.write(old_src)
                out.write("\n\nNEW:\n")
                out.write(new_src)
                out.write("\n\n")
                files_processed += 1
                continue

            old_funcs = _extract_functions_with_code(old_src)
            new_funcs = _extract_functions_with_code(new_src)

            all_funcs = set(old_funcs) | set(new_funcs)

            out.write(f"=== FILE: {file} ===\n\n")

            for fn in all_funcs:
                old_f = old_funcs.get(fn)
                new_f = new_funcs.get(fn)

                if old_f and not new_f:
                    out.write(f"--- FUNCTION: {fn} (REMOVED) ---\n")
                    if include_context:
                        out.write(f"# line: {old_f['line']}\n")
                    out.write("OLD:\n")
                    out.write(old_f["code"])
                    out.write("\n\n")

                elif new_f and not old_f:
                    out.write(f"--- FUNCTION: {fn} (ADDED) ---\n")
                    if include_context:
                        out.write(f"# line: {new_f['line']}\n")
                    out.write("NEW:\n")
                    out.write(new_f["code"])
                    out.write("\n\n")

                elif old_f and new_f:
                    if old_f["hash"] != new_f["hash"]:
                        out.write(f"--- FUNCTION: {fn} (UPDATED) ---\n")
                        if include_context:
                            out.write(f"# old line: {old_f['line']}, new line: {new_f['line']}\n")
                        out.write("OLD:\n")
                        out.write(old_f["code"])
                        out.write("\n\nNEW:\n")
                        out.write(new_f["code"])
                        out.write("\n\n")

            files_processed += 1

    return files_processed, output_path