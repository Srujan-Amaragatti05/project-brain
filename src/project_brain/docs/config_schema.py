CONFIG_SCHEMA = {
    "version": {
        "type": "string",
        "default": "1.1.0",
        "description": "Configuration schema version.",
    },
    "llm.provider": {
        "type": "enum",
        "default": "none",
        "allowed": [
            "none",
            "openai",
            "ollama",
            "gemini",
            "huggingface",
        ],
        "description": "Active LLM provider for code review and explanation.",
    },
    "llm.model": {
        "type": "string",
        "default": "",
        "description": "Specific model name to use with the selected provider.",
    },
    "llm.timeout_sec": {
        "type": "integer",
        "default": 60,
        "description": "Timeout in seconds for provider requests.",
    },
    "analysis.depth": {
        "type": "enum",
        "default": "fast",
        "allowed": [
            "fast",
            "full",
        ],
        "description": "Granularity of repository analysis.",
    },
    "analysis.include_tests": {
        "type": "boolean",
        "default": False,
        "description": "Whether to include test files in general analysis.",
    },
    "analysis.ignore": {
        "type": "list",
        "default": [".brain/", ".git/", "node_modules/", "venv/"],
        "description": "Patterns to exclude from repository analysis.",
    },
    "diff.mode": {
        "type": "enum",
        "default": "function",
        "allowed": ["function", "file"],
        "description": "Diff analysis granularity (function-level or file-level).",
    },
    "export.full_code.include_tests": {
        "type": "boolean",
        "default": False,
        "description": "Include test files in full-code exports.",
    },
    "export.full_code.max_file_size_kb": {
        "type": "integer",
        "default": 200,
        "description": "Skip files larger than this size in full-code exports.",
    },
    "export.manual_add.allow_duplicates": {
        "type": "boolean",
        "default": True,
        "description": "Allow adding the same file multiple times to an export.",
    },
    "export.changes.mode": {
        "type": "enum",
        "default": "function",
        "allowed": ["function", "file"],
        "description": "Granularity for code-changes export.",
    },
    "export.changes.include_context": {
        "type": "boolean",
        "default": True,
        "description": "Include surrounding code context in change exports.",
    },
    "export.changes.output_path": {
        "type": "string",
        "default": ".brain/exports/code_changes.txt",
        "description": "Default destination for code-change exports.",
    },
    "export.ignore": {
        "type": "list",
        "default": [".brain/", ".git/", "node_modules/"],
        "description": "Patterns to exclude specifically from exports.",
    },
    "explain.level": {
        "type": "enum",
        "default": "detailed",
        "allowed": ["concise", "detailed"],
        "description": "Verbosity of code explanations.",
    },
    "explain.include_risks": {
        "type": "boolean",
        "default": True,
        "description": "Include potential security/logic risks in explanations.",
    },
    "output.format": {
        "type": "enum",
        "default": "text",
        "allowed": [
            "text",
            "json",
            "markdown",
        ],
        "description": "CLI output rendering format.",
    },
}
