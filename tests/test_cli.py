from typer.testing import CliRunner
from project_brain.cli import app

runner = CliRunner()


def test_project_init(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["project", "init"])

    assert result.exit_code == 0
    assert (tmp_path / ".brain").exists()


def test_project_analyze(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # init first
    runner.invoke(app, ["project", "init"])

    # create file
    f = tmp_path / "test.py"
    f.write_text("def x(): pass")

    result = runner.invoke(app, ["project", "analyze", "."])

    assert result.exit_code == 0
    assert (tmp_path / ".brain" / "data.json").exists()


def test_diff_show_not_git(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["diff", "show"])

    assert result.exit_code != 0
    assert "not a git repository" in result.output.lower()