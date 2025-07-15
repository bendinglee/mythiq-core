def validate_memory(session_id):
    from .session_tracker import _session_store
    session = _session_store.get(session_id)
    if not session or not isinstance(session.get("entries"), list):
        return False

    for entry in session["entries"]:
        if not all(key in entry for key in ("route", "request", "response", "timestamp")):
            return False
    return True
