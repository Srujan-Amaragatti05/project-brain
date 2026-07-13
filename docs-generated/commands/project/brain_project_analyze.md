# `brain project analyze`

> Analyze repository structure using AST parsing.

---

## Overview

Analyze repository structure using AST parsing.

Extracts:
- files
- functions
- classes
- metadata

Stores results inside:
.brain/data.json

Example:
    brain project analyze .

---

## When to use

This command is part of the **project** workflow.

---

## Syntax

```bash
brain project analyze [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `path` | `str` |  | `.` | Repository path to analyze |

---

## Examples

```bash
brain project analyze .
```
```bash
brain project analyze ./src
```

---

## Outputs

- `.brain/data.json`

---

## Errors

| Code | Description |
|------|-------------|
| `NOT_GIT_REPO` | Current directory is not a git repository. |

---

## Related commands

- `brain project summary`
- `brain project doctor`

---

## Notes

- Uses AST parsing for repository analysis.

---

## Edge cases

- Large repositories may take longer to analyze.

---

## Demo

![Demo: analyze.gif](../../../demo/gifs/analyze.gif)


---

## Usage Guide

### When would I use this?

Use `brain project analyze` when you need to gain a structured understanding of a codebase’s architecture, including its classes, functions, and file hierarchy. It is ideal for onboarding into a new project, performing impact analysis before refactoring, or generating metadata for documentation tools.

### How it fits in the workflow

This command acts as the initial ingestion step in your development workflow. By executing it against your source code, you generate a comprehensive `data.json` file inside the `.brain/` directory. Subsequent tools in the suite consume this structured output to provide summaries, dependency graphs, or diagnostic reports without re-parsing the source code each time.

### Practical tips

*   **Target specific modules:** If you are working on a massive repository, run the command on sub-directories (e.g., `brain project analyze ./src/api`) to speed up processing.
*   **Version control:** Ensure your `.brain/` directory is added to your `.gitignore` to prevent tracking generated metadata in your repository.
*   **Automate in CI/CD:** Run this command in your pre-commit hooks or CI pipeline to ensure the stored metadata stays synchronized with your latest code changes.

### Common failure causes

*   **NOT_GIT_REPO:** The command requires the target directory to be initialized as a git repository. Verify your path with `git status` before running the analysis.
*   **Syntax Errors:** Because the tool uses AST parsing, malformed source code that cannot be parsed by the underlying engine will cause the analysis to fail. Ensure your project builds correctly before running the analyzer.
*   **Permission Denied:** Ensure the user running the command has read permissions for the target directory and write permissions for the `.brain/` directory.

### FAQ

**Does this command modify my source code?**
No. It only reads your source files and outputs a data file into the `.brain/` directory.

**How do I handle very large repositories?**
The tool uses AST parsing, which can be resource-intensive. If analysis takes too long, try targeting specific sub-folders rather than the root directory.

**Where is the analysis stored?**
All extracted metadata is saved to `.brain/data.json`.

**What information is extracted?**
The command extracts high-level metadata, including file paths, class definitions, and function signatures.
