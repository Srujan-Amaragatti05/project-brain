# Contributing to project-brain

Thank you for contributing to project-brain.

## Development Setup

```bash
git clone https://github.com/Srujan-Amaragatti05/project-brain
cd project-brain

python -m venv env

# Windows
env\Scripts\activate

# Linux/macOS
source env/bin/activate

pip install -e .
```

---

## Running Tests

```bash
pytest
```

---

## Contribution Guidelines

Please:

* keep PRs focused
* preserve CLI consistency
* add tests for new behavior
* avoid unnecessary dependencies
* maintain local-first philosophy

---

## Recommended Workflow

```bash
git checkout -b feature/my-feature
```

Commit style:

```text
feat: add semantic export filtering
fix: improve git diff handling
docs: update README
```

---

## Pull Requests

Before opening a PR:

* tests should pass
* CLI commands should work
* documentation should be updated if behavior changed

---

## Philosophy

project-brain prioritizes:

* developer productivity
* semantic understanding
* privacy-friendly tooling
* local-first workflows
