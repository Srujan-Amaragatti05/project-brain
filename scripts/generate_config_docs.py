from __future__ import annotations

from pathlib import Path

from project_brain.docs.config_schema import CONFIG_SCHEMA
from lib.atomic_write import safe_write

OUTPUT_DIR = Path("docs-generated/handbook")


def render_entry(key: str, value: dict) -> str:
    lines = [f"### `{key}`\n", f"{value['description']}\n"]
    lines.append(f"| Property | Value |\n|----------|-------|")
    lines.append(f"| Type | `{value['type']}` |")
    lines.append(f"| Default | `{value['default']}` |")
    if "allowed" in value:
        allowed = " · ".join(f"`{a}`" for a in value["allowed"])
        lines.append(f"| Allowed values | {allowed} |")
    lines.append("\n---")
    return "\n".join(lines)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sections = [
        "# Configuration reference\n",
        "_Auto-generated — do not edit manually._\n",
        "---\n",
        "Edit `brain.yaml` in your project root. Unknown keys are ignored; "
        "invalid values fall back to defaults.\n",
        "---\n",
    ]
    for key, value in CONFIG_SCHEMA.items():
        sections.append(render_entry(key, value))
        sections.append("")

    out = OUTPUT_DIR / "CONFIGURATION.md"
    if not safe_write(out, "\n".join(sections), newline="\n"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
