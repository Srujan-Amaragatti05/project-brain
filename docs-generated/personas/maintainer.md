# Maintainer

## Who Is This Persona

**Persona:** Maintainer

**Description:** Maintains repository health and tooling.

**Goals:**
* Validate environment
* Diagnose problems
* Maintain workflows

**Workflow:**
* `brain project doctor`

**Commands:**
* `brain project init`
* `brain project doctor`
* `brain diff show`

## Typical Responsibilities

* Ensuring all environment dependencies are correctly configured and up to date.
* Monitoring repository health through automated diagnostics.
* Streamlining developer workflows to reduce friction and technical debt.
* Auditing code changes for consistency with project standards.
* Resolving configuration drifts or broken integration pipelines.

## Recommended Approach

* **Proactive Validation:** Execute `brain project doctor` frequently to preemptively identify potential issues before they impact development.
* **Standardization:** Utilize `brain project init` to enforce uniform tooling and configurations across new or existing environments.
* **Continuous Review:** Use `brain diff show` to maintain visibility over architectural changes and ensure alignment with established project patterns.
* **Documentation-First:** Maintain clear instructions for workflow execution to ensure team autonomy.

## Common Scenarios

* **Onboarding:** Setting up a fresh development environment for a new contributor using `brain project init`.
* **Troubleshooting:** Investigating CI/CD failures or local build issues by running the `brain project doctor` suite.
* **Code Review:** Inspecting granular changes via `brain diff show` to identify regressions or deviations from the repository's structural integrity.
* **Maintenance Windows:** Performing routine environment audits to prune outdated tools or sync local configs with updated master definitions.

---

## Overview

Maintains repository health and tooling.

## Statistics

- Recommended Commands: 3
- Workflow Steps: 1

## Typical Goals

- Validate environment
- Diagnose problems
- Maintain workflows

## Recommended Workflow

1. `brain project doctor`

## Recommended Commands

| Command | Description |
|----------|-------------|
| `brain diff show` | Show semantic git differences between references. |
| `brain project doctor` | Repository diagnostics and environment health checks. |
| `brain project init` | Initialize project-brain in the current directory |

## Related Personas

- Developer
- Reviewer