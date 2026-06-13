from __future__ import annotations

import re
from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.atomic_write import safe_write

OUTPUT_FILE = Path(
    "docs-generated/architecture/LIFECYCLE.md"
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
        "# Command Lifecycle",
        "",
        "## Dependency Graph",
        "",
        "```mermaid",
        "graph LR",
    ]

    for command in commands:
        cmd_name = command["command"]
        meta = command["metadata"]
        node_id = sanitize_id(cmd_name)
        
        prereqs = meta.get("prerequisites", [])
        for pre in prereqs:
            if pre.startswith("brain "):
                pre_id = sanitize_id(pre)
                lines.append(f"    {pre_id} --> {node_id}")

    lines.extend([
        "```",
        "",
    ])

    for command in commands:

        meta = command["metadata"]

        workflow = meta.get(
            "workflow",
            [],
        )

        prerequisites = meta.get(
            "prerequisites",
            [],
        )

        if not workflow and not prerequisites:
            continue

        lines.append(
            f"## {command['command']}"
        )

        lines.append("")

        if prerequisites:

            lines.append(
                "### Prerequisites"
            )

            lines.append("")

            for item in prerequisites:

                lines.append(
                    f"- {item}"
                )

            lines.append("")

        if workflow:

            lines.append(
                "### Workflow"
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
