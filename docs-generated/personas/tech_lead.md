# Tech Lead

## Who Is This Persona

**Persona:** Tech Lead

**Description:** Leads engineering decisions and reviews.

**Goals:** ['Review implementations', 'Guide architecture', 'Coordinate development']

**Workflow:** ['brain project analyze', 'brain diff review', 'brain export code-changes']

**Commands:** ['brain diff review']

## Typical Responsibilities

*   **Architectural Oversight:** Establishing technical standards and ensuring long-term maintainability of the codebase.
*   **Code Quality Assurance:** Performing deep-dive reviews to ensure adherence to design patterns, security standards, and performance benchmarks.
*   **Technical Mentorship:** guiding engineers through complex challenges and promoting best practices.
*   **Strategic Alignment:** Bridging the gap between product requirements and technical feasibility.
*   **Cross-team Coordination:** Synchronizing efforts across engineering pods to prevent technical debt and integration friction.

## Recommended Approach

*   **Systemic Analysis:** Prioritize the use of `brain project analyze` to gain a holistic understanding of the current state before initiating changes.
*   **Iterative Reviews:** Utilize `brain diff review` to provide granular, constructive feedback that focuses on structural integrity rather than just syntax.
*   **Incremental Refactoring:** Favor small, verifiable changes exported via `brain export code-changes` to minimize risk and simplify debugging.
*   **Decoupled Logic:** Enforce strict interface contracts to ensure individual components remain testable and modular.
*   **Evidence-Based Decisions:** Base architectural pivots on objective data (performance metrics, complexity analysis) rather than subjective preference.

## Common Scenarios

*   **Pull Request Bottlenecks:** Resolving high-complexity code reviews where logic is unclear or violates established architectural patterns.
*   **Legacy System Integration:** Auditing an existing codebase to determine the most effective path for introducing a new, scalable module.
*   **Performance Optimization:** Identifying bottlenecks during a project analysis and implementing targeted refactors to improve system throughput.
*   **Onboarding New Features:** Translating high-level product requirements into actionable architectural blueprints for the engineering team.
*   **Technical Debt Management:** Conducting scheduled reviews to identify and prioritize the elimination of technical debt that hinders velocity.

---

## Overview

Leads engineering decisions and reviews.

## Statistics

- Recommended Commands: 1
- Workflow Steps: 3

## Typical Goals

- Review implementations
- Guide architecture
- Coordinate development

## Recommended Workflow

1. `brain project analyze`
2. `brain diff review`
3. `brain export code-changes`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain diff review` | Explain code changes using LLM |

## Related Personas

- Developer
- Reviewer