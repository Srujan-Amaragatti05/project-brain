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

* Ensuring local development environments are correctly configured and functional.
* Auditing project dependencies and configuration files for drift or errors.
* Monitoring CI/CD workflows to prevent pipeline failures.
* Reviewing code changes through diffs to ensure adherence to repository standards.
* Facilitating the onboarding of new developers by automating initialization sequences.

## Recommended Approach

* **Proactive Validation:** Run health checks frequently to detect configuration decay before it impacts build stability.
* **Standardization:** Utilize initialization scripts to enforce consistent tooling across all developer workstations.
* **Root Cause Analysis:** Leverage diagnostic tools immediately upon failure to isolate environment issues from code logic errors.
* **Incremental Verification:** Use diff analysis to verify the impact of configuration changes before committing to repository metadata.

## Common Scenarios

* **Onboarding New Contributors:** Running `brain project init` to bootstrap a new environment with the correct toolchains and dependencies.
* **Resolving Build Failures:** Executing `brain project doctor` to identify missing environment variables, mismatched versioning, or broken symlinks.
* **Code Review:** Invoking `brain diff show` to inspect non-obvious changes in build artifacts or environment-specific configuration files that might not be visible in standard PR views.
* **Environment Drift:** Periodically running status commands to reconcile local environment states with the project's baseline definition.

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