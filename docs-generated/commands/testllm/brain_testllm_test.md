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

_No demo available._


---

## Usage Guide

### When would I use this?

Use this command when you need to verify that your LLM provider is correctly configured and reachable. It is the primary tool for troubleshooting connection issues between your environment and the LLM API.

### How it fits in the workflow

Before initiating complex tasks like `brain diff review` or executing automated code generation, run this command to ensure your credentials and API endpoints are functional. It serves as a pre-flight check to validate that the underlying communication channel is stable.

### Practical tips

*   Run this command immediately after updating your `brain.yaml` file to confirm your API keys are valid.
*   Use this as the first step in your debugging process if you receive unexpected response errors during normal operation.
*   Incorporate this into your CI/CD pipeline or environment setup scripts to ensure developers have configured their local access correctly.

### Common failure causes

*   **LLM_PROVIDER_FAILURE**: The configured provider is returning an error, usually due to an expired API key, network restrictions, or service outages.
*   **Misconfiguration**: The credentials or endpoint URL defined in `brain.yaml` are incorrect or improperly formatted.
*   **Network/Proxy**: Local firewall settings or corporate proxy requirements are blocking the connection to the LLM provider's API.

### FAQ

**Does this command consume tokens?**
No, this is a connectivity check and does not perform significant processing, though it may trigger a minor heartbeat request depending on your provider.

**What if I receive an LLM_PROVIDER_FAILURE error?**
Check your `brain.yaml` file to ensure the provider is correctly defined and that your API credentials have not expired. Verify your internet connection or proxy settings if necessary.

**Is it required to run this every time?**
No, it is only necessary when you suspect connectivity issues or after modifying your configuration.
