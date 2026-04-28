import copy
from pathlib import Path

import yaml

from project_brain.core.logger import log_warning

DEFAULT_CONFIG = {
    "version": "1.0",
    "llm": {
        "provider": "none",
        "model": "",
        "api_key": "",
        "timeout_sec": 60,
    },
    "analysis": {
        "depth": "fast",
        "include_tests": False,
        "ignore": [
            ".brain/",
            ".git/",
            "node_modules/",
            "venv/",
            ".venv/",
            "__pycache__/",
            "env/",
            ".env/",
            "*.egg-info/",
            "tests/",
            "test/",
        ],
    },
    "diff": {
        "mode": "function",
    },
    "export": {
        "full_code": {
            "include_tests": False,
            "max_file_size_kb": 200,
        },
        "manual_add": {
            "allow_duplicates": True,
        },
        "changes": {
            "mode": "function",
            "include_context": True,
            "output_path": ".brain/exports/code_changes.txt",
        },
        "ignore": [
            ".brain/",
            ".git/",
            "node_modules/",
            "venv/",
            ".venv/",
            "__pycache__/",
            "env/",
            ".env/",
            "*.egg-info/",
            "tests/",
            "test/",
        ],
    },
    "explain": {
        "level": "detailed",
        "include_risks": True,
    },
    "output": {
        "format": "text",
    },
}


def merge(default, user):
    result = copy.deepcopy(default)

    for k, v in (user or {}).items():
        if isinstance(v, dict) and k in result:
            result[k] = merge(result[k], v)
        else:
            result[k] = v

    return result


# -----------------------------
# Validation Helpers
# -----------------------------
def _warn(path: str, value, default):
    log_warning(f"Invalid value for {path}='{value}', using default='{default}'")


def _validate_enum(config, path, allowed, default):
    keys = path.split(".")
    node = config
    for k in keys[:-1]:
        node = node.get(k, {})
    last = keys[-1]

    value = node.get(last)

    if value not in allowed:
        _warn(path, value, default)
        node[last] = default


def _validate_int_positive(config, path, default):
    keys = path.split(".")
    node = config
    for k in keys[:-1]:
        node = node.get(k, {})
    last = keys[-1]

    value = node.get(last)

    if not isinstance(value, int) or value <= 0:
        _warn(path, value, default)
        node[last] = default


# -----------------------------
# Main Validation
# -----------------------------
def validate_config(config: dict) -> dict:
    safe = merge(DEFAULT_CONFIG, config or {})

    _validate_enum(
        safe,
        "llm.provider",
        ["none", "openai", "ollama", "gemini", "huggingface"],
        DEFAULT_CONFIG["llm"]["provider"],
    )

    _validate_enum(
        safe,
        "diff.mode",
        ["function", "file"],
        DEFAULT_CONFIG["diff"]["mode"],
    )

    _validate_enum(
        safe,
        "export.changes.mode",
        ["function", "file"],
        DEFAULT_CONFIG["export"]["changes"]["mode"],
    )

    _validate_enum(
        safe,
        "analysis.depth",
        ["fast", "full"],
        DEFAULT_CONFIG["analysis"]["depth"],
    )

    _validate_enum(
        safe,
        "output.format",
        ["text", "json", "markdown"],
        DEFAULT_CONFIG["output"]["format"],
    )

    _validate_int_positive(
        safe,
        "llm.timeout_sec",
        DEFAULT_CONFIG["llm"]["timeout_sec"],
    )

    return safe


# -----------------------------
# Load Config
# -----------------------------
def load_config(root: Path) -> dict:
    path = root / "brain.yaml"

    if not path.exists():
        return DEFAULT_CONFIG

    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except Exception as e:
        log_warning(f"Failed to parse YAML: {str(e)}")
        return DEFAULT_CONFIG

    try:
        merged = merge(DEFAULT_CONFIG, raw)
        return validate_config(merged)
    except Exception as e:
        log_warning(f"Validation failed: {str(e)}")
        return DEFAULT_CONFIG


def dump_config(config: dict) -> str:
    return yaml.dump(config, sort_keys=False)