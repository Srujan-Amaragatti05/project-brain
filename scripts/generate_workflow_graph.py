from __future__ import annotations

import re
from pathlib import Path
from lib.cli_introspector import generate_command_graph
from lib.atomic_write import safe_write

OUTPUT_FILE = Path("docs-generated/architecture/WORKFLOW_GRAPH.md")

def sanitize_id(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")

def main():
    commands = generate_command_graph()

    lines = [
        "# Workflow Relationship Graph",
        "",
        "This graph shows how commands are linked through the `workflow` metadata.",
        "",
        "```mermaid",
        "graph TD",
    ]

    found_edges = set()

    for command in commands:
        cmd_name = command["command"]
        meta = command["metadata"]
        node_id = sanitize_id(cmd_name)
        
        workflow = meta.get("workflow", [])
        if not workflow:
            continue

        lines.append(f"    {node_id}[\"{cmd_name}\"]")

        for i in range(len(workflow) - 1):
            source = workflow[i]
            target = workflow[i+1]
            
            source_id = sanitize_id(source)
            target_id = sanitize_id(target)
            
            edge = (source_id, target_id)
            if edge not in found_edges:
                lines.append(f"    {source_id} --> {target_id}")
                found_edges.add(edge)

    lines.append("```")

    if not safe_write(OUTPUT_FILE, "\n".join(lines)):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
