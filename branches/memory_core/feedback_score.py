def score_feedback(session_id):
    from .session_tracker import _session_store
    entries = _session_store.get(session_id, {}).get("entries", [])
    if not entries:
        return { "confidence_score": 0.0 }

    route_set = set(entry["route"] for entry in entries)
    diversity = len(route_set)
    depth = len(entries)
    score = round((depth + diversity * 2) / (depth + 1) * 100, 2)

    return {
        "confidence_score": score,
        "diversity": diversity,
        "depth": depth
    }
