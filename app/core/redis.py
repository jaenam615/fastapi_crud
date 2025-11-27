from redis.asyncio import Redis


class RedisConstants:
    CACHE_KEY_POST_ALL = "posts:all"
    CACHE_TTL_POSTS = 60


redis = Redis.from_url(
    "redis://localhost:6379/0",
    encoding="utf-8",
    decode_responses=True,
)
