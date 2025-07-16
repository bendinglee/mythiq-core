import json, os

def load_quota(user_id):
    path = f"quota_store/{user_id}.json"
    if not os.path.exists(path): return {"count": 0}
    return json.load(open(path))

def update_quota(user_id):
    quota = load_quota(user_id)
    quota["count"] = quota.get("count", 0) + 1
    os.makedirs("quota_store", exist_ok=True)
    with open(f"quota_store/{user_id}.json", "w") as f:
        json.dump(quota, f)
    return quota
