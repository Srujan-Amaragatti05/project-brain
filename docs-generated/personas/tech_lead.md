# Tech Lead

## Who Is This Persona

**Persona:** Tech Lead

**Description:** Leads engineering decisions and reviews.

**Goals:**
* Review implementations
* Guide architecture
* Coordinate development

**Workflow:**
* brain project analyze
* brain diff review
* brain export code-changes

**Commands:**
* brain diff review

## Typical Responsibilities

* Setting technical standards and ensuring code quality across the codebase.
* Facilitating architectural discussions to ensure scalability and maintainability.
* Mentoring engineers and providing constructive feedback during code reviews.
* Balancing feature velocity with technical debt reduction.
* Bridging the gap between high-level product requirements and low-level technical execution.

## Recommended Approach

* **Context-First:** Utilize `brain project analyze` before making decisions to understand the existing architectural patterns and legacy constraints.
* **Rigorous Review:** Use `brain diff review` to enforce design patterns and performance standards before merging changes.
* **Evidence-Based Guidance:** Provide clear, actionable feedback linked to specific code sections to foster team growth.
* **Iterative Refinement:** Rely on `brain export code-changes` to document and apply structural refactors consistently.

## Common Scenarios

* **Code Review Bottleneck:** Analyzing a large pull request to ensure it aligns with the project's long-term architectural goals rather than just syntax correctness.
* **Technical Debt Assessment:** Running `brain project analyze` to identify clusters of high-complexity code that require immediate refactoring.
* **Onboarding New Features:** Coordinating cross-team efforts by reviewing implementation plans and diffs to prevent regression in critical paths.
* **System Design Shifts:** Transitioning a module to a new pattern by defining the changes and exporting them as standardized templates for the team to follow.

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