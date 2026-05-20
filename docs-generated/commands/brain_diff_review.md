# brain diff review

## Purpose

Explain code changes using LLM

---

## Syntax

    brain diff review

---

## Parameters

| Name | Type | Required | Kind | Default | Description |
|---|---|---|---|---|---|
| from_ref | str | No | argument | - | Starting git reference |
| to_ref | str | No | argument | - | Ending git reference |

---

## Examples

- brain diff review
- brain diff review HEAD~1 HEAD

---

## Outputs

- .brain/reports/*.json
- .brain/reports/*.html

---

## Related Commands

- brain diff show
- brain export code_changes

---

## Error Codes

- INVALID_GIT_REF
- LLM_PROVIDER_FAILURE

---

## Notes

- Uses configured LLM provider to explain changes.

---

## Edge Cases

- Large diffs may increase LLM response time.

---

## Demo

![Demo](../../demo/gifs/review.gif)
