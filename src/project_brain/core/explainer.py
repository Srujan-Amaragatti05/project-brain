from pathlib import Path
import hashlib
import json
import re

from project_brain.core.differ import compute_diff, get_file_from_ref, extract_functions
from project_brain.llm.provider import call_llm
from project_brain.core.config_loader import load_config


def hash_pair(old: str, new: str, fn: str) -> str:
    return hashlib.sha256((old + new + fn).encode()).hexdigest()


def load_cache(cache_dir: Path, key: str):
    path = cache_dir / f"{key}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            print(f"⚠️ Corrupted cache ignored: {path}")
            return None
    return None


def cleanup_cache(cache_dir: Path, max_files=1000):
    files = sorted(cache_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)

    if len(files) > max_files:
        for f in files[: len(files) - max_files]:
            f.unlink()


def save_cache(cache_dir: Path, key: str, data: dict):
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.json"
    path.write_text(json.dumps(data, indent=2))
    cleanup_cache(cache_dir)


def build_prompt(old_code: str, new_code: str, fn: str) -> str:
    return f"""
        You are a senior software engineer performing a code review.

        Analyze the function change and return STRICT JSON ONLY.

        DO NOT use markdown.
        DO NOT add text outside JSON.

        Return EXACTLY:

        {{
          "fast": {{
            "change": "(1-2 lines) short line summary",
            "impact": "(1-2 lines) short line impact",
            "risk": "low | medium | high"
          }},
          "detailed": {{
            "change": "Explain what changed at logic level (4-6 lines)",
            "impact": "Explain system-level impact and behavior changes (4-6 lines)",
            "risk": "Explain actual risk reasoning + severity (2-3 lines, end with low|medium|high)"
          }}
        }}

        Rules:
        - fast = minimal summary only
        - detailed MUST include reasoning, not just description
        - DO NOT repeat fast output in detailed
        - risk must still end with one of: low, medium, high

        Function: {fn}

        Old Code:
        {old_code}

        New Code:
        {new_code}
        """.strip()


def safe_extract(source: str):
    try:
        return extract_functions(source)
    except Exception:
        return {}


def explain_diff(from_ref: str, to_ref: str, root: Path):
    config = load_config(root)
    llm_cfg = config.get("llm", {})

    provider = llm_cfg.get("provider", "none")
    model = llm_cfg.get("model", "")
    api_key = llm_cfg.get("api_key", "")

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
                # Case 1: new structured cache
                if "fast" in cached and "detailed" in cached:
                    data = select_output(cached, config)
                    results.append({"file": file, "function": fn, **data})
                    continue
                
                # Case 2: old cache → migrate
                normalized = normalize_cached_data(cached, provider, model, api_key)

                # convert normalized → full structure
                parsed = {
                    "fast": normalized,
                    "detailed": normalized
                }

                save_cache(cache_dir, key, parsed)

                data = select_output(parsed, config)

                results.append({"file": file, "function": fn, **data})
                continue

            # No LLM configured
            if provider == "none":
                data = {
                    "change": f"Function '{fn}' has code-level changes",
                    "impact": "Behavior may differ depending on logic changes",
                    "risk": "medium",
                }
                results.append({"file": file, "function": fn, **data})
                continue

            prompt = build_prompt(old_code, new_code, fn)
            response = call_llm(provider, model, prompt, api_key)
            
            parsed = parse_llm_json(response["output"])
            
            # retry if parsing failed
            if not parsed:
                fix_prompt = f"""
                Convert this into the required JSON structure:
            
                {response["output"]}
            
                Return ONLY:
                {{
                "fast": {{ "change": "...", "impact": "...", "risk": "low|medium|high" }},
                "detailed": {{ "change": "...", "impact": "...", "risk": "low|medium|high" }}
                }}
                """
                response = call_llm(provider, model, fix_prompt, api_key)
                if response["error"]:
                    parsed = None
                else:
                    parsed = parse_llm_json(response["output"])
            
            if parsed:
                data = select_output(parsed, config)
            else:
                data = {
                    "change": "Failed to generate structured output",
                    "impact": "Unknown",
                    "risk": "high"
                }

            if parsed:
                save_cache(cache_dir, key, parsed)

            results.append({"file": file, "function": fn, **data})
    explain_cfg = config.get("explain", {})
    include_risks = explain_cfg.get("include_risks", True)

    if not include_risks:
        for result in results:
            result["risk"] = ""
    return results


def parse_llm_json(response: str):
    import json

    try:
        data = json.loads(response)

        if not all(k in data for k in ["fast", "detailed"]):
            raise ValueError("Missing structure")

        return data

    except Exception as e:
        return None


def is_structured(data: object) -> bool:
    return (
        isinstance(data, dict)
        and "change" in data
        and "impact" in data
        and "risk" in data
        and data["risk"] in ["low", "medium", "high"]
    )


def normalize_cached_data(cached, provider, model, api_key):
    # Already structured
    if is_structured(cached):
        return cached

    # Try JSON parse (maybe partially structured)
    if isinstance(cached, dict) and "change" in cached:
        parsed = parse_llm_json(cached["change"])
        if is_structured(parsed):
            return parsed

        # 🔥 NEW: extract from old text
        extracted = extract_from_old_text(cached["change"])
        if extracted["change"]:
            return extracted

    # LAST fallback → use LLM
    raw_text = str(cached)

    fix_prompt = f"""
        Convert this into STRICT JSON:
        
        {raw_text}
        
        Return ONLY:
        {{
          "change": "...",
          "impact": "...",
          "risk": "low|medium|high"
        }}
        """

    response = call_llm(provider, model, fix_prompt, api_key)
    parsed = parse_llm_json(response["output"])

    if parsed and "fast" in parsed:
        return parsed["detailed"]  # prefer detailed for recovery
    
    return {
        "change": "Failed to normalize cached data",
        "impact": "Unknown",
        "risk": "medium"
    }


def extract_from_old_text(text: str):
    sections = {"change": "", "impact": "", "risk": ""}

    # Normalize
    text = text.replace("\r", "").strip()

    # Patterns
    change_match = re.search(
        r"(?:What changed|### 1\..*?changed)(.*?)(?:###|$)", text, re.S | re.I
    )
    impact_match = re.search(
        r"(?:Why it matters|Impact|### 2\..*?|### 3\..*?)(.*?)(?:###|$)",
        text,
        re.S | re.I,
    )
    risk_match = re.search(r"(?:Risk|### 4\..*?risk)(.*?)(?:###|$)", text, re.S | re.I)

    if change_match:
        sections["change"] = change_match.group(1).strip()

    if impact_match:
        sections["impact"] = impact_match.group(1).strip()

    if risk_match:
        sections["risk"] = risk_match.group(1).strip()

    # Normalize risk
    r = sections["risk"].lower()
    if "high" in r:
        sections["risk"] = "high"
    elif "medium" in r:
        sections["risk"] = "medium"
    else:
        sections["risk"] = "low"

    return sections

def select_output(parsed: dict, config: dict):
    explain_cfg = config.get("explain", {})

    level = explain_cfg.get("level", "detailed")
    include_risks = explain_cfg.get("include_risks", True)

    selected = parsed.get(level, {})

    # ensure fields exist
    change = selected.get("change", "")
    impact = selected.get("impact", "")
    risk = selected.get("risk", "medium")

    if risk not in ["low", "medium", "high"]:
        risk = "medium"

    if not include_risks:
        return {
            "change": change,
            "impact": impact,
            "risk": ""
        }

    return {
        "change": change,
        "impact": impact,
        "risk": risk
    }
