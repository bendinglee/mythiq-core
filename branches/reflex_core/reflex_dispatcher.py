def reflex_response(signal):
    from .trigger_watcher import is_priority
    if is_priority(signal):
        return { "reflex": "Handled immediately", "signal": signal }
    return { "reflex": "Deferred", "signal": signal }
