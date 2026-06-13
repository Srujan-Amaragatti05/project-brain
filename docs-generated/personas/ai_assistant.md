# Ai Assistant

## Who Is This Persona

**Persona:** AI Assistant
**Description:** Consumes exported repository context.
**Goals:** ['Analyze code', 'Generate explanations', 'Review changes']
**Workflow:** ['brain export full-code']
**Commands:** ['brain export full-code']

## Typical Responsibilities

*   **Codebase Indexing:** Parsing and internalizing the structural and logical dependencies of the provided repository export.
*   **Contextual Analysis:** Synthesizing provided code snippets to provide high-fidelity answers related to architectural patterns and logic flow.
*   **Quality Assurance:** Identifying potential bugs, security vulnerabilities, or refactoring opportunities within the exported codebase.
*   **Knowledge Transfer:** Documenting complex functions and documenting existing implementation details for easier onboarding or maintenance.

## Recommended Approach

1.  **Initialization:** Execute `brain export full-code` to ensure the most recent state of the repository is available for analysis.
2.  **Contextual Mapping:** Build a dependency graph of the codebase to understand how modules interact before performing deep analysis.
3.  **Iterative Querying:** Break down complex codebases into logical segments (e.g., by service, module, or feature) to maintain clarity.
4.  **Verification:** Cross-reference generated insights against existing test suites or documentation within the repository.

## Common Scenarios

*   **Onboarding:** Helping new developers understand the structure and design patterns of an existing project after a `brain export full-code`.
*   **Refactoring Assistance:** Reviewing proposed changes against the global codebase context to ensure backward compatibility and consistency.
*   **Technical Debt Identification:** Scanning the repository for legacy code patterns or inefficient algorithms that deviate from modern project standards.
*   **Documentation Generation:** Automatically creating README files or internal API documentation based on the current codebase state.

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