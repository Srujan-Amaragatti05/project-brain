from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.atomic_write import safe_write


OUTPUT_FILE = Path(
    "docs-generated/COMMAND_MATRIX.md"
)


def main():

    commands = generate_command_graph()

    lines = [
        "# Command Matrix",
        "",
        "| Command | Category | Personas | Use Cases |",
        "|----------|----------|----------|----------|",
    ]

    for command in commands:

        meta = command["metadata"]

        personas = ", ".join(
            meta.get(
                "personas",
                [],
            )
        )

        use_cases = ", ".join(
            meta.get(
                "use_cases",
                [],
            )
        )

        lines.append(
            f"| `{command['command']}` "
            f"| {meta.get('category', '-')} "
            f"| {personas or '-'} "
            f"| {use_cases or '-'} |"
        )

    if not safe_write(
        OUTPUT_FILE,
        "\n".join(lines),
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
