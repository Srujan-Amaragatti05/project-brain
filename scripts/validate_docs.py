from __future__ import annotations

import subprocess
import sys


VALIDATORS = [
    "scripts/check_missing_gifs.py",
    "scripts/check_doc_drift.py",
]


def run_validator(script_path: str):

    print(f"\nRunning: {script_path}")

    result = subprocess.run(
        [sys.executable, script_path],
    )

    if result.returncode != 0:

        print(f"\nFAILED: {script_path}")

        raise SystemExit(result.returncode)

    print(f"PASSED: {script_path}")


def main():

    for validator in VALIDATORS:
        run_validator(validator)

    print("\nAll documentation validations passed.")


if __name__ == "__main__":
    main()