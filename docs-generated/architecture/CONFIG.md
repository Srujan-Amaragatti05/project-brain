# Configuration

This document describes all available configuration settings in `brain.yaml`.

## `analysis.depth`

Granularity of repository analysis.

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `fast` |
| Allowed | `fast`, `full` |

## `analysis.ignore`

Patterns to exclude from repository analysis.

| Property | Value |
|----------|-------|
| Type | `list` |
| Default | `['.brain/', '.git/', 'node_modules/', 'venv/']` |

## `analysis.include_tests`

Whether to include test files in general analysis.

| Property | Value |
|----------|-------|
| Type | `boolean` |
| Default | `False` |

## `diff.mode`

Diff analysis granularity (function-level or file-level).

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `function` |
| Allowed | `function`, `file` |

## `explain.include_risks`

Include potential security/logic risks in explanations.

| Property | Value |
|----------|-------|
| Type | `boolean` |
| Default | `True` |

## `explain.level`

Verbosity of code explanations.

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `detailed` |
| Allowed | `concise`, `detailed` |

## `export.changes.include_context`

Include surrounding code context in change exports.

| Property | Value |
|----------|-------|
| Type | `boolean` |
| Default | `True` |

## `export.changes.mode`

Granularity for code-changes export.

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `function` |
| Allowed | `function`, `file` |

## `export.changes.output_path`

Default destination for code-change exports.

| Property | Value |
|----------|-------|
| Type | `string` |
| Default | `.brain/exports/code_changes.txt` |

## `export.full_code.include_tests`

Include test files in full-code exports.

| Property | Value |
|----------|-------|
| Type | `boolean` |
| Default | `False` |

## `export.full_code.max_file_size_kb`

Skip files larger than this size in full-code exports.

| Property | Value |
|----------|-------|
| Type | `integer` |
| Default | `200` |

## `export.ignore`

Patterns to exclude specifically from exports.

| Property | Value |
|----------|-------|
| Type | `list` |
| Default | `['.brain/', '.git/', 'node_modules/']` |

## `export.manual_add.allow_duplicates`

Allow adding the same file multiple times to an export.

| Property | Value |
|----------|-------|
| Type | `boolean` |
| Default | `True` |

## `llm.model`

Specific model name to use with the selected provider.

| Property | Value |
|----------|-------|
| Type | `string` |
| Default | `` |

## `llm.provider`

Active LLM provider for code review and explanation.

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `none` |
| Allowed | `none`, `openai`, `ollama`, `gemini`, `huggingface` |

## `llm.timeout_sec`

Timeout in seconds for provider requests.

| Property | Value |
|----------|-------|
| Type | `integer` |
| Default | `60` |

## `output.format`

CLI output rendering format.

| Property | Value |
|----------|-------|
| Type | `enum` |
| Default | `text` |
| Allowed | `text`, `json`, `markdown` |

## `version`

Configuration schema version.

| Property | Value |
|----------|-------|
| Type | `string` |
| Default | `1.1.0` |
