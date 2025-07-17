import os, json

def get_user_memory(user_id):
    path = f"memory_store/{user_id}.json"
    if os.path.exists(path):
        return json.load(open(path))
    return {}

def save_user_memory(user_id, memory):
    os.makedirs("memory_store", exist_ok=True)
    with open(f"memory_store/{user_id}.json", "w") as f:
        json.dump(memory, f)
