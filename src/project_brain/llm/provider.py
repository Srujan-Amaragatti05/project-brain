import os
import subprocess
import requests


def call_ollama(model: str, prompt: str) -> str:
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore"
        )
        return proc.stdout.strip()
    except Exception:
        return ""


def call_openai(model: str, prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            },
            timeout=30
        )

        if response.status_code != 200:
            return ""

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception:
        return ""


def generate_explanation(provider: str, model: str, prompt: str) -> str:
    if provider == "ollama":
        return call_ollama(model, prompt)

    if provider == "openai":
        return call_openai(model, prompt)

    return ""