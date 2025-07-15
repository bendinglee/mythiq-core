def overlay_memory():
    from branches.memory_core.recall import retrieve_entries
    from branches.memory_core.session_tracker import current_session
    sid = current_session()
    entries = retrieve_entries(sid)[-3:]
    return "\n".join([str(e["request"]) for e in entries])
