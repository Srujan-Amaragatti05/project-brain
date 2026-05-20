CONFIG_SCHEMA = {
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
        "description": "Active LLM provider.",
    },
    "llm.timeout_sec": {
        "type": "integer",
        "default": 60,
        "description": "Timeout for provider requests.",
    },
    "analysis.depth": {
        "type": "enum",
        "default": "fast",
        "allowed": [
            "fast",
            "full",
        ],
        "description": "Repository analysis depth.",
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