from __future__ import annotations

from lib.cli_introspector import generate_command_graph


def main():

    commands = generate_command_graph()

    command_names = {
        command["command"]
        for command in commands
    }

    failed = False

    for command in commands:

        metadata = command["metadata"]

        references = []

        references.extend(
            metadata.get(
                "related",
                []
            )
        )

        references.extend(
            metadata.get(
                "prerequisites",
                []
            )
        )

        for reference in references:

            if reference not in command_names:

                print(
                    f"[ERROR] "
                    f"{command['command']} "
                    f"references unknown command: "
                    f"{reference}"
                )

                failed = True

    if failed:
        raise SystemExit(1)

    print(
        "Relationship validation passed."
    )


if __name__ == "__main__":
    main()