import os
import subprocess
from pathlib import Path

from project_brain.core.config_loader import load_config
from project_brain.core.doctor_checks.models import DoctorCheck


def run_llm_checks(root: Path):
    checks = []

    config = load_config(root)

    llm = config.get("llm", {})

    provider = llm.get("provider", "none")
    model = llm.get("model", "")

    checks.append(
        DoctorCheck(
            "LLM",
            "Provider",
            "info",
            provider,
        )
    )

    if provider == "none":
        checks.append(
            DoctorCheck(
                "LLM",
                "Status",
                "info",
                "LLM disabled",
            )
        )
        return checks

    if not model:
        checks.append(
            DoctorCheck(
                "LLM",
                "Model",
                "fail",
                "No model configured",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                "LLM",
                "Model",
                "pass",
                model,
            )
        )

    if provider == "ollama":
        try:
            subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                check=True,
            )

            checks.append(
                DoctorCheck(
                    "LLM",
                    "Ollama",
                    "pass",
                    "Ollama available",
                )
            )

        except Exception:
            checks.append(
                DoctorCheck(
                    "LLM",
                    "Ollama",
                    "fail",
                    "Ollama unavailable",
                    "Install Ollama",
                )
            )

    elif provider == "openai":
        if os.getenv("OPENAI_API_KEY"):
            checks.append(
                DoctorCheck(
                    "LLM",
                    "OPENAI_API_KEY",
                    "pass",
                    "API key configured",
                )
            )
        else:
            checks.append(
                DoctorCheck(
                    "LLM",
                    "OPENAI_API_KEY",
                    "fail",
                    "Missing API key",
                    "Set OPENAI_API_KEY",
                )
            )

    return checks