from __future__ import annotations

import json
from pathlib import Path
from lib.cli_introspector import generate_command_graph

OUTPUT_FILE = Path("docs-generated/METADATA_COVERAGE.md")

def calculate_coverage(commands):
    total = len(commands)
    if total == 0:
        return {}

    stats = {
        "examples": 0,
        "use_cases": 0,
        "personas": 0,
        "errors": 0,
        "outputs": 0,
        "consumes": 0,
        "produces": 0,
        "workflow": 0,
        "gifs": 0,
    }

    details = []

    for command in commands:
        meta = command["metadata"]
        cmd_stats = {}
        for key in stats.keys():
            val = meta.get(key, [])
            if val:
                stats[key] += 1
                cmd_stats[key] = "✓"
            else:
                cmd_stats[key] = "✗"
        
        details.append({
            "command": command["command"],
            **cmd_stats
        })

    return {
        "total": total,
        "averages": {k: (v / total) * 100 for k, v in stats.items()},
        "details": details
    }

def main():
    commands = generate_command_graph()
    coverage = calculate_coverage(commands)

    lines = [
        "# Metadata Coverage Report",
        "",
        f"Total Commands: {coverage['total']}",
        "",
        "## Overall Completion",
        "",
        "| Field | Completion % |",
        "|-------|--------------|",
    ]

    for field, percent in coverage["averages"].items():
        lines.append(f"| {field.title()} | {percent:.1f}% |")

    lines.extend([
        "",
        "## Command Details",
        "",
        "| Command | Ex | UC | Per | Err | Out | Cons | Prod | WF | GIF |",
        "|---------|:--:|:--:|:---:|:---:|:---:|:----:|:----:|:--:|:---:|",
    ])

    for d in coverage["details"]:
        lines.append(
            f"| `{d['command']}` "
            f"| {d['examples']} | {d['use_cases']} | {d['personas']} | {d['errors']} "
            f"| {d['outputs']} | {d['consumes']} | {d['produces']} | {d['workflow']} | {d['gifs']} |"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {OUTPUT_FILE}")

    # --- P0: Generate coverage.json ---
    coverage_json = {}
    for command in commands:
        meta = command["metadata"]
        coverage_json[command["command"]] = {
            "examples": bool(meta.get("examples")),
            "workflow": bool(meta.get("workflow")),
            "personas": bool(meta.get("personas")),
            "use_cases": bool(meta.get("use_cases")),
            "gifs": bool(meta.get("gifs")),
            "errors": bool(meta.get("errors")),
        }

    json_out = Path("docs-generated/metadata/coverage.json")
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(coverage_json, indent=2), encoding="utf-8")
    print(f"Generated: {json_out}")

if __name__ == "__main__":
    main()
