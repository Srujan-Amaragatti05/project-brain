from __future__ import annotations

import os
import time
from pathlib import Path
import re

import yaml

from project_brain.llm.provider import (
    call_openai,
    call_gemini,
    call_huggingface,
    call_ollama,
)


CONFIG_FILE = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    /"lib"
    / "docs.yaml"
)


def load_docs_config():

    return yaml.safe_load(
        CONFIG_FILE.read_text(
            encoding="utf-8"
        )
    )


def normalize_output(
    text: str,
) -> str:

    if not text:
        return ""

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"<thinking>.*?</thinking>",
        "",
        text,
        flags=re.DOTALL,
    )

    start_markers = [
        "# ProjectBrain Documentation",
        "## Who Is This Persona",
        "## Goal",
        "### When would I use this?",
    ]

    positions = []

    for marker in start_markers:

        pos = text.find(marker)

        if pos >= 0:
            positions.append(pos)

    if positions:

        text = text[min(positions):]

    return text.strip()


def call_provider(
    provider: str,
    model: str,
    prompt: str,
    timeout: int,
):

    if provider == "openai":

        result = call_openai(
            model=model,
            prompt=prompt,
            api_key=os.getenv(
                "OPENAI_API_KEY",
                "",
            ),
            include_models=False,
            timeout=timeout,
        )

    elif provider == "gemini":

        result = call_gemini(
            model=model,
            prompt=prompt,
            api_key=os.getenv(
                "GEMINI_API_KEY",
                "",
            ),
            include_models=False,
            timeout=timeout,
        )

    elif provider == "huggingface":

        result = call_huggingface(
            model=model,
            prompt=prompt,
            api_key=os.getenv(
                "HUGGINGFACE_API_KEY",
                "",
            ),
            include_models=False,
            timeout=timeout,
        )

    elif provider == "ollama":

        result = call_ollama(
            model=model,
            prompt=prompt,
            include_models=False,
            timeout=timeout,
        )

    else:

        raise RuntimeError(
            f"Unsupported provider: {provider}"
        )

    if result["error"]:

        raise RuntimeError(
            result["error"]
        )

    return normalize_output(
        result["output"]
    )


def generate_docs_content(
    prompt: str,
) -> str:

    config = load_docs_config()

    timeout = config.get(
        "timeout",
        120,
    )

    retries = config.get(
        "max_retries",
        3,
    )

    providers = [
        {
            "provider":
                config["provider"],
            "model":
                config["model"],
        }
    ]

    providers.extend(
        config.get(
            "fallbacks",
            [],
        )
    )

    last_error = None

    for item in providers:

        provider = item["provider"]
        model = item["model"]

        for attempt in range(retries):

            try:

                print(
                    f"[DOCS LLM] "
                    f"{provider} :: "
                    f"{model}"
                )

                return call_provider(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    timeout=timeout,
                )

            except Exception as exc:

                last_error = exc

                print(
                    f"[FAILED] "
                    f"{provider} :: "
                    f"{model}"
                )

                print(exc)

                time.sleep(2)

    raise RuntimeError(
        f"All documentation providers failed: {last_error}"
    )