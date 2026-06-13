# Maintainer

## Who Is This Persona

**Persona:** maintainer

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

* Ensuring all project dependencies and configurations meet current environment requirements.
* Monitoring repository health through automated diagnostic checks.
* Managing CI/CD workflows to ensure consistent build and deployment quality.
* Auditing code changes via diff analysis to prevent regression.
* Provisioning new development environments to ensure project consistency.

## Recommended Approach

* **Proactive Diagnosis:** Run diagnostic checks regularly to identify potential environment drift before it affects development.
* **Standardization:** Use initialization scripts to ensure all contributors operate within a unified, tested environment.
* **Transparency:** Utilize diff tools to conduct thorough reviews of structural changes, ensuring that configuration updates align with project standards.
* **Iterative Improvement:** Treat workflow maintenance as a core task, applying feedback from the "doctor" commands to refine project tooling.

## Common Scenarios

* **Onboarding New Contributors:** Running `brain project init` to configure the local environment and verify system prerequisites.
* **Resolving CI Failures:** Executing `brain project doctor` to pinpoint discrepancies between the local environment and the project's expected configuration.
* **Reviewing Configuration Changes:** Using `brain diff show` to validate updates to environment files or workflow definitions before committing them to the repository.
* **Post-Update Verification:** Running diagnostic suite commands after a dependency upgrade to ensure project stability.

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