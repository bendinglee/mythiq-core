def validate_memory(session_id):
    from .session_tracker import _session_store
    session = _session_store.get(session_id)
    if not session or not isinstance(session.get("entries"), list):
        return False

    required_keys = {"route", "request", "response", "timestamp"}
    for entry in session["entries"]:
        if not required_keys.issubset(entry.keys()):
            return False
    return True
