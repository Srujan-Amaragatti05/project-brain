from __future__ import annotations

import re
from pathlib import Path

from lib.cli_introspector import (
    generate_command_graph,
)
from lib.atomic_write import safe_write

OUTPUT_FILE = Path(
    "docs-generated/architecture/DATAFLOW.md"
)


def sanitize_id(text: str) -> str:
    """
    Sanitize a string for use as a Mermaid node ID.
    Replaces non-alphanumeric characters with underscores.
    """
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")


def main():

    commands = generate_command_graph()

    lines = [
        "# Data Flow",
        "",
        "## System Graph",
        "",
        "```mermaid",
        "graph TD",
    ]

    # Build graph nodes and edges
    for command in commands:
        cmd_name = command["command"]
        meta = command["metadata"]
        
        # Clean name for Mermaid
        node_id = sanitize_id(cmd_name)
        lines.append(f"    {node_id}[\"{cmd_name}\"]")

        for prod in meta.get("produces", []):
            # Find commands that consume this
            for consumer in commands:
                if prod in consumer["metadata"].get("consumes", []):
                    cons_id = sanitize_id(consumer["command"])
                    lines.append(f"    {node_id} -- \"{prod}\" --> {cons_id}")

    lines.extend([
        "```",
        "",
    ])

    for command in commands:

        meta = command["metadata"]

        produces = meta.get(
            "produces",
            [],
        )

        consumes = meta.get(
            "consumes",
            [],
        )

        workflow = meta.get(
            "workflow",
            [],
        )

        prerequisites = meta.get(
            "prerequisites",
            [],
        )

        if (
            not produces
            and not consumes
            and not workflow
            and not prerequisites
        ):
            continue

        lines.append(
            f"## {command['command']}"
        )

        lines.append("")

        if prerequisites:

            lines.append(
                "**Prerequisites**"
            )

            lines.append("")

            for item in prerequisites:

                lines.append(
                    f"- {item}"
                )

            lines.append("")

        if consumes:

            lines.append(
                "**Consumes**"
            )

            lines.append("")

            for item in consumes:

                lines.append(
                    f"- {item}"
                )

            lines.append("")

        if produces:

            lines.append(
                "**Produces**"
            )

            lines.append("")

            for item in produces:

                lines.append(
                    f"- {item}"
                )

            lines.append("")

        if workflow:

            lines.append(
                "**Workflow**"
            )

            lines.append("")

            for index, step in enumerate(
                workflow,
                start=1,
            ):

                lines.append(
                    f"{index}. `{step}`"
                )

            lines.append("")

    if not safe_write(
        OUTPUT_FILE,
        "\n".join(lines),
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
