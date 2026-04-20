import subprocess
from pathlib import Path
import ast


def run_git_command(args, cwd: Path):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception:
        return None


def is_git_repo(path: Path) -> bool:
    result = run_git_command(["rev-parse", "--is-inside-work-tree"], path)
    return result is not None and result.strip() == "true"


def parse_name_status(output: str):
    added, modified, deleted = [], [], []

    for line in output.splitlines():
        if not line.strip():
            continue

        status, file = line.split(maxsplit=1)

        if status == "A":
            added.append(file)
        elif status == "M":
            modified.append(file)
        elif status == "D":
            deleted.append(file)

    return added, modified, deleted


def get_file_from_ref(ref: str, file: str, cwd: Path):
    content = run_git_command(["show", f"{ref}:{file}"], cwd)
    return content


def extract_functions(source: str):
    names = set()

    try:
        tree = ast.parse(source)
    except Exception:
        return names

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)

    return names


def diff_functions(old_src: str, new_src: str):
    old_funcs = extract_functions(old_src or "")
    new_funcs = extract_functions(new_src or "")

    added = sorted(list(new_funcs - old_funcs))
    removed = sorted(list(old_funcs - new_funcs))
    modified = sorted(list(old_funcs & new_funcs))

    return added, removed, modified


def compute_diff(from_ref: str, to_ref: str, root: Path):
    diff_output = run_git_command(
        ["diff", "--name-status", from_ref, to_ref],
        root
    )

    if diff_output is None:
        return None

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

        function_diffs.append({
            "file": file,
            "added": fn_added,
            "removed": fn_removed,
            "modified": fn_modified
        })

    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "function_diffs": function_diffs
    }