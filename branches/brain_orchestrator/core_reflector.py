from branches.memory_core.recall import retrieve_entries
from branches.self_learning.reflect import generate_summary

def reflect_on_session():
    from branches.memory_core.session_tracker import current_session
    sid = current_session()
    entries = retrieve_entries(sid)
    return generate_summary(entries)
