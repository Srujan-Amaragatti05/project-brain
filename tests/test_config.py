from project_brain.core.config_loader import validate_config


def test_invalid_config_fallback():
    bad_config = {
        "llm": {
            "provider": "invalid-provider",
            "timeout_sec": -10
        },
        "output": {
            "format": "invalid"
        }
    }

    safe = validate_config(bad_config)

    # Should fallback to defaults
    assert safe["llm"]["provider"] == "none"
    assert safe["llm"]["timeout_sec"] > 0
    assert safe["output"]["format"] == "text"