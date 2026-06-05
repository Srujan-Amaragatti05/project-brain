# brain diff show

## Overview

Show semantic git differences between references.

---

## When To Use

This command is intended for **diff** workflows.

---

## Syntax

```bash
brain diff show
```

---

## Arguments

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

## Expected Outputs

_None_

---

## Error Reference

- INVALID_GIT_REF
- NOT_GIT_REPO

---

## Related Commands

- brain diff review
- brain export code_changes

---

## Operational Notes

- Supports file-level and function-level diff modes.

---

## Edge Cases

- Requires valid git history.

---

## Demo

![Demo](../../demo/gifs/diff.gif)
