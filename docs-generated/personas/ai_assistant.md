# Ai Assistant

## Who Is This Persona

**Persona:** AI Assistant
**Description:** Consumes exported repository context.
**Goals:** ['Analyze code', 'Generate explanations', 'Review changes']
**Workflow:** ['brain export full-code']
**Commands:** ['brain export full-code']

## Typical Responsibilities

*   **Context Synthesis:** Processing structured repository exports to gain a holistic understanding of the codebase structure, dependencies, and logic.
*   **Code Analysis:** Identifying patterns, potential bugs, architectural bottlenecks, and areas for refactoring based on the provided context.
*   **Documentation:** Generating high-quality technical explanations, docstrings, and README updates to ensure code maintainability.
*   **Quality Assurance:** Conducting comprehensive reviews of pull requests or proposed changes to verify adherence to project standards and logic consistency.

## Recommended Approach

1.  **Initialization:** Execute `brain export full-code` to ingest the necessary state of the repository.
2.  **Indexing:** Map the file hierarchy and resolve cross-reference dependencies to ensure accurate cross-file analysis.
3.  **Iterative Analysis:** Apply targeted logic checks, focusing on the specific modules or functions relevant to the user’s query.
4.  **Feedback Loop:** Present findings clearly, offering actionable suggestions for code improvement or debugging steps.

## Common Scenarios

*   **Onboarding:** Providing a high-level summary of a complex repository for a new developer.
*   **Debugging:** Tracing data flow across multiple files to identify the root cause of an unexpected behavior.
*   **Feature Implementation:** Analyzing existing architectural patterns to ensure new code remains consistent with the current implementation style.
*   **Refactoring:** Suggesting modularization strategies based on redundant logic detected during the `full-code` analysis.

---

## Overview

Consumes exported repository context.

## Statistics

- Recommended Commands: 1
- Workflow Steps: 1

## Typical Goals

- Analyze code
- Generate explanations
- Review changes

## Recommended Workflow

1. `brain export full-code`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain export full-code` | Export entire codebase into structured file |

## Related Personas

- Developer
- Architect