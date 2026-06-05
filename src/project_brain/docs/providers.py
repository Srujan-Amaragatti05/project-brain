PROVIDER_REGISTRY = {
    "none": {
        "mode": "offline",
        "requires_api_key": False,
        "description": "Fully offline local-first mode.",
    },
    "openai": {
        "mode": "cloud",
        "requires_api_key": True,
        "env_var": "OPENAI_API_KEY",
        "description": "OpenAI Responses API integration.",
    },
    "ollama": {
        "mode": "local",
        "requires_api_key": False,
        "description": "Local Ollama runtime integration.",
    },
    "gemini": {
        "mode": "cloud",
        "requires_api_key": True,
        "env_var": "GEMINI_API_KEY",
        "description": "Google Gemini integration.",
    },
    "huggingface": {
        "mode": "cloud",
        "requires_api_key": True,
        "env_var": "HUGGINGFACE_API_KEY",
        "description": "HuggingFace inference integration.",
    },
}