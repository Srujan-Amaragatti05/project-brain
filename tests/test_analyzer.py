from pathlib import Path
from project_brain.core.analyzer import analyze_project


def test_analyze_small_project(tmp_path: Path):
    # Create sample python file
    file = tmp_path / "sample.py"
    file.write_text(
        """
def foo():
    pass

def bar(x):
    return x
"""
    )

    data, files = analyze_project(tmp_path)

    # Verify file count
    assert data["project"]["total_files"] == 1

    # Verify function extraction
    fn_names = [f["name"] for f in data["functions"]]
    assert "foo" in fn_names
    assert "bar" in fn_names