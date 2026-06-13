# `brain diff explain`

> Explain a file or function

---

## Overview

Explain a file or function

---

## When to use

This command is part of the **diff** workflow.

---

## Syntax

```bash
brain diff explain [options]
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `target` | `str` | ✓ | `—` | File path or file:function target |

---

## Examples

```bash
brain diff explain src/main.py
```
```bash
brain diff explain src/main.py:function_name
```

---

## Outputs

_None_

---

## Errors

_None_

---

## Related commands

- `brain diff review`

---

## Notes

- Supports file-level and function-level explanation.

---

## Edge cases

- Function name must exist in file.

---

## Demo

![Demo: explain.gif](../../../demo/gifs/explain.gif)


---

## Usage Guide

### When would I use this?

Use `brain diff explain` when you need a concise, high-level summary of the logic and intent behind a specific file or a discrete function. This command is ideal for onboarding into a new codebase, reviewing complex legacy code, or generating context for documentation when you need to understand what a block of code does without manual line-by-line analysis.

### How it fits in the workflow

This tool acts as an intermediary step during code reviews or refactoring. After checking the differences in a branch, you use `brain diff explain` to gain semantic understanding of changes. Once you grasp the intent, you can transition to `brain diff review` to perform a formal quality and security audit of those specific changes.

### Practical tips

*   **Be specific:** Target functions by name (e.g., `brain diff explain src/utils.py:calculate_tax`) to reduce noise and get a focused explanation of the business logic.
*   **Use before refactoring:** Run the command on a module before modifying it to ensure you have a clear map of the current function dependencies and responsibilities.
*   **Combine with version control:** Pipe the output into a temporary scratchpad when documenting pull requests to quickly populate "Summary of Changes" sections.

### Common failure causes

*   **Non-existent targets:** Providing a function name that has been renamed or deleted in the working directory will result in an error.
*   **Ambiguous names:** If multiple functions share the same name within different scopes or nested classes, the tool may fail to disambiguate, leading to incomplete explanations.
*   **Contextual gaps:** If the logic depends heavily on external environment variables or hidden configuration files, the explanation may miss the "why" behind the implementation.

### FAQ

**Does this command modify my code?**
No, `brain diff explain` is a read-only analysis tool. It generates documentation based on your codebase and has no write permissions.

**Can I use this for non-Python files?**
The command is language-agnostic regarding syntax, but efficacy depends on the tool's ability to parse the specific file structure provided.

**How does this differ from a standard diff?**
A standard diff shows *what* lines changed; `brain diff explain` uses AI to interpret *what those changes achieve* in terms of functional behavior.
