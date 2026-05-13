from typer.testing import CliRunner
from project_brain.cli import app

runner = CliRunner()


def test_logging_on_invalid_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["project", "init"])

    runner.invoke(app, ["diff", "explain", "missing.py"])

    log_file = tmp_path / ".brain" / "logs.txt"

    assert log_file.exists()

    content = log_file.read_text()
    assert "ERROR" in content or "WARNING" in content