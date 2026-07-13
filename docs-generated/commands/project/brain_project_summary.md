# `brain project summary`

> Summarize the analyzed data

---

## Overview

Summarize the analyzed data

---

## When to use

This command is part of the **project** workflow.

---

## Syntax

```bash
brain project summary [options]
```

---

## Parameters

_No parameters._

---

## Examples

```bash
brain project summary
```

---

## Outputs

- `terminal summary`

---

## Errors

_None_

---

## Related commands

- `brain project analyze`

---

## Notes

- Displays summarized repository analysis.

---

## Edge cases

- Requires previous analysis.

---

## Demo

![Demo: summary.gif](../../../demo/gifs/summary.gif)


---

## Usage Guide

### When would I use this?

Use this command when you need to view a concise, high-level overview of the data collected during a repository analysis. It is intended for quick verification of project states, trends, or metrics after the analysis phase is complete.

### How it fits in the workflow

1.  **Analyze**: Run `brain project analyze` to scan the codebase and populate `.brain/data.json`.
2.  **Summarize**: Execute `brain project summary` to parse the generated JSON file and output the human-readable terminal report.
3.  **Action**: Use the summary output to inform decision-making, track project health, or identify areas requiring further investigation.

### Practical tips

*   Always run the `brain project analyze` command immediately before requesting a summary to ensure the report reflects the most current state of the repository.
*   Pipe the terminal output to a text file (e.g., `brain project summary > report.txt`) if you need to share the summary with team members who do not have access to the terminal.
*   Use the summary to quickly spot discrepancies in file structures or coding patterns before diving into deeper manual analysis.

### Common failure causes

*   **Missing Analysis Data**: The command will fail if `.brain/data.json` has not been generated or if it has been deleted since the last analysis.
*   **Corrupted Data**: If the previous `brain project analyze` process was interrupted, the resulting JSON file may be malformed, causing the summary generator to return an error.
*   **Permission Denied**: The command may fail if the current user lacks read access to the `.brain/` directory or write access to generate terminal output.

### FAQ

**Q: Can I customize the format of the summary output?**
A: No, the output is strictly defined by the tool's internal template and is designed for standard terminal display.

**Q: Does this command modify my project files?**
A: No, the command only consumes data from `.brain/data.json` and does not perform any write operations on your source code or project structure.

**Q: Why is my summary empty or blank?**
A: This typically occurs if the `.brain/data.json` file exists but contains no data, which may happen if the analysis phase did not successfully target any files. Ensure your project is correctly configured for analysis.
