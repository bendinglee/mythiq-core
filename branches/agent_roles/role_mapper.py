def map_role(intent):
    if "plan" in intent:
        return "advisor"
    elif "create" in intent:
        return "artist"
    return "explorer"
