from pathlib import Path
import hashlib
import ast
from datetime import datetime

# EXCLUDE_DIRS = {".brain", ".git", "node_modules", "venv", ".venv", "__pycache__", "env", ".env", "*.egg-info"}
# EXCLUDE_FILES = {".env", ".gitignore", "README.md", "LICENSE", "CHANGELOG.md"}


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


def is_binary(path: Path):
    try:
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    except:
        return True


def analyze_project(root_path: Path, ignore_patterns=None, include_tests=False):
    root_path = root_path.resolve()

    files_data = []
    functions = []
    classes = []
    files_path = []

    for path in root_path.rglob("*"):
        if path.is_dir():
            continue

        if should_skip(path, ignore_patterns):
            continue
        
        if is_binary(path):
            continue
        
        if not include_tests and "test" in path.name.lower():
            continue
        # files_path.append(path)
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
            files_path.append(rel_path)

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
        "classes": classes,
    }, files_path