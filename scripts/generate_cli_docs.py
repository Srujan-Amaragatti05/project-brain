from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.atomic_write import safe_write

OUTPUT_DIR = Path("docs-generated/commands")


from project_brain.docs.errors import ERROR_REGISTRY

# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------

def render_parameters(parameters: list) -> str:
    if not parameters:
        return "_No parameters._"

    lines = [
        "| Parameter | Type | Required | Default | Description |",
        "|-----------|------|:--------:|---------|-------------|",
    ]
    for p in parameters:
        required = "✓" if p["default"] == "REQUIRED" else ""
        default = p["default"] if p["default"] not in (None, "REQUIRED") else "—"
        lines.append(
            f"| `{p['name']}` | `{p['type']}` | {required} | `{default}` | {p['help']} |"
        )
    return "\n".join(lines)


def render_list(items: list, code: bool = False) -> str:
    if not items:
        return "_None_"
    fmt = "`{}`" if code else "{}"
    return "\n".join(f"- {fmt.format(item)}" for item in items)


def render_gifs(gifs: list) -> str:
    if not gifs:
        return "_No demo available._"
    return "\n\n".join(
        f"![Demo: {gif}](../../../demo/gifs/{gif})" for gif in gifs
    )


def render_errors(errors: list) -> str:
    if not errors:
        return "_None_"
    lines = [
        "| Code | Description |",
        "|------|-------------|",
    ]
    for e in errors:
        error_data = ERROR_REGISTRY.get(e, {})
        desc = error_data.get("message", "See error reference for details.")
        lines.append(f"| `{e}` | {desc} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main markdown builder
# ---------------------------------------------------------------------------

def generate_markdown(command_data: dict) -> str:
    meta = command_data["metadata"]
    title = command_data["command"]
    help_text = command_data["help"].strip() or "No description available."
    category = meta["category"]

    # Build examples block
    examples_block = (
        "\n".join(f"```bash\n{ex}\n```" for ex in meta["examples"])
        if meta["examples"]
        else "_No examples._"
    )

    md = f"""\
# `{title}`

> {help_text.splitlines()[0]}

---

## Overview

{help_text}

---

## When to use

This command is part of the **{category}** workflow.

---

## Syntax

```bash
{title} [options]
```

---

## Parameters

{render_parameters(command_data["parameters"])}

---

## Examples

{examples_block}

---

## Outputs

{render_list(meta["outputs"], code=True)}

---

## Errors

{render_errors(meta["errors"])}

---

## Related commands

{render_list(meta["related"], code=True)}

---

## Notes

{render_list(meta["notes"])}

---

## Edge cases

{render_list(meta["edge_cases"])}

---

## Demo

{render_gifs(meta["gifs"])}
"""
    return md


def generate_slug(command_name: str) -> str:
    return command_name.replace(" ", "_")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    commands = generate_command_graph()

    success = True
    for command in commands:
        category = command["metadata"]["category"]
        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        slug = generate_slug(command["command"])
        output_file = category_dir / f"{slug}.md"
        # newline="\n" ensures LF on all platforms — prevents Windows CRLF drift
        if not safe_write(
            output_file, generate_markdown(command), newline="\n"
        ):
            success = False

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
