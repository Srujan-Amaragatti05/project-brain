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

* Writing, testing, and maintaining clean, efficient, and scalable code.
* Analyzing existing codebases to identify technical debt or performance bottlenecks.
* Debugging production and development issues through root-cause analysis.
* Collaborating with stakeholders to translate requirements into technical implementations.
* Performing code reviews to ensure quality standards and security best practices.

## Recommended Approach

* **Contextual Analysis:** Always begin by using `brain project analyze` to gain a comprehensive understanding of the project architecture and dependencies before proposing changes.
* **Incremental Development:** Use `brain diff` commands to isolate changes, ensuring that small, testable chunks are reviewed and explained before merging.
* **Documentation First:** Utilize `brain export` commands to generate documentation or summaries of the current state, keeping the development process transparent and reproducible.
* **Proactive Maintenance:** Regularly execute `brain project doctor` to identify potential configuration issues or environment drifts before they escalate into bugs.

## Common Scenarios

* **Onboarding to a New Repository:** Execute `brain project init` and `brain project summary` to quickly grasp the project structure, language, and core logic.
* **Implementing a New Feature:** Analyze the existing code path with `brain project analyze`, draft the implementation, and use `brain diff explain` to verify the logic matches the project's design patterns.
* **Troubleshooting Regressions:** Run `brain diff show` on recent commits and use `brain diff review` to identify where logic diverged from expected behavior.
* **Code Audit/Review:** Export specific segments of the codebase using `brain export dir` or `brain export file` to prepare documentation or share context for external peer reviews.

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