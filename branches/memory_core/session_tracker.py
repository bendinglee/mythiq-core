import time
import uuid

_session_store = {}

def start_session():
    session_id = str(uuid.uuid4())
    _session_store[session_id] = {
        "started": time.strftime('%Y-%m-%d %H:%M:%S'),
        "entries": []
    }
    return session_id

def get_session_data(session_id):
    return _session_store.get(session_id, {})

def current_session():
    # This can be upgraded to use per-user context later
    if not _session_store:
        session_id = start_session()
    else:
        session_id = list(_session_store.keys())[-1]
    return {
        "session_id": session_id,
        "metadata": _session_store[session_id]
    }
