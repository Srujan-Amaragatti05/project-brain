# brain export dir

## Overview

Manually add a directory to export

---

## When To Use

This command is intended for **export** workflows.

---

## Syntax

```bash
brain export dir
```

---

## Arguments

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| path | str | Yes | argument | REQUIRED | Directory path to include |

---

## Examples

- brain export dir src/

---

## Expected Outputs

- .brain/exports/manual_export.txt

---

## Error Reference

_None_

---

## Related Commands

- brain export full_code
- brain export file

---

## Operational Notes

- Adds directory recursively into export bundle.

---

## Edge Cases

- Large directories increase export size.

---

## Demo

_No demo available._
