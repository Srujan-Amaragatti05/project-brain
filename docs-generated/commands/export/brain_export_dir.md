# `brain export dir`

> Manually add a directory to export

---

## Overview

Manually add a directory to export

---

## When to use

This command is part of the **export** workflow.

---

## Syntax

```bash
brain export dir [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `path` | `str` | ✓ | `—` | Directory path to include |

---

## Examples

```bash
brain export dir src/
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
- `brain export file`

---

## Notes

- Adds directory recursively into export bundle.

---

## Edge cases

- Large directories increase export size.

---

## Demo

![Demo: export_dir.gif](../../../demo/gifs/export_dir.gif)


---

## Usage Guide

### When would I use this?

Use `brain export dir` when you need to manually include a specific local directory in your export bundle that is not captured by default scanning or when you want to explicitly isolate a sub-folder for targeted documentation or analysis.

### How it fits in the workflow

This command functions as a configuration step. By providing a `path` to a directory, you direct the system to include all files within that directory recursively. The command consumes the specified `directory` and writes the path reference to `.brain/exports/manual_export.txt`, ensuring it is included when the final export bundle is generated.

### Practical tips

*   **Target specific modules:** Use this to export complex sub-modules individually to keep your export bundles manageable.
*   **Verification:** After running the command, check the contents of `.brain/exports/manual_export.txt` to confirm the directory path has been correctly registered.
*   **Version Control:** If your workflow requires reproducible exports, ensure the `.brain/` directory is tracked or shared so the manual export configuration persists.

### Common failure causes

*   **Invalid Path:** Providing a path that does not exist on the local filesystem will result in the directory being ignored during the final bundle creation.
*   **Permissions:** Lack of read access to the specified directory will prevent the files within from being processed.
*   **Path Nesting:** Specifying a parent directory already included in a broader export may lead to redundant file inclusion.

### FAQ

**Does this command export files immediately?**
No, it registers the directory in `manual_export.txt`. The actual export happens when you trigger the final build process.

**Are subdirectories included?**
Yes, the command adds the directory recursively, meaning all nested files and folders within the provided path will be included in the export.

**What happens if the directory is very large?**
Adding large directories will significantly increase the total size of your export bundle, which may impact processing time or exceed size limits for certain output formats.
