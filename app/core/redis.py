import os

from dotenv import load_dotenv
from redis.asyncio import Redis

from app.metrics.redis_metrics import redis_hits, redis_misses

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


async def cached_get(key: str):
    value = await redis.get(key)
    if value is None:
        redis_misses.inc()
    else:
        redis_hits.inc()
    return value


async def cached_set(key: str, value: str, ttl: int):
    await redis.set(key, value, ex=ttl)
