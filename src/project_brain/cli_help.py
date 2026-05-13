ROOT_HELP = """
🧠 project-brain

Developer intelligence CLI for understanding repositories,
Git changes, and AI-assisted code analysis.

COMMON WORKFLOW

  1. Initialize project
     brain project init

  2. Analyze repository
     brain project analyze .

  3. View project summary
     brain project summary

  4. Inspect code changes
     brain diff show

  5. Generate semantic review
     brain diff review

POPULAR COMMANDS

  project   Repository analysis and diagnostics
  diff      Git-aware change intelligence
  export    AI-friendly code exports
  testllm   Validate LLM connectivity

EXAMPLES

  brain diff show HEAD~3 HEAD
  brain export full_code
  brain diff explain src/api.py:create_user
"""

PROJECT_HELP = """
Project analysis and repository management commands.
"""

DIFF_HELP = """
Git-aware repository change analysis.
"""

EXPORT_HELP = """
Export repository content into AI-friendly formats.
"""

LLM_HELP = """
LLM provider testing and diagnostics.
"""