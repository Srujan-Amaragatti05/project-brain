# 🧠 project-brain

> **Developer Intelligence CLI for understanding codebases and code evolution at a semantic level.**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![CLI](https://img.shields.io/badge/interface-CLI-black)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Tests](https://github.com/Srujan-Amaragatti05/project-brain/actions/workflows/tests.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/project-brain-cli)
![Downloads](https://static.pepy.tech/badge/project-brain-cli)

---

## 🚀 What is project-brain?

`project-brain` is a CLI-first developer intelligence tool built for analyzing codebases, tracking Git changes at function level, generating structured exports for AI systems, and explaining code changes using optional LLM integrations.

Unlike traditional Git tooling that operates on raw line diffs, project-brain uses AST-based parsing to understand code structure and produce developer-friendly insights.

The project is designed around a **local-first**, **privacy-friendly**, and **AI-optional** workflow.

---

# 🎯 Why project-brain Exists

Modern development workflows suffer from several problems:

### Git diffs are noisy

Traditional diffs show line changes, not semantic meaning.

A small refactor can generate large diffs while hiding the actual behavioral impact.

---

### Codebases become difficult to understand

Large repositories contain:

* deeply nested modules
* duplicated logic
* unclear ownership
* hidden dependencies

Understanding them manually is slow.

---

### AI tools require structured context

Most AI systems perform poorly when fed raw repositories.

project-brain creates:

* structured exports
* focused change sets
* function-level intelligence
* AI-friendly context

---

### Local-first tooling matters

Many developers do not want:

* automatic code uploads
* cloud dependency
* vendor lock-in

project-brain works fully offline when:

```yaml
llm:
  provider: none
```

---

# ✨ Features

## Implemented

* 🔍 Recursive repository scanning
* 🧠 AST-based Python analysis
* 🧩 Function extraction
* 🏛️ Class extraction
* 🔄 Git diff parsing
* 📌 Function-level change tracking
* 📦 AI-friendly code export system
* 🤖 Optional LLM explanations
* 💾 Explanation caching
* 🌐 HTML diff reports
* ⚠️ Config validation
* 🩺 Environment diagnostics
* 🪵 Persistent logging
* 🚫 Binary file skipping
* 🛡️ Invalid Python safety handling
* ⚡ Deep directory traversal

---

# 🏗️ Architecture Overview

project-brain is structured into independent modules.

```text
CLI Layer
│
├── Analyzer
├── Diff Engine
├── Explain Engine
├── Export Engine
├── Doctor / Diagnostics
├── Config Validation
├── Logging System
└── LLM Provider Layer
```

---

## 🔍 Analyzer

Responsible for:

* filesystem traversal
* AST parsing
* metadata extraction
* hashing files
* extracting functions/classes

Uses Python `ast` module for semantic analysis.

---

## 🔄 Diff Engine

Responsible for:

* Git diff parsing
* tracking modified files
* function-level change detection
* comparing AST extracted function bodies

Supports:

* added files
* modified files
* deleted files

---

## 🧠 Explain Engine

Responsible for:

* generating semantic explanations
* producing structured summaries
* LLM provider integration
* caching explanations
* fallback behavior when AI disabled

---

## 📦 Export Engine

Responsible for:

* exporting entire repositories
* exporting changed code only
* generating AI-friendly code bundles
* structured file aggregation

---

## 🤖 LLM Provider Layer

Supports:

* OpenAI
* Ollama
* Gemini
* HuggingFace

Provider abstraction includes:

* timeout handling
* model listing
* response normalization
* error handling

---

## 💾 Cache System

Explanation results are cached inside:

```text
.brain/cache/
```

This avoids repeated LLM calls for unchanged function diffs.

---

# ⚙️ Installation

---

## Requirements

* Python >= 3.10
* Git installed
* Optional:

  * Ollama
  * OpenAI API access
  * Gemini API access
  * HuggingFace API access

---

## Install from PyPI

```bash
pip install project-brain-cli
```

---

## Verify Installation

```bash
brain --version
```

---

## Upgrade

```bash
pip install --upgrade project-brain-cli
```
---

## CLI Aliases

Both commands work:

```bash
brain
```

```bash
project-brain
```

---

# ⚡ Quick Start (30 Seconds)

---

## 1. Initialize project-brain

```bash
brain project init
```

Creates:

```text
.brain/
brain.yaml
```

---

## 2. Analyze Repository

```bash
brain project analyze .
```

Performs:

* recursive scan
* AST parsing
* metadata generation

Stores results inside:

```text
.brain/data.json
```

---

## 3. Inspect Git Changes

```bash
brain diff show
```

Default behavior:

```text
HEAD~1 → HEAD
```

Shows:

* modified files
* added files
* deleted files
* function-level changes

---

## 4. Export AI-Friendly Context

```bash
brain export full_code
```

Creates:

```text
.brain/exports/full_code.txt
```
---

## 5. Access Community Resources

```bash
brain community
```

Open feedback/discussions directly:

```bash
brain --feedback
```

---

# 🧠 Command Reference

---

# 📁 Project Commands

---

## `brain project init`

Initialize project-brain.

### Syntax

```bash
brain project init
```

### What It Does

Creates:

* `.brain/`
* `.brain/cache/`
* `.brain/data.json`
* `.brain/index.json`
* `brain.yaml`

### Notes

* Existing files are preserved
* Safe to rerun

---

## `brain project analyze`

Analyze repository structure.

### Syntax

```bash
brain project analyze [path]
```

### Arguments

| Argument | Default | Description    |
| -------- | ------- | -------------- |
| path     | `.`     | Root directory |

---

### Internal Behavior

* recursively traverses directories
* skips ignored paths
* skips binary files
* optionally skips tests
* extracts:

  * functions
  * classes
  * hashes
  * metadata

---

### Output

```text
.brain/data.json
```

---

### Example

```bash
brain project analyze .
```

---

### Edge Cases

* invalid Python files are skipped safely
* unreadable files do not crash analysis

---

## `brain project summary`

Generate repository summary.

### Syntax

```bash
brain project summary
```

### What It Shows

* total files
* total functions
* total classes
* top files by function count
* detected architecture hints

---

### Output Modes

Configured using:

```yaml
output:
  format: text
```

Supported:

* text
* json
* markdown

---

## `brain project doctor`

Run comprehensive environment and repository diagnostics.

### Syntax

```bash id="j9l8qk"
brain project doctor
```

---

### What It Checks

#### Environment

* Python installation/version
* operating system info
* virtual environment detection
* Git installation

---

#### Repository

* Git repository detection
* current branch
* latest commit
* repository size

---

#### Analysis

* `.brain/` initialization
* analysis database presence
* analyzed file count
* analysis freshness/staleness detection

---

#### Exports

* exports directory availability
* full code export presence
* code changes export presence

---

#### LLM

* configured provider
* provider status
* offline mode detection

---

### Example Output

```text id="zx9v4m"
🩺 Project Brain Diagnostics

Environment
✔ Python 3.14
✔ Virtual environment active
✔ Git installed

Repository
✔ Git repository detected
✔ Branch: dev

Analysis
✔ data.json exists
⚠ Analysis may be stale

Exports
✔ Full code export available

LLM
ℹ Provider: none
ℹ LLM disabled
```

---

### Final Status

| Status    | Meaning                             |
| --------- | ----------------------------------- |
| READY     | Repository fully configured         |
| PARTIAL   | Configuration incomplete but usable |
| NOT READY | Critical setup missing              |

---

### Notes

Freshness warnings appear when:

* repository changes may not match current analysis
* `data.json` appears outdated

Recommended refresh:

```bash id="2twmq7"
brain project analyze .
```

---

### Notes

The doctor system is designed to:

* detect broken setups early
* validate developer environments
* reduce CLI/runtime failures
* improve operational reliability


---

# 🔄 Diff Commands

---

## `brain diff show`

Show repository changes.

### Syntax

```bash
brain diff show [from_ref] [to_ref]
```

---

### Default Behavior

If no refs provided:

```bash
brain diff show
```

Equivalent to:

```bash
brain diff show HEAD~1 HEAD
```

---

### Git Reference Explanation

| Ref    | Meaning               |
| ------ | --------------------- |
| HEAD   | current commit        |
| HEAD~1 | previous commit       |
| HEAD~5 | 5 commits before HEAD |

---

### Internal Workflow

project-brain:

1. validates git refs
2. runs git diff logic
3. computes changed files
4. extracts Python functions
5. compares function bodies

---

### Output Example

```text
Files Changed: 2

Modified:
* src/api.py

Added:
* src/utils.py

Deleted:
* src/legacy.py
```

---

### Function-Level Output

```text
Functions Added:
* validate_user

Functions Modified:
* create_user
```

---

### Edge Cases

* non-Python files only receive file-level diff
* invalid git refs fail safely
* non-git repositories rejected

---

## `brain diff review`

Generate semantic diff explanations.

### Syntax

```bash
brain diff review [from_ref] [to_ref]
```

---

### What It Does

* computes git diff
* extracts changed functions
* builds prompts
* calls LLM provider
* caches results
* generates reports

---

### Outputs

```text
.brain/reports/diff_<timestamp>.json
.brain/reports/diff_<timestamp>.html
```

---

### HTML Report

Interactive HTML report includes:

* grouped files
* risk labels
* semantic summaries
* impact descriptions

---

### LLM Disabled Mode

If:

```yaml
provider: none
```

project-brain generates fallback heuristic summaries.

---

## `brain diff explain`

Explain a file or function.

### Syntax

```bash
brain diff explain <target>
```

---

### File Example

```bash
brain diff explain src/api.py
```

---

### Function Example

```bash
brain diff explain src/api.py:create_user
```

---

### Behavior

Without LLM:

* structural summary only

With LLM:

* semantic explanation
* risks
* logic overview

---

# 📦 Export Commands

---

## `brain export full_code`

Export entire repository.

### Syntax

```bash
brain export full_code
```

---

### Output

```text
.brain/exports/full_code.txt
```

---

### Export Format

```text
=== FILE: src/api.py ===
<content>
```

---

### Behavior

* recursively scans files
* respects ignore rules
* respects file size limits
* optionally skips tests

---

## `brain export file`

Manually export single file.

### Syntax

```bash
brain export file <path>
```

---

### Example

```bash
brain export file src/api.py
```

---

## `brain export dir`

Manually export directory.

### Syntax

```bash
brain export dir <path>
```

---

### Example

```bash
brain export dir src/
```

---

## `brain export code_changes`

Export changed code between refs.

### Syntax

```bash
brain export code_changes <from_ref> <to_ref>
```

---

### Example

```bash
brain export code_changes HEAD~3 HEAD
```

---

### Output

```text
=== FILE: src/api.py ===

--- FUNCTION: create_user (UPDATED) ---
OLD:
...

NEW:
...
```

---

# 🧪 LLM Commands

---

## `brain testllm test`

Test provider connectivity.

### Syntax

```bash
brain testllm test
```

---

### What It Does

* loads provider config
* sends test prompt
* validates response
* optionally fetches model list

---

### Disabled Mode

If:

```yaml
provider: none
```

Output:

```text
LLM disabled
```

---

# ⚙️ Configuration

Configuration file:

```text
brain.yaml
```

---

# Example Configuration

```yaml id="g8r7wq"
version: "1.1.0"

llm:
  provider: none
  model: ""
  timeout_sec: 60

analysis:
  depth: fast
  include_tests: false

  ignore:
    - .brain/
    - .git/
    - node_modules/
    - venv/
    - .venv/
    - __pycache__/
    - env/
    - .env/
    - project_brain_cli.egg-info/
    - tests/
    - test/

diff:
  mode: function

export:
  full_code:
    include_tests: false
    max_file_size_kb: 200

  manual_add:
    allow_duplicates: true

  changes:
    mode: function
    include_context: true
    output_path: .brain/exports/code_changes.txt

  ignore:
    - .brain/
    - .git/
    - node_modules/
    - venv/
    - .venv/
    - __pycache__/
    - env/
    - .env/
    - project_brain_cli.egg-info/
    - tests/
    - test/

explain:
  level: detailed
  include_risks: true

output:
  format: text
```

---

# 🔑 API Key Setup

Secrets should NEVER be stored inside `brain.yaml`.

---

## Windows CMD

```bash
setx OPENAI_API_KEY "your_key"
```

```bash
setx GEMINI_API_KEY "your_key"
```

```bash
setx HUGGINGFACE_API_KEY "your_key"
```

---

## PowerShell

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY","your_key","User")
```

---

## Linux/macOS

```bash
export OPENAI_API_KEY="your_key"
```

---

# 📴 Offline Mode

project-brain fully supports offline workflows.

Use:

```yaml
llm:
  provider: none
```

Behavior:

* no API calls
* no cloud dependency
* local-only analysis
* fallback explanations enabled

---

# 📄 Example Outputs

---

## Analysis

```text
🔍 Analyzing: .

📋 File Paths:
src/api.py
src/utils.py

✅ Analysis complete
```

---

## Diff Review

```text
Function: create_user

Change:
Added validation layer

Impact:
Improves input integrity

Risk:
medium
```

---

# 📁 Project Structure

```text
project-brain/
│
├── src/
│   └── project_brain/
│       ├── cli.py
│       ├── core/
│       ├── llm/
│       ├── storage/
│       └── config/
│
├── tests/
├── brain.yaml
├── pyproject.toml
└── README.md
```

---

# 🪵 Logging System

Logs stored inside:

```text
.brain/logs.txt
```

Tracks:

* warnings
* provider failures
* parsing errors
* export failures
* cache issues

Logging failures never crash the CLI.

---

# 🛠️ Troubleshooting

---

## ❌ Not a git repository

Initialize git:

```bash
git init
```

---

## ❌ Invalid git reference

Check refs:

```bash
git log --oneline
```

---

## ❌ Empty export

Possible causes:

* ignored paths
* file size limits
* tests excluded

---

## ❌ Provider failures

Check:

* API keys
* internet connectivity
* provider model name

---

## ❌ Missing API key

Verify environment variable:

```bash
echo %OPENAI_API_KEY%
```

---

# 🧪 Testing & QA

Current QA status:

* 18 automated tests passing
* export validation
* function diff validation
* config validation
* edge-case handling
* provider fallback testing

---
# 🌍 Community & Feedback

project-brain includes built-in community workflows to simplify feedback and contributor interaction.

---

## Open Feedback Page

```bash
brain --feedback
```

Behavior:

* opens GitHub Discussions page
* fallback prints URL if browser launch fails

---

## Community Resources

```bash
brain community
```

Displays:

* GitHub repository
* PyPI package
* Discussions
* Issues
* documentation links

---

## GitHub Discussions

Use Discussions for:

* feature ideas
* workflow discussions
* troubleshooting
* integrations
* feedback

Repository:
[project-brain GitHub Repository](https://github.com/Srujan-Amaragatti05/project-brain?utm_source=chatgpt.com)

Discussions:
[project-brain Discussions](https://github.com/Srujan-Amaragatti05/project-brain/discussions?utm_source=chatgpt.com)

PyPI:
[project-brain-cli on PyPI](https://pypi.org/project/project-brain-cli/?utm_source=chatgpt.com)


---
# 🔮 Roadmap

## Near-Term

* semantic diff intelligence
* integration tests
* incremental analysis
* performance improvements
* rename detection

---

## Mid-Term

* multi-language parsing
* plugin architecture
* dependency graphing
* richer semantic indexing

---

# 🔐 Security & Privacy

project-brain is designed with a local-first philosophy.

Key principles:

* no automatic code uploads
* offline workflows supported
* API keys via environment variables only
* repository data stored locally

LLM usage is fully optional.

---

# 🤝 Contributing

Contributions are welcome.

Recommended workflow:

```bash
git checkout -b feature/my-feature
```

Guidelines:

* keep PRs focused
* preserve CLI consistency
* add tests for new logic
* avoid unnecessary dependencies

---

# 📜 License

MIT License

---

# 🧠 Final Positioning

> project-brain is a local-first developer intelligence CLI that transforms repositories and Git diffs into structured, explainable engineering context.
