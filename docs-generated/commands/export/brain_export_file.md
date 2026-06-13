# `brain export file`

> Manually add a single file to export

---

## Overview

Manually add a single file to export

---

## When to use

This command is part of the **export** workflow.

---

## Syntax

```bash
brain export file [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `path` | `str` | ✓ | `—` | File path to include |

---

## Examples

```bash
brain export file src/main.py
```

---

## Outputs

- `.brain/exports/manual_export.txt`

---

## Errors

_None_

---

## Related commands

- `brain export full-code`
- `brain export dir`

---

## Notes

- Adds a single file into export bundle.

---

## Edge cases

- File must exist.

---

## Demo

_No demo available._


---

## Usage Guide

### When would I use this?

Use `brain export file` when you need to selectively include a single, specific file in your export bundle rather than generating a full repository dump or an entire directory. This is ideal for sharing individual configuration files, specific logic modules, or debugging isolated code segments.

### How it fits in the workflow

This command acts as a surgical tool within your versioning or documentation pipeline. By integrating it into your workflow, you maintain a clean export structure, allowing you to curate the content of your output manually. It typically serves as a building block for automated scripts where only unique or modified files need to be bundled for review or transfer.

### Practical tips

*   **Specify Paths Carefully:** Always provide the relative or absolute path from the project root to ensure the correct file is targeted.
*   **Sequential Execution:** You can run the command multiple times to build a custom bundle of disparate files that do not share a common parent directory.
*   **Validation:** Use `ls` or your IDE’s file explorer to verify the path before executing the command to avoid "file not found" errors.

### Common failure causes

*   **Missing File:** The command will fail if the provided file path does not exist on the filesystem.
*   **Permission Denied:** Attempting to export a file that your user account does not have read access to.
*   **Incorrect Pathing:** Providing a path relative to a subdirectory instead of the project root can result in a failure to locate the target.

### FAQ

**Can I export multiple files at once using this command?**
No, this command is designed to process exactly one file per invocation. For multiple files, you may need to chain the commands or use `brain export dir`.

**Does this command overwrite existing exports?**
It adds the specified file to the active export bundle. Ensure your bundle management system handles versioning or appending correctly.

**What happens if I target a directory instead of a file?**
The command is strictly defined for files; targeting a directory may result in an error or unexpected behavior depending on the underlying implementation. Use `brain export dir` for folder-level operations.
