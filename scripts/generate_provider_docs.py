from __future__ import annotations

from pathlib import Path

from project_brain.docs.providers import PROVIDER_REGISTRY
from lib.atomic_write import safe_write

OUTPUT_DIR = Path("docs-generated/handbook")

_MODE_BADGE = {
    "offline": "💾 Offline",
    "local":   "🖥️ Local",
    "cloud":   "☁️ Cloud",
}


def render_provider(name: str, info: dict) -> str:
    mode  = _MODE_BADGE.get(info["mode"], info["mode"])
    key   = "Required" if info["requires_api_key"] else "Not required"
    env   = f"`{info['env_var']}`" if "env_var" in info else "—"

    return f"""\
### `{name}`

{info['description']}

| Property | Value |
|----------|-------|
| Mode | {mode} |
| API key | {key} |
| Environment variable | {env} |

---
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sections = [
        "# LLM providers\n",
        "_Auto-generated — do not edit manually._\n",
        "---\n",
        "Set your provider in `brain.yaml`:\n",
        "```yaml\nllm:\n  provider: openai   # none | openai | ollama | gemini | huggingface\n  model: gpt-4o\n```\n",
        "---\n",
    ]
    for name, info in PROVIDER_REGISTRY.items():
        sections.append(render_provider(name, info))

    out = OUTPUT_DIR / "PROVIDERS.md"
    if not safe_write(out, "\n".join(sections), newline="\n"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
