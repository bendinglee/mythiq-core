import time

def log_entry(session_id, route, request_data, response_data):
    entry = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "route": route,
        "request": request_data,
        "response": response_data
    }

    from .session_tracker import _session_store
    _session_store.setdefault(session_id, {
        "started": "unknown",
        "entries": []
    })["entries"].append(entry)

    return entry
