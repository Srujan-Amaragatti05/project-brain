# 🧠 project-brain

---

## 🚀 Badges

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![CLI](https://img.shields.io/badge/interface-CLI-black)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

**Developer Intelligence CLI for understanding codebases and changes at a deeper level.**

`project-brain` analyzes your code using AST, tracks Git changes at function level, and explains what actually changed — with optional AI support.

---

## 🚀 What Problem It Solves

* Git diffs are noisy → no semantic understanding
* Codebases are hard to navigate → no structure
* AI tools need clean input → code is messy

**project-brain bridges this gap by converting code into structured, explainable intelligence.**

---

## ⚙️ Installation

### Requirements

- Python **>= 3.10**
- Git (required for diff features)

### Install Locally

```bash
git clone <repo-url>
cd project-brain
pip install -e .
```

### CLI Access

```bash
project-brain
brain
```

---

## ⚡ Core Workflow

```bash
brain init
brain analyze
brain changes
brain explain
brain export
```

---

---

## 🧠 CLI Commands

### project init
Initializes project structure and creates `.brain/` directory and config files.

### project analyze [path]
Analyzes files and stores metadata in `.brain/data.json`.

### project summary
Displays summary of analyzed data.

### project doctor
Runs environment and setup checks.

### diff show [from_ref] [to_ref]
Displays git diff including file and function-level changes.

### diff review [from_ref] [to_ref]
Generates LLM-based explanation reports (JSON + HTML).

### diff explain <target>
Explains a file or function.

### export full_code
Exports entire codebase into a structured text file.

### export file <path>
Adds a file to export.

### export dir <path>
Adds a directory to export.

### export code_changes <from> <to>
Exports changed code between git references.

### testllm test
Tests LLM provider configuration.

---

## 📄 Output Structure

```
.brain/
├── data.json
├── index.json
├── cache/
├── exports/
├── reports/
├── logs.txt
```

---

## ⚙️ Configuration (brain.yaml)

Example:

```yaml
llm:
  provider: none
  model: ""
  api_key: ""

analysis:
  include_tests: false

diff:
  mode: function

export:
  full_code:
    max_file_size_kb: 200

explain:
  level: detailed
  include_risks: true

output:
  format: text
```

---

# 🧠 CLI COMMAND REFERENCE

This CLI follows a **pipeline model**:

> **Analyze → Detect → Explain → Export**

Each command represents a stage in this pipeline.

---

## 🔧 `brain init`

Initialize configuration for the project.

### Description

Creates a `brain.yaml` file with default settings.

### Responsibilities

* Setup analysis config
* Define ignore paths
* Configure LLM provider (optional)

### Usage

```bash
brain init
```

### Output

* Generates `brain.yaml`

---

## 🔍 `brain analyze`

Builds a structured representation of your codebase.

### Description

Parses source code using AST and creates an internal project map.

### Responsibilities

* Extract functions, classes, modules
* Build dependency-aware structure
* Store metadata in `.brain/`

### Usage

```bash
brain analyze
```

### Expected Behavior

* Runs locally
* No Git dependency required

### Output

* Internal metadata (not user-facing)

---

## 🔄 `brain changes`

Detects code changes using Git.

### Description

Compares current working state with previous commits.

### Responsibilities

* Identify modified files
* Track function-level changes
* Detect additions/removals

### Usage

```bash
brain changes
```

### Output Example

```txt
Modified File: src/api/user.py

Functions Changed:
- create_user()
- validate_email()

Summary:
+ Added validation logic
- Removed legacy flow
```

### Requirements

* Git repository must exist
* At least one commit required

---

## 🧠 `brain explain`

Explains detected changes in human-readable form.

### Description

Generates semantic explanations of changes with optional AI.

### Responsibilities

* Summarize code changes
* Identify risks
* Explain impact

### Usage

```bash
brain explain
```

### Behavior Modes

| Mode        | Description                    |
| ----------- | ------------------------------ |
| AI enabled  | Uses LLM for deep explanation  |
| AI disabled | Uses basic heuristic summaries |

### Output Example

```txt
This change introduces stricter validation before user creation.

Impact:
- Improves data integrity
- May break clients relying on previous behavior

Risk:
- Backward compatibility issues
```

---

## 📦 `brain export`

Exports code in AI-friendly format.

### Description

Bundles relevant files into structured output.

### Responsibilities

* Collect important files
* Remove ignored paths
* Format for LLM consumption

### Usage

```bash
brain export
```

### Output Example

```txt
=== FILE: src/api/user.py ===
<code>

=== FILE: src/utils/validation.py ===
<code>
```

---

## ⚙️ Global Configuration (`brain.yaml`)

```yaml
version: "1.0"

llm:
  provider: ollama
  model: phi3
  timeout_sec: 60

analysis:
  depth: fast
  include_tests: false
  ignore:
    - .brain/
    - .git/
    - node_modules/

explain:
  level: detailed
  include_risks: true
```

---

## 🧩 Command Relationships

| Command | Depends On | Purpose           |
| ------- | ---------- | ----------------- |
| init    | —          | Setup config      |
| analyze | init       | Build structure   |
| changes | analyze    | Detect diffs      |
| explain | changes    | Interpret changes |
| export  | analyze    | Prepare AI input  |

---

## 🎯 Real Use Cases

### 🔍 Code Review

```bash
brain analyze
brain changes
brain explain
```

→ Understand PR impact instantly

---

### 🧠 AI Debugging

```bash
brain export
```

→ Feed clean code into ChatGPT

---

### ⚡ Daily Development

```bash
brain changes
```

→ Know exactly what you changed

---

## 🤖 Supported LLM Providers

* OpenAI
* Ollama (local models)

> Fully usable without AI.

---

## 🛠 Troubleshooting

### No changes detected

* Ensure Git repo exists
* Commit at least once

---

### Empty export

* Check ignore rules
* Run `brain analyze` first

---

### LLM issues

* Verify API key (OpenAI)
* Ensure Ollama is running

---

## 🤝 Contributing

* Fork repo
* Create feature branch
* Keep PRs focused
* Add tests if needed

---

## 📌 Positioning

> **project-brain is a developer intelligence CLI that converts code and Git diffs into structured, explainable insights.**

---

## 🔮 Roadmap

### v1.0

* CLI stability improvements
* Better diff precision

### v2.0

* Plugin system
* Multi-language support

### v3.0

* CI integration
* Team workflows

---

## 📜 License

MIT
