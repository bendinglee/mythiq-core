def fallback_response(prompt):
    from .cache_manager import get_from_cache
    return get_from_cache(prompt)
