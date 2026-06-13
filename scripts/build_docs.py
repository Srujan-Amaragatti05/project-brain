from __future__ import annotations

import subprocess
import sys

SCRIPTS = [
    "scripts/generate_cli_docs.py",
    "scripts/generate_metadata.py",

    "scripts/generate_handbook.py",
    "scripts/generate_error_handbook.py",
    "scripts/generate_provider_docs.py",
    "scripts/generate_config_docs.py",

    "scripts/generate_workflows.py",

    "scripts/generate_relationships.py",
    "scripts/generate_personas.py",
    "scripts/generate_architecture_docs.py",
    "scripts/generate_use_cases.py",
    "scripts/generate_command_matrix.py",
    "scripts/generate_dataflow_docs.py",
    "scripts/generate_lifecycle_docs.py",
    "scripts/generate_workflow_graph.py",

    "scripts/generate_web_docs.py",

    "scripts/check_coverage.py",
    "scripts/check_metadata.py",
    "scripts/check_relationships.py",
    "scripts/check_metadata_drift.py",
    "scripts/generate_readme.py",
    "scripts/validate_docs.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\nRunning: {script}")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            raise SystemExit(result.returncode)
    print("\nDocumentation build completed.")


if __name__ == "__main__":
    main()
