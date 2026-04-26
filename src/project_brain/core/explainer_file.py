from pathlib import Path
import ast
import yaml

from project_brain.llm.provider import generate_explanation  # type: ignore


def load_config(root: Path):
    default = {
        "llm": {"provider": "none", "model": ""},
        "explain": {"level": "basic", "include_risks": True}
    }

    config_path = root / "brain.yaml"
    if not config_path.exists():
        return default

    try:
        data = yaml.safe_load(config_path.read_text())
        return data or default
    except Exception:
        return default


def extract_file_structure(source: str):
    functions = []
    classes = []

    try:
        tree = ast.parse(source)
    except Exception:
        return functions, classes

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return functions, classes


def extract_function(source: str, func_name: str):
    try:
        tree = ast.parse(source)
    except Exception:
        return None

    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            start = node.lineno - 1
            end = getattr(node, "end_lineno", start + 1)
            code = "\n".join(lines[start:end])

            return {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "line": node.lineno,
                "code": code
            }

    return None


def explain_file(root: Path, file_path: str):
    config = load_config(root)
    provider = config["llm"]["provider"]
    model = config["llm"]["model"]
    api_key = config["llm"]["api_key"]

    path = root / file_path
    if not path.exists():
        return "❌ File not found"

    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "❌ Unable to read file"

    functions, classes = extract_file_structure(source)

    if provider == "none":
        lines = []
        lines.append(f"File: {file_path}\n")
        lines.append("Summary:")
        lines.append(f"- Functions: {len(functions)}")
        lines.append(f"- Classes: {len(classes)}\n")

        lines.append("Functions:\n")
        for fn in functions:
            lines.append(f"* {fn}")

        return "\n".join(lines)

    prompt = f"""
Explain this file: purpose, main components, data flow, key risks.

{source}
""".strip()

    response = generate_explanation(provider, model, prompt, api_key)

    return f"File: {file_path}\n\nSummary:\n{response.strip()}"


def explain_function(root: Path, file_path: str, func_name: str):
    config = load_config(root)
    provider = config["llm"]["provider"]
    model = config["llm"]["model"]
    api_key = config["llm"]["api_key"]
    include_risks = config.get("explain", {}).get("include_risks", True)

    path = root / file_path
    if not path.exists():
        return "❌ File not found"

    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "❌ Unable to read file"

    fn = extract_function(source, func_name)
    if not fn:
        return "❌ Function not found"

    if provider == "none":
        lines = []
        lines.append(f"Function: {fn['name']}\n")
        lines.append(f"Args: {', '.join(fn['args'])}")
        lines.append(f"Line: {fn['line']}")
        return "\n".join(lines)

    risk_part = ", edge cases, risks" if include_risks else ""

    prompt = f"""
Explain this function: purpose, inputs, outputs, logic{risk_part}.

{fn['code']}
""".strip()

    response = generate_explanation(provider, model, prompt, api_key)

    return f"Function: {fn['name']}\n\n{response.strip()}"