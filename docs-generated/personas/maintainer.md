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

* Ensuring all environment dependencies are correctly configured for contributors.
* Auditing project health via automated diagnostic checks.
* Managing repository workflows to prevent regressions.
* Reviewing configuration drift and applying patches.
* Monitoring CI/CD and local development environment stability.

## Recommended Approach

1. **Verify State:** Run `brain project doctor` frequently to ensure the local environment aligns with the source of truth.
2. **Standardize:** Use `brain project init` to enforce project-wide configurations and tooling versions.
3. **Analyze Changes:** Utilize `brain diff show` before any maintenance task to understand the delta between the current state and intended project standards.
4. **Iterative Repair:** Apply automated fixes provided by diagnostic tools rather than performing manual overrides.

## Common Scenarios

* **New Contributor Onboarding:** Running `brain project init` to bootstrap a clean environment.
* **Environment Troubleshooting:** Investigating build failures or test inconsistencies by executing `brain project doctor`.
* **Code Review Maintenance:** Comparing local project structure against repository standards using `brain diff show` to identify configuration drift.
* **Workflow Optimization:** Updating underlying project tooling and validating that existing workflows remain functional post-upgrade.

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