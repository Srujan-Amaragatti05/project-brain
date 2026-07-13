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

![Demo: export_file.gif](../../../demo/gifs/export_file.gif)


---

## Usage Guide

### When would I use this?

Use this command when you need to selectively include a specific file in an export bundle rather than exporting an entire directory or the full codebase. It is ideal for sharing individual components, configuration files, or documentation pieces that are critical for an external review.

### How it fits in the workflow

The command functions as a surgical tool during the export phase of your project. By running `brain export file <path>`, you populate the `.brain/exports/manual_export.txt` manifest. This workflow allows you to curate exactly which files are bundled for transport or backup, ensuring that only necessary single files are staged for the final output.

### Practical tips

*   **Verify path accuracy:** Use tab-completion or check your current working directory with `ls` before executing to ensure the path is correct.
*   **Sequential additions:** You can run the command multiple times to append multiple individual files to the `manual_export.txt` manifest.
*   **Pre-export staging:** Run this command while building your export bundle to keep your manifest clean and minimal.

### Common failure causes

*   **Non-existent file:** The command will fail if the provided path does not point to an existing file on the local filesystem.
*   **Permission errors:** Lack of read access to the target file will prevent it from being added to the export bundle.
*   **Typographical errors:** Incorrect relative paths or missing extensions will result in a failure to locate the intended resource.

### FAQ

**Does this command overwrite existing exports?**
No, it appends the file to the current `manual_export.txt` manifest.

**Can I export multiple files at once?**
The command is designed for a single file path at a time. To add multiple files, execute the command sequentially for each file.

**Where does the file go?**
The file reference is added to `.brain/exports/manual_export.txt`.

**What happens if I enter an invalid path?**
The system will return an error indicating that the file must exist for the export process to proceed.
