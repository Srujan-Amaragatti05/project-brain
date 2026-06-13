from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Callable

def safe_write(
    target: Path,
    content: str,
    validate: Callable[[str], bool] | None = None,
    encoding: str = "utf-8",
    newline: str | None = None,
) -> bool:
    """
    Atomically write content to a target file.
    Writes to a temporary file first, validates, then replaces the target.
    """
    if not content:
        print(f"[SKIPPED] {target.name} (content is empty, old version preserved)")
        return False

    # Validation: Traceback check
    if "Traceback (most recent call last):" in content:
        print(f"[SKIPPED] {target.name} (contains traceback, old version preserved)")
        return False

    # Validation: Placeholder check
    if "{{" in content and "}}" in content:
        print(f"[SKIPPED] {target.name} (contains unresolved placeholders, old version preserved)")
        return False

    # Validation: Markdown heading check
    if target.suffix == ".md":
        if not any(line.strip().startswith("#") for line in content.splitlines()):
            print(f"[SKIPPED] {target.name} (missing markdown heading, old version preserved)")
            return False

    # Validation: JSON parseable
    if target.suffix == ".json":
        try:
            json.loads(content)
        except json.JSONDecodeError:
            print(f"[SKIPPED] {target.name} (invalid JSON, old version preserved)")
            return False

    # Custom validation
    if validate and not validate(content):
        print(f"[SKIPPED] {target.name} (custom validation failed, old version preserved)")
        return False

    temp_file = target.with_suffix(target.suffix + ".tmp")
    try:
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file.write_text(content, encoding=encoding, newline=newline)
        
        # Atomic replace
        temp_file.replace(target)
        print(f"[UPDATED] {target.name}")
        return True
    except Exception as e:
        print(f"[SKIPPED] {target.name} (write failed: {e}, old version preserved)")
        if temp_file.exists():
            temp_file.unlink()
        return False
