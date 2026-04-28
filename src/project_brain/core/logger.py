from datetime import datetime
from pathlib import Path

LOG_FILE = Path(".brain") / "logs.txt"


def _write(level: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{level}] {message}"

    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        # fallback: never crash logging
        print(formatted)


def log_info(message: str):
    _write("INFO", message)


def log_warning(message: str):
    _write("WARNING", message)
    print(f"[WARNING] {message}")  # keep visible


def log_error(message: str):
    _write("ERROR", message)
    print(f"[ERROR] {message}")  # keep visible