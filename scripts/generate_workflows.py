from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.docs_llm import (
    generate_docs_content,
)
from lib.atomic_write import safe_write

DOCS_DIR = Path("docs-generated/commands")
CACHE_DIR = Path(".brain/docs_cache")

# Must stay in sync with check_doc_drift._USAGE_GUIDE_MARKER
_SEPARATOR = "\n\n---\n\n"
_GUIDE_HEADER = "## Usage Guide\n\n"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_slug(command_name: str) -> str:
    return command_name.replace(" ", "_")


def compute_hash(command_data: dict) -> str:
    serialized = json.dumps(command_data, sort_keys=True)
    return hashlib.md5(serialized.encode()).hexdigest()


def _strip_preamble(text: str) -> str:

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"^```(?:markdown)?\n",
        "",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"\n```$",
        "",
        text,
    )

    start_markers = [
        "### When would I use this?",
        "## Who Is This Persona",
        "## Business Goal",
        "# ProjectBrain Documentation",
    ]

    positions = []

    for marker in start_markers:

        pos = text.find(marker)

        if pos >= 0:
            positions.append(pos)

    if positions:

        text = text[min(positions):]

    return text.strip()


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def load_cache(cache_file: Path) -> dict | None:
    if not cache_file.exists():
        return None
    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_cache(cache_file: Path, data: dict) -> None:
    cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def build_prompt(command: dict) -> str:
    meta = command["metadata"]
    params = command["parameters"]
    
    params_str = json.dumps([
        {
            "name": p["name"],
            "type": p["type"],
            "required": p["default"] == "REQUIRED",
            "help": p["help"]
        } for p in params
    ], indent=2)

    return f"""
Generate markdown only.

Do not explain instructions.
Do not describe the task.
Do not repeat the prompt.
Do not include:
- Role
- Task
- Constraints
- Command
- Purpose
- Category
- Examples
- Related
- Errors
- Notes
- Edge Cases

Never write:
"Here is the markdown"
"Below is the documentation"
"Certainly"
"Sure"

Use ONLY supplied metadata and parameters. Do NOT invent flags or options. Use 'consumes' and 'produces' information when generating practical recommendations. Never invent outputs. Never invent side effects.

Command Metadata

Command: {command["command"]}
Purpose: {command["help"]}
Category: {meta["category"]}
Parameters: {params_str}
Consumes: {json.dumps(meta.get("consumes", []))}
Produces: {json.dumps(meta.get("produces", []))}
Examples: {json.dumps(meta["examples"])}
Related: {json.dumps(meta["related"])}
Errors: {json.dumps(meta["errors"])}
Notes: {json.dumps(meta["notes"])}
Edge Cases: {json.dumps(meta["edge_cases"])}

Start immediately with:

### When would I use this?

Required Sections:

### When would I use this?

### How it fits in the workflow

### Practical tips

### Common failure causes

### FAQ
"""


# ---------------------------------------------------------------------------
# Enhancement
# ---------------------------------------------------------------------------

def enhance_command(command: dict) -> str:

    slug = generate_slug(
        command["command"]
    )

    cache_file = (
        CACHE_DIR
        / f"{slug}.json"
    )

    command_hash = compute_hash(
        command
    )

    cached = load_cache(
        cache_file
    )

    if (
        cached
        and cached.get("hash")
        == command_hash
    ):

        print(
            f"[CACHE HIT] "
            f"{command['command']}"
        )

        return cached["content"]

    print(
        f"[GENERATING] "
        f"{command['command']}"
    )

    prompt = build_prompt(
        command
    )

    try:

        content = (
            generate_docs_content(
                prompt
            )
        )

    except Exception as exc:

        print(
            f"[FAILED] "
            f"{command['command']}"
        )

        print(exc)

        return ""

    content = _strip_preamble(
        content or ""
    )

    save_cache(
        cache_file,
        {
            "hash":
                command_hash,
            "content":
                content,
        },
    )

    return content


def append_ai_section(doc_path: Path, ai_content: str) -> bool:
    original = doc_path.read_text(encoding="utf-8")

    # Idempotent: skip if already enhanced
    if "## Usage Guide" in original:
        return True

    enhanced = original + _SEPARATOR + _GUIDE_HEADER + ai_content + "\n"
    # newline="\n" keeps LF on Windows — required for check_doc_drift to pass
    return safe_write(doc_path, enhanced, newline="\n")


def main() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    commands = generate_command_graph()

    success = True
    for command in commands:
        category = command["metadata"]["category"]
        slug = generate_slug(command["command"])
        doc_path = DOCS_DIR / category / f"{slug}.md"

        if not doc_path.exists():
            print(f"[SKIP]       Missing doc: {doc_path}")
            continue

        ai_content = enhance_command(command)
        if ai_content:
            if not append_ai_section(doc_path, ai_content):
                success = False
        else:
            print(f"[WARNING]    AI enhancement skipped for {slug} (no provider/keys or generation failed).")

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
