import json
from typing import Any, Optional

import redis

from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)

def get_cache(key: str) -> Optional[Any]:
    """Get data from Redis cache."""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """Set data in Redis cache with expiration time in seconds."""
    try:
        redis_client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        print(f"Redis error: {e}")
        return False

def delete_cache(key: str) -> bool:
    """Delete data from Redis cache."""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Redis error: {e}")
        return False 