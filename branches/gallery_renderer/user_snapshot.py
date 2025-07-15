_snapshots = {}

def save_snapshot(user_id, media_info):
    if user_id not in _snapshots:
        _snapshots[user_id] = []
    _snapshots[user_id].append(media_info)

def get_user_gallery(user_id):
    return _snapshots.get(user_id, [])
