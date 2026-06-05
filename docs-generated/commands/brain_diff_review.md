# brain diff review

## Overview

Explain code changes using LLM

---

## When To Use

This command is intended for **diff** workflows.

---

## Syntax

```bash
brain diff review
```

---

## Arguments

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| from_ref | str | No | argument | - | Starting git reference |
| to_ref | str | No | argument | - | Ending git reference |

---

## Examples

- brain diff review
- brain diff review HEAD~1 HEAD

---

## Expected Outputs

- .brain/reports/*.json
- .brain/reports/*.html

---

## Error Reference

- INVALID_GIT_REF
- LLM_PROVIDER_FAILURE

---

## Related Commands

- brain diff show
- brain export code_changes

---

## Operational Notes

- Uses configured LLM provider to explain changes.

---

## Edge Cases

- Large diffs may increase LLM response time.

---

## Demo

![Demo](../../demo/gifs/review.gif)
