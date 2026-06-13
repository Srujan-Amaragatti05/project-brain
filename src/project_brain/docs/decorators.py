from __future__ import annotations

from typing import Any, Callable

COMMAND_REGISTRY: dict[str, dict[str, Any]] = {}


def docs(
    *,
    command: str,
    category: str,

    examples: list[str] | None = None,
    related: list[str] | None = None,

    outputs: list[str] | None = None,

    consumes: list[str] | None = None,
    produces: list[str] | None = None,

    prerequisites: list[str] | None = None,

    use_cases: list[str] | None = None,

    personas: list[str] | None = None,

    tags: list[str] | None = None,

    gifs: list[str] | None = None,
    errors: list[str] | None = None,
    notes: list[str] | None = None,
    edge_cases: list[str] | None = None,
    workflow: list[str] | None = None,
    stability: str = "stable",
    introduced: str = "0.1.0"
):
    """
    Attach structured documentation metadata to CLI commands.
    """

    def wrapper(func: Callable):
        metadata = {
        "command": command,
        "category": category,
        "examples": examples or [],
        "related": related or [],
        "outputs": outputs or [],
        "consumes": consumes or [],
        "produces": produces or [],
        "prerequisites": prerequisites or [],
        "use_cases": use_cases or [],
        "personas": personas or [],
        "tags": tags or [],
        "stability": stability,
        "introduced": introduced,
        "gifs": gifs or [],
        "errors": errors or [],
        "notes": notes or [],
        "edge_cases": edge_cases or [],
        "workflow": workflow or [],
    }

        COMMAND_REGISTRY[command] = metadata

        setattr(func, "__docs_metadata__", metadata)

        return func

    return wrapper