from __future__ import annotations

import inspect
import json

from typer.models import ArgumentInfo, OptionInfo

from project_brain.cli import app
from project_brain.docs.decorators import COMMAND_REGISTRY


def extract_parameters(callback):
    signature = inspect.signature(callback)

    parameters = []

    for name, param in signature.parameters.items():

        default = param.default

        param_data = {
            "name": name,
            "required": default == inspect._empty,
            "default": None,
            "type": "unknown",
            "kind": "argument",
            "help": "",
        }

        if default != inspect._empty:

            if isinstance(default, ArgumentInfo):
                param_data["kind"] = "argument"

                if default.default is ...:
                    param_data["default"] = "REQUIRED"
                else:
                    param_data["default"] = default.default

                param_data["help"] = default.help or ""

            elif isinstance(default, OptionInfo):
                param_data["kind"] = "option"

                if default.default is ...:
                    param_data["default"] = "REQUIRED"
                else:
                    param_data["default"] = default.default

                param_data["help"] = default.help or ""

            else:
                param_data["default"] = str(default)

        annotation = param.annotation

        if annotation != inspect._empty:

            if hasattr(annotation, "__name__"):
                param_data["type"] = annotation.__name__
            else:
                param_data["type"] = str(annotation)

        parameters.append(param_data)

    return parameters


def walk_typer(app_instance, prefix=""):

    commands = []

    registered_commands = getattr(app_instance, "registered_commands", [])
    registered_groups = getattr(app_instance, "registered_groups", [])

    for command_info in registered_commands:

        callback = command_info.callback

        command_name = command_info.name or callback.__name__

        full_command = f"{prefix} {command_name}".strip()

        metadata = COMMAND_REGISTRY.get(full_command)

        if metadata is None:
            metadata = {
                "command": full_command,
                "category": "uncategorized",
                "examples": [],
                "related": [],
                "outputs": [],
                "consumes": [],
                "produces": [],
                "prerequisites": [],
                "use_cases": [],
                "personas": [],
                "tags": [],
                "stability": "experimental",
                "introduced": "unknown",
                "gifs": [],
                "errors": [],
                "notes": [],
                "edge_cases": [],
            }

        commands.append(
            {
                "command": full_command,
                "help": inspect.cleandoc(callback.__doc__ or ""),
                "parameters": extract_parameters(callback),
                "metadata": metadata,
            }
        )

    for group in registered_groups:

        group_name = group.name

        sub_prefix = f"{prefix} {group_name}".strip()

        commands.extend(
            walk_typer(group.typer_instance, sub_prefix)
        )

    return commands


def generate_command_graph():
    return walk_typer(app, prefix="brain")


if __name__ == "__main__":

    data = generate_command_graph()

    print(json.dumps(data, indent=2))