"""Database Module."""
from cachetools import Cache, TTLCache


class NoneSupportedTTLCache(TTLCache):
    """Cache Customization to not Save None Values in Memory."""

    def __setitem__(self, key, value, cache_setitem=Cache.__setitem__) -> None:  # type: ignore
        """Customize __setitem__  to do not save nullable values."""
        if value:
            super().__setitem__(key, value, cache_setitem)  # type: ignore


GROUPS_CACHE: NoneSupportedTTLCache = NoneSupportedTTLCache(maxsize=256, ttl=300)
USERS_CACHE: NoneSupportedTTLCache = NoneSupportedTTLCache(maxsize=2048, ttl=300)
