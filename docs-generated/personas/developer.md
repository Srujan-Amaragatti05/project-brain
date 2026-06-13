# Developer

## Who Is This Persona

**Persona:** Developer

**Description:** Builds and modifies application code.

## Typical Responsibilities

*   Writing, testing, and maintaining clean, efficient, and scalable application code.
*   Analyzing existing codebases to identify technical debt, bugs, and areas for performance optimization.
*   Implementing new features based on project requirements and specifications.
*   Conducting peer reviews and providing explanations for architectural changes.
*   Ensuring project integrity through systematic diagnostics and automated testing.

## Recommended Approach

1.  **Project Contextualization:** Use `brain project init` and `brain project analyze` to map out the codebase, understand dependency structures, and generate project summaries.
2.  **Iterative Development:** Utilize `brain diff explain` to understand the impact of proposed changes before implementation and `brain diff review` to ensure quality.
3.  **Diagnostic Troubleshooting:** Run `brain project doctor` to identify configuration issues and use `brain diff show` to trace the history of code modifications.
4.  **Verification:** Integrate `brain testllm test` into the workflow to validate logic and ensure new features do not introduce regressions.
5.  **Documentation & Portability:** Leverage `brain export` commands to share specific file segments or full-code snapshots for documentation and team collaboration.

## Common Scenarios

*   **Onboarding to a new repository:** Use `brain project analyze` and `brain project summary` to quickly grasp the project structure and architectural patterns.
*   **Fixing a critical bug:** Use `brain diff show` to compare recent changes, then use `brain diff explain` to understand the logic flow of the problematic section.
*   **Code Reviewing:** Use `brain diff review` to evaluate incoming pull requests, ensuring they align with project standards and goals.
*   **Knowledge Sharing:** Use `brain export full-code` or `brain export dir` to provide context for cross-functional meetings or to generate documentation for stakeholders.
*   **System Health Checks:** Regularly run `brain project doctor` to ensure the development environment and project dependencies remain stable.

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