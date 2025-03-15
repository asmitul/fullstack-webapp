import os
import sys
import pytest

# Add the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_simple():
    """A simple test that should always pass."""
    assert True

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 