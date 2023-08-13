import os
import redis
from dotenv import load_dotenv
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_redis():
    """Function to get a Redis connection from the connection pool."""
    try:
        return redis.Redis(connection_pool=pool)
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")
        raise HTTPException(status_code=500, detail="Error getting microwave state.")
    
