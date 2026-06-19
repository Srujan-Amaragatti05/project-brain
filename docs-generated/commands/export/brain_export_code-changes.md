# `brain export code-changes`

> Export changed code between two git references

---

## Overview

Export changed code between two git references

---

## When to use

This command is part of the **export** workflow.

---

## Syntax

```bash
brain export code-changes [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `from_ref` | `str` | ✓ | `—` | Starting git reference |
| `to_ref` | `str` | ✓ | `—` | Ending git reference |

---

## Examples

```bash
brain export code-changes HEAD~1 HEAD
```

---

## Outputs

- `.brain/exports/code-changes.txt`

---

## Errors

| Code | Description |
|------|-------------|
| `INVALID_GIT_REF` | Invalid git reference. |

---

## Related commands

- `brain diff show`
- `brain diff review`

---

## Notes

- Exports changed files between git references.

---

## Edge cases

- Requires valid git history.

---

## Demo

![Demo: code_changes.gif](../../../demo/gifs/code_changes.gif)


---

## Usage Guide

### When would I use this?

Use this command when you need to generate a comprehensive record of source code modifications between two specific points in your git history. It is ideal for audit trails, documenting feature implementation progress, or extracting specific deltas for external review.

### How it fits in the workflow

1.  **Preparation**: Ensure your local repository has the necessary commit history for `from_ref` and `to_ref`.
2.  **Execution**: Run `brain export code-changes <from_ref> <to_ref>` to generate the diff report.
3.  **Consumption**: Access the generated file at `.brain/exports/code-changes.txt` for integration into reports, documentation, or change logs.

### Practical tips

*   Use tags or commit hashes for precise control over the range.
*   Check the contents of `.brain/exports/` immediately after execution to verify the export was generated successfully.
*   Combine this command with `brain diff show` if you need to inspect the changes in your terminal before exporting them to a file.

### Common failure causes

*   **INVALID_GIT_REF**: Provided references do not exist in the repository or are incorrectly formatted.
*   **Missing History**: The repository lacks the required commit history to compute the difference between the specified points.
*   **Permission Denied**: The system lacks write access to the `.brain/` directory.

### FAQ

**Where is the output saved?**
The output is saved to `.brain/exports/code-changes.txt`.

**What does this command consume?**
It consumes your local `git history`.

**Can I specify an output path?**
No, the command consistently produces the output in the predefined `.brain/exports/` location.

**What happens if the git references are the same?**
If `from_ref` and `to_ref` point to the same commit, the exported file will be empty as there are no changes to report.
