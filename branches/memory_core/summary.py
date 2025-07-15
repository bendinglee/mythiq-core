def generate_session_summary(session_id):
    from .session_tracker import _session_store
    if session_id not in _session_store:
        return { "error": "Session not found", "session_id": session_id }

    entries = _session_store[session_id]["entries"]
    route_counts = {}
    for e in entries:
        route = e.get("route")
        route_counts[route] = route_counts.get(route, 0) + 1

    return {
        "total_entries": len(entries),
        "routes_used": list(route_counts.keys()),
        "most_used_route": max(route_counts, key=route_counts.get) if entries else None,
        "most_recent_entry": entries[-1] if entries else None
    }
