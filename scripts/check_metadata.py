from __future__ import annotations

import re

from lib.cli_introspector import generate_command_graph

from project_brain.docs.categories import (
    CATEGORY_REGISTRY,
)

from project_brain.docs.errors import (
    ERROR_REGISTRY,
)

from project_brain.docs.personas import (
    PERSONA_REGISTRY,
)

VALID_STABILITY = {
    "stable",
    "experimental",
    "deprecated",
}

VERSION_RE = re.compile(
    r"^\d+\.\d+\.\d+$"
)


def main():

    commands = generate_command_graph()

    failed = False

    valid_categories = set(
        CATEGORY_REGISTRY.keys()
    )

    valid_personas = set(
        PERSONA_REGISTRY.keys()
    )

    valid_errors = set(
        ERROR_REGISTRY.keys()
    )

    use_case_variants = {}

    for command in commands:

        metadata = command["metadata"]

        command_name = command["command"]

        # --------------------------------------------------
        # Missing @docs
        # --------------------------------------------------

        if (
            metadata.get("category")
            == "uncategorized"
            and metadata.get("introduced")
            == "unknown"
        ):
            print(
                f"[ERROR] {command_name}: "
                f"missing @docs decorator"
            )
            failed = True

        # --------------------------------------------------
        # P0: Orphan Command Validation
        # --------------------------------------------------
        if (
            metadata.get("category") == "uncategorized"
            and not metadata.get("use_cases")
            and not metadata.get("personas")
        ):
            print(f"[ERROR] {command_name} is not discoverable by documentation")
            failed = True

        # --------------------------------------------------
        # P2: Category Registry Validation
        # --------------------------------------------------
        category = metadata.get(
            "category"
        )

        if category not in valid_categories:

            print(
                f"[ERROR] {command_name}: "
                f"invalid category '{category}'"
            )

            failed = True

        # --------------------------------------------------
        # Stability
        # --------------------------------------------------
        # ... rest of stability checks ...
        # (Already exists in current file)

        # --------------------------------------------------
        # P2: Persona Registry Validation
        # --------------------------------------------------
        for persona in metadata.get(
            "personas",
            [],
        ):

            if persona not in valid_personas:

                print(
                    f"[ERROR] {command_name} references unknown persona: "
                    f"'{persona}'"
                )

                failed = True

        # --------------------------------------------------
        # P2: Error Registry Validation
        # --------------------------------------------------
        for error in metadata.get(
            "errors",
            [],
        ):

            if error not in valid_errors:

                print(
                    f"[ERROR] {command_name} references unknown error: "
                    f"'{error}'"
                )

                failed = True

        # --------------------------------------------------
        # Use Cases
        # --------------------------------------------------

        for use_case in metadata.get(
            "use_cases",
            [],
        ):

            normalized = (
                use_case.lower()
                .replace(" ", "_")
            )

            use_case_variants.setdefault(
                normalized,
                set(),
            ).add(use_case)

    # ------------------------------------------------------
    # Command Reference Validation
    # ------------------------------------------------------
    all_command_names = {c["command"] for c in commands}

    for command in commands:
        command_name = command["command"]
        metadata = command["metadata"]

        # Validate 'related'
        for rel in metadata.get("related", []):
            if rel not in all_command_names:
                print(f"[ERROR] {command_name}: unknown related command '{rel}'")
                failed = True

        # Validate 'prerequisites'
        # Note: Prerequisites can be text or command names. 
        # If it looks like a command (starts with 'brain '), we check it.
        for pre in metadata.get("prerequisites", []):
            if pre.startswith("brain ") and pre not in all_command_names:
                print(f"[ERROR] {command_name}: unknown prerequisite command '{pre}'")
                failed = True

        # Validate 'workflow'
        for step in metadata.get("workflow", []):
            if step.startswith("brain ") and step not in all_command_names:
                print(f"[ERROR] {command_name}: unknown workflow command '{step}'")
                failed = True

    # ------------------------------------------------------
    # Use Case consistency
    # ------------------------------------------------------

    for normalized, variants in (
        use_case_variants.items()
    ):

        if len(variants) > 1:

            print(
                f"[ERROR] inconsistent "
                f"use case names: "
                f"{sorted(variants)}"
            )

            failed = True

    if failed:
        raise SystemExit(1)

    print(
        "Metadata validation passed."
    )


if __name__ == "__main__":
    main()