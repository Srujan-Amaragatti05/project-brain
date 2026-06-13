# LLM providers

_Auto-generated — do not edit manually._

---

Set your provider in `brain.yaml`:

```yaml
llm:
  provider: openai   # none | openai | ollama | gemini | huggingface
  model: gpt-4o
```

---

### `none`

Fully offline local-first mode.

| Property | Value |
|----------|-------|
| Mode | 💾 Offline |
| API key | Not required |
| Environment variable | — |

---

### `openai`

OpenAI Responses API integration.

| Property | Value |
|----------|-------|
| Mode | ☁️ Cloud |
| API key | Required |
| Environment variable | `OPENAI_API_KEY` |

---

### `ollama`

Local Ollama runtime integration.

| Property | Value |
|----------|-------|
| Mode | 🖥️ Local |
| API key | Not required |
| Environment variable | — |

---

### `gemini`

Google Gemini integration.

| Property | Value |
|----------|-------|
| Mode | ☁️ Cloud |
| API key | Required |
| Environment variable | `GEMINI_API_KEY` |

---

### `huggingface`

HuggingFace inference integration.

| Property | Value |
|----------|-------|
| Mode | ☁️ Cloud |
| API key | Required |
| Environment variable | `HUGGINGFACE_API_KEY` |

---
