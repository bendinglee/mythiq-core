def overlay_recent_history(session_id):
    from branches.memory_core.recall import retrieve_entries
    entries = retrieve_entries(session_id)[-5:]
    return [e["route"] + ": " + str(e["request"]) for e in entries]
