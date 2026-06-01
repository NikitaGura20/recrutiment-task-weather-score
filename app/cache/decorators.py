from datetime import datetime, timedelta
from functools import wraps
from typing import Callable

from app.cache.memory_cache import cache

CACHE_TTL = timedelta(days=1)


def cached(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_date = kwargs["start_date"]
        end_date = kwargs["end_date"]

        cache_key = f"{start_date.isoformat()}:{end_date.isoformat()}"

        cached_item = cache.get(cache_key)

        if cached_item is not None:
            created_at, cached_value = cached_item

            if datetime.now() - created_at < CACHE_TTL:
                return cached_value

        result = await func(*args, **kwargs)

        cache[cache_key] = (datetime.now(), result)

        return result

    return wrapper