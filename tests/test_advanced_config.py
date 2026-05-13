from project_brain.core.config_loader import load_config


def test_invalid_config_types(tmp_path):
    cfg = tmp_path / "brain.yaml"

    cfg.write_text("""
llm:
  timeout_sec: "invalid"
output:
  format: 123
""")

    config = load_config(tmp_path)

    assert isinstance(config, dict)