# ProjectBrain CLI Reference

Auto-generated command reference.

---


# Diff Commands

## brain diff show

Show semantic git differences between references.

**Category:** diff

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| from_ref | str | No | - |
| to_ref | str | No | - |

### Examples

```bash
brain diff show
```
```bash
brain diff show HEAD~3 HEAD
```
```bash
brain diff show main dev
```

### Related Commands

- `brain diff review`
- `brain export code-changes`

---

## brain diff review

Explain code changes using LLM

**Category:** diff

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| from_ref | str | No | - |
| to_ref | str | No | - |

### Examples

```bash
brain diff review
```
```bash
brain diff review HEAD~1 HEAD
```

### Outputs

- .brain/reports/*.json
- .brain/reports/*.html

### Related Commands

- `brain diff show`
- `brain export code-changes`

---

## brain diff explain

Explain a file or function

**Category:** diff

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| target | str | Yes | REQUIRED |

### Examples

```bash
brain diff explain src/main.py
```
```bash
brain diff explain src/main.py:function_name
```

### Related Commands

- `brain diff review`

---


# Export Commands

## brain export full-code

Export entire codebase into structured file

**Category:** export

### Examples

```bash
brain export full-code
```

### Outputs

- .brain/exports/full_code.txt

### Related Commands

- `brain export file`
- `brain export dir`

---

## brain export file

Manually add a single file to export

**Category:** export

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| path | str | Yes | REQUIRED |

### Examples

```bash
brain export file src/main.py
```

### Outputs

- .brain/exports/manual_export.txt

### Related Commands

- `brain export full-code`
- `brain export dir`

---

## brain export dir

Manually add a directory to export

**Category:** export

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| path | str | Yes | REQUIRED |

### Examples

```bash
brain export dir src/
```

### Outputs

- .brain/exports/manual_export.txt

### Related Commands

- `brain export full-code`
- `brain export file`

---

## brain export code-changes

Export changed code between two git references

**Category:** export

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| from_ref | str | Yes | REQUIRED |
| to_ref | str | Yes | REQUIRED |

### Examples

```bash
brain export code-changes HEAD~1 HEAD
```

### Outputs

- .brain/exports/code-changes.txt

### Related Commands

- `brain diff show`
- `brain diff review`

---


# Project Commands

## brain project init

Initialize project-brain in the current directory

**Category:** project

### Examples

```bash
brain project init
```

### Outputs

- .brain/
- brain.yaml

### Related Commands

- `brain project analyze`
- `brain project doctor`

---

## brain project analyze

Analyze repository structure using AST parsing.

Extracts:
- files
- functions
- classes
- metadata

Stores results inside:
.brain/data.json

Example:
    brain project analyze .

**Category:** project

### Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| path | str | No | . |

### Examples

```bash
brain project analyze .
```
```bash
brain project analyze ./src
```

### Outputs

- .brain/data.json

### Related Commands

- `brain project summary`
- `brain project doctor`

---

## brain project summary

Summarize the analyzed data

**Category:** project

### Examples

```bash
brain project summary
```

### Outputs

- terminal summary

### Related Commands

- `brain project analyze`

---

## brain project doctor

Repository diagnostics and environment health checks.

**Category:** project

### Examples

```bash
brain project doctor
```

### Outputs

- terminal diagnostics

### Related Commands

- `brain project init`
- `brain project analyze`

---


# Testllm Commands

## brain testllm test

Test configured LLM provider connectivity.

**Category:** testllm

### Examples

```bash
brain testllm test
```

### Related Commands

- `brain diff review`

---
