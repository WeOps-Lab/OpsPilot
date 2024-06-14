import os

REDIS_CACHE_URL = os.environ.get("REDIS_CACHE_URL", "")
if REDIS_CACHE_URL != "":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_CACHE_URL,
        }
    }
