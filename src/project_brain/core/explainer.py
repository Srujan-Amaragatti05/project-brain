from pathlib import Path
import hashlib
import json

from project_brain.core.differ import (
    compute_diff,
    get_file_from_ref,
    extract_functions
)
from project_brain.llm.provider import generate_explanation
import yaml


def load_config(root: Path):
    config_path = root / "brain.yaml"
    if not config_path.exists():
        return {"llm": {"provider": "none", "model": ""}}

    try:
        return yaml.safe_load(config_path.read_text())
    except Exception:
        return {"llm": {"provider": "none", "model": ""}}


def hash_pair(old: str, new: str) -> str:
    return hashlib.sha256((old + new).encode()).hexdigest()


def load_cache(cache_dir: Path, key: str):
    path = cache_dir / f"{key}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None


def save_cache(cache_dir: Path, key: str, data: dict):
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.json"
    path.write_text(json.dumps(data, indent=2))


def build_prompt(old_code: str, new_code: str) -> str:
    return f"""
Old Code:
{old_code}

New Code:
{new_code}

Explain:
- What changed
- Why it matters
- Impact on system
- Risks
""".strip()


def explain_diff(from_ref: str, to_ref: str, root: Path):
    config = load_config(root)
    provider = config.get("llm", {}).get("provider", "none")
    model = config.get("llm", {}).get("model", "")

    diff = compute_diff(from_ref, to_ref, root)
    if not diff:
        return None

    results = []
    cache_dir = root / ".brain" / "cache"

    for fd in diff["function_diffs"]:
        file = fd["file"]

        old_src = get_file_from_ref(from_ref, file, root) or ""
        new_src = get_file_from_ref(to_ref, file, root) or ""

        old_funcs = extract_functions(old_src)
        new_funcs = extract_functions(new_src)

        changed_funcs = (
            set(fd["added"]) |
            set(fd["removed"]) |
            set(fd["modified"])
        )

        for fn in changed_funcs:
            key = hash_pair(old_src, new_src)
            cached = load_cache(cache_dir, key)

            if cached:
                results.append({
                    "file": file,
                    "function": fn,
                    **cached
                })
                continue

            if provider == "none":
                data = {
                    "change": "Function changed",
                    "impact": "Unknown",
                    "risk": "Unknown"
                }
                results.append({
                    "file": file,
                    "function": fn,
                    **data
                })
                continue

            prompt = build_prompt(old_src, new_src)
            response = generate_explanation(provider, model, prompt)

            if not response:
                data = {
                    "change": "LLM failed",
                    "impact": "Unknown",
                    "risk": "Unknown"
                }
            else:
                # simple parsing fallback
                data = {
                    "change": response.strip(),
                    "impact": "",
                    "risk": ""
                }

            save_cache(cache_dir, key, data)

            results.append({
                "file": file,
                "function": fn,
                **data
            })

    return results