from __future__ import annotations

import json
from pathlib import Path

from lib.cli_introspector import generate_command_graph


OUTPUT_FILE = Path(
    "docs-generated/metadata/relationships.json"
)


def build_relationships():

    commands = generate_command_graph()

    relationships = {}

    for command in commands:

        meta = command["metadata"]

        relationships[
            command["command"]
        ] = {
            "related": meta.get(
                "related",
                [],
            ),
            "consumes": meta.get(
                "consumes",
                [],
            ),
            "produces": meta.get(
                "produces",
                [],
            ),
            "prerequisites": meta.get(
                "prerequisites",
                [],
            ),
            "use_cases": meta.get(
                "use_cases",
                [],
            ),
            "personas": meta.get(
                "personas",
                [],
            ),
            "tags": meta.get(
                "tags",
                [],
            ),
        }

    return relationships


def main():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    relationships = build_relationships()

    OUTPUT_FILE.write_text(
        json.dumps(
            relationships,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Generated: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()