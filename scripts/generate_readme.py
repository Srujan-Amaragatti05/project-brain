from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph
from lib.docs_llm import generate_docs_content
from lib.atomic_write import safe_write


OUTPUT_FILE = Path(
    "docs-generated/README.md"
)


def count_files(path: str) -> int:

    directory = Path(path)

    if not directory.exists():
        return 0

    return len(
        list(directory.glob("*.md"))
    )


def build_prompt(
    commands: list[dict],
) -> str:

    categories = {}

    for command in commands:

        category = (
            command["metadata"]
            .get(
                "category",
                "uncategorized",
            )
        )

        categories.setdefault(
            category,
            [],
        ).append(
            command["command"]
        )

    category_text = []

    for category, items in sorted(
        categories.items()
    ):

        category_text.append(
            f"{category}: "
            f"{', '.join(items)}"
        )

    return f"""
Return ONLY markdown.

The first line of your response MUST be:

# ProjectBrain Documentation

Do not explain.
Do not analyze.
Do not describe the task.
Do not restate instructions.
Do not mention requirements.

Facts:

Commands: {len(commands)}
Personas: {count_files("docs-generated/personas")}
Use Cases: {count_files("docs-generated/use-cases")}

Categories:

{chr(10).join(category_text)}

Required Sections:

# ProjectBrain Documentation

## What Is ProjectBrain

## Key Capabilities

## Core Workflows

## Documentation Structure

## Command Categories

## Getting Started

## Documentation Statistics
"""
    

def main():

    commands = generate_command_graph()

    prompt = build_prompt(
        commands
    )

    content = generate_docs_content(
        prompt
    )

    if not safe_write(
        OUTPUT_FILE,
        content,
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
