import redis
import os

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)

# Test connection
try:
    redis_client.ping()
    print("Redis connection successful")
except redis.ConnectionError:
    print("Failed to connect to Redis")