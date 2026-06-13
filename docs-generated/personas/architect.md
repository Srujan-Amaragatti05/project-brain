# Architect

## Who Is This Persona

**Persona:** Architect

**Description:**
An expert in system design, repository structuring, and high-level software engineering principles. This persona focuses on the integrity, scalability, and maintainability of codebases.

## Typical Responsibilities

*   **Structural Analysis:** Evaluating existing directory hierarchies and module dependencies.
*   **Design Pattern Review:** Assessing the application of architectural patterns (e.g., MVC, Clean Architecture, Hexagonal).
*   **Technical Documentation:** Generating clear, concise summaries of project components and data flows.
*   **Refactoring Guidance:** Providing recommendations for decoupled, modular, and testable code organization.
*   **Knowledge Transfer:** Exporting full repository states to facilitate comprehensive reviews or documentation audits.

## Recommended Approach

1.  **Discovery:** Execute `brain project analyze` to map out the current directory tree and identify core design patterns.
2.  **Synthesis:** Utilize `brain project summary` to condense technical debt, architectural strengths, and component interdependencies into a high-level overview.
3.  **Documentation:** Use `brain export full-code` to produce a structured snapshot of the codebase for documentation, onboarding, or architectural auditing.

## Common Scenarios

*   **New Project Onboarding:** Quickly grasping the logic, dependencies, and entry points of a complex, unfamiliar repository.
*   **Technical Debt Audit:** Identifying areas of the system that lack clear separation of concerns or are becoming overly coupled.
*   **Documentation Automation:** Streamlining the creation of READMEs or architectural design records (ADRs) by extracting metadata directly from the file structure.
*   **System Migration:** Preparing a comprehensive repository export to assist in planning a transition or refactor to a new architectural paradigm.

---

## Overview

Understands system design and repository structure.

## Statistics

- Recommended Commands: 3
- Workflow Steps: 3

## Typical Goals

- Analyze architecture
- Review structure
- Generate repository exports

## Recommended Workflow

1. `brain project analyze`
2. `brain project summary`
3. `brain export full-code`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain export full-code` | Export entire codebase into structured file |
| `brain project analyze` | Analyze repository structure using AST parsing. |
| `brain project summary` | Summarize the analyzed data |

## Related Personas

- Developer
- Reviewer
- Ai Assistant