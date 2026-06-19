# `brain testllm test`

> Test configured LLM provider connectivity.

---

## Overview

Test configured LLM provider connectivity.

---

## When to use

This command is part of the **testllm** workflow.

---

## Syntax

```bash
brain testllm test [options]
```

---

## Parameters

_No parameters._

---

## Examples

```bash
brain testllm test
```

---

## Outputs

_None_

---

## Errors

| Code | Description |
|------|-------------|
| `LLM_PROVIDER_FAILURE` | LLM provider request failed. |

---

## Related commands

- `brain diff review`

---

## Notes

- Verifies configured LLM provider connectivity.

---

## Edge cases

- Provider must be configured in brain.yaml.

---

## Demo

![Demo: testllm.gif](../../../demo/gifs/testllm.gif)


---

## Usage Guide

### When would I use this?

Use this command to verify that your environment is correctly connected to the configured Large Language Model (LLM) provider. It is the primary diagnostic step to ensure that API keys, network settings, and provider availability are functioning as expected before running resource-intensive operations.

### How it fits in the workflow

1. **Configuration**: Edit `brain.yaml` to define your LLM provider and credentials.
2. **Verification**: Execute `brain testllm test` to confirm the handshake with the provider.
3. **Execution**: Proceed to use features like `brain diff review` once the connectivity report confirms a successful status.

### Practical tips

*   Run this command immediately after updating your `brain.yaml` file to validate syntax and credential integrity.
*   If you are switching between different LLM providers, use this command to ensure the new configuration is active and responsive.
*   Integrate this into your local environment setup script to ensure all dependencies are reachable for team members.

### Common failure causes

*   **LLM_PROVIDER_FAILURE**: The configured provider is returning an error (e.g., 401 Unauthorized, 429 Too Many Requests, or 503 Service Unavailable).
*   **Missing Configuration**: The `brain.yaml` file is missing the required provider settings or is incorrectly formatted.
*   **Network Restrictions**: Corporate firewalls or proxy settings are blocking the outbound connection to the LLM API endpoints.

### FAQ

**Does this command send data to the LLM?**
No, it only performs a lightweight handshake to test connectivity.

**What should I do if the test fails?**
Check your `brain.yaml` file for valid API keys and ensure your network environment allows traffic to the LLM provider's API.

**Do I need an internet connection to run this?**
Yes, the command requires an active connection to reach the external LLM provider service.
