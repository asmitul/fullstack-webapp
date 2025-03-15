import os
import sys

# Add the current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    from app.core.config import settings
    print("Successfully imported settings!")
    print(f"API_V1_STR: {settings.API_V1_STR}")
except ImportError as e:
    print(f"Failed to import settings: {e}")

try:
    from app.db.mongodb import db
    print("Successfully imported db!")
except ImportError as e:
    print(f"Failed to import db: {e}")

try:
    from main import app
    print("Successfully imported app!")
except ImportError as e:
    print(f"Failed to import app: {e}") 