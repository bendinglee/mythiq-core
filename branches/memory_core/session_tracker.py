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
    if not _session_store:
        return start_session()
    return list(_session_store.keys())[-1]
