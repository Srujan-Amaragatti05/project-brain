from __future__ import annotations

import json
from pathlib import Path

from lib.cli_introspector import generate_command_graph
from project_brain.docs.errors import ERROR_REGISTRY
from lib.atomic_write import safe_write
from project_brain import __version__

OUTPUT_DIR = Path("docs-generated/metadata")


def _write_json(filename: str, data: object) -> bool:
    out = OUTPUT_DIR / filename
    return safe_write(out, json.dumps(data, indent=2), newline="\n")


def main() -> None:
    commands = generate_command_graph()

    success = True
    if not _write_json("commands.json", {"version": __version__, "commands": commands}):
        success = False

    sidebar: dict[str, list] = {}
    for cmd in commands:
        cat = cmd["metadata"]["category"]
        slug = f"{cat}/{cmd['command'].replace(' ', '_')}"
        sidebar.setdefault(cat, []).append(
            {"title": cmd["command"], "slug": slug}
        )
    if not _write_json("sidebar.json", sidebar):
        success = False

    search_index = [
        # ... (rest of search_index logic)
        {
            "command": cmd["command"],
            "category": cmd["metadata"]["category"],
            "help": cmd["help"],
            "examples": cmd["metadata"]["examples"],
            "errors": cmd["metadata"]["errors"],
            "related": cmd["metadata"]["related"],
            "keywords": [
                cmd["command"],
                cmd["metadata"]["category"],
            
                *cmd["metadata"]["examples"],
                *cmd["metadata"]["errors"],
            
                *cmd["metadata"]["tags"],
                *cmd["metadata"]["personas"],
                *cmd["metadata"]["use_cases"],
            
                *cmd["metadata"]["related"],
            ],
            
        }
        for cmd in commands
    ]
    if not _write_json("search-index.json", search_index):
        success = False
    
    if not _write_json("errors.json", ERROR_REGISTRY):
        success = False

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
