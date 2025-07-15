vault = {}

def store_data(payload):
    key = payload.get("key", "")
    data = payload.get("data", "")
    vault[key] = data
    return { "stored": key }

def fetch_data(key):
    return vault.get(key, "Not found")
