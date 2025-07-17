import os, json

def load_quota(user_id):
    path = f"quota_store/{user_id}.json"
    if os.path.exists(path):
        return json.load(open(path))
    return {"count": 0}

def update_quota(user_id):
    data = load_quota(user_id)
    data["count"] += 1
    os.makedirs("quota_store", exist_ok=True)
    with open(f"quota_store/{user_id}.json", "w") as f:
        json.dump(data, f)
    return data
