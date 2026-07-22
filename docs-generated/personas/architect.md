# Architect

## Who Is This Persona

**Persona:** Architect

**Description:** An expert in system design, infrastructure patterns, and repository organization, focused on maintaining technical integrity and scalability across complex codebases.

## Typical Responsibilities

*   **Structural Audits:** Evaluating folder hierarchies, module boundaries, and dependency graphs.
*   **Design Pattern Enforcement:** Ensuring consistency in architecture across microservices or monolithic structures.
*   **Documentation Synthesis:** Generating high-level summaries of complex system designs for stakeholder review.
*   **Technical Debt Identification:** Pinpointing bottlenecks and architectural anti-patterns that hinder scalability.
*   **Knowledge Transfer:** Exporting codebase snapshots for external auditing or cross-team onboarding.

## Recommended Approach

1.  **Discovery:** Execute `brain project analyze` to map out the technical landscape and identify core architectural pillars.
2.  **Contextualization:** Use `brain project summary` to distill the purpose, stack, and structural logic of the repository.
3.  **Visualization:** Utilize `brain export tree` to provide a clear mental model of the project’s file hierarchy for stakeholders.
4.  **Verification:** Implement `brain export full-code` to facilitate a deep-dive peer review or archival of the system state.

## Common Scenarios

*   **Onboarding:** A new lead dev needs an immediate high-level grasp of an existing, undocumented repository.
*   **Refactoring:** Initiating a major restructuring effort requires an objective analysis of current module coupling.
*   **Code Audits:** An external security or architectural review necessitates a complete export and visual summary of the source code.
*   **Scalability Planning:** Assessing whether the current directory structure can support a planned increase in service count or complexity.

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