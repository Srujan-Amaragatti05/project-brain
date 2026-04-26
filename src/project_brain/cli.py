import typer
from pathlib import Path
import yaml
import json
import sys
from collections import defaultdict
import importlib.metadata

from project_brain.core.analyzer import analyze_project
from project_brain.core.summarizer import load_data, format_summary
from project_brain.core.differ import compute_diff, is_git_repo
from project_brain.core.explainer import explain_diff
from project_brain.llm.provider import call_huggingface, test_openai, test_gemini
from project_brain.core.doctor import run_doctor
from project_brain.core.exporter import (
    add_code_file,
    add_code_dir,
    export_full_code,
    export_code_changes,
)
from project_brain.core.explainer_file import explain_file, explain_function


def configure_output_encoding():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]


configure_output_encoding()

app = typer.Typer(help="project-brain CLI")
project_app = typer.Typer(help="Project management commands")
diff_app = typer.Typer(help="Diff and change analysis")
export_app = typer.Typer(help="Code export tools")
llm_app = typer.Typer(help="LLM testing tools")

app.add_typer(project_app, name="project")
app.add_typer(diff_app, name="diff")
app.add_typer(export_app, name="export")
app.add_typer(llm_app, name="testllm")


def version_callback(value: bool):
    if value:
        try:
            version = importlib.metadata.version("project-brain")
        except Exception:
            version = "unknown"
        typer.echo(f"project-brain version: {version}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    )
):
    pass


DEFAULT_CONFIG = {
    "version": "1.0",  # Config version (used for future migrations)
    "llm": {
        "provider": "none",  # Options: none | openai | ollama
        "model": "",  # OpenAI: gpt-4.1-mini | Ollama: llama3, phi3, etc.
        "api_key": "",  # Optional: API key for OpenAI (not needed for Ollama)
        "timeout_sec": 60,  # Max time (seconds) to wait for LLM response
    },
    "analysis": {
        "depth": "fast",  # Options: fast | deep (future use)
        "include_tests": False,  # Include test files in analysis
        "ignore": [  # Directories/files to skip during analysis
            ".brain/",
            ".git/",
            "node_modules/",
            "venv/",
            ".venv/",
            "__pycache__/",
            "env/",
            ".env/",
            "*.egg-info/",
        ],
    },
    "diff": {
        "mode": "function",  # Options: function | file
    },
    "export": {
        "full_code": {
            "include_tests": False,  # Include test files in export
            "max_file_size_kb": 200,  # Skip files larger than this size
        },
        "manual_add": {
            "allow_duplicates": True,  # Allow same file to be added multiple times
        },
        "changes": {
            "mode": "function",  # Options: function | file
            "include_context": True,  # Include line numbers and metadata
            "output_path": ".brain/exports/code_changes.txt",  # Output file location
        },
        "ignore": [  # Directories/files to skip during analysis
            ".brain/",
            ".git/",
            "node_modules/",
            "venv/",
            ".venv/",
            "__pycache__/",
            "env/",
            ".env/",
            "*.egg-info/",
        ],
    },
    "explain": {
        "level": "detailed",  # Options: basic | detailed
        "include_risks": True,  # Include risk analysis in explanations
    },
    "output": {
        "format": "text",  # Options: text | json
    },
}


def create_file(path: Path, content: str):
    if path.exists():
        typer.echo(f"⚠️  Skipped (already exists): {path}")
        return False
    path.write_text(content)
    typer.echo(f"✅ Created: {path}")
    return True


@project_app.command()
def init():
    """Initialize project-brain in the current directory"""
    cwd = Path.cwd()

    brain_yaml = cwd / "brain.yaml"
    brain_dir = cwd / ".brain"
    data_json = brain_dir / "data.json"
    index_json = brain_dir / "index.json"
    cache_dir = brain_dir / "cache"

    created_anything = False

    if not brain_dir.exists():
        brain_dir.mkdir()
        created_anything = True
        typer.echo(f"✅ Created: {brain_dir}")
    else:
        typer.echo(f"⚠️  Exists: {brain_dir}")

    if not cache_dir.exists():
        cache_dir.mkdir()
        created_anything = True
        typer.echo(f"✅ Created: {cache_dir}")
    else:
        typer.echo(f"⚠️  Exists: {cache_dir}")

    created_brain_yaml = create_file(
        brain_yaml, yaml.dump(DEFAULT_CONFIG, sort_keys=False)
    )
    created_data_json = create_file(data_json, json.dumps({}, indent=2))
    created_index_json = create_file(index_json, json.dumps({}, indent=2))
    created_anything = (
        created_anything
        or created_brain_yaml
        or created_data_json
        or created_index_json
    )

    if created_anything:
        typer.echo("\n🎉 project-brain initialized successfully!")
    else:
        typer.echo("\nℹ️ Project already initialized.")


@project_app.command()
def analyze(path: str = "."):
    """
    Analyze the project
    """
    root = Path(path).resolve()

    typer.echo(f"🔍 Analyzing: {root}")

    config_path = root / "brain.yaml"
    config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}

    analysis_cfg = config.get("analysis", {})

    ignore = analysis_cfg.get("ignore", [])
    include_tests = analysis_cfg.get("include_tests", False)

    data, files_path = analyze_project(
        root, ignore_patterns=ignore, include_tests=include_tests
    )

    brain_dir = root / ".brain"
    brain_dir.mkdir(exist_ok=True)

    data_path = brain_dir / "data.json"
    data_path.write_text(json.dumps(data, indent=2))

    formatted_paths = "\n\t\t".join(str(p) for p in files_path)
    typer.echo(f"📋 File Paths: {formatted_paths}")
    typer.echo("✅ Analysis complete. Data saved to .brain/data.json")


@project_app.command()
def summary():
    """Summarize the analyzed data"""
    root = Path.cwd()
    data = load_data(root)

    if not data:
        typer.echo("❌ Run 'project-brain analyze .' first")
        raise typer.Exit(code=1)

    config = yaml.safe_load((root / "brain.yaml").read_text())
    fmt = config.get("output", {}).get("format", "text")

    if fmt == "json":
        import json

        typer.echo(json.dumps(data, indent=2))
        typer.echo(
            "✅ Summary complete (JSON format), its already saved in .brain/data.json"
        )
        return

    output = format_summary(root, data)
    typer.echo(output)


@diff_app.command()
def diff(from_ref: str, to_ref: str):
    """
    Show git-based diff with function-level insights
    """
    root = Path.cwd()

    if not is_git_repo(root):
        typer.echo("❌ Not a git repository")
        raise typer.Exit(code=1)

    config = yaml.safe_load((root / "brain.yaml").read_text()) or {}
    mode = config.get("diff", {}).get("mode", "function")

    def validate_ref(ref: str):
        import subprocess

        try:
            subprocess.run(
                ["git", "rev-parse", ref],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except:
            return False

    if not validate_ref(from_ref) or not validate_ref(to_ref):
        typer.echo("❌ Invalid git reference provided")
        raise typer.Exit(code=1)

    try:
        result = compute_diff(from_ref, to_ref, root)
    except Exception as e:
        typer.echo(f"❌ Diff failed: {str(e)}")
        raise typer.Exit(code=1)

    if result is None:
        typer.echo("❌ Failed to compute diff")
        raise typer.Exit(code=1)

    added = result["added"]
    modified = result["modified"]
    deleted = result["deleted"]

    typer.echo(f"Files Changed: {len(added) + len(modified) + len(deleted)}\n")

    typer.echo("Modified:\n")
    for f in modified:
        typer.echo(f"* {f}")
    if not modified:
        typer.echo("* None")

    typer.echo("\nAdded:\n")
    for f in added:
        typer.echo(f"* {f}")
    if not added:
        typer.echo("* None")

    typer.echo("\nDeleted:\n")
    for f in deleted:
        typer.echo(f"* {f}")
    if not deleted:
        typer.echo("* None")

    if mode == "file":
        return

    # Function-level diff
    for fd in result["function_diffs"]:
        typer.echo(f"\nFile: {fd['file']}\n")

        typer.echo("Functions Added:\n")
        for fn in fd["added"]:
            typer.echo(f"* {fn}")
        if not fd["added"]:
            typer.echo("* None")

        typer.echo("\nFunctions Removed:\n")
        for fn in fd["removed"]:
            typer.echo(f"* {fn}")
        if not fd["removed"]:
            typer.echo("* None")

        typer.echo("\nFunctions Modified:\n")
        for fn in fd["modified"]:
            typer.echo(f"* {fn}")
        if not fd["modified"]:
            typer.echo("* None")

        typer.echo("")


@diff_app.command(name="explain")
def explain_diff_cmd(from_ref: str, to_ref: str):
    """
    Explain code changes using LLM
    """
    root = Path.cwd()

    if not is_git_repo(root):
        typer.echo("❌ Not a git repository")
        raise typer.Exit(code=1)
    results = explain_diff(from_ref, to_ref, root)
    # print(results, "from explain_diff_cmd in cli.py")

    if not results:
        typer.echo("❌ Failed to compute explain-diff")
        raise typer.Exit(code=1)

    grouped = defaultdict(list)
    from datetime import datetime

    reports_dir = root / ".brain" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    json_path = reports_dir / f"diff_{timestamp}.json"
    html_path = reports_dir / f"diff_{timestamp}.html"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    html_path.write_text(generate_html(results), encoding="utf-8")
    typer.echo("\n✅ Analysis complete\n")
    typer.echo(f"📄 JSON:  {json_path}")
    typer.echo(f"🌐 HTML:  {html_path}")
    import webbrowser
    webbrowser.open(str(html_path))


    # for item in results:
    #     grouped[item["file"]].append(item)

    # for file, items in grouped.items():
    #     typer.echo(f"\n📄 File: {file}\n")

    #     for item in items:
    #         typer.echo(f"🔧 Function: {item['function']}")
    #         typer.echo(f"🧠 Change: {item['change']}")
    #         typer.echo(f"⚡ Impact: {item['impact']}")
    #         typer.echo(f"⚠️ Risk: {item['risk']}\n")

# import webbrowser
# from pathlib import Path
# import json

# def open_in_browser(results, root: Path):
#     output_file = root / ".brain" / "report.html"

#     html = "<html><body><h2>Project Brain Report</h2><pre>"
#     html += json.dumps(results, indent=2)
#     html += "</pre></body></html>"

#     output_file.write_text(html)
#     webbrowser.open(str(output_file))
def generate_html(results):
    from collections import defaultdict

    grouped = defaultdict(list)
    for item in results:
        grouped[item["file"]].append(item)

    sections = ""

    for file, items in grouped.items():
        rows = ""

        for item in items:
            risk = item["risk"] or "unknown"

            if "high" in risk.lower():
                risk_class = "risk-high"
            elif "medium" in risk.lower():
                risk_class = "risk-medium"
            else:
                risk_class = "risk-low"

            rows += f"""
            <div class="function-card">
                <div class="fn-header">
                    <span class="fn-name">{item['function']}</span>
                    <span class="badge {risk_class}">{risk}</span>
                </div>

                <div class="section">
                    <b>Change</b>
                    <p>{item['change']}</p>
                </div>

                <div class="section">
                    <b>Impact</b>
                    <p>{item['impact']}</p>
                </div>

                <div class="section">
                    <b>Risk</b>
                    <p>{item['risk']}</p>
                </div>
            </div>
            """

        sections += f"""
        <div class="file-block">
            <div class="file-header" onclick="toggle(this)">
                📂 {file}
            </div>
            <div class="file-content">
                {rows}
            </div>
        </div>
        """

    return f"""
<html>
<head>
<meta charset="UTF-8">
<title>Project Brain Report</title>

<style>
body {{
    font-family: Inter, Arial;
    background: #0f172a;
    color: #e2e8f0;
    padding: 20px;
}}

h1 {{
    color: #38bdf8;
    margin-bottom: 20px;
}}

.file-block {{
    margin-bottom: 20px;
    border: 1px solid #334155;
    border-radius: 10px;
    overflow: hidden;
}}

.file-header {{
    background: #1e293b;
    padding: 12px;
    cursor: pointer;
    font-weight: bold;
}}

.file-content {{
    display: none;
    padding: 15px;
}}

.function-card {{
    background: #020617;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
}}

.fn-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}}

.fn-name {{
    font-weight: bold;
    color: #22c55e;
}}

.section {{
    margin-bottom: 8px;
}}

.section p {{
    margin: 4px 0;
    color: #cbd5f5;
}}

.badge {{
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
}}

.risk-high {{
    background: #dc2626;
}}

.risk-medium {{
    background: #f59e0b;
}}

.risk-low {{
    background: #16a34a;
}}
</style>

<script>
function toggle(el) {{
    let content = el.nextElementSibling;
    content.style.display =
        content.style.display === "block" ? "none" : "block";
}}
</script>

</head>

<body>

<h1>🧠 Project Brain - Diff Analysis</h1>

{sections}

</body>
</html>
"""
@project_app.command()
def doctor():
    """
    Validate project setup and environment
    """
    root = Path.cwd()

    results, final_status = run_doctor(root)

    typer.echo("\nProject Brain Doctor Report\n")

    for line in results:
        typer.echo(line)

    typer.echo(f"\nStatus: {final_status}")


@export_app.command()
def full_code():
    """
    Export entire codebase into structured file
    """
    root = Path.cwd()

    count, output_path, files_path = export_full_code(root)

    typer.echo(f"📦 Files exported: {count}")
    typer.echo(f"📄 Output: {output_path}")
    formatted_paths = "\n\t\t".join(files_path)
    typer.echo(f"📋 File Paths: {formatted_paths}")


# add_code_app = typer.Typer()
# app.add_typer(add_code_app, name="add-code")


@export_app.command("file")
def add_code_file_cmd(path: str):
    """
    Manually add a single file to export
    """
    root = Path.cwd()
    target = Path(path)

    count, output_path, msg = add_code_file(root, target)

    if msg:
        typer.echo(msg)

    typer.echo(f"📦 Files added: {count}")
    typer.echo(f"📄 Output: {output_path}")


@export_app.command("dir")
def add_code_dir_cmd(path: str):
    """
    Manually add a directory to export
    """
    root = Path.cwd()
    target = Path(path)

    count, output_path, msg = add_code_dir(root, target)

    if msg:
        typer.echo(msg)

    typer.echo(f"📦 Files added: {count}")
    typer.echo(f"📄 Output: {output_path}")


@export_app.command()
def code_changes(from_ref: str, to_ref: str):
    """
    Export changed code between two git references
    """
    root = Path.cwd()

    count, output_path = export_code_changes(root, from_ref, to_ref)

    typer.echo(f"📦 Files processed: {count}")
    typer.echo(f"📄 Output: {output_path}")


@diff_app.command()
def explain(target: str):
    """
    Explain a file or function
    """
    root = Path.cwd()

    if ":" in target:
        file_path, func_name = target.split(":", 1)
        output = explain_function(root, file_path, func_name)
    else:
        output = explain_file(root, target)

    typer.echo(output)


@llm_app.command()
def openai():
    """
    Test API connectivity and LLM response
    """
    root = Path.cwd()
    config = yaml.safe_load((root / "brain.yaml").read_text()) or {}
    provider = config.get("llm", {}).get("provider", "none")

    if provider == "none":
        typer.echo("LLM Provider: none (no API calls will be made)")
        return

    test_prompt = "What is 2 + 2?"
    try:
        if provider == "openai":
            response, model_data= test_openai(
                config["llm"]["model"],
                test_prompt,
                config["llm"].get("api_key", ""),
            )
            typer.echo(f"✅ LLM Response: {response}")
            typer.echo(f"✅ Model Data: {model_data}")
            # typer.echo(f"✅ Status Code: {status_code}")
        else:
            typer.echo(f"❌ Unsupported LLM provider: {provider}")
            return
    except Exception as e:
        typer.echo(f"❌ LLM API test failed: {str(e)}")

@llm_app.command()
def hugface():
    provider= "huggingface"
    model= "google/flan-t5-large"
    api_key= "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"
    prompt= "What is 2 + 2?"
    result = call_huggingface(model, prompt, api_key)
    typer.echo(f"📡 Status Code: {result['status_code']}")

    if result["error"]:
        typer.echo(f"❌ Error: {result['error']}")
    else:
        typer.echo(f"✅ Output: {result['output']}")

    if result["models"]:
        typer.echo(f"📦 Sample Models: {result['models'][:5]}") 

@llm_app.command()
def gemini():
    provider = "gemini"
    model = "gemini-flash-lite-latest"
    api_key = "AIzaSyBFeEFpWe82e7VLZUKm3susjWf70dRM6r8"
    prompt = "tell me everything about car?"
    result = test_gemini(model, prompt, api_key)
    typer.echo(f"✅ Gemini Response: {result}")

def main():
    app()


if __name__ == "__main__":
    main()
