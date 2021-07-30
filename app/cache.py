import time

class SimpleCache:
    """
    An in-memory cache with time-to-live expiration
    """

    def __init__(self):
        self.cache = {}

    def __contains__(self, key):
        return key in self.cache

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __getitem__(self, key):
        return self.cache[key]

    def __delitem__(self, key):
        del self.cache[key]

    def get(self, key, ignore_ttl=False):
        if key not in self: return None
        item = self.cache[key]
        if (not ignore_ttl) and (ttl := item['ttl']):
            if time.time() > ttl:
                del self.cache[key]
                return None
        return item['data']

    def set(self, key, value, ttl=None):
        if ttl is not None:
            ttl += time.time()
        item = {'ttl': ttl, 'data': value}
        self[key] = item


cache = SimpleCache()