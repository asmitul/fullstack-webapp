from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from app.core.config import settings

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