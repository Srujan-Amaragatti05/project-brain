from __future__ import annotations

import json
from pathlib import Path


METADATA_FILE = Path(
    "docs-generated/metadata/commands.json"
)

OUTPUT_DIR = Path(
    "docs-generated/handbook"
)


def render_command(command):

    metadata = command["metadata"]

    lines = []

    lines.append(
        f"## {command['command']}\n"
    )

    if command["help"]:
        lines.append(
            f"{command['help']}\n"
        )

    lines.append(
        f"**Category:** {metadata['category']}\n"
    )

    if metadata["examples"]:

        lines.append(
            "\n### Examples\n"
        )

        for example in metadata["examples"]:
            lines.append(
                f"- `{example}`"
            )

    if metadata["related"]:

        lines.append(
            "\n### Related Commands\n"
        )

        for related in metadata["related"]:
            lines.append(
                f"- `{related}`"
            )

    lines.append("\n---\n")

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

    output_file.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"Generated: {output_file}"
    )


if __name__ == "__main__":
    main()