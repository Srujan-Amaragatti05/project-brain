# brain export code_changes

## Purpose

Export changed code between two git references

---

## Syntax

    brain export code_changes

---

## Parameters

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| from_ref | str | Yes | argument | REQUIRED | Starting git reference |
| to_ref | str | Yes | argument | REQUIRED | Ending git reference |

---

## Examples

- brain export code_changes HEAD~1 HEAD

---

## Outputs

- .brain/exports/code_changes.txt

---

## Related Commands

- brain diff show
- brain diff review

---

## Error Codes

- INVALID_GIT_REF

---

## Notes

- Exports changed files between git references.

---

## Edge Cases

- Requires valid git history.

---

## Demo

_No demo available._
