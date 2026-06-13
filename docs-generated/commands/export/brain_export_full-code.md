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

![Demo: full_code.gif](../../../demo/gifs/full_code.gif)


---

## Usage Guide

### When would I use this?

Use `brain export full-code` when you need to provide a complete context of your repository to an AI model for analysis, refactoring, or documentation generation. It is ideal for large-scale architectural reviews, debugging complex cross-file dependency issues, or preparing a codebase for migration.

### How it fits in the workflow

This command acts as a data preparation layer. By consolidating the codebase into a single, structured, AI-readable file, it bypasses the limitations of manual file uploading. Once generated, the resulting file serves as the primary input for AI-driven code reviews, documentation extraction, or automated system explanations.

### Practical tips

* **Ignore redundant files:** Ensure your `.gitignore` is correctly configured before running the export to prevent the inclusion of unnecessary build artifacts, logs, or dependency folders that waste tokens.
* **Review the output:** Scan the generated file briefly before uploading to a chat interface to confirm that no sensitive credentials or environment variables were captured.
* **Chunking:** For exceptionally large repositories, consider using `brain export dir` to export specific modules if the full export exceeds your target AI's context window.

### Common failure causes

* **Memory constraints:** Large repositories can cause system timeouts or memory overflows during the file compilation process.
* **Permission errors:** Attempting to export directories or files that the current user does not have read access to will result in partial or empty exports.
* **Encoding conflicts:** Files with non-standard character encodings may cause the export process to stall or generate corrupted output text.

### FAQ

**Does this command compress the files?**  
No, `brain export full-code` produces a structured plaintext file. Compression is not applied to ensure immediate readability by LLMs.

**Will this include files listed in `.gitignore`?**  
No, the command respects standard ignore files to ensure the export remains focused on relevant source code.

**How does this differ from `brain export dir`?**  
`brain export full-code` processes the entire repository starting from the root directory, whereas `brain export dir` is scoped to a specific subdirectory.

**Is the generated output file proprietary?**  
No, it is a standard structured text file designed to be portable and compatible with all major AI analysis platforms.
