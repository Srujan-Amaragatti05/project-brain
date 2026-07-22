# Developer

## Who Is This Persona

**Persona:** Developer

**Description:** Builds and modifies application code.

**Goals:**
* Implement features
* Debug issues
* Understand code

**Workflow:**
* `brain project analyze`
* `brain diff explain`
* `brain diff review`

**Commands:**
* `brain project init`
* `brain project analyze`
* `brain project summary`
* `brain project doctor`
* `brain diff show`
* `brain diff review`
* `brain diff explain`
* `brain export full-code`
* `brain export file`
* `brain export dir`
* `brain export code-changes`
* `brain export tree`
* `brain testllm test`

## Typical Responsibilities

* Writing, testing, and maintaining clean, efficient codebases.
* Diagnosing performance bottlenecks and logical errors within complex modules.
* Integrating third-party APIs and internal services.
* Documenting system architecture and code logic for team visibility.
* Conducting peer reviews to ensure code quality and adherence to style guides.

## Recommended Approach

* **Contextual Analysis:** Always begin by running `brain project analyze` to ensure the model has an updated understanding of the codebase structure and dependencies.
* **Iterative Modification:** Use `brain diff explain` on changes before committing to ensure the logic aligns with project requirements.
* **Automated Verification:** Leverage `brain testllm test` to validate code integrity before pushing changes.
* **Documentation First:** Utilize `brain export tree` or `brain project summary` when onboarding to a new module to grasp the high-level architecture quickly.

## Common Scenarios

* **Legacy Codebase Onboarding:** Run `brain project summary` and `brain project analyze` to identify core logic paths and potential technical debt.
* **Feature Development:** Utilize `brain export file` to isolate relevant files, draft implementation code, and verify with `brain diff review`.
* **Bug Triaging:** Use `brain project doctor` to identify configuration issues or environment drifts, followed by targeted `brain diff explain` to isolate faulty logic.
* **Code Refactoring:** Run `brain export full-code` to visualize large-scale changes and ensure refactored blocks maintain parity with original requirements.

---

## Overview

Builds and modifies application code.

## Statistics

- Recommended Commands: 13
- Workflow Steps: 3

## Typical Goals

- Implement features
- Debug issues
- Understand code

## Recommended Workflow

1. `brain project analyze`
2. `brain diff explain`
3. `brain diff review`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain diff explain` | Explain a file or function |
| `brain diff review` | Explain code changes using LLM |
| `brain diff show` | Show semantic git differences between references. |
| `brain export code-changes` | Export changed code between two git references |
| `brain export dir` | Manually add a directory to export |
| `brain export file` | Manually add a single file to export |
| `brain export full-code` | Export entire codebase into structured file |
| `brain export tree` | Export repository tree structure into tree and JSON formats. |
| `brain project analyze` | Analyze repository structure using AST parsing. |
| `brain project doctor` | Repository diagnostics and environment health checks. |
| `brain project init` | Initialize project-brain in the current directory |
| `brain project summary` | Summarize the analyzed data |
| `brain testllm test` | Test configured LLM provider connectivity. |

## Related Personas

- Reviewer
- Architect
- Maintainer