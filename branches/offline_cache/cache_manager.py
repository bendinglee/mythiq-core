_cache = {}

def store_in_cache(key, content):
    _cache[key] = content

def get_from_cache(key):
    return _cache.get(key, "No cached content found.")
