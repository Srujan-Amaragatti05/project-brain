from __future__ import annotations

import json
from pathlib import Path

from lib.atomic_write import safe_write

METADATA_FILE = Path(
    "docs-generated/metadata/commands.json"
)

OUTPUT_DIR = Path(
    "docs-generated/handbook"
)


def render_command(command):

    metadata = command["metadata"]

    lines = [
        f"## {command['command']}",
        "",
        command["help"],
        "",
        f"**Category:** {metadata['category']}",
        "",
    ]

    if command["parameters"]:

        lines.extend(
            [
                "### Parameters",
                "",
                "| Name | Type | Required | Default |",
                "|------|------|----------|---------|",
            ]
        )

        for parameter in command["parameters"]:

            required = (
                "Yes"
                if parameter["default"] == "REQUIRED"
                else "No"
            )

            default = (
                parameter["default"]
                if parameter["default"] is not None
                else "-"
            )

            lines.append(
                f"| {parameter['name']} "
                f"| {parameter['type']} "
                f"| {required} "
                f"| {default} |"
            )

        lines.append("")

    if metadata["examples"]:

        lines.extend(
            [
                "### Examples",
                "",
            ]
        )

        for example in metadata["examples"]:

            lines.append(
                f"```bash\n{example}\n```"
            )

        lines.append("")

    if metadata.get("outputs"):

        lines.extend(
            [
                "### Outputs",
                "",
            ]
        )

        for output in metadata["outputs"]:

            lines.append(
                f"- {output}"
            )

        lines.append("")

    if metadata.get("related"):

        lines.extend(
            [
                "### Related Commands",
                "",
            ]
        )

        for related in metadata["related"]:

            lines.append(
                f"- `{related}`"
            )

        lines.append("")

    lines.extend(
        [
            "---",
            "",
        ]
    )

    return "\n".join(lines)


def generate_cli_reference(commands):

    sections = [
        "# ProjectBrain CLI Reference\n",
        "Auto-generated command reference.\n",
        "---\n",
    ]

    categories = {}

    for command in commands:

        category = command["metadata"]["category"]

        categories.setdefault(
            category,
            []
        ).append(command)

    for category in sorted(categories):

        sections.append(
            f"\n# {category.title()} Commands\n"
        )

        for command in categories[category]:

            sections.append(
                render_command(command)
            )

    return "\n".join(sections)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = json.loads(
        METADATA_FILE.read_text(
            encoding="utf-8"
        )
    )

    commands = data["commands"]

    content = generate_cli_reference(
        commands
    )

    output_file = (
        OUTPUT_DIR /
        "CLI_REFERENCE.md"
    )

    if not safe_write(
        output_file,
        content,
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
