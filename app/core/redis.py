import os

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()


class RedisConstants:
    CACHE_KEY_POST_ALL = "posts:all"
    CACHE_TTL_POSTS = 60


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis = Redis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    encoding="utf-8",
    decode_responses=True,
)
