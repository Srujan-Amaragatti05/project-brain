import ast
import subprocess
from pathlib import Path

from project_brain.core.logger import log_error


# -----------------------------
# Git Utilities (SAFE)
# -----------------------------
def run_git_command(args: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",  # 🔥 CRITICAL FIX
            errors="ignore",  # 🔥 PREVENT CRASH
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        log_error(f"Function failed: {str(e)}")
        return None


def is_git_repo(path: Path) -> bool:
    result = run_git_command(["rev-parse", "--is-inside-work-tree"], path)
    return result == "true"


# -----------------------------
# Diff Parsing
# -----------------------------
def parse_name_status(output: str):
    added, modified, deleted = [], [], []

    for line in output.splitlines():
        if not line.strip():
            continue

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue  # 🔥 safe guard

        status, file = parts

        if status == "A":
            added.append(file)
        elif status == "M":
            modified.append(file)
        elif status == "D":
            deleted.append(file)

    return added, modified, deleted


# -----------------------------
# File Content Retrieval
# -----------------------------
def get_file_from_ref(ref: str, file: str, cwd: Path) -> str | None:
    return run_git_command(["show", f"{ref}:{file}"], cwd)


# -----------------------------
# AST Function Extraction
# -----------------------------
def extract_functions(source: str):
    """
    Returns dict:
    {
        "function_name": "function_source_code"
    }
    """
    functions = {}

    try:
        tree = ast.parse(source)
    except Exception:
        return functions  # 🔥 invalid python safety

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            try:
                code = ast.get_source_segment(source, node) or ""
            except Exception:
                code = ""

            functions[node.name] = code

    return functions


# -----------------------------
# Function Diff Logic
# -----------------------------
def diff_functions(old_src: str, new_src: str):
    old_funcs = extract_functions(old_src or "")
    new_funcs = extract_functions(new_src or "")

    old_set = set(old_funcs.keys())
    new_set = set(new_funcs.keys())

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    modified = sorted(
        [fn for fn in old_set & new_set if old_funcs.get(fn) != new_funcs.get(fn)]
    )  # simple heuristic

    return added, removed, modified


# -----------------------------
# Main Diff Engine
# -----------------------------
def compute_diff(from_ref: str, to_ref: str, root: Path):
    diff_output = run_git_command(
        ["log", "--name-status", "--pretty=format:", f"{from_ref}..{to_ref}"], root
    )

    if diff_output is None:
        raise RuntimeError("Git command failed")

    if diff_output.strip() == "":
        return {"added": [], "modified": [], "deleted": [], "function_diffs": []}

    added, modified, deleted = parse_name_status(diff_output)

    function_diffs = []

    for file in modified:
        if not file.endswith(".py"):
            continue

        old_src = get_file_from_ref(from_ref, file, root)
        new_src = get_file_from_ref(to_ref, file, root)

        if old_src is None or new_src is None:
            continue

        fn_added, fn_removed, fn_modified = diff_functions(old_src, new_src)

        function_diffs.append(
            {
                "file": file,
                "added": fn_added,
                "removed": fn_removed,
                "modified": fn_modified,
            }
        )

    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "function_diffs": function_diffs,
    }
