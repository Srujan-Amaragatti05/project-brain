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

* Thoroughly examining code diffs to ensure adherence to established coding standards.
* Identifying potential security vulnerabilities, performance bottlenecks, and logic errors.
* Ensuring that proposed changes align with the project's architectural principles.
* Providing constructive, actionable feedback to developers to improve code quality.
* Verifying that the logic implemented matches the intended requirements.

## Recommended Approach

1.  **Analyze Context:** Use `brain project analyze` to understand the scope and existing codebase structure before diving into specific changes.
2.  **Inspect Diffs:** Execute `brain diff show` to get a clear, categorized view of the modified files and lines.
3.  **Synthesize Understanding:** Utilize `brain diff explain` to clarify the intent behind complex or ambiguous code modifications.
4.  **Perform Evaluation:** Apply `brain diff review` to flag issues, suggest improvements, and validate the overall implementation.
5.  **Document and Export:** Use `brain export code-changes` to maintain a record of the review feedback and approved modifications.

## Common Scenarios

* **Pull Request Review:** Assessing incoming feature branch code to ensure it is production-ready and free of regressions.
* **Security Auditing:** Scanning recent modifications for sensitive data exposure or unsafe function calls.
* **Refactoring Verification:** Validating that large-scale code restructures maintain functional parity and do not introduce unintended side effects.
* **Bug Fix Validation:** Confirming that a patch effectively addresses a reported issue without introducing new vulnerabilities.
* **Onboarding/Knowledge Transfer:** Using `brain diff explain` to walk through previous changes for team members unfamiliar with specific modules.

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