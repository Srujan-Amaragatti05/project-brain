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

_No demo available._


---

## Usage Guide

### When would I use this?

Use this command when you need to extract or isolate specific files that have been modified between two points in your git history. This is particularly useful for generating patches, preparing code bundles for audits, or archiving changesets for documentation purposes.

### How it fits in the workflow

1.  **Code Review**: Isolate changes for external review without sharing the entire repository.
2.  **Deployment Prep**: Identify and export only the files modified since the last production release.
3.  **CI/CD Pipelines**: Automate the collection of changed artifacts to trigger targeted builds.
4.  **Version Archiving**: Create snapshots of code differences for specific project milestones.

### Practical tips

*   **Specify Ref Ranges**: Always define the range clearly. For example, use `brain export code-changes main feature-branch` to export all changes made in your feature branch relative to `main`.
*   **Verify History**: Ensure your local repository is updated with `git fetch` before running the command to ensure the references exist.
*   **Pipeline Integration**: Pipe the output of this command into a compression utility if you need to generate a portable archive of the changed code.

### Common failure causes

*   **INVALID_GIT_REF**: Occurs when one or both of the provided git references do not exist in the local repository history.
*   **Disconnected History**: Attempting to export changes between two commits that do not share a common ancestor.
*   **Uncommitted Changes**: Changes not yet committed to the git history cannot be exported using reference-based commands.

### FAQ

**Q: Does this command modify my local repository?**
A: No, `brain export code-changes` is a read-only operation that extracts file contents based on git references.

**Q: Can I use commit hashes instead of branch names?**
A: Yes, the command accepts any valid git reference, including full commit hashes, short hashes, or tag names.

**Q: What happens if a file was deleted between the two references?**
A: The tool will identify the deletion; check the command output to see how deleted files are handled within the export package.
