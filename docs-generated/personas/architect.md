# Architect

## Who Is This Persona

**Persona:** Architect

**Description:** Understands system design and repository structure.

**Goals:** ['Analyze architecture', 'Review structure', 'Generate repository exports']

**Workflow:** ['brain project analyze', 'brain project summary', 'brain export full-code']

**Commands:** ['brain project analyze', 'brain project summary', 'brain export full-code', 'brain export tree']

## Typical Responsibilities

*   **Structural Auditing:** Evaluating repository organization, modularity, and adherence to design patterns.
*   **System Mapping:** Creating high-level architectural overviews from complex codebases.
*   **Dependency Analysis:** Identifying coupling issues and ensuring clean separation of concerns.
*   **Knowledge Preservation:** Generating comprehensive documentation and codebase exports for architectural reviews or onboarding.
*   **Technical Governance:** Maintaining standards for folder structure, naming conventions, and resource management.

## Recommended Approach

1.  **Discovery:** Begin by running `brain project tree` to visualize the structural hierarchy and identify potential bottlenecks or organizational issues.
2.  **Evaluation:** Execute `brain project analyze` to extract insights into the core components, inter-dependencies, and technological stack.
3.  **Synthesis:** Utilize `brain project summary` to distill findings into actionable insights, highlighting design strengths and technical debt.
4.  **Reporting:** Use `brain export full-code` to produce documentation or raw assets required for architectural peer reviews or architectural decision records (ADRs).

## Common Scenarios

*   **Legacy Refactoring:** Mapping out old architectures to identify candidates for microservices migration or modularization.
*   **Onboarding:** Providing new team members with a rapid, high-level summary of the system’s architecture and design philosophy.
*   **Codebase Audits:** Conducting security or performance reviews based on structural weaknesses identified during the analysis phase.
*   **Knowledge Transfer:** Exporting the full project state for cross-team documentation or offboarding processes.

---

## Overview

Understands system design and repository structure.

## Statistics

- Recommended Commands: 4
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
| `brain export tree` | Export repository tree structure into tree and JSON formats. |
| `brain project analyze` | Analyze repository structure using AST parsing. |
| `brain project summary` | Summarize the analyzed data |

## Related Personas

- Developer
- Reviewer
- Ai Assistant