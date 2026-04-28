import typer
from pathlib import Path
import json
import sys
import importlib.metadata
import webbrowser
from datetime import datetime

from project_brain.core.analyzer import analyze_project
from project_brain.core.summarizer import load_data, format_summary
from project_brain.core.differ import compute_diff, is_git_repo
from project_brain.core.explainer import explain_diff
from project_brain.llm.provider import call_llm
from project_brain.core.doctor import run_doctor
from project_brain.core.exporter import (
    add_code_file,
    add_code_dir,
    export_full_code,
    export_code_changes,
)
from project_brain.core.explainer_file import explain_file, explain_function
from project_brain.core.results import generate_html
from project_brain.core.config_loader import dump_config, load_config, DEFAULT_CONFIG


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
        brain_yaml, dump_config(DEFAULT_CONFIG)
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
def analyze(path: str = typer.Argument(".", help="Path to analyze")):
    """
    Analyze the project
    """
    root = Path(path)

    typer.echo(f"🔍 Analyzing: {root}")

    config = load_config(root)

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

    config = load_config(root)
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


@diff_app.callback(invoke_without_command=True)
def diff(
    ctx: typer.Context,
    from_ref: str = typer.Argument(None),
    to_ref: str = typer.Argument(None),
):
    """
    Show git-based diff with function-level insights
    """
    # If subcommand used → skip
    if ctx.invoked_subcommand:
        return

    # Defaults
    if not from_ref and not to_ref:
        from_ref, to_ref = "HEAD~1", "HEAD"

    elif from_ref and not to_ref:
        to_ref = "HEAD"

    root = Path.cwd()

    if not is_git_repo(root):
        typer.echo("❌ Not a git repository")
        raise typer.Exit(code=1)

    config = load_config(root)
    mode = config.get("diff", {}).get("mode", "function")

    def validate_ref(ref: str):
        import subprocess

        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", ref],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
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


@diff_app.command()
def review(
    from_ref: str = typer.Argument(None),
    to_ref: str = typer.Argument(None),
):
    """
    Explain code changes using LLM
    """
    if not from_ref and not to_ref:
        from_ref, to_ref = "HEAD~1", "HEAD"

    elif from_ref and not to_ref:
        to_ref = "HEAD"

    root = Path.cwd()

    if not is_git_repo(root):
        typer.echo("❌ Not a git repository")
        raise typer.Exit(code=1)
    results = explain_diff(from_ref, to_ref, root)
    # print(results, "from explain_diff_cmd in cli.py")

    if not results:
        typer.echo("❌ Failed to compute explain-diff")
        raise typer.Exit(code=1)

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

    webbrowser.open(str(html_path))


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
def test():
    root = Path.cwd()
    config = load_config(root)

    llm = config.get("llm", {})
    provider = llm.get("provider", "none")
    timeout = llm.get("timeout_sec", 60)
    timeout = int(timeout) if timeout else 60

    if provider == "none":
        typer.echo("LLM disabled")
        return

    result = call_llm(
        provider,
        llm.get("model"),
        "What is 2 + 2?",
        llm.get("api_key", ""),
        include_models=True,
        timeout=timeout
    )

    if result["error"]:
        typer.echo(f"❌ Error: {result['error']}")
        return

    typer.echo(f"✅ Output: {result['output']}")
    typer.echo(f"📦 Models: {result['models'][:5]}")


def main():
    app()


if __name__ == "__main__":
    main()
