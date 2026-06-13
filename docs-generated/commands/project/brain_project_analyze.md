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

Use `brain project analyze` when you need to gain a deep, machine-readable understanding of a codebase's structural architecture. This is ideal for generating documentation, identifying architectural bottlenecks, mapping dependency graphs, or onboarding team members to an unfamiliar repository.

### How it fits in the workflow

1. **Initialization:** Run the command at the root of a project to index its entire structure.
2. **Data Persistence:** The tool parses files, classes, and functions via AST (Abstract Syntax Tree), saving the result into `.brain/data.json`.
3. **Integration:** Use the generated JSON as a source of truth for other development tools, IDE plugins, or custom automation scripts that require programmatic access to the project's symbols and metadata.

### Practical tips

* **Target specific directories:** If you only need to analyze a sub-module, pass the path directly (e.g., `brain project analyze ./src/services`) to reduce processing time.
* **Continuous Integration:** Trigger this command in your CI pipeline to track architectural drift or symbol complexity over time.
* **Keep the index clean:** Regularly check `.brain/data.json` into your workflow to ensure team members are referencing the same structural analysis.

### Common failure causes

* **`NOT_GIT_REPO`:** The command requires the target directory to be initialized as a Git repository; ensure `git init` has been executed.
* **Unsupported File Types:** Since the tool relies on AST parsing, files with syntax errors or unsupported languages may result in incomplete metadata extraction.
* **Performance Bottlenecks:** Large-scale repositories with thousands of files may significantly increase analysis time; consider analyzing individual directories if performance degrades.

### FAQ

**Does this command modify my source code?**
No. The command is strictly read-only and uses AST parsing to extract information; it only writes to the local `.brain/` directory.

**Is the generated JSON human-readable?**
Yes, `data.json` is formatted for structured data access, but it is structured clearly enough for developers to review specific class or function metadata manually if necessary.

**Why does it take a long time to run?**
The tool performs a deep parse of the source code to build the AST. Large repositories require more compute cycles to map the relationships between classes and functions.
