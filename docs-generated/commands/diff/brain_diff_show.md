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

![Demo: diff.gif](../../../demo/gifs/diff.gif)


---

## Usage Guide

### When would I use this?

Use `brain diff show` to perform a semantic analysis of code changes between two git references. This command is ideal for understanding the logic behind a commit or a branch merge rather than relying on standard line-by-line diffs.

### How it fits in the workflow

1.  **Code Review:** Use this to gain a high-level overview of complex changes before performing a line-by-line manual audit.
2.  **Context Switching:** Use it when returning to a long-running feature branch to quickly summarize the semantic intent of your recent work.
3.  **Debugging:** Use it to isolate changes in specific functions across commits to identify when a particular behavior was introduced.

### Practical tips

*   **Specify references:** Run `brain diff show HEAD~3 HEAD` to review the semantic evolution of the last three commits.
*   **Compare branches:** Use `brain diff show main dev` to see the functional differences between your current development branch and the production baseline.
*   **Target scopes:** Leverage the built-in support for function-level diffs when you need to ignore boilerplate changes and focus on logic updates.

### Common failure causes

*   **NOT_GIT_REPO:** The command is being executed outside of a initialized git directory.
*   **INVALID_GIT_REF:** One or both of the provided commit hashes, tags, or branch names do not exist in the current repository history.
*   **Insufficient History:** The repository lacks enough commit history to perform a meaningful comparison between the specified references.

### FAQ

**Q: Does this replace `git diff`?**  
A: No, it complements it. While `git diff` shows textual changes, `brain diff show` highlights the semantic impact of the code changes.

**Q: Can I use this for non-git directories?**  
A: No, this command requires a valid git repository to track references and history.

**Q: Does it support file-level filtering?**  
A: Yes, the tool supports both file-level and function-level modes to help you narrow down the analysis to specific areas of your codebase.
