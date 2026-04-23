from pathlib import Path
import hashlib
import json
import yaml

from project_brain.core.differ import compute_diff, get_file_from_ref, extract_functions
from project_brain.llm.provider import generate_explanation


def load_config(root: Path):
    config_path = root / "brain.yaml"
    if not config_path.exists():
        return {"llm": {"provider": "none", "model": ""}}

    try:
        return yaml.safe_load(config_path.read_text())
    except Exception:
        return {"llm": {"provider": "none", "model": ""}}


def hash_pair(old: str, new: str, fn: str) -> str:
    return hashlib.sha256((old + new + fn).encode()).hexdigest()


def load_cache(cache_dir: Path, key: str):
    path = cache_dir / f"{key}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None


def cleanup_cache(cache_dir: Path, max_files=1000):
    files = sorted(cache_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)

    if len(files) > max_files:
        for f in files[:len(files) - max_files]:
            f.unlink()


def save_cache(cache_dir: Path, key: str, data: dict):
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.json"
    path.write_text(json.dumps(data, indent=2))
    cleanup_cache(cache_dir)


def build_prompt(old_code: str, new_code: str, fn: str) -> str:
    return f"""
Function: {fn}

Old Code:
{old_code}

New Code:
{new_code}

Explain clearly:
1. What changed
2. Why it matters
3. Impact on system
4. Risks
""".strip()


def safe_extract(source: str):
    try:
        return extract_functions(source)
    except Exception:
        return {}


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

        old_funcs = safe_extract(old_src)
        new_funcs = safe_extract(new_src)

        changed_funcs = list(
            set(fd["added"]) | set(fd["removed"]) | set(fd["modified"])
        )

        if not changed_funcs:
            continue

        for fn in changed_funcs:
            old_code = old_funcs.get(fn, "")
            new_code = new_funcs.get(fn, "")

            key = hash_pair(old_code, new_code, fn)
            cached = load_cache(cache_dir, key)

            if cached:
                results.append({"file": file, "function": fn, **cached})
                continue

            # No LLM configured
            if provider == "none":
                data = {
                    "change": f"Function '{fn}' has code-level changes",
                    "impact": "Behavior may differ depending on logic changes",
                    "risk": "Review required before deployment",
                }
                results.append({"file": file, "function": fn, **data})
                continue

            prompt = build_prompt(old_code, new_code, fn)
            response = generate_explanation(provider, model, prompt)

            if not response:
                data = {
                    "change": "LLM failed to generate explanation",
                    "impact": "Unknown",
                    "risk": "Unknown",
                }
            else:
                data = {"change": response.strip(), "impact": "", "risk": ""}

            save_cache(cache_dir, key, data)

            results.append({"file": file, "function": fn, **data})

    return results
