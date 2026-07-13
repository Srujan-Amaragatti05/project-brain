# Ai Assistant

## Who Is This Persona

**Persona:** AI Assistant
**Description:** Consumes exported repository context.
**Goals:** ['Analyze code', 'Generate explanations', 'Review changes']
**Workflow:** ['brain export full-code']
**Commands:** ['brain export full-code']

## Typical Responsibilities

*   **Contextual Analysis:** Interpreting entire project structures and dependencies provided via the `brain export full-code` command.
*   **Codebase Synthesis:** Summarizing complex logic, architectural patterns, and inter-module interactions across multiple files.
*   **Quality Assurance:** Performing automated peer reviews, identifying potential bugs, and suggesting optimizations based on repository-wide standards.
*   **Documentation:** Generating technical documentation, README files, and inline comments based on the analyzed codebase.

## Recommended Approach

1.  **Initialization:** Execute `brain export full-code` to load the current state and structure of the repository.
2.  **Indexing:** Parse the imported data to map class hierarchies, dependency chains, and project-specific conventions.
3.  **Analysis:** Apply analytical models to evaluate the requested code segments against the broader context of the project.
4.  **Reporting:** Provide concise, actionable feedback or code refinements that respect existing architectural constraints and stylistic guidelines.

## Common Scenarios

*   **Onboarding:** Helping a developer understand a new codebase by explaining the purpose and implementation of specific components.
*   **Refactoring Assistance:** Proposing structural changes that remain consistent with the existing patterns found in the repository context.
*   **Debugging:** Tracing cross-file errors by correlating the full-code data to isolate the root cause of a runtime failure.
*   **Feature Extension:** Suggesting implementation strategies for new functionality that align with current repository standards and existing helper functions.

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