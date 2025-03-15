import os
import sys
import pytest

# Add the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Try to import from app package
from app.core.config import settings

def test_settings():
    """Test that settings can be imported and accessed."""
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PROJECT_NAME == "Task Management API"

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 