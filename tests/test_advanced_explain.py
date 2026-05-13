from typer.testing import CliRunner
from project_brain.cli import app

runner = CliRunner()


def test_explain_file_no_llm(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["project", "init"])

    f = tmp_path / "a.py"
    f.write_text("def foo(): pass")

    result = runner.invoke(app, ["diff", "explain", "a.py"])

    assert result.exit_code == 0


def test_explain_function_no_llm(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["project", "init"])

    f = tmp_path / "a.py"
    f.write_text("def foo(): pass")

    result = runner.invoke(app, ["diff", "explain", "a.py:foo"])

    assert result.exit_code == 0