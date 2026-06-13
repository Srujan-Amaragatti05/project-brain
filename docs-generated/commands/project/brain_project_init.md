# `brain project init`

> Initialize project-brain in the current directory

---

## Overview

Initialize project-brain in the current directory

---

## When to use

This command is part of the **project** workflow.

---

## Syntax

```bash
brain project init [options]
```

---

## Parameters

_No parameters._

---

## Examples

```bash
brain project init
```

---

## Outputs

- `.brain/`
- `brain.yaml`

---

## Errors

_None_

---

## Related commands

- `brain project analyze`
- `brain project doctor`

---

## Notes

- Safe to rerun.

---

## Edge cases

- Existing files are preserved.

---

## Demo

![Demo: init.gif](../../../demo/gifs/init.gif)


---

## Usage Guide

### When would I use this?

Use `brain project init` to bootstrap the `project-brain` configuration within your current directory. It is the primary entry point for setting up your project environment to enable subsequent analysis and diagnostic tooling.

### How it fits in the workflow

This command serves as the foundational step in the project lifecycle. After initializing the environment, you would typically run `brain project analyze` to scan your codebase or `brain project doctor` to verify configuration integrity and environment health.

### Practical tips

*   **Idempotency:** The command is safe to rerun at any time. If you have modified your project structure or need to reset internal configurations, executing this command again will align your local directory with the standard `project-brain` requirements.
*   **Non-Destructive:** You do not need to worry about losing work; existing files within your project are strictly preserved during the initialization process.

### Common failure causes

*   **Insufficient Permissions:** Lacking write access to the current directory will prevent the creation of necessary configuration files.
*   **Path Conflicts:** Attempting to run the command in a read-only filesystem or a directory with restricted system locks.

### FAQ

**Will this command overwrite my existing source code?**
No. Existing files are preserved during the initialization process.

**Can I run this command multiple times?**
Yes. It is safe to rerun if configurations need to be refreshed or validated.

**Do I need to run this before analyzing my project?**
Yes, initialization is required to establish the necessary environment state before running `brain project analyze` or `brain project doctor`.
