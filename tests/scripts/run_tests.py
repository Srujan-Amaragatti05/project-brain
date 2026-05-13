import json
import subprocess
from datetime import datetime
from pathlib import Path
import re


REPORT_DIR = Path("tests") / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def run_pytest():
    """Run pytest and capture structured output"""
    result = subprocess.run(
        ["pytest", "-q", "--tb=short"],
        capture_output=True,
        text=True
    )
    return result


def parse_failures(output: str):
    """
    Extract failure blocks
    """
    failures = []

    current = []
    capture = False

    for line in output.splitlines():
        if "FAILURES" in line:
            capture = True
            continue

        if capture:
            if line.startswith("==="):
                continue

            # New failure block
            if line.startswith("___"):
                if current:
                    failures.append("\n".join(current))
                    current = []

            current.append(line)

    if current:
        failures.append("\n".join(current))

    return failures

def extract_summary(stdout):
    passed = 0
    failed = 0

    m = re.search(r"(\d+)\s+passed", stdout)
    if m:
        passed = int(m.group(1))

    m = re.search(r"(\d+)\s+failed", stdout)
    if m:
        failed = int(m.group(1))

    return passed, failed

def build_report(result, failures):
    passed, failed = extract_summary(result.stdout)
    return {
        "timestamp": datetime.now().isoformat(),
        "exit_code": result.returncode,
        "summary": {
            "passed": passed,
            "failed": failed,
        },
        "failures": failures,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def save_reports(report):
    json_path = REPORT_DIR / "test_report.json"
    txt_path = REPORT_DIR / "test_report.txt"

    # JSON
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # TXT (for LLM)
    lines = []
    lines.append("=== PROJECT TEST REPORT ===\n")
    lines.append(f"Time: {report['timestamp']}")
    lines.append(f"Exit Code: {report['exit_code']}\n")

    lines.append("=== SUMMARY ===")
    lines.append(f"Passed: {report['summary']['passed']}")
    lines.append(f"Failed: {report['summary']['failed']}\n")

    lines.append("=== FAILURES ===\n")

    if not report["failures"]:
        lines.append("No failures 🎉")
    else:
        for i, f in enumerate(report["failures"], 1):
            lines.append(f"\n--- FAILURE {i} ---\n")
            lines.append(f)

    txt_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, txt_path



def main():
    print("🔍 Running tests...")

    result = run_pytest()

    failures = parse_failures(result.stdout + "\n" + result.stderr)

    report = build_report(result, failures)

    json_path, txt_path = save_reports(report)

    print("\n✅ Test run complete")
    print(f"📄 JSON report: {json_path}")
    print(f"📄 TXT report: {txt_path}")

    if report["exit_code"] != 0:
        print("\n⚠️ Failures detected. Send report to debugger.")
    else:
        print("\n🎉 All tests passed")


if __name__ == "__main__":
    main()