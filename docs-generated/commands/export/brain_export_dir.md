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

_No demo available._


---

## Usage Guide

### When would I use this?

Use `brain export dir` when you need to include an entire directory, including all its subdirectories and files, into your current export bundle. This is ideal for sharing modular components, source code trees, or structured documentation folders without having to specify each file individually.

### How it fits in the workflow

This command acts as a batch processor in your export pipeline. After initializing your export context, you define the scope of your data by pointing to specific paths. By adding a directory, you ensure that all relevant project logic contained within that folder is bundled for analysis or external portability. It complements `brain export file` by handling bulk project structures, bridging the gap between isolated file exports and a `brain export full-code` operation.

### Practical tips

*   **Path Precision:** Always provide the path relative to your current working directory to ensure the command correctly maps the folder structure.
*   **Selective Bundling:** Use this command to isolate specific modules (e.g., `brain export dir src/components/`) rather than the entire project when you want to focus on a particular architectural feature.
*   **Verification:** After running the command, check the current export manifest to ensure the directory was added as expected.

### Common failure causes

*   **Invalid Pathing:** Providing a path that does not exist or has incorrect permissions will cause the command to fail.
*   **Recursive Depth:** While the command handles recursion, extremely deep nested structures may hit system path length limits on certain operating systems.
*   **Access Denied:** Attempting to export directories that contain system-protected files or files currently locked by other processes.

### FAQ

**Does this command add new files created in the directory later?**
No, the command adds the directory contents as they exist at the moment of execution. If you add new files to the directory afterward, you may need to re-run the command or update the bundle.

**Will this exceed my export size limit?**
It might. Because this command adds directories recursively, large folders can significantly increase the total export size. Always verify the size of your target directory before exporting.

**Can I exclude specific files within the added directory?**
This command adds the entire directory structure. If you need to exclude specific files, add the directory first and then perform individual removals or use a more granular export strategy.
