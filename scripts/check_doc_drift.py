from __future__ import annotations

from pathlib import Path

from generate_cli_docs import generate_markdown, generate_slug
from lib.cli_introspector import generate_command_graph

DOCS_DIR = Path("docs-generated/commands")

# Must match the separator written by enhance_docs_llm.append_ai_section
_USAGE_GUIDE_MARKER = "\n\n---\n\n## Usage Guide\n"


def _strip_usage_guide(text: str) -> str:
    """Remove the LLM-appended Usage Guide section (and its preceding separator)."""
    if _USAGE_GUIDE_MARKER in text:
        return text.split(_USAGE_GUIDE_MARKER, 1)[0].rstrip()
    # Fallback: legacy marker without the leading separator
    if "\n## Usage Guide\n" in text:
        return text.split("\n## Usage Guide\n", 1)[0].rstrip()
    return text.rstrip()


def main() -> None:
    commands = generate_command_graph()
    drift_found = False

    for command in commands:
        category = command["metadata"]["category"]
        slug = generate_slug(command["command"])
        doc_path = DOCS_DIR / category / f"{slug}.md"

        if not doc_path.exists():
            print(f"[ERROR] Missing doc: {doc_path}")
            drift_found = True
            continue

        # Normalise line endings before any comparison (Windows CRLF safety)
        raw = doc_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        current_content = _strip_usage_guide(raw)
        expected_content = generate_markdown(command).rstrip()

        if current_content != expected_content:
            print(f"[ERROR] Drift detected: {doc_path}")
            # Helpful debug output — show first diverging line
            for i, (c, e) in enumerate(
                zip(current_content.splitlines(), expected_content.splitlines()), 1
            ):
                if c != e:
                    print(f"  Line {i}: got    {c!r}")
                    print(f"  Line {i}: expect {e!r}")
                    break
            drift_found = True

    if drift_found:
        print("\nDocumentation drift detected.")
        raise SystemExit(1)

    print("Documentation is up-to-date.")


if __name__ == "__main__":
    main()