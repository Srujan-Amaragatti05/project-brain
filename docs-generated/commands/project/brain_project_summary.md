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

_No demo available._


---

## Usage Guide

### When would I use this?

Use this command when you need to generate a high-level overview of a repository's current status, health, or structure after you have completed an initial data examination. It is intended for creating executive reports, team briefings, or quick status updates based on the processed information.

### How it fits in the workflow

1.  **Analyze**: Execute the `brain project analyze` command to parse the repository data.
2.  **Summarize**: Run `brain project summary` to condense that technical analysis into a readable report.
3.  **Review**: Present the summary to stakeholders or use it to inform your next development sprint or refactoring tasks.

### Practical tips

*   **Run after analysis**: Always ensure `brain project analyze` has been successfully executed in the current session; otherwise, the summary will fail due to missing dependencies.
*   **Automate updates**: Integrate this command into your CI/CD pipelines to automatically generate project status artifacts after every major commit or nightly build.
*   **Focus on metrics**: Use the summary output to identify "hot spots" in your code that require immediate developer attention.

### Common failure causes

*   **Missing Analysis Data**: The most frequent cause is attempting to summarize without first running the analysis command.
*   **Repository Access Issues**: If the tool cannot access the local directory or file structures required for the analysis, the summary output will be incomplete or error out.
*   **Large Dataset Overload**: On extremely massive repositories, the summary generation may time out if the initial analysis phase was not optimized.

### FAQ

**Q: Can I customize the format of the summary?**
A: Depending on your current configuration, the summary output usually follows a standardized template; check your local settings to see if alternative report schemas are supported.

**Q: Does this command change my code?**
A: No, this is a read-only operation. It strictly generates a report based on existing analysis data and does not modify source files.

**Q: Why is my summary empty?**
A: This usually indicates that the `brain project analyze` process did not identify any actionable data or that the repository contains no supported file types for the current analysis configuration.
