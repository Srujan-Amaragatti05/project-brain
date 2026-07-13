# `brain diff review`

> Explain code changes using LLM

---

## Overview

Explain code changes using LLM

---

## When to use

This command is part of the **diff** workflow.

---

## Syntax

```bash
brain diff review [options]
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
brain diff review
```
```bash
brain diff review HEAD~1 HEAD
```

---

## Outputs

- `.brain/reports/*.json`
- `.brain/reports/*.html`

---

## Errors

| Code | Description |
|------|-------------|
| `INVALID_GIT_REF` | Invalid git reference. |
| `LLM_PROVIDER_FAILURE` | LLM provider request failed. |

---

## Related commands

- `brain diff show`
- `brain export code-changes`

---

## Notes

- Uses configured LLM provider to explain changes.

---

## Edge cases

- Large diffs may increase LLM response time.

---

## Demo

![Demo: diff_review.gif](../../../demo/gifs/diff_review.gif)


---

## Usage Guide

### When would I use this?

Use `brain diff review` when you need to generate a summary or explanation of code modifications between two git references. This is ideal for peer reviews, documentation updates, or preparing release notes by leveraging an LLM to analyze the impact of changes.

### How it fits in the workflow

1.  **Consumption:** The command reads the `git history` between the specified `from_ref` and `to_ref`.
2.  **Processing:** It sends the identified code changes to your configured LLM provider for analysis.
3.  **Production:** It saves the resulting insights into `.brain/reports/*.json` for programmatic use and `.brain/reports/*.html` for human-readable review.

### Practical tips

*   **Specify Ranges:** Use `brain diff review HEAD~1 HEAD` to focus exclusively on the latest commit.
*   **Default Behavior:** If no arguments are provided, the command defaults to the current working state, which is useful for checking uncommitted changes against the last commit.
*   **Version Control:** Run this command before pushing code to generate documentation that stays synchronized with your repository state.

### Common failure causes

*   **INVALID_GIT_REF:** Occurs when the provided `from_ref` or `to_ref` does not exist in the local git history or is formatted incorrectly.
*   **LLM_PROVIDER_FAILURE:** Occurs when the connection to the LLM service is interrupted, authentication is missing, or the service is temporarily unavailable.
*   **Timeout:** Large diffs may exceed typical LLM token limits or processing windows, potentially leading to incomplete reports.

### FAQ

**Does this command modify my source code?**
No, `brain diff review` only reads the git history and generates report files. It does not alter your working directory.

**Where can I find the output?**
All generated reports are stored in the `.brain/reports/` directory in your project root.

**What happens if I don't provide refs?**
The command defaults to the standard git diff behavior, typically comparing your current working tree against the last commit.
