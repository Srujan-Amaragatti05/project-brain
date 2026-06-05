from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph


GIF_DIR = Path("demo/gifs")


def main():

    commands = generate_command_graph()

    missing = []

    for command in commands:

        gifs = command["metadata"]["gifs"]

        for gif in gifs:

            gif_path = GIF_DIR / gif

            if not gif_path.exists():

                missing.append(
                    {
                        "command": command["command"],
                        "gif": gif,
                    }
                )

    if missing:

        print("\nMissing GIFs detected:\n")

        for item in missing:

            print(
                f"[ERROR] "
                f"{item['command']} "
                f"→ missing {item['gif']}"
            )

        raise SystemExit(1)

    print("All GIF references are valid.")


if __name__ == "__main__":
    main()