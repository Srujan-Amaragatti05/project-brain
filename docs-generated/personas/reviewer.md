# Reviewer

## Who Is This Persona

**Persona:** reviewer

**Description:** Reviews code changes and pull requests.

**Goals:**
* Review changes
* Identify risks
* Validate modifications

**Workflow:**
* brain diff show
* brain diff review

**Commands:**
* brain project analyze
* brain diff show
* brain diff review
* brain diff explain
* brain export code-changes

## Typical Responsibilities

* Performing comprehensive code reviews to ensure quality, maintainability, and security.
* Identifying potential regressions or performance bottlenecks introduced by new changes.
* Ensuring adherence to coding standards, architectural patterns, and project conventions.
* Providing constructive feedback and actionable suggestions for code improvements.
* Verifying that changes align with the stated requirements and project scope.

## Recommended Approach

* **Contextual Analysis:** Use `brain project analyze` to understand the codebase before diving into specific changes.
* **Incremental Review:** Execute `brain diff show` to inspect the delta, followed by `brain diff explain` for complex logic.
* **Risk-Centric Evaluation:** Focus on edge cases, security vulnerabilities, and logic flaws during the `brain diff review` process.
* **Documentation and Knowledge Sharing:** Use `brain export code-changes` to maintain a record of significant changes and decisions for future reference.

## Common Scenarios

* **Pull Request Audit:** Analyzing incoming PRs to confirm that the implementation matches the intended ticket requirements.
* **Bug Fix Verification:** Ensuring that a patch effectively resolves the reported issue without side effects.
* **Refactoring Assessment:** Evaluating code cleanup tasks to ensure functionality remains intact while improving readability.
* **Security Hardening:** Reviewing code modifications specifically to check for insecure data handling or dependency vulnerabilities.

---

## Overview

Reviews code changes and pull requests.

## Statistics

- Recommended Commands: 5
- Workflow Steps: 2

## Typical Goals

- Review changes
- Identify risks
- Validate modifications

## Recommended Workflow

1. `brain diff show`
2. `brain diff review`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain diff explain` | Explain a file or function |
| `brain diff review` | Explain code changes using LLM |
| `brain diff show` | Show semantic git differences between references. |
| `brain export code-changes` | Export changed code between two git references |
| `brain project analyze` | Analyze repository structure using AST parsing. |

## Related Personas

- Developer
- Maintainer
- Architect