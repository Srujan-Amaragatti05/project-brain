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

Use `brain project doctor` whenever you suspect repository corruption, configuration drift, or inconsistent environment settings. It is the primary tool for performing comprehensive diagnostics on your local project structure to ensure all dependencies and tracking mechanisms are functioning as expected.

### How it fits in the workflow

1. **Onboarding:** Run immediately after cloning a repository to verify your local environment meets project requirements.
2. **Maintenance:** Execute periodically to validate that build artifacts, hooks, and configuration files remain synchronized with the project schema.
3. **Troubleshooting:** Use this as your first step when encountering unexpected behavior, build failures, or issues with version control integration.

### Practical tips

*   **Pre-commit check:** Run the command before opening a pull request to ensure your local environment state matches the project standards.
*   **Log capture:** If the command reports issues, pipe the output to a text file (`brain project doctor > debug.log`) to share with team leads or support engineers.
*   **Isolated environments:** Ensure you are running the command from the root of your project directory to allow the tool to correctly identify the workspace configuration.

### Common failure causes

*   **NOT_GIT_REPO:** The tool was executed outside of a initialized Git repository, preventing it from validating branch tracking or index health.
*   **Connectivity Issues:** Certain diagnostic checks require verifying external dependency registries; an unstable internet connection may cause these specific validations to timeout or fail.
*   **Permission Denied:** Insufficient file system permissions may prevent the doctor from inspecting hidden configuration folders or system-level symlinks.

### FAQ

**Q: Does `brain project doctor` modify my files?**  
A: No, this command is strictly diagnostic. It reports findings and potential issues but will not alter, delete, or "fix" project files automatically unless explicitly prompted by a secondary command.

**Q: Why does the command take longer than usual?**  
A: Diagnostic duration depends on the size of the repository and the number of remote verification checks. If the tool is checking remote dependency hashes, connectivity latency may impact response times.

**Q: How often should I run this?**  
A: It is recommended to run this command whenever you switch branches, pull significant upstream changes, or after installing new global development tools.
