# brain export code_changes

## Overview

Export changed code between two git references

---

## When To Use

This command is intended for **export** workflows.

---

## Syntax

```bash
brain export code_changes
```

---

## Arguments

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| from_ref | str | Yes | argument | REQUIRED | Starting git reference |
| to_ref | str | Yes | argument | REQUIRED | Ending git reference |

---

## Examples

- brain export code_changes HEAD~1 HEAD

---

## Expected Outputs

- .brain/exports/code_changes.txt

---

## Error Reference

- INVALID_GIT_REF

---

## Related Commands

- brain diff show
- brain diff review

---

## Operational Notes

- Exports changed files between git references.

---

## Edge Cases

- Requires valid git history.

---

## Demo

_No demo available._
