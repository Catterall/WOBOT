"""
Shooterspool - SPCache.py
Nothing fancy here; just a simple cache system for Shooterspool to cache the HTML of the pages for a certain amount of time.

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 01:30 GMT
"""

import asyncio
import time

class SPCache:
    def __init__(self, cache_duration: int):
        self.cache_duration = cache_duration
        self.cache = {}

    async def cachedValue(self, func, *args, **kwargs):
        """Return the cached value of an async function, or call the function and cache the result if it is not cached."""
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return value
        try:
            if asyncio.iscoroutinefunction(func):
                value = await func(*args, **kwargs)
            else:
                value = func(*args, **kwargs)
        except Exception as e:
            raise e
        self.cache[key] = (value, time.time())
        return value
