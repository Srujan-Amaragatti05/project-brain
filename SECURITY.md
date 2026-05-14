# Security Policy

## Supported Versions

Security updates are currently provided for the latest release only.

---

## Reporting Vulnerabilities

Please do not open public GitHub issues for security vulnerabilities.

Instead, contact the maintainer directly with:

* reproduction steps
* affected version
* impact description

---

## Security Principles

project-brain is designed around:

* local-first workflows
* optional cloud integrations
* environment-variable-based secret handling

API keys should NEVER be committed to repositories.

Supported environment variables:

* OPENAI_API_KEY
* GEMINI_API_KEY
* HUGGINGFACE_API_KEY

---

## Scope

Potential security-sensitive areas include:

* export pipelines
* file traversal
* subprocess git execution
* LLM provider integrations
