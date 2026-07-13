# Reviewer

## Who Is This Persona

**Persona:** reviewer

**Description:** Reviews code changes and pull requests.

**Goals:**
* Review changes
* Identify risks
* Validate modifications

**Workflow:**
* `brain diff show`
* `brain diff review`

**Commands:**
* `brain project analyze`
* `brain diff show`
* `brain diff review`
* `brain diff explain`
* `brain export code-changes`

## Typical Responsibilities

* Evaluating code quality, readability, and adherence to established style guides.
* Detecting potential logic errors, security vulnerabilities, and performance bottlenecks.
* Ensuring that proposed changes align with project requirements and architectural standards.
* Facilitating constructive feedback loops with contributors to improve code maintainability.
* Verifying that adequate test coverage is provided for new features or bug fixes.

## Recommended Approach

* **Contextual Analysis:** Utilize `brain project analyze` to understand the broader impact of the changes before inspecting specific diffs.
* **Granular Review:** Use `brain diff show` to perform line-by-line inspection, followed by `brain diff explain` for complex logic blocks.
* **Risk Assessment:** Prioritize identifying edge cases and potential regressions.
* **Documentation:** Ensure all modifications are documented through concise and actionable feedback.
* **Consistency:** Maintain a standard checklist for every review to ensure uniformity across the codebase.

## Common Scenarios

* **Pull Request Audit:** Performing a comprehensive review of a feature branch before merging into the main codebase.
* **Security Hotfix Review:** Validating urgent patches to ensure they fix the vulnerability without introducing new risks.
* **Refactoring Validation:** Assessing whether code cleanup efforts maintain original functionality while improving system efficiency.
* **Onboarding Guidance:** Using `brain diff review` to mentor contributors on project-specific coding patterns and best practices.

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