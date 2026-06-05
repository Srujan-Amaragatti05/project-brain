from __future__ import annotations

import hashlib
import json
from pathlib import Path

import ollama

from lib.cli_introspector import generate_command_graph


DOCS_DIR = Path("docs-generated/commands")
CACHE_DIR = Path("docs-generated/cache")


MODEL = "llama3"


def generate_slug(command_name: str):

    return command_name.replace(" ", "_")


def compute_hash(command_data):

    serialized = json.dumps(
        command_data,
        sort_keys=True,
    )

    return hashlib.md5(
        serialized.encode()
    ).hexdigest()


def build_prompt(command):

    metadata = command["metadata"]

    return f"""
You are a senior CLI documentation engineer.

Use ONLY the information provided.

Never invent:
- flags
- commands
- options
- files
- outputs
- errors

Return valid markdown only.

Command:
{command["command"]}

Purpose:
{command["help"]}

Parameters:
{json.dumps(command["parameters"], indent=2)}

Metadata:
{json.dumps(metadata, indent=2)}

Generate:

## Typical Workflow

Explain how developers usually use this command.

## Best Practices

Provide practical recommendations.

## Common Mistakes

List realistic user mistakes.

## Troubleshooting Guidance

Explain how to resolve common issues.

## FAQ

Provide 3 concise question-answer pairs.
"""


def load_cache(cache_file):

    if not cache_file.exists():
        return None

    return json.loads(
        cache_file.read_text(
            encoding="utf-8"
        )
    )


def save_cache(cache_file, data):

    cache_file.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def enhance_command(command):

    slug = generate_slug(command["command"])

    cache_file = CACHE_DIR / f"{slug}.json"

    command_hash = compute_hash(command)

    cached = load_cache(cache_file)

    if cached and cached["hash"] == command_hash:

        print(f"[CACHE HIT] {command['command']}")

        return cached["content"]

    print(f"[GENERATING] {command['command']}")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": build_prompt(command),
            }
        ],
    )

    content = response["message"]["content"]

    save_cache(
        cache_file,
        {
            "hash": command_hash,
            "content": content,
        },
    )

    return content


def append_ai_section(doc_path, ai_content):

    original = doc_path.read_text(
        encoding="utf-8"
    )

    if "## AI Insights" in original:
        return

    enhanced = (
        original
        + "\n\n---\n\n"
        + "## Usage Guide\n\n"
        + ai_content
        + "\n"
    )

    doc_path.write_text(
        enhanced,
        encoding="utf-8",
    )


def main():

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    commands = generate_command_graph()

    for command in commands:

        slug = generate_slug(command["command"])

        doc_path = DOCS_DIR / f"{slug}.md"

        if not doc_path.exists():

            print(f"[SKIP] Missing doc: {doc_path}")

            continue

        ai_content = enhance_command(command)

        append_ai_section(
            doc_path,
            ai_content,
        )

        print(f"[ENHANCED] {doc_path}")


if __name__ == "__main__":
    main()