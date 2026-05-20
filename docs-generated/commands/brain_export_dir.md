# brain export dir

## Purpose

Manually add a directory to export

---

## Syntax

    brain export dir

---

## Parameters

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| path | str | Yes | argument | REQUIRED | Directory path to include |

---

## Examples

- brain export dir src/

---

## Outputs

- .brain/exports/manual_export.txt

---

## Related Commands

- brain export full_code
- brain export file

---

## Error Codes

_None_

---

## Notes

- Adds directory recursively into export bundle.

---

## Edge Cases

- Large directories increase export size.

---

## Demo

_No demo available._
