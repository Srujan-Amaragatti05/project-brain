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

Use `brain project init` to bootstrap a new workspace when starting a project that requires local intelligence indexing, dependency tracking, or metadata management. This command establishes the foundational directory structure required for subsequent analysis and project health monitoring.

### How it fits in the workflow

This command is the entry point for project-brain. Executing it generates the `.brain/` configuration directory and the `brain.yaml` file, which serve as the foundation for the `brain project analyze` and `brain project doctor` commands. By initializing the project early, you enable the system to track data and state as you build.

### Practical tips

* **Run early:** Execute this command immediately after cloning or creating a project directory to ensure all metadata is tracked from the start.
* **Safe execution:** Because the command is idempotent, it is safe to rerun if you suspect your configuration files have been deleted or corrupted; existing files are preserved during the process.
* **Version control:** It is recommended to add `brain.yaml` to your version control system, while keeping the contents of the `.brain/` directory (specifically `.brain/cache/`) in your `.gitignore` to avoid bloating the repository.

### Common failure causes

* **Permission issues:** If the current user lacks write access to the target directory, the command will fail to create the `.brain/` folder or the `brain.yaml` file.
* **Directory conflicts:** Although the command preserves existing files, a file or directory already existing with the name `.brain` that is not a directory or is locked by another process may prevent initialization.

### FAQ

**Does running this command overwrite my existing work?**
No. The initialization process is designed to be safe; existing files are preserved.

**What specific files are created by this command?**
The command produces the `.brain/` directory, the `.brain/cache/` directory, `data.json`, `index.json`, and the `brain.yaml` configuration file.

**Can I move the .brain directory after initialization?**
It is not recommended, as the CLI expects the configuration to reside in the root of the initialized directory to maintain internal indexing.
