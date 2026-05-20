ERROR_REGISTRY = {
    "NOT_GIT_REPO": {
        "message": "Current directory is not a git repository.",
        "cause": [
            "Git repository was never initialized.",
            "Command executed outside repository root.",
        ],
        "fix": [
            "Run: git init",
            "Create initial commit.",
        ],
        "severity": "high",
        "related_commands": [
            "brain diff show",
            "brain diff review",
        ],
    },
    "INVALID_GIT_REF": {
        "message": "Invalid git reference.",
        "cause": [
            "Branch does not exist.",
            "Commit hash invalid.",
            "Repository has insufficient history.",
        ],
        "fix": [
            "Run: git log --oneline",
            "Verify branch names.",
        ],
        "severity": "medium",
        "related_commands": [
            "brain diff show",
            "brain diff review",
            "brain export code_changes",
        ],
    },
    "LLM_PROVIDER_FAILURE": {
        "message": "LLM provider request failed.",
        "cause": [
            "Invalid API key.",
            "Provider outage.",
            "Model unavailable.",
            "Timeout exceeded.",
        ],
        "fix": [
            "Verify API key.",
            "Verify model name.",
            "Check internet connectivity.",
        ],
        "severity": "medium",
        "related_commands": [
            "brain diff review",
            "brain testllm test",
        ],
    },
}