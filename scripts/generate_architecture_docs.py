from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.atomic_write import safe_write

from project_brain.docs.config_schema import (
    CONFIG_SCHEMA,
)
from project_brain.docs.errors import (
    ERROR_REGISTRY,
)
from project_brain.docs.providers import (
    PROVIDER_REGISTRY,
)


OUTPUT_DIR = Path(
    "docs-generated/architecture"
)


def generate_system_overview():

    commands = generate_command_graph()

    categories = {}

    for command in commands:

        category = (
            command["metadata"]
            .get(
                "category",
                "uncategorized",
            )
        )

        categories.setdefault(
            category,
            []
        ).append(command)

    lines = [
        "# System Overview",
        "",
        "## Statistics",
        "",
        f"- Total Commands: {len(commands)}",
        f"- Providers: {len(PROVIDER_REGISTRY)}",
        f"- Error Codes: {len(ERROR_REGISTRY)}",
        f"- Config Keys: {len(CONFIG_SCHEMA)}",
        "",
        "---",
        "",
        "## Command Categories",
        "",
    ]

    for category in sorted(categories):

        lines.extend(
            [
                f"### {category.title()}",
                "",
            ]
        )

        for command in sorted(
            categories[category],
            key=lambda x: x["command"],
        ):

            lines.append(
                f"- `{command['command']}`"
            )

        lines.append("")

    return "\n".join(lines)


def generate_providers_doc():

    lines = [
        "# Providers",
        "",
    ]

    for name, data in sorted(
        PROVIDER_REGISTRY.items()
    ):

        lines.extend(
            [
                f"## {name}",
                "",
                f"- Mode: {data['mode']}",
                f"- Requires API Key: {data.get('requires_api_key', False)}",
                f"- Description: {data.get('description', '')}",
                "",
            ]
        )

    return "\n".join(lines)


def generate_errors_doc():

    lines = [
        "# Error Codes",
        "",
    ]

    for name, data in sorted(
        ERROR_REGISTRY.items()
    ):

        lines.extend(
            [
                f"## {name}",
                "",
                data["message"],
                "",
            ]
        )

    return "\n".join(lines)


def generate_config_doc():

    lines = [
        "# Configuration",
        "",
        "This document describes all available configuration settings in `brain.yaml`.",
        "",
    ]

    for key, data in sorted(CONFIG_SCHEMA.items()):
        lines.extend([
            f"## `{key}`",
            "",
            data.get("description", "No description available."),
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Type | `{data['type']}` |",
            f"| Default | `{data['default']}` |",
        ])
        
        if "allowed" in data:
            allowed = ", ".join(f"`{a}`" for a in data["allowed"])
            lines.append(f"| Allowed | {allowed} |")
        
        lines.append("")

    return "\n".join(lines)


def write_file(
    name: str,
    content: str,
) -> bool:

    path = OUTPUT_DIR / name

    return safe_write(path, content)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    success = True
    if not write_file(
        "SYSTEM_OVERVIEW.md",
        generate_system_overview(),
    ):
        success = False

    if not write_file(
        "PROVIDERS.md",
        generate_providers_doc(),
    ):
        success = False

    if not write_file(
        "ERRORS.md",
        generate_errors_doc(),
    ):
        success = False

    if not write_file(
        "CONFIG.md",
        generate_config_doc(),
    ):
        success = False

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
