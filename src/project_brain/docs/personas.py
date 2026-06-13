PERSONA_REGISTRY = {
    "developer": {
        "description":
            "Builds and modifies application code.",
        "goals": [
            "Implement features",
            "Debug issues",
            "Understand code",
        ],
        "workflow": [
            "brain project analyze",
            "brain diff explain",
            "brain diff review",
        ],
    },

    "reviewer": {
        "description":
            "Reviews code changes and pull requests.",
        "goals": [
            "Review changes",
            "Identify risks",
            "Validate modifications",
        ],
        "workflow": [
            "brain diff show",
            "brain diff review",
        ],
    },

    "architect": {
        "description":
            "Understands system design and repository structure.",
        "goals": [
            "Analyze architecture",
            "Review structure",
            "Generate repository exports",
        ],
        "workflow": [
            "brain project analyze",
            "brain project summary",
            "brain export full-code",
        ],
    },

    "tech lead": {
        "description":
            "Leads engineering decisions and reviews.",
        "goals": [
            "Review implementations",
            "Guide architecture",
            "Coordinate development",
        ],
        "workflow": [
            "brain project analyze",
            "brain diff review",
            "brain export code-changes",
        ],
    },

    "maintainer": {
        "description":
            "Maintains repository health and tooling.",
        "goals": [
            "Validate environment",
            "Diagnose problems",
            "Maintain workflows",
        ],
        "workflow": [
            "brain project doctor",
        ],
    },

    "new contributor": {
        "description":
            "Learning the repository for the first time.",
        "goals": [
            "Understand project",
            "Navigate codebase",
            "Learn workflows",
        ],
        "workflow": [
            "brain project analyze",
            "brain project summary",
            "brain diff explain",
        ],
    },

    "ai assistant": {
        "description":
            "Consumes exported repository context.",
        "goals": [
            "Analyze code",
            "Generate explanations",
            "Review changes",
        ],
        "workflow": [
            "brain export full-code",
        ],
    },
}