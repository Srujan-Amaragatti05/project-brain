import typer
from pathlib import Path
import yaml
import json

from project_brain.core.analyzer import analyze_project
from project_brain.storage.storage import save_data
from project_brain.core.summarizer import load_data, format_summary
from project_brain.core.differ import compute_diff, is_git_repo
from project_brain.core.explainer import explain_diff

app = typer.Typer(help="project-brain CLI")

DEFAULT_CONFIG = {
    "llm": {
        "provider": "none",
        "model": ""
    },
    "analysis": {
        "depth": "fast"
    },
    "diff": {
        "mode": "function"
    },
    "output": {
        "format": "text"
    }
}


def create_file(path: Path, content: str):
    if path.exists():
        typer.echo(f"⚠️  Skipped (already exists): {path}")
        return
    path.write_text(content)
    typer.echo(f"✅ Created: {path}")


@app.command()
def init():
    cwd = Path.cwd()

    brain_yaml = cwd / "brain.yaml"
    brain_dir = cwd / ".brain"
    data_json = brain_dir / "data.json"
    index_json = brain_dir / "index.json"
    cache_dir = brain_dir / "cache"

    if not brain_dir.exists():
        brain_dir.mkdir()
        typer.echo(f"✅ Created: {brain_dir}")
    else:
        typer.echo(f"⚠️  Exists: {brain_dir}")

    if not cache_dir.exists():
        cache_dir.mkdir()
        typer.echo(f"✅ Created: {cache_dir}")
    else:
        typer.echo(f"⚠️  Exists: {cache_dir}")

    create_file(brain_yaml, yaml.dump(DEFAULT_CONFIG, sort_keys=False))
    create_file(data_json, json.dumps({}, indent=2))
    create_file(index_json, json.dumps({}, indent=2))

    typer.echo("\n🎉 project-brain initialized successfully!")


@app.command()
def analyze(path: str = "."):
    target_path = Path(path).resolve()

    if not target_path.exists():
        typer.echo("❌ Path does not exist")
        raise typer.Exit(code=1)

    typer.echo(f"🔍 Analyzing: {target_path}")

    data = analyze_project(target_path)
    save_data(data, target_path)

    typer.echo("✅ Analysis complete. Data saved to .brain/data.json")


@app.command()
def summary():
    root = Path.cwd()
    data = load_data(root)

    if not data:
        typer.echo("❌ Run 'project-brain analyze .' first")
        raise typer.Exit(code=1)

    output = format_summary(root, data)
    typer.echo(output)


@app.command()
def diff(from_ref: str, to_ref: str):
    """
    Show git-based diff with function-level insights
    """
    root = Path.cwd()

    if not is_git_repo(root):
        typer.echo("❌ Not a git repository")
        raise typer.Exit(code=1)

    result = compute_diff(from_ref, to_ref, root)

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


@app.command()
def explain_diff_cmd(from_ref: str, to_ref: str):
    """
    Explain code changes using LLM
    """
    root = Path.cwd()

    results = explain_diff(from_ref, to_ref, root)

    if not results:
        typer.echo("❌ Failed to compute explain-diff")
        raise typer.Exit(code=1)

    for item in results:
        typer.echo(f"\nFile: {item['file']}")
        typer.echo(f"Function: {item['function']}")
        typer.echo(f"Change: {item['change']}")
        typer.echo(f"Impact: {item['impact']}")
        typer.echo(f"Risk: {item['risk']}")

def main():
    app()


if __name__ == "__main__":
    main()