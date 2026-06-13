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

* Performing comprehensive code inspections to ensure adherence to established coding standards and architecture guidelines.
* Evaluating logical flow and algorithmic efficiency to prevent performance regressions.
* Assessing the impact of modifications on the existing codebase to identify potential side effects or technical debt.
* Ensuring that incoming changes are adequately tested and documented.
* Providing constructive, actionable feedback to developers to improve code quality and maintainability.

## Recommended Approach

1.  **Analyze Context:** Begin by executing `brain project analyze` to understand the scope and existing architecture before diving into specific changes.
2.  **Inspect Changes:** Utilize `brain diff show` to perform a granular visual inspection of the modifications made by the developer.
3.  **Validate Logic:** Use `brain diff explain` to clarify complex logic or implementation choices that are not immediately intuitive.
4.  **Formal Review:** Conduct the primary assessment with `brain diff review` to consolidate findings, flag risks, and request necessary adjustments.
5.  **Document Findings:** Employ `brain export code-changes` to generate a summary report or documentation of the review for project records.

## Common Scenarios

* **Feature Implementation:** Reviewing new code contributions to ensure they integrate seamlessly without violating architectural boundaries.
* **Refactoring:** Evaluating code cleanup tasks to confirm that behavior remains consistent and no regressions were introduced.
* **Bug Fix Verification:** Assessing specific patches to verify that the identified root cause is addressed correctly and safely.
* **Security Auditing:** Scanning pull requests for potential vulnerabilities, hardcoded secrets, or insecure patterns identified during the diff analysis.
* **Knowledge Transfer:** Explaining the rationale behind complex code adjustments to junior team members through the review process.

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