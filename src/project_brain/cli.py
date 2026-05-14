import importlib.metadata
import json
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
import os

import typer
import typer.rich_utils
from rich.console import Console
from rich.panel import Panel

from project_brain.core.analyzer import analyze_project
from project_brain.core.config_loader import (DEFAULT_CONFIG, dump_config,
                                              load_config)
from project_brain.core.differ import compute_diff, is_git_repo, run_git_command
from project_brain.core.doctor import run_doctor
from project_brain.core.explainer import explain_diff
from project_brain.core.explainer_file import explain_file, explain_function
from project_brain.core.exporter import (add_code_dir, add_code_file,
                                         export_code_changes, export_full_code)
from project_brain.core.results import generate_html
from project_brain.core.summarizer import format_summary, load_data
from project_brain.llm.provider import call_llm

from project_brain.cli_help import (
    ROOT_HELP,
    PROJECT_HELP,
    DIFF_HELP,
    EXPORT_HELP,
    LLM_HELP,
)

from project_brain.cli_ui import (
    console,
    section,
    success,
    error,
    info,
    key_value_table,
    doctor_panel,
)

typer.rich_utils.STYLE_HELPTEXT = "bold"
typer.rich_utils.STYLE_OPTIONS_PANEL_BORDER = "cyan"
typer.rich_utils.STYLE_COMMANDS_PANEL_BORDER = "cyan"

def configure_output_encoding():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]


configure_output_encoding()

app = typer.Typer(
    help=ROOT_HELP,
    rich_markup_mode="rich",
    no_args_is_help=True,
)

project_app = typer.Typer(
    help=PROJECT_HELP,
    no_args_is_help=True,
)

diff_app = typer.Typer(
    help=DIFF_HELP,
    no_args_is_help=True,
)

export_app = typer.Typer(
    help=EXPORT_HELP,
    no_args_is_help=True,
)

llm_app = typer.Typer(
    help=LLM_HELP,
    no_args_is_help=True,
)

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
    """ project-brain CLI entrypoint """


def require_git_repo(root: Path):
    if not is_git_repo(root):
        error(
            "Current directory is not a git repository",
            suggestion="""
Initialize git:

git init

Then create first commit:

git add .
git commit -m "initial commit"
""",
        )
        raise typer.Exit(code=1)


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
        success(
            "project-brain initialized successfully",
            next_step="brain project analyze .",
        )
    else:
        info("Project already initialized")


@project_app.command()
def analyze(
    path: str = typer.Argument(
        ".",
        help="Repository path to analyze",
    )
):
    """
    Analyze repository structure using AST parsing.

    Extracts:
    - files
    - functions
    - classes
    - metadata

    Stores results inside:
    .brain/data.json

    Example:
        brain project analyze .
    """
    root = Path(path)

    section("Project Analysis")
    info(f"Analyzing: {root}")

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
    success(
        "Analysis complete",
        next_step="brain project summary",
    )


@project_app.command()
def summary():
    """Summarize the analyzed data"""
    root = Path.cwd()
    data = load_data(root)

    if not data:
        error(
            "Project has not been analyzed yet",
            suggestion="""
        Run:

        brain project analyze .
        """,
        )
        raise typer.Exit(code=1)

    config = load_config(root)
    fmt = config.get("output", {}).get("format", "text")

    if fmt == "json":

        typer.echo(json.dumps(data, indent=2))
        typer.echo(
            "✅ Summary complete (JSON format), its already saved in .brain/data.json"
        )
        return

    output = format_summary(root, data)
    typer.echo(output)


@diff_app.callback(invoke_without_command=True)
def diff(ctx: typer.Context):
    """
    Diff command group
    """
    if ctx.invoked_subcommand is None:
        typer.echo("❌ Missing subcommand")
        typer.echo("👉 Use: brain diff show or brain diff review")
        raise typer.Exit(code=1)
    

@diff_app.command()
def show(
    from_ref: str = typer.Argument(None),
    to_ref: str = typer.Argument(None),
):

    # Defaults
    if not from_ref and not to_ref:
        from_ref, to_ref = "HEAD~1", "HEAD"

    elif from_ref and not to_ref:
        to_ref = "HEAD"

    root = Path.cwd()

    require_git_repo(root)

    config = load_config(root)
    mode = config.get("diff", {}).get("mode", "function")

    def validate_ref(ref: str):
        return run_git_command(["rev-parse", "--verify", ref], root) is not None

    if not validate_ref(from_ref) or not validate_ref(to_ref):
        error(
            f"Invalid git reference: {from_ref} {to_ref}",
            suggestion="""
        brain diff show HEAD~1 HEAD
        brain diff show main dev

        Check refs using:
        git log --oneline
        """,
        )
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

    section("Modified Files")

    if modified:
        for f in modified:
            console.print(f"[yellow]•[/yellow] {f}")
    else:
        info("No modified files")

    section("Added Files")
    if added:
        for f in added:
            console.print(f"[green]•[/green] {f}")
    else:
        info("No added files")

    section("Deleted Files")
    if deleted:
        for f in deleted:
            console.print(f"[red]•[/red] {f}")
    else:
        info("No deleted files")

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

    require_git_repo(root)
    def validate_ref(ref: str):
        return run_git_command(["rev-parse", "--verify", ref], root) is not None
    
    if not validate_ref(from_ref) or not validate_ref(to_ref):
        error(
            f"Invalid git reference: {from_ref} {to_ref}",
            suggestion="""
        brain diff show HEAD~1 HEAD
        brain diff show main dev

        Check refs using:
        git log --oneline
        """,
        )
        typer.echo(f"   From: {from_ref}")
        typer.echo(f"   To: {to_ref}")
        raise typer.Exit(code=1)
    results = explain_diff(from_ref, to_ref, root)


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
    Repository diagnostics and environment health checks.
    """

    root = Path.cwd()

    checks, final_status = run_doctor(root)

    console.print(
        Panel.fit(
            "[bold cyan]🩺 Project Brain Diagnostics[/bold cyan]",
            border_style="cyan",
        )
    )

    grouped = {}

    for check in checks:
        grouped.setdefault(check.category, []).append(check)

    for category, items in grouped.items():
        rows = []

        for item in items:

            if item.status == "pass":
                status = "[green]PASS[/green]"
            elif item.status == "warn":
                status = "[yellow]WARN[/yellow]"
            elif item.status == "fail":
                status = "[red]FAIL[/red]"
            else:
                status = "[cyan]INFO[/cyan]"

            detail = item.message

            if item.fix:
                detail += f"\n[dim]{item.fix}[/dim]"

            rows.append(
                (
                    item.name,
                    status,
                    detail,
                )
            )

        doctor_panel(category, rows)

    if final_status == "READY":
        success(
            "Repository is fully operational",
            next_step="brain diff review",
        )

    elif final_status == "PARTIAL":
        info("Repository partially configured")

    else:
        error(
            "Repository is not ready",
            suggestion="""
brain project init
brain project analyze .
""",
        )

@export_app.command()
def full_code():
    """
    Export entire codebase into structured file
    """
    root = Path.cwd()

    count, output_path, files_path = export_full_code(root)

    success(
        f"Exported {count} files",
        next_step="brain export code_changes HEAD~1 HEAD",
    )

    info(f"Output: {output_path}")
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
    model = llm.get("model", "")
    timeout = llm.get("timeout_sec", 60)

    if provider == "none":
        info("LLM disabled (provider=none)")
        return

    result = call_llm(
        provider,
        model,
        "What is 2 + 2?",
        api_key="",
        include_models=True,
        timeout=timeout
    )
    print(f"LLM Call - Provider: {provider}, Model: {model}, Timeout: {timeout}s")


    if result["error"]:
        error(
        f"LLM test failed: {result['error']}",
        suggestion="""
    Check:
    - provider name
    - model name
    - API keys
    - internet connectivity
    """,
    )
        return

    typer.echo(f"✅ Output: {result['output']}")
    typer.echo(f"📦 Models: {result['models'][:5]}")


def main():
    app()


if __name__ == "__main__":
    main()
