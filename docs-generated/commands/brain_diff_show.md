# brain diff show

## Purpose

Show semantic git differences between references.

---

## Syntax

    brain diff show

---

## Parameters

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| from_ref | str | No | argument | - | Starting git reference |
| to_ref | str | No | argument | - | Ending git reference |

---

## Examples

- brain diff show
- brain diff show HEAD~3 HEAD
- brain diff show main dev

---

## Outputs

_None_

---

## Related Commands

- brain diff review
- brain export code_changes

---

## Error Codes

- INVALID_GIT_REF
- NOT_GIT_REPO

---

## Notes

- Supports file-level and function-level diff modes.

---

## Edge Cases

- Requires valid git history.

---

## Demo

![Demo](../../demo/gifs/diff.gif)
