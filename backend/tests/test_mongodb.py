import importlib.util
import pathlib
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

# Get the absolute path to the config.py file
base_dir = pathlib.Path(__file__).parent.parent
config_path = base_dir / "app" / "core" / "config.py"

# Import the module
spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
settings = config.Settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db: Database = None

db = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client.get_database()
    print(f"Connected to MongoDB at {settings.MONGODB_URI}")

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        print("Closed connection to MongoDB") 