from pathlib import Path
import hashlib
import ast
from datetime import datetime

EXCLUDE_DIRS = {".brain", ".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", "eggs", "parts", "sdist", "develop-eggs", "env"}
EXCLUDE_FILES = {".env"}


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""


def analyze_python_file(path: Path, rel_path: str):
    functions = []
    classes = []

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception:
        return functions, classes

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "arguments": [arg.arg for arg in node.args.args],
                "line": node.lineno,
                "file": rel_path
            })

        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "file": rel_path
            })

    return functions, classes


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def analyze_project(root_path: Path):
    root_path = root_path.resolve()

    files_data = []
    functions = []
    classes = []

    for path in root_path.rglob("*"):
        if path.is_dir():
            continue

        if should_skip(path):
            continue

        try:
            rel_path = str(path.relative_to(root_path))
            stat = path.stat()

            file_info = {
                "path": rel_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "sha256": sha256_file(path)
            }

            files_data.append(file_info)

            if path.suffix == ".py":
                fn, cls = analyze_python_file(path, rel_path)
                functions.extend(fn)
                classes.extend(cls)

        except Exception:
            continue  # skip unreadable files safely

    return {
        "project": {
            "root": str(root_path),
            "total_files": len(files_data)
        },
        "files": files_data,
        "functions": functions,
        "classes": classes
    }