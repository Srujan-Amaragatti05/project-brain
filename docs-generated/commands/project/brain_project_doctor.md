# `brain project doctor`

> Repository diagnostics and environment health checks.

---

## Overview

Repository diagnostics and environment health checks.

---

## When to use

This command is part of the **project** workflow.

---

## Syntax

```bash
brain project doctor [options]
```

---

## Parameters

_No parameters._

---

## Examples

```bash
brain project doctor
```

---

## Outputs

- `terminal diagnostics`

---

## Errors

| Code | Description |
|------|-------------|
| `NOT_GIT_REPO` | Current directory is not a git repository. |

---

## Related commands

- `brain project init`
- `brain project analyze`

---

## Notes

- Runs repository and environment diagnostics.

---

## Edge cases

- Some checks depend on internet connectivity.

---

## Demo

![Demo: doctor.gif](../../../demo/gifs/doctor.gif)


---

## Usage Guide

### When would I use this?

Use `brain project doctor` whenever you suspect repository misconfiguration, environment inconsistencies, or need a baseline health assessment of your project workspace. It serves as a diagnostic tool to verify that the environment meets all requirements before performing critical operations.

### How it fits in the workflow

This command acts as a pre-flight check. It is best utilized:
* Immediately after cloning a repository to ensure the local environment is correctly set up.
* Before executing `brain project analyze` to guarantee that data sources and configurations are accessible.
* After updating local dependencies or configuration files to confirm that changes have not introduced environment conflicts.

### Practical tips

* Run `brain project doctor` in the root directory of your project to ensure the tool correctly identifies the repository configuration.
* Pipe the output to a log file or share the generated health report with team members when troubleshooting environment-specific issues.
* Use this command as a mandatory step in your local development cycle to prevent runtime failures caused by misaligned configurations.

### Common failure causes

* **NOT_GIT_REPO**: The command is being executed outside of a valid Git repository; ensure you are in the project root.
* **Connectivity issues**: Some diagnostic checks require external reachability; verify your internet connection if the command hangs or returns network-related warnings.
* **Permission errors**: Lack of read/write access to project configuration files or environment directories can trigger false negatives in the health report.

### FAQ

**Does this command modify my files?**
No, `brain project doctor` is a read-only diagnostic tool that strictly produces a health report.

**What happens if the health report identifies errors?**
The report will highlight specific areas of failure. Review the reported diagnostics to identify which configuration parameters need adjustment before proceeding with further project tasks.

**Do I need internet access to run this?**
While core repository checks function offline, certain environment health checks may require internet connectivity to validate remote endpoints or dependencies.
