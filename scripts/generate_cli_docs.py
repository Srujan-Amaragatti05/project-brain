from __future__ import annotations

from pathlib import Path

from lib.cli_introspector import generate_command_graph


OUTPUT_DIR = Path("docs-generated/commands")


def render_parameters(parameters):

    if not parameters:
        return "_No parameters._"

    lines = [
        "| Name | Type | Required | Kind | Default | Description |",
        "|---|---|---|---|---|---|",
    ]

    for param in parameters:

        required = "Yes" if param["default"] == "REQUIRED" else "No"

        default = param["default"]

        if default is None:
            default = "-"

        lines.append(
            f"| {param['name']} "
            f"| {param['type']} "
            f"| {required} "
            f"| {param['kind']} "
            f"| {default} "
            f"| {param['help']} |"
        )

    return "\n".join(lines)


def render_list(items):

    if not items:
        return "_None_"

    return "\n".join(f"- {item}" for item in items)


def render_gifs(gifs):

    if not gifs:
        return "_No demo available._"

    return "\n".join(
        f"![Demo](../../demo/gifs/{gif})"
        for gif in gifs
    )


def generate_markdown(command_data):

    metadata = command_data["metadata"]

    title = command_data["command"]

    help_text = command_data["help"]

    if not help_text.strip():
        help_text = "No description available."

    markdown = (
        f"# {title}\n\n"

        f"## Overview\n\n"
        f"{help_text}\n\n"

        f"---\n\n"

        f"## When To Use\n\n"
        f"This command is intended for "
        f"**{metadata['category']}** workflows.\n\n"

        f"---\n\n"

        f"## Syntax\n\n"
        f"```bash\n"
        f"{title}\n"
        f"```\n\n"

        f"---\n\n"

        f"## Arguments\n\n"
        f"{render_parameters(command_data['parameters'])}\n\n"

        f"---\n\n"

        f"## Examples\n\n"
        f"{render_list(metadata['examples'])}\n\n"

        f"---\n\n"

        f"## Expected Outputs\n\n"
        f"{render_list(metadata['outputs'])}\n\n"

        f"---\n\n"

        f"## Error Reference\n\n"
        f"{render_list(metadata['errors'])}\n\n"

        f"---\n\n"

        f"## Related Commands\n\n"
        f"{render_list(metadata['related'])}\n\n"

        f"---\n\n"

        f"## Operational Notes\n\n"
        f"{render_list(metadata['notes'])}\n\n"

        f"---\n\n"

        f"## Edge Cases\n\n"
        f"{render_list(metadata['edge_cases'])}\n\n"

        f"---\n\n"

        f"## Demo\n\n"
        f"{render_gifs(metadata['gifs'])}\n"
    )

    return markdown


def generate_slug(command_name: str):

    return command_name.replace(" ", "_")


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    commands = generate_command_graph()

    for command in commands:

        slug = generate_slug(command["command"])

        output_file = OUTPUT_DIR / f"{slug}.md"

        markdown = generate_markdown(command)

        output_file.write_text(
            markdown,
            encoding="utf-8",
        )

        print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()