# ProjectBrain CLI Reference

Auto-generated command reference.

---


# Diff Commands

## brain diff show

Show semantic git differences between references.

**Category:** diff


### Examples

- `brain diff show`
- `brain diff show HEAD~3 HEAD`
- `brain diff show main dev`

### Related Commands

- `brain diff review`
- `brain export code_changes`

---

## brain diff review

Explain code changes using LLM

**Category:** diff


### Examples

- `brain diff review`
- `brain diff review HEAD~1 HEAD`

### Related Commands

- `brain diff show`
- `brain export code_changes`

---

## brain diff explain

Explain a file or function

**Category:** diff


### Examples

- `brain diff explain src/main.py`
- `brain diff explain src/main.py:function_name`

### Related Commands

- `brain diff review`

---


# Export Commands

## brain export full_code

Export entire codebase into structured file

**Category:** export


### Examples

- `brain export full_code`

### Related Commands

- `brain export file`
- `brain export dir`

---

## brain export file

Manually add a single file to export

**Category:** export


### Examples

- `brain export file src/main.py`

### Related Commands

- `brain export full_code`
- `brain export dir`

---

## brain export dir

Manually add a directory to export

**Category:** export


### Examples

- `brain export dir src/`

### Related Commands

- `brain export full_code`
- `brain export file`

---

## brain export code_changes

Export changed code between two git references

**Category:** export


### Examples

- `brain export code_changes HEAD~1 HEAD`

### Related Commands

- `brain diff show`
- `brain diff review`

---


# Llm Commands

## brain testllm test

Test configured LLM provider connectivity.

**Category:** llm


### Examples

- `brain testllm test`

### Related Commands

- `brain diff review`

---


# Project Commands

## brain project init

Initialize project-brain in the current directory

**Category:** project


### Examples

- `brain project init`

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


### Examples

- `brain project analyze .`
- `brain project analyze ./src`

### Related Commands

- `brain project summary`
- `brain project doctor`

---

## brain project summary

Summarize the analyzed data

**Category:** project


### Examples

- `brain project summary`

### Related Commands

- `brain project analyze`

---

## brain project doctor

Repository diagnostics and environment health checks.

**Category:** project


### Examples

- `brain project doctor`

### Related Commands

- `brain project init`
- `brain project analyze`

---
