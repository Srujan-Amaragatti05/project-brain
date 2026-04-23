from pathlib import Path
import json
from collections import Counter


def load_data(root: Path):
    data_path = root / ".brain" / "data.json"
    if not data_path.exists():
        return None

    try:
        with data_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("❌ Corrupted data.json. Run 'brain analyze .' again.")
        return None


def compute_basic_stats(data: dict):
    total_files = data.get("project", {}).get("total_files", 0)
    total_functions = len(data.get("functions", []))
    total_classes = len(data.get("classes", []))

    return total_files, total_functions, total_classes


def get_top_files(functions: list, limit: int = 5):
    counter = Counter()

    for fn in functions:
        file = fn.get("file")
        if file:
            counter[file] += 1

    return counter.most_common(limit)


def get_key_classes(classes: list, limit: int = 5):
    result = []
    for cls in classes[:limit]:
        result.append((cls.get("name"), cls.get("file")))
    return result


def generate_overview(files: list):
    names = " ".join([f.get("path", "").lower() for f in files])

    parts = []

    if "auth" in names:
        parts.append("authentication")
    if "db" in names or "database" in names:
        parts.append("database layer")
    if "api" in names or "routes" in names:
        parts.append("API/backend")

    if "cli" in names:
        parts.append("CLI tool")
        
    if not parts:
        return "General purpose codebase with modular structure."

    if len(parts) == 1:
        return f"Project includes {parts[0]} functionality."

    return f"Project includes {', '.join(parts[:-1])} and {parts[-1]}."
    

def format_summary(root: Path, data: dict):
    total_files, total_functions, total_classes = compute_basic_stats(data)

    top_files = get_top_files(data.get("functions", []))
    key_classes = get_key_classes(data.get("classes", []))
    overview = generate_overview(data.get("files", []))

    lines = []

    lines.append(f"Project: {root}")
    lines.append("")
    lines.append(f"Files: {total_files}")
    lines.append(f"Functions: {total_functions}")
    lines.append(f"Classes: {total_classes}")
    lines.append("")
    lines.append("Top Files:")
    lines.append("")

    if top_files:
        for file, count in top_files:
            lines.append(f"* {file} ({count} functions)")
    else:
        lines.append("* None")

    lines.append("")
    lines.append("Key Classes:")
    lines.append("")

    if key_classes:
        for name, file in key_classes:
            lines.append(f"* {name} ({file})")
    else:
        lines.append("* None")

    lines.append("")
    lines.append(f"Overview: {overview}")

    return "\n".join(lines)