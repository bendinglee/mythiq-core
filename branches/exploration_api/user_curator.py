curated = {}

def save_discovery(user_id, item):
    curated.setdefault(user_id, []).append(item)
    return { "saved": item }

def get_discoveries(user_id):
    return curated.get(user_id, [])
