from __future__ import annotations

import json
from pathlib import Path

from lib.cli_introspector import generate_command_graph
from project_brain.docs.errors import ERROR_REGISTRY


OUTPUT_DIR = Path("docs-generated/metadata")


def generate_commands_metadata(commands):

    return {
        "commands": commands,
    }


def generate_sidebar(commands):

    sidebar = {}

    for command in commands:

        category = command["metadata"]["category"]

        if category not in sidebar:
            sidebar[category] = []

        sidebar[category].append(
            {
                "title": command["command"],
                "slug": command["command"].replace(" ", "_"),
            }
        )

    return sidebar


def generate_search_index(commands):

    search_entries = []

    for command in commands:

        metadata = command["metadata"]

        search_entries.append(
            {
                "command": command["command"],
                "category": metadata["category"],
                "help": command["help"],
                "examples": metadata["examples"],
                "errors": metadata["errors"],
                "related": metadata["related"],
                "keywords": [
                    command["command"],
                    metadata["category"],
                    *metadata["examples"],
                    *metadata["errors"],
                ],
            }
        )

    return search_entries


def write_json(filename: str, data):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = OUTPUT_DIR / filename

    output_file.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    print(f"Generated: {output_file}")


def main():

    commands = generate_command_graph()

    commands_metadata = generate_commands_metadata(commands)

    sidebar = generate_sidebar(commands)

    search_index = generate_search_index(commands)

    write_json(
        "commands.json",
        commands_metadata,
    )

    write_json(
        "sidebar.json",
        sidebar,
    )

    write_json(
        "search-index.json",
        search_index,
    )

    write_json(
        "errors.json",
        ERROR_REGISTRY,
    )


if __name__ == "__main__":
    main()