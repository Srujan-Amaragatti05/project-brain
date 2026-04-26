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
            errors="ignore",
            timeout=60
        )

        if proc.returncode != 0:
            print("❌ Ollama error:", proc.stderr)
            return ""

        return proc.stdout.strip()

    except Exception as e:
        print("❌ Ollama exception:", str(e))
        return ""


def call_openai(model: str, prompt: str, api_key: str) -> str:
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
            print("❌ OpenAI error:", response.text)
            return ""

        data = response.json()

        return data.get("output", [{}])[0].get("content", [{}])[0].get("text", "")

    except Exception as e:
        print("❌ OpenAI exception:", str(e))
        return ""

def test_openai(model: str, prompt: str, api_key: str) -> tuple:
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

        models_res = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        # Handle API failure
        if response.status_code != 200:
            return f"❌ OpenAI Error: {response.json().get('error', {}).get('message')}, Status Code: {response.status_code}", []

        output = response.json().get("output", [{}])[0].get("content", [{}])[0].get("text", "")

        model_list = models_res.json().get("data", []) if models_res.status_code == 200 else []

        return output, model_list

    except Exception as e:
        return f"❌ Exception: {str(e)}", []
    
def call_huggingface(model: str, prompt: str, api_key: str):
    url = f"https://api-inference.huggingface.co/v1/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        status_code = response.status_code

        # Try parsing JSON safely
        try:
            data = response.json()
        except Exception:
            return {
                "status_code": status_code,
                "error": response.text,
                "models": [],
                "output": ""
            }

        # Handle errors
        if status_code != 200:
            return {
                "status_code": status_code,
                "error": data,
                "models": [],
                "output": ""
            }

        # Extract text
        if isinstance(data, list):
            output = data[0].get("generated_text", "")
        else:
            output = str(data)

        # OPTIONAL: fetch available models
        models_res = requests.get(
            "https://huggingface.co/api/models",
            timeout=20
        )

        models = []
        if models_res.status_code == 200:
            models = [m.get("id") for m in models_res.json()[:10]]

        return {
            "status_code": status_code,
            "output": output,
            "models": models,
            "error": None
        }

    except Exception as e:
        return {
            "status_code": 500,
            "output": "",
            "models": [],
            "error": str(e)
        }

def call_gemini(model: str, prompt: str, api_key: str):
    
    if not api_key:
        return "❌ Missing GEMINI_API_KEY"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=60)

        if res.status_code != 200:
            return f"❌ Gemini Error: {res.text}"

        data = res.json()

        # Extract text safely
        candidates = data.get("candidates", [])
        if not candidates:
            return "❌ No response from Gemini"

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)

        return text.strip() or "❌ Empty response"

    except Exception as e:
        return f"❌ Gemini Exception: {str(e)}"
    

def test_gemini(model: str, prompt: str, api_key: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    url2 = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    resp = requests.get(url2)

    # print(resp.text)
    data = resp.json()

    # for model in data.get('models', []):
    #     name = model.get('name')
    #     display_name = model.get('displayName')
    #     print(name, display_name)
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        res = requests.post(url, json=payload, timeout=60)

        if res.status_code != 200:
            return f"❌ Gemini Error: {res.text}, Status Code: {res.status_code}, message: {res.json().get('error', {}).get('message', '')}"

        data = res.json()

        # Extract text safely
        candidates = data.get("candidates", [])
        if not candidates:
            return "❌ No response from Gemini"

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)

        return text.strip() or "❌ Empty response"

    except Exception as e:
        return f"❌ Gemini Exception: {str(e)}"

def generate_explanation(provider: str, model: str, prompt: str, api_key: str = "") -> str:
    if provider == "ollama":
        return call_ollama(model, prompt)

    if provider == "openai":
        return call_openai(model, prompt, api_key)
     
    if provider == "gemini":
        return call_gemini(model, prompt, api_key)

    return ""