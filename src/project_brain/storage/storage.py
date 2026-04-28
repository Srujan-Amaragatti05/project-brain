import json
from pathlib import Path


def save_data(data: dict, root: Path):
    brain_dir = root / ".brain"
    brain_dir.mkdir(exist_ok=True)

    data_path = brain_dir / "data.json"

    with data_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)