from pathlib import Path
from typer.testing import CliRunner
from project_brain.cli import app

runner = CliRunner()


def test_export_full_code(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["project", "init"])

    f = tmp_path / "a.py"
    f.write_text("def foo(): pass")

    result = runner.invoke(app, ["export", "full-code"])

    assert result.exit_code == 0

    export_file = tmp_path / ".brain" / "exports" / "full_code.txt"
    assert export_file.exists()

    content = export_file.read_text()
    assert "=== FILE:" in content


def test_export_file_duplicate(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["project", "init"])

    f = tmp_path / "a.py"
    f.write_text("print('x')")

    runner.invoke(app, ["export", "file", "a.py"])
    result = runner.invoke(app, ["export", "file", "a.py"])

    assert result.exit_code == 0