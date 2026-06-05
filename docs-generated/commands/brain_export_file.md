# brain export file

## Overview

Manually add a single file to export

---

## When To Use

This command is intended for **export** workflows.

---

## Syntax

```bash
brain export file
```

---

## Arguments

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| path | str | Yes | argument | REQUIRED | File path to include |

---

## Examples

- brain export file src/main.py

---

## Expected Outputs

- .brain/exports/manual_export.txt

---

## Error Reference

_None_

---

## Related Commands

- brain export full_code
- brain export dir

---

## Operational Notes

- Adds a single file into export bundle.

---

## Edge Cases

- File must exist.

---

## Demo

_No demo available._
