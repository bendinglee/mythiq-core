from difflib import SequenceMatcher

def retrieve_entries(session_id, route_filter=None):
    from .session_tracker import _session_store
    if session_id not in _session_store:
        return []
    entries = _session_store[session_id]["entries"]
    return [entry for entry in entries if not route_filter or entry["route"] == route_filter]


def semantic_search(session_id, query, top_k=5):
    from .session_tracker import _session_store
    if session_id not in _session_store:
        return []
    entries = _session_store[session_id]["entries"]

    def score(entry):
        request_str = str(entry.get("request", ""))
        return SequenceMatcher(None, query, request_str).ratio()

    return sorted(entries, key=score, reverse=True)[:top_k]


def generate_summary():
    from .session_tracker import current_session
    from .summary import generate_session_summary

    session_id = current_session()
    summary = generate_session_summary(session_id)

    return {
        "session_id": session_id,
        "entries_analyzed": summary.get("total_entries", 0),
        "dominant_route": summary.get("most_used_route"),
        "confidence_score": f"{summary.get('confidence_score', 0)}%",
        "diversity": summary.get("diversity", 0),
        "depth": summary.get("depth", 0),
        "memory_integrity": summary.get("memory_integrity", "unknown"),
        "recent_activity": summary.get("most_recent_entry", {}).get("route", "none")
    }
