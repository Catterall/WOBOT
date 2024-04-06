"""
Shooterspool - SPCache.py
A class for caching various values, such as function results and username IDs.

Created & Maintained by K. Catterall
(XORBit64 @ Discord)

Last Revision: 06/04/2024 18:20 GMT
"""

import asyncio
import time

class SPCache:
    def __init__(self, cache_duration: int):
        self.cache_duration = cache_duration
        self.functionCache = {}
        self.usernameIDCache = {}

    async def cachedValue(self, func, *args, **kwargs):
        """Return the cached value of an async function, or call the function and cache the result if it is not cached."""
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key in self.functionCache:
            value, timestamp = self.functionCache[key]
            if time.time() - timestamp < self.cache_duration:
                return value
        try:
            if asyncio.iscoroutinefunction(func):
                value = await func(*args, **kwargs)
            else:
                value = func(*args, **kwargs)
        except Exception as e:
            raise e
        self.functionCache[key] = (value, time.time())
        return value
    
    async def cachedUsernameID(self, username: str) -> int | None:
        entry = self.usernameIDCache.get(username)
        if entry:
            user_id, timestamp = entry
            if time.time() - timestamp < self.cache_duration:
                return user_id
        return None

    async def cacheUsernameID(self, username: str, user_id: int, timestamp=None):
        timestamp = timestamp or time.time()
        self.usernameIDCache[username] = (user_id, timestamp)
