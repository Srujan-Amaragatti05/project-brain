# Ai Assistant

## Who Is This Persona

**Persona:** AI Assistant
**Description:** Consumes exported repository context.
**Goals:** ['Analyze code', 'Generate explanations', 'Review changes']
**Workflow:** ['brain export full-code']
**Commands:** ['brain export full-code']

## Typical Responsibilities

*   Parsing and indexing repository structures and source code files.
*   Synthesizing high-level summaries of complex logic and architecture.
*   Identifying potential bugs, security vulnerabilities, or refactoring opportunities within the codebase.
*   Drafting documentation, docstrings, and commit messages based on code changes.
*   Assisting developers in navigating large codebases by providing cross-reference context.

## Recommended Approach

*   **Contextual Integrity:** Always initiate the workflow with `brain export full-code` to ensure the most current state of the repository is being referenced.
*   **Modular Analysis:** Break down large files into logical segments to maintain deep focus on specific functions or classes.
*   **Iterative Querying:** Use specific questions regarding dependencies, data flow, and state management rather than broad, general prompts.
*   **Verification:** Cross-check generated insights against the exported raw code to ensure alignment with existing patterns.

## Common Scenarios

*   **Onboarding:** Helping a new developer understand the architecture and style conventions of a project.
*   **Code Review:** Performing a preliminary pass on a Pull Request to identify style violations or logic errors before human review.
*   **Refactoring:** Suggesting optimal ways to modularize legacy code while preserving functionality.
*   **Bug Triaging:** Analyzing stack traces in conjunction with the codebase to pinpoint the source of an issue.

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