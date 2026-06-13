# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

# [0.1.0] - 2026-05-14

Initial public release of `project-brain`.

project-brain is a CLI-first developer intelligence tool focused on:

* AST-based repository analysis
* function-level Git diff intelligence
* structured AI-friendly code exports
* optional LLM-powered explanations
* local-first developer workflows

---

## Added

### Core Analysis Engine

* Recursive repository scanning
* AST-based Python parsing
* Function extraction
* Class extraction
* File metadata indexing
* SHA256-based file tracking
* Binary file detection and skipping

### Git Diff Intelligence

* Git reference comparison
* File-level diff tracking
* Function-level diff analysis for Python
* Added / modified / deleted file detection
* Semantic function comparison workflows

### Export System

* Full repository export
* Single-file export
* Directory export
* Diff-based code export
* AI-friendly structured output format

### Explain Engine

* File explanation workflows
* Function explanation workflows
* LLM-assisted diff review generation
* Structured HTML diff reports
* JSON report generation
* Explanation caching system

### LLM Provider Layer

Support for:

* OpenAI
* Ollama
* Gemini
* HuggingFace

Offline/local-only mode:

```yaml
llm:
  provider: none
```

### Diagnostics & Validation

* Environment diagnostics system
* Repository readiness validation
* Git availability checks
* Config validation
* Provider validation
* Logging/error reporting system

### Configuration System

* YAML configuration support
* Recursive default merging
* Output formatting controls
* Export controls
* Explain-level controls

### CLI

Implemented command hierarchy:

```text
brain project init
brain project analyze
brain project summary
brain project doctor

brain diff show
brain diff review
brain diff explain

brain export full-code
brain export file
brain export dir
brain export code_changes

brain testllm test
```

---

## Improved

* Defensive error handling across CLI workflows
* Invalid Python parsing resilience
* Graceful subprocess failure handling
* Provider response normalization
* Recursive directory traversal stability
* Structured logging consistency

---

## Fixed

* Unicode-safe subprocess execution
* Safer file reading workflows
* Improved Git command handling
* Better provider fallback behavior
* More robust export filtering logic

---

## Testing & QA

### Automated Testing

* 18 automated tests passing
* CLI validation tests
* Export validation tests
* Function diff validation
* Config validation coverage

### Operational QA

Real-world repository testing executed against:

* Flask
* Typer
* Additional open-source repositories

Validation included:

* repository cloning
* CLI execution
* git-history processing
* export generation
* diagnostics validation
* runtime verification
* stdout/stderr capture
* failure detection

### CI/CD

* GitHub Actions CI integration
* Automated test execution
* Build validation workflows

---

## Notes

This is the first public OSS release of project-brain.

Current implementation focuses on:

* Python semantic analysis
* local-first workflows
* developer productivity tooling

Future releases will expand:

* semantic diff intelligence
* incremental analysis
* multi-language support
* richer repository indexing


# [1.1.0] - 2026-05-14
## Added

- community command group
- --feedback CLI option
- GitHub Discussions integration
- community resource panel

## Improved

- version consistency fixes
- packaging metadata cleanup
- OSS ecosystem readiness

## Fixed

- CLI version resolution issue
- package metadata mismatch