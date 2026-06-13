# ProjectBrain Documentation

## What Is ProjectBrain
ProjectBrain is an advanced orchestration framework designed to streamline project management, code analysis, and intelligence-driven workflows within complex development environments.

## Key Capabilities
- Automated repository analysis and summarization.
- Intelligent code difference explanation and review.
- Multi-persona task execution.
- LLM testing and validation.
- Standardized project health diagnostics.

## Core Workflows
1. **Initialization**: Establishing project context using `brain project init`.
2. **Analysis**: Executing deep scans with `brain project analyze` and `brain project summary`.
3. **Review**: Analyzing modifications via `brain diff` commands.
4. **Export**: Generating outputs using `brain export` suite.
5. **Validation**: Stress-testing configurations with `brain testllm`.

## Documentation Structure
The documentation is organized by functional modules, including command specifications, operational strategies for defined personas, and specific use case implementations to ensure modularity and ease of reference.

## Command Categories
- **diff**: `brain diff show`, `brain diff review`, `brain diff explain`
- **export**: `brain export full-code`, `brain export file`, `brain export dir`, `brain export code-changes`
- **project**: `brain project init`, `brain project analyze`, `brain project summary`, `brain project doctor`
- **testllm**: `brain testllm test`

## Getting Started
To begin, initialize your environment within the root directory of your project by executing `brain project init`. Follow the prompts to configure your preferences and verify system readiness using `brain project doctor`.

## Documentation Statistics
- Commands: 12
- Personas: 7
- Use Cases: 27