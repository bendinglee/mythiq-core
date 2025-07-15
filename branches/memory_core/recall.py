from difflib import SequenceMatcher

def retrieve_entries(session_id, route_filter=None):
    from .session_tracker import _session_store
    if session_id not in _session_store:
        return []
    entries = _session_store[session_id]["entries"]
    return [e for e in entries if not route_filter or e["route"] == route_filter]

def semantic_search(session_id, query, top_k=5):
    from .session_tracker import _session_store
    if session_id not in _session_store:
        return []
    entries = _session_store[session_id]["entries"]

    def score(entry):
        request_str = str(entry.get("request", ""))
        return SequenceMatcher(None, query, request_str).ratio()

    return sorted(entries, key=score, reverse=True)[:top_k]
