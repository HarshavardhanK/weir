import redis
import os

from dotenv import load_dotenv
load_dotenv()

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "weir-redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)