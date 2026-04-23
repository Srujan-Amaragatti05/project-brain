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
        if proc.returncode != 0:
            print("❌ Ollama error:", proc.stderr)
            return ""
        return proc.stdout.strip()
    except Exception:
        print("❌ Error calling Ollama")
        return ""


def call_openai(model: str, prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""

    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "input": prompt
            },
            timeout=30
        )

        if response.status_code != 200:
            return ""

        data = response.json()

        return data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")

    except Exception:
        return ""


def generate_explanation(provider: str, model: str, prompt: str) -> str:
    if provider == "ollama":
        return call_ollama(model, prompt)

    if provider == "openai":
        return call_openai(model, prompt)

    return ""