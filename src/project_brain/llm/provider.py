import subprocess

import requests


def call_ollama(model, prompt, include_models=False, timeout=60):
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout = int(timeout) if timeout else 60
        )

        if proc.returncode != 0:
            return _response(error=proc.stderr, status=500)

        models = []
        if include_models:
            m = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if m.returncode == 0:
                models = m.stdout.splitlines()

        return _response(proc.stdout.strip(), models, 200)

    except subprocess.TimeoutExpired:
        return _response(error="Ollama timeout", status=408)

    except Exception as e:
        return _response(error=str(e), status=500)


def call_openai(model, prompt, api_key, include_models=False, timeout=60):
    if not api_key:
        return _response(error="Missing API key", status=401)

    try:
        res = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"model": model, "input": prompt},
            timeout = int(timeout) if timeout else 60
        )

        if res.status_code != 200:
            try:
                err = res.json()
            except Exception:
                err = res.text
            return _response(
                error=str(err),
                status=res.status_code
            )

        data = res.json()
        output = extract_openai_output(data)
        if not output:
            return _response(
                error="Empty response from OpenAI",
                status=502
            )

        models = []
        if include_models:
            m = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if m.status_code == 200:
                models = [x.get("id") for x in m.json().get("data", [])]

        return _response(output, models, res.status_code)

    except requests.Timeout:
        return _response(error="Request timeout", status=408)

    except requests.ConnectionError:
        return _response(error="Connection failed", status=503)

    except Exception as e:
        return _response(error=str(e), status=500)

    
def call_huggingface(model, prompt, api_key, include_models=False, timeout=60):
    url = f"https://api-inference.huggingface.co/v1/models/{model}"

    try:
        res = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"inputs": prompt},
            timeout = int(timeout) if timeout else 60
        )

        if res.status_code != 200:
            return _response(error=res.text, status=res.status_code)

        data = res.json()
        output = data[0].get("generated_text", "") if isinstance(data, list) else str(data)

        models = []
        if include_models:
            m = requests.get("https://huggingface.co/api/models", timeout=timeout)
            if m.status_code == 200:
                models = [x.get("id") for x in m.json()[:10]]

        return _response(output, models, res.status_code)

    except requests.Timeout:
        return _response(error="Request timeout", status=408)

    except requests.ConnectionError:
        return _response(error="Connection failed", status=503)

    except Exception as e:
        return _response(error=str(e), status=500)

def call_gemini(model, prompt, api_key, include_models=False, timeout=60):
    if not api_key:
        return _response(error="Missing API key", status=401)

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        res = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout = int(timeout) if timeout else 60
        )

        if res.status_code != 200:
            return _response(error=res.text, status=res.status_code)

        data = res.json()
        parts = data.get("candidates", [])[0].get("content", {}).get("parts", [])
        output = "".join(p.get("text", "") for p in parts)

        models = []
        if include_models:
            m = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            )
            if m.status_code == 200:
                models = [x.get("name") for x in m.json().get("models", [])]

        return _response(output.strip(), models, res.status_code)

    except requests.Timeout:
        return _response(error="Request timeout", status=408)

    except requests.ConnectionError:
        return _response(error="Connection failed", status=503)

    except Exception as e:
        return _response(error=str(e), status=500)
    

def call_llm(provider, model, prompt, api_key="", include_models=False, timeout=60):
    if not model and provider != "none":
        return _response(error="Model not specified", status=400)

    if provider == "openai":
        return call_openai(model, prompt, api_key, include_models, timeout)

    if provider == "huggingface":   
        return call_huggingface(model, prompt, api_key, include_models, timeout)

    if provider == "gemini":
        return call_gemini(model, prompt, api_key, include_models, timeout)

    if provider == "ollama":
        return call_ollama(model, prompt, include_models, timeout)

    return _response(error="Unsupported provider", status=400)

def _response(output="", models=None, status=200, error=None):
    return {
        "output": output or "",
        "models": models or [],
        "status_code": status,
        "error": error
    }

def extract_openai_output(data):
    try:
        # ✅ Case 1: direct shortcut (new API)
        if "output_text" in data:
            return data["output_text"]
        # ✅ Case 2: structured output
        for item in data.get("output", []):
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    return c.get("text", "")
                if "text" in c:
                    return c["text"]
    except Exception:
        pass
    return ""
