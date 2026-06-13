from __future__ import annotations

from pathlib import Path

from project_brain.docs.errors import ERROR_REGISTRY
from lib.atomic_write import safe_write

OUTPUT_DIR = Path("docs-generated/handbook")

_SEVERITY_BADGE = {
    "high":   "🔴 High",
    "medium": "🟡 Medium",
    "low":    "🟢 Low",
}


def render_error(code: str, error: dict) -> str:
    severity = _SEVERITY_BADGE.get(error["severity"], error["severity"])
    causes = "\n".join(f"- {c}" for c in error["cause"])
    fixes  = "\n".join(f"- {f}" for f in error["fix"])
    cmds   = " · ".join(f"`{c}`" for c in error["related_commands"])

    return f"""\
### `{code}`

**Severity:** {severity}

**Message:** _{error['message']}_

**Causes**

{causes}

**How to fix**

{fixes}

**Relevant commands:** {cmds}

---
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sections = [
        "# Error reference\n",
        "_Auto-generated — do not edit manually._\n",
        "---\n",
    ]
    for code, error in ERROR_REGISTRY.items():
        sections.append(render_error(code, error))

    out = OUTPUT_DIR / "ERROR_REFERENCE.md"
    if not safe_write(out, "\n".join(sections), newline="\n"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
