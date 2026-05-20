from __future__ import annotations

from pathlib import Path

from generate_cli_docs import (
    generate_markdown,
    generate_slug,
)

from lib.cli_introspector import generate_command_graph


DOCS_DIR = Path("docs-generated/commands")


def main():

    commands = generate_command_graph()

    drift_found = False

    for command in commands:

        slug = generate_slug(command["command"])

        doc_path = DOCS_DIR / f"{slug}.md"

        expected_content = generate_markdown(command)

        if not doc_path.exists():

            print(f"[ERROR] Missing doc: {doc_path}")

            drift_found = True

            continue

        current_content = doc_path.read_text(
            encoding="utf-8"
        )

        if current_content != expected_content:

            print(f"[ERROR] Drift detected: {doc_path}")

            drift_found = True

    if drift_found:

        print("\nDocumentation drift detected.")

        raise SystemExit(1)

    print("Documentation is up-to-date.")


if __name__ == "__main__":
    main()