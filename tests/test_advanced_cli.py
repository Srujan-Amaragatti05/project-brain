from typer.testing import CliRunner
from project_brain.cli import app

runner = CliRunner()


def test_analyze_invalid_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["project", "analyze", "missing_dir"])

    assert result.exit_code != 0 or "Error" in result.output


def test_diff_without_git(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["diff", "show"])

    assert result.exit_code != 0