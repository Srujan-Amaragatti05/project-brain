# brain project analyze

## Overview

Analyze repository structure using AST parsing.

Extracts:
- files
- functions
- classes
- metadata

Stores results inside:
.brain/data.json

Example:
    brain project analyze .

---

## When To Use

This command is intended for **project** workflows.

---

## Syntax

```bash
brain project analyze
```

---

## Arguments

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| path | str | No | argument | . | Repository path to analyze |

---

## Examples

- brain project analyze .
- brain project analyze ./src

---

## Expected Outputs

- .brain/data.json

---

## Error Reference

- NOT_GIT_REPO

---

## Related Commands

- brain project summary
- brain project doctor

---

## Operational Notes

- Uses AST parsing for repository analysis.

---

## Edge Cases

- Large repositories may take longer to analyze.

---

## Demo

![Demo](../../demo/gifs/analyze.gif)
