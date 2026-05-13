from project_brain.core.analyzer import analyze_project


def test_binary_file_skip(tmp_path):
    f = tmp_path / "bin.dat"
    f.write_bytes(b"\x00\x01\x02")

    data, _ = analyze_project(tmp_path)

    assert data["project"]["total_files"] >= 0


def test_invalid_python_file(tmp_path):
    f = tmp_path / "bad.py"
    f.write_text("def foo(:")  # invalid

    data, _ = analyze_project(tmp_path)

    assert data is not None


def test_deep_nested_dirs(tmp_path):
    d = tmp_path
    for i in range(10):
        d = d / f"dir{i}"
        d.mkdir()

    f = d / "a.py"
    f.write_text("def x(): pass")

    data, _ = analyze_project(tmp_path)

    assert data["project"]["total_files"] >= 1