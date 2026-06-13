from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph
from project_brain.docs.personas import PERSONA_REGISTRY
from lib.docs_llm import (
    generate_docs_content,
)
from lib.atomic_write import safe_write


OUTPUT_DIR = Path("docs-generated/personas")


def normalize_description(text: str) -> str:
    """
    Convert multi-line help text into a single line.
    """

    return " ".join(
        text.splitlines()
    ).strip()

def generate_ai_section(
    persona: str,
    info: dict,
    commands: list[str],
) -> str:

    prompt = f"""
Return ONLY markdown.

The first line MUST be:

## Who Is This Persona

Persona:
{persona}

Description:
{info.get("description", "")}

Goals:
{info.get("goals", [])}

Workflow:
{info.get("workflow", [])}

Commands:
{commands}

Do not explain the task.
Do not repeat the input.
Do not list instructions.

Required sections:

## Who Is This Persona

## Typical Responsibilities

## Recommended Approach

## Common Scenarios
"""

    try:

        return generate_docs_content(
            prompt
        )

    except Exception:

        return ""

def build_persona_map(commands: list[dict]) -> dict[str, list[str]]:

    personas: dict[str, list[str]] = {}

    for command in commands:

        metadata = command["metadata"]

        for persona in metadata.get(
            "personas",
            [],
        ):

            personas.setdefault(
                persona,
                [],
            ).append(
                command["command"]
            )

    return personas


def build_command_descriptions(
    commands: list[dict],
) -> dict[str, str]:

    descriptions = {}

    for command in commands:

        help_text = command.get(
            "help",
            "",
        )

        first_line = (
            help_text.splitlines()[0].strip()
            if help_text
            else "-"
        )

        descriptions[
            command["command"]
        ] = normalize_description(
            first_line
        )

    return descriptions


def build_related_personas(
    current_persona: str,
    persona_map: dict[str, list[str]],
) -> list[str]:

    current_commands = set(
        persona_map.get(
            current_persona,
            [],
        )
    )

    related = []

    for persona, commands in persona_map.items():

        if persona == current_persona:
            continue

        overlap = current_commands.intersection(
            commands
        )

        if overlap:
            related.append(
                (
                    persona,
                    len(overlap),
                )
            )

    related.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        persona
        for persona, _
        in related[:3]
    ]


def generate_doc(
    persona: str,
    commands: list[str],
    persona_map: dict[str, list[str]],
    command_descriptions: dict[str, str],
) -> str:

    info = PERSONA_REGISTRY.get(
        persona,
        {},
    )

    description = info.get(
        "description",
        "No description available.",
    )

    goals = info.get(
        "goals",
        [],
    )

    workflow = info.get(
        "workflow",
        [],
    )

    related_personas = build_related_personas(
        persona,
        persona_map,
    )
    ai_section = generate_ai_section(
        persona,
        info,
        commands,
    )

    lines = [
        f"# {persona.title()}",
        "",
    ]

    if ai_section:

        lines.extend(
            [
                ai_section,
                "",
                "---",
                "",
            ]
        )

    lines.extend(
        [
            "## Overview",
            "",
            description,
            "",
            "## Statistics",
            "",
            f"- Recommended Commands: {len(commands)}",
            f"- Workflow Steps: {len(workflow)}",
            "",
            "## Typical Goals",
            "",
        ]
    )
    
    if goals:

        for goal in goals:

            lines.append(
                f"- {goal}"
            )

    else:

        lines.append(
            "_No goals defined._"
        )

    lines.extend(
        [
            "",
            "## Recommended Workflow",
            "",
        ]
    )

    if workflow:

        for index, step in enumerate(
            workflow,
            start=1,
        ):

            lines.append(
                f"{index}. `{step}`"
            )

    else:

        lines.append(
            "_No workflow defined._"
        )

    lines.extend(
        [
            "",
            "## Recommended Commands",
            "",
            "| Command | Description |",
            "|----------|-------------|",
        ]
    )

    for command in sorted(commands):

        description = command_descriptions.get(
            command,
            "-",
        )

        lines.append(
            f"| `{command}` | {description} |"
        )

    lines.extend(
        [
            "",
            "## Related Personas",
            "",
        ]
    )

    if related_personas:

        for related in related_personas:

            lines.append(
                f"- {related.title()}"
            )

    else:

        lines.append(
            "_No related personas found._"
        )

    return "\n".join(lines)


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    commands = generate_command_graph()

    persona_map = build_persona_map(
        commands
    )

    command_descriptions = (
        build_command_descriptions(
            commands
        )
    )

    success = True
    for persona, commands_list in sorted(
        persona_map.items()
    ):

        slug = (
            persona.lower()
            .replace(" ", "_")
        )

        output_file = (
            OUTPUT_DIR
            / f"{slug}.md"
        )

        markdown = generate_doc(
            persona=persona,
            commands=commands_list,
            persona_map=persona_map,
            command_descriptions=command_descriptions,
        )

        if not safe_write(output_file, markdown):
            success = False

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
