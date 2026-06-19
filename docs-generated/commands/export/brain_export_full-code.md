# `brain export full-code`

> Export entire codebase into structured file

---

## Overview

Export entire codebase into structured file

---

## When to use

This command is part of the **export** workflow.

---

## Syntax

```bash
brain export full-code [options]
```

---

## Parameters

_No parameters._

---

## Examples

```bash
brain export full-code
```

---

## Outputs

- `.brain/exports/full_code.txt`

---

## Errors

_None_

---

## Related commands

- `brain export file`
- `brain export dir`

---

## Notes

- Exports repository into AI-friendly format.

---

## Edge cases

- Large repositories generate large export files.

---

## Demo

![Demo: export_full_code.gif](../../../demo/gifs/export_full_code.gif)


---

## Usage Guide

### When would I use this?

Use `brain export full-code` when you need to provide an entire codebase as context to an AI model for deep analysis, architectural review, or refactoring assistance. It is ideal for scenarios where global code knowledge is required to maintain consistency across the project.

### How it fits in the workflow

1.  **Preparation**: Navigate to the root directory of your project.
2.  **Execution**: Run `brain export full-code` to aggregate the repository source code.
3.  **Consumption**: The system produces `.brain/exports/full_code.txt`, which acts as the source for AI-assisted documentation, debugging, or code generation tasks.
4.  **Integration**: Upload or paste the resulting file into your AI interface to perform holistic analysis.

### Practical tips

*   **Cleanup**: Remove unnecessary files (like build artifacts or dependency folders) before running the command to ensure the exported content remains relevant.
*   **Version Control**: Always verify that your repository is in a clean state before exporting to ensure the generated file reflects the desired source code version.
*   **Large Repositories**: Be aware that large repositories will generate large export files; consider using `brain export file` or `brain export dir` if you only require specific modules.

### Common failure causes

*   **Insufficient Permissions**: Failure to write to the `.brain/exports/` directory due to system-level access restrictions.
*   **Disk Space**: Running the command on a repository that exceeds available storage when converted into a single text file.
*   **Non-standard Structure**: Attempting to run the command outside of a recognized repository root.

### FAQ

**Q: Where is the generated file located?**
A: The output is saved to `.brain/exports/full_code.txt` within your project root.

**Q: Does this export my local configuration files?**
A: It exports the repository source code; ensure sensitive configuration files (e.g., `.env`) are ignored or excluded to maintain security.

**Q: How do I handle very large projects that exceed context windows?**
A: If the generated `full_code.txt` is too large for your AI's context window, use the related commands `brain export file` or `brain export dir` to export specific components.
