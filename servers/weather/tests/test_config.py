import pytest

from weather_mcp.config import Settings

def test_settings_from_environment(monkeypatch):
    # Set the environment variable for testing
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test_api_key")

    settings = Settings.from_environment()

    assert settings.openweather_api_key == "test_api_key"

def test_settings_from_environment_missing_key(monkeypatch):
    # Ensure the environment variable is not set
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(RuntimeError,
                        match="OPENWEATHER_API_KEY environment variable is not set") as exc_info:
        Settings.from_environment()

    assert str(exc_info.value) == "OPENWEATHER_API_KEY environment variable is not set."