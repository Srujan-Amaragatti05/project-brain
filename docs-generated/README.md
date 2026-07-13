# ProjectBrain Documentation

## What Is ProjectBrain
ProjectBrain is an advanced utility designed to interface with complex codebases, providing deep analysis, automated documentation, and intelligent synchronization between human intent and machine execution.

## Key Capabilities
*   Automated repository analysis and summarization.
*   Intelligent diff generation and explanation for code changes.
*   Flexible export options for documentation and code segments.
*   Integrated testing framework for LLM-based verification.
*   Multi-persona support for tailored interaction models.

## Core Workflows
1.  **Project Initialization:** Establishing the workspace and indexing the codebase.
2.  **Analysis and Review:** Generating insights through diff explanation and project summaries.
3.  **Exportation:** Extracting specific code artifacts or file trees for external use.
4.  **Verification:** Running LLM-specific tests to ensure consistency and output quality.

## Documentation Structure
The documentation is organized by functional domains, mapping specific command sets to their respective utility roles, ensuring developers can navigate the tool's capabilities efficiently.

## Command Categories
*   **diff:** `brain diff show`, `brain diff review`, `brain diff explain`
*   **export:** `brain export full-code`, `brain export file`, `brain export dir`, `brain export code-changes`, `brain export tree`
*   **project:** `brain project init`, `brain project analyze`, `brain project summary`, `brain project doctor`
*   **testllm:** `brain testllm test`

## Getting Started
1.  Initialize your environment using `brain project init`.
2.  Analyze your current repository state with `brain project analyze`.
3.  Review changes using the `diff` command suite.
4.  Export required documentation or code segments as needed.

## Documentation Statistics
*   Total Commands: 13
*   Available Personas: 7
*   Supported Use Cases: 29