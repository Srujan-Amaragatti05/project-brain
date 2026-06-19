# `brain diff show`

> Show semantic git differences between references.

---

## Overview

Show semantic git differences between references.

---

## When to use

This command is part of the **diff** workflow.

---

## Syntax

```bash
brain diff show [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `from_ref` | `str` |  | `—` | Starting git reference |
| `to_ref` | `str` |  | `—` | Ending git reference |

---

## Examples

```bash
brain diff show
```
```bash
brain diff show HEAD~3 HEAD
```
```bash
brain diff show main dev
```

---

## Outputs

_None_

---

## Errors

| Code | Description |
|------|-------------|
| `INVALID_GIT_REF` | Invalid git reference. |
| `NOT_GIT_REPO` | Current directory is not a git repository. |

---

## Related commands

- `brain diff review`
- `brain export code-changes`

---

## Notes

- Supports file-level and function-level diff modes.

---

## Edge cases

- Requires valid git history.

---

## Demo

![Demo: diff_show.gif](../../../demo/gifs/diff_show.gif)


---

## Usage Guide

### When would I use this?

Use `brain diff show` to identify semantic changes between two git references. It is ideal for code reviews, auditing logic shifts, or summarizing modifications between branches, commits, or tags.

### How it fits in the workflow

This command consumes the `git repository` and `git history` to generate a `terminal diff report`. It acts as an intermediary step during development cycles, positioned between initial code modification and final review, helping developers isolate logic changes rather than just raw character differences.

### Practical tips

*   **Compare recent progress:** Use `brain diff show HEAD~3 HEAD` to review the last three commits for a quick pulse check on your current feature branch.
*   **Branch validation:** Use `brain diff show main dev` to see exactly what logic has drifted between your development and production branches before merging.
*   **Targeted analysis:** Utilize the file-level or function-level modes to filter noise and focus specifically on high-impact areas of the codebase.

### Common failure causes

*   **NOT_GIT_REPO:** Executing the command outside of a directory initialized with git.
*   **INVALID_GIT_REF:** Providing reference strings (such as commit hashes, branch names, or tags) that do not exist or are malformed within the current history.
*   **Insufficient history:** Attempting to diff references that do not share a common ancestor or exist in a shallow clone where history has been truncated.

### FAQ

**Does this command show raw line changes or semantic changes?**
The command focuses on semantic differences, meaning it identifies changes in code structure, function logic, and behavioral patterns rather than simple character-based line additions or deletions.

**Can I use this without arguments?**
Yes, running `brain diff show` without parameters defaults to standard reference comparisons, typically between the last commit and the current working state.

**Does this produce permanent side effects?**
No, this is a read-only operation. It only produces a `terminal diff report` and does not modify the git repository or state.
