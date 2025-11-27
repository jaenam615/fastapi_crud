from prometheus_client import Counter

redis_hits = Counter("redis_cache_hits_total", "Number of successful Redis cache hits.")

redis_misses = Counter("redis_cache_misses_total", "Number of Redis cache misses.")
