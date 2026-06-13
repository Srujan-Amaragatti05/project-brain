from __future__ import annotations

import json
from pathlib import Path

from lib.cli_introspector import (
    generate_command_graph,
)


COMMANDS_FILE = Path(
    "docs-generated/metadata/commands.json"
)


def main():

    current = {
        "commands":
        generate_command_graph()
    }

    generated = json.loads(
        COMMANDS_FILE.read_text(
            encoding="utf-8"
        )
    )

    if current != generated:

        print(
            "Metadata drift detected."
        )

        raise SystemExit(1)

    print(
        "Metadata is up-to-date."
    )


if __name__ == "__main__":
    main()