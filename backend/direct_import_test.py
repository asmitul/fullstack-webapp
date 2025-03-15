import os
import sys
import importlib.util
import pathlib
import pytest

# Get the absolute path to the config.py file
base_dir = pathlib.Path(__file__).parent
config_path = base_dir / "app" / "core" / "config.py"

print(f"Looking for config at: {config_path}")
print(f"Config file exists: {config_path.exists()}")

# Import the module
spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
settings = config.Settings()

def test_settings():
    """Test that settings can be imported and accessed."""
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PROJECT_NAME == "Task Management API"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 