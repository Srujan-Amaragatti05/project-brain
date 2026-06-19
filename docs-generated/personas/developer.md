# Developer

## Who Is This Persona

**Persona:** Developer

**Description:** Builds and modifies application code.

**Goals:**
* Implement features
* Debug issues
* Understand code

## Typical Responsibilities

* Writing, testing, and maintaining clean, efficient, and scalable code.
* Analyzing existing codebases to identify technical debt, bugs, or performance bottlenecks.
* Reviewing code changes to ensure architectural integrity and adherence to project standards.
* Documenting system functionality and logic for team knowledge sharing.
* Integrating new libraries, frameworks, or APIs into existing projects.

## Recommended Approach

* **Analyze First:** Utilize `brain project analyze` to gain a comprehensive understanding of the existing codebase and architecture before making modifications.
* **Iterative Development:** Leverage `brain project summary` to maintain context across sessions and ensure project goals remain aligned.
* **Proactive Debugging:** Run `brain project doctor` to identify potential configuration issues or environment inconsistencies early.
* **Contextual Reviews:** Always use `brain diff explain` and `brain diff review` to ensure changes are verified and clearly documented before integration.
* **Knowledge Retention:** Export relevant project artifacts using the `brain export` commands to maintain external documentation or perform offline audits.

## Common Scenarios

* **Onboarding to a new project:** Use `brain project init` and `brain project analyze` to map out the codebase structure and dependencies.
* **Implementing a new feature:** Begin by analyzing the related modules, drafting the logic, and using `brain diff explain` to validate the proposed implementation path.
* **Troubleshooting a production bug:** Run `brain project doctor` to check for environment issues, then use `brain diff show` to isolate changes that might have introduced the regression.
* **Code Refactoring:** Use `brain export full-code` for offline review, followed by iterative diff reviews to ensure refactoring does not break existing business logic.

---

## Overview

Builds and modifies application code.

## Statistics

- Recommended Commands: 12
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
| `brain project analyze` | Analyze repository structure using AST parsing. |
| `brain project doctor` | Repository diagnostics and environment health checks. |
| `brain project init` | Initialize project-brain in the current directory |
| `brain project summary` | Summarize the analyzed data |
| `brain testllm test` | Test configured LLM provider connectivity. |

## Related Personas

- Reviewer
- Maintainer
- Architect