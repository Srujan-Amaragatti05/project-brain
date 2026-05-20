# brain project analyze

## Purpose

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

## Syntax

    brain project analyze

---

## Parameters

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| path | str | No | argument | . | Repository path to analyze |

---

## Examples

- brain project analyze .
- brain project analyze ./src

---

## Outputs

- .brain/data.json

---

## Related Commands

- brain project summary
- brain project doctor

---

## Error Codes

- NOT_GIT_REPO

---

## Notes

- Uses AST parsing for repository analysis.

---

## Edge Cases

- Large repositories may take longer to analyze.

---

## Demo

![Demo](../../demo/gifs/analyze.gif)
