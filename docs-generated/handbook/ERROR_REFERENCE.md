# Error reference

_Auto-generated — do not edit manually._

---

### `NOT_GIT_REPO`

**Severity:** 🔴 High

**Message:** _Current directory is not a git repository._

**Causes**

- Git repository was never initialized.
- Command executed outside repository root.

**How to fix**

- Run: git init
- Create initial commit.

**Relevant commands:** `brain diff show` · `brain diff review`

---

### `INVALID_GIT_REF`

**Severity:** 🟡 Medium

**Message:** _Invalid git reference._

**Causes**

- Branch does not exist.
- Commit hash invalid.
- Repository has insufficient history.

**How to fix**

- Run: git log --oneline
- Verify branch names.

**Relevant commands:** `brain diff show` · `brain diff review` · `brain export code_changes`

---

### `LLM_PROVIDER_FAILURE`

**Severity:** 🟡 Medium

**Message:** _LLM provider request failed._

**Causes**

- Invalid API key.
- Provider outage.
- Model unavailable.
- Timeout exceeded.

**How to fix**

- Verify API key.
- Verify model name.
- Check internet connectivity.

**Relevant commands:** `brain diff review` · `brain testllm test`

---
